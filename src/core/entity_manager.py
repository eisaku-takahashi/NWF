"""
Source: src/core/entity_manager.py
Updated: 2026-04-07T07:52:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Core_Spec/NWF_Data_Model_v2.0.1.md
    - docs/spec/Core_Spec/NWF_Entity_ID_System_v2.0.1.md
    - docs/spec/Core_Spec/NWF_State_Transition_Model_v2.0.1.md
    - docs/spec/Core_Spec/NWF_File_System_v2.0.1.md
    - docs/spec/Kernel_Spec/NWF_Kernel_Audit_System_Spec_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
Docstring:
    Entity Manager モジュール。
    NWF における Entity の生成・取得・更新・論理削除を統制する中核コンポーネント。
    各種 Manager（IdGenerator / MetadataManager / DataStateManager / VersionManager /
    AuditLogManager）と連携し、因果律とトランザクション整合性を保証する。
"""

import json
import os
from datetime import datetime, timezone, timedelta
from typing import Dict, Optional, Any

from src.models.nwf_object import NWFObject
from src.core.id_generator import IdGenerator
from src.core.metadata_manager import MetadataManager
from src.core.data_state_manager import DataStateManager
from src.core.version_manager import VersionManager
from src.core.audit_log_manager import AuditLogManager

# JST タイムゾーン定義
JST = timezone(timedelta(hours=9))

# デフォルト保存ディレクトリ
DEFAULT_ENTITY_DIR = "data/state/entities"

__all__ = [
    "EntityManager",
]


def _now_jst_iso() -> str:
    """
    現在時刻（JST）を ISO8601 形式で取得する。

    Returns:
        str: JST ISO8601 タイムスタンプ
    """
    return datetime.now(JST).isoformat()


class EntityManager:
    """
    EntityManager クラス。

    Entity のライフサイクル管理と因果律同期を担う。
    各種 Manager をオーケストレーションし、トランザクション単位で整合性を保証する。
    """

    def __init__(
        self,
        entity_dir: str = DEFAULT_ENTITY_DIR,
        id_generator: Optional[IdGenerator] = None,
        metadata_manager: Optional[MetadataManager] = None,
        state_manager: Optional[DataStateManager] = None,
        version_manager: Optional[VersionManager] = None,
        audit_log_manager: Optional[AuditLogManager] = None,
    ):
        """
        初期化処理。

        Args:
            entity_dir (str): Entity 保存ディレクトリ
            id_generator (IdGenerator): ID生成器
            metadata_manager (MetadataManager): メタデータ管理
            state_manager (DataStateManager): 状態管理
            version_manager (VersionManager): バージョン管理
            audit_log_manager (AuditLogManager): 監査ログ管理
        """
        self.entity_dir = entity_dir
        self.registry: Dict[str, NWFObject] = {}

        self.id_generator = id_generator or IdGenerator()
        self.metadata_mgr = metadata_manager or MetadataManager()
        self.state_mgr = state_manager or DataStateManager()
        self.version_mgr = version_manager or VersionManager()
        self.audit_mgr = audit_log_manager or AuditLogManager()

        os.makedirs(self.entity_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # Create
    # ------------------------------------------------------------------
    def create_entity(
        self,
        entity_type: str,
        attributes: Dict[str, Any],
        actor_id: str,
        transaction_id: str,
    ) -> NWFObject:
        """
        Entity を生成する。

        Args:
            entity_type (str): Entity種別
            attributes (Dict[str, Any]): 属性データ
            actor_id (str): 実行者ID
            transaction_id (str): トランザクションID

        Returns:
            NWFObject: 作成されたEntity
        """
        # ID生成（Spec準拠）
        subject_id = self.id_generator.generate_id(entity_type)

        # メタデータ生成
        metadata = self.metadata_mgr.create_metadata(actor_id, transaction_id)

        entity = NWFObject(
            subject_id=subject_id,
            entity_type=entity_type,
            state="DRAFT",
            version="1.0.0",
            content=attributes,
            metadata=metadata,
            relationships=[],
        )

        # 永続化
        self._save_entity(entity)

        # レジストリ登録
        self.registry[subject_id] = entity

        # 監査ログ（因果確定）
        event_id = self.audit_mgr.record_event(
            event_type="CREATE_ENTITY",
            actor_id=actor_id,
            target_id=subject_id,
            payload={"entity_type": entity_type},
            transaction_id=transaction_id,
        )

        # audit_context 更新
        self.metadata_mgr.update_audit_context(
            entity.metadata,
            transaction_id=transaction_id,
            event_id=event_id,
        )

        self._save_entity(entity)

        return entity

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------
    def get_entity(self, subject_id: str) -> Optional[NWFObject]:
        """
        Entity を取得する。

        Args:
            subject_id (str): Entity ID

        Returns:
            Optional[NWFObject]: Entity
        """
        if subject_id in self.registry:
            return self.registry[subject_id]

        path = self._get_entity_path(subject_id)
        if not os.path.exists(path):
            return None

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        entity = NWFObject.from_dict(data)
        self.registry[subject_id] = entity
        return entity

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------
    def update_entity(
        self,
        subject_id: str,
        updates: Dict[str, Any],
        actor_id: str,
        transaction_id: str,
    ) -> bool:
        """
        Entity 更新処理。

        Args:
            subject_id (str): Entity ID
            updates (Dict[str, Any]): 更新内容
            actor_id (str): 実行者
            transaction_id (str): トランザクションID

        Returns:
            bool: 成功可否
        """
        entity = self.get_entity(subject_id)
        if not entity:
            return False

        # 属性更新
        entity.content.update(updates)

        # メタデータ更新
        self.metadata_mgr.update_metadata(
            entity.metadata,
            actor_id=actor_id,
            transaction_id=transaction_id,
        )

        # バージョン更新
        entity.version = self.version_mgr.increment_patch(entity.version)

        # 永続化
        self._save_entity(entity)

        # 監査ログ
        event_id = self.audit_mgr.record_event(
            event_type="UPDATE_ENTITY",
            actor_id=actor_id,
            target_id=subject_id,
            payload={"updates": updates},
            transaction_id=transaction_id,
        )

        # audit_context 更新
        self.metadata_mgr.update_audit_context(
            entity.metadata,
            transaction_id=transaction_id,
            event_id=event_id,
        )

        self._save_entity(entity)

        return True

    # ------------------------------------------------------------------
    # Delete (Logical)
    # ------------------------------------------------------------------
    def delete_entity(
        self,
        subject_id: str,
        actor_id: str,
        transaction_id: str,
    ) -> bool:
        """
        Entity を論理削除（ARCHIVED遷移）。

        Args:
            subject_id (str): Entity ID
            actor_id (str): 実行者
            transaction_id (str): トランザクションID

        Returns:
            bool: 成功可否
        """
        entity = self.get_entity(subject_id)
        if not entity:
            return False

        # 状態遷移（直接代入禁止）
        self.state_mgr.change_state(
            subject_id=subject_id,
            new_state="ARCHIVED",
            actor_id=actor_id,
            transaction_id=transaction_id,
        )

        entity.state = "ARCHIVED"

        # 永続化
        self._save_entity(entity)

        # 監査ログ
        event_id = self.audit_mgr.record_event(
            event_type="DELETE_ENTITY",
            actor_id=actor_id,
            target_id=subject_id,
            payload={"state": "ARCHIVED"},
            transaction_id=transaction_id,
        )

        # audit_context 更新
        self.metadata_mgr.update_audit_context(
            entity.metadata,
            transaction_id=transaction_id,
            event_id=event_id,
        )

        self._save_entity(entity)

        return True

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------
    def _get_entity_path(self, subject_id: str) -> str:
        """
        Entity ファイルパス取得。
        """
        return os.path.join(self.entity_dir, f"{subject_id}.json")

    def _save_entity(self, entity: NWFObject) -> None:
        """
        Entity 永続化処理。

        Raises:
            IOError: 書き込み失敗時
        """
        path = self._get_entity_path(entity.subject_id)

        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(entity.to_dict(), f, ensure_ascii=False, indent=2)
        except Exception as e:
            # 因果律崩壊防止のため例外は握り潰さない
            raise IOError(f"Failed to save entity: {entity.subject_id}") from e


if __name__ == "__main__":
    manager = EntityManager()
    print("EntityManager initialized.")


# [EOF]