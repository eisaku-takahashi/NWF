"""
Source: src/core/entity_manager.py
Updated: 2026-04-04T20:18:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Core_Spec/NWF_Data_Model_v2.0.1.md
    - docs/spec/Core_Spec/NWF_Entity_ID_System_v2.0.1.md
    - docs/spec/Core_Spec/NWF_State_Transition_Model_v2.0.1.md
    - docs/spec/Data_Spec/NWF_Data_Spec_Index_v2.0.1.md
    - docs/spec/Kernel_Spec/NWF_Kernel_Audit_System_Spec_v2.0.1.md
Docstring:
    Entity Manager モジュール。
    NWF システムにおける Entity の生成、取得、更新、アーカイブ、
    および Entity 間の関係管理を担当するコアコンポーネント。
    DataStateManager、VersionManager、MetadataManager、AuditLogger と連携し、
    Entity のライフサイクル全体を管理する。
"""

import json
import os
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any

from src.models.nwf_object import NWFObject
from src.core.audit_logger import AuditLogger
from src.core.data_state_manager import DataStateManager

# JST タイムゾーン定義
JST = timezone(timedelta(hours=9))

# Entity 保存ディレクトリ
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

    NWF における Entity の CRUD 操作、永続化、レジストリ管理、
    および Entity 間の Relationship 管理を行う。

    Attributes:
        entity_dir (str): Entity 保存ディレクトリ
        registry (Dict[str, NWFObject]): メモリ上の Entity レジストリ
        state_manager (DataStateManager): 状態管理マネージャ
        audit_logger (AuditLogger): 監査ログロガー
    """

    def __init__(
        self,
        entity_dir: str = DEFAULT_ENTITY_DIR,
        state_manager: Optional[DataStateManager] = None,
        audit_logger: Optional[AuditLogger] = None,
    ):
        """
        EntityManager 初期化。

        Args:
            entity_dir (str): Entity 保存ディレクトリ
            state_manager (DataStateManager): 状態管理マネージャ
            audit_logger (AuditLogger): 監査ログロガー
        """
        self.entity_dir = entity_dir
        self.registry: Dict[str, NWFObject] = {}
        self.state_manager = state_manager
        self.audit_logger = audit_logger

        # ディレクトリが存在しない場合は作成
        os.makedirs(self.entity_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # Create
    # ------------------------------------------------------------------
    def create_entity(
        self,
        subject_id: str,
        entity_type: str,
        content: Dict[str, Any],
        actor_id: str,
    ) -> NWFObject:
        """
        Entity を新規作成する。

        Args:
            subject_id (str): Entity ID
            entity_type (str): Entity タイプ
            content (Dict[str, Any]): Entity コンテンツ
            actor_id (str): 作成者 ID

        Returns:
            NWFObject: 作成された Entity

        Raises:
            ValueError: 既に同じ ID が存在する場合
        """
        if subject_id in self.registry:
            raise ValueError(f"Entity already exists: {subject_id}")

        metadata = {
            "created_at": _now_jst_iso(),
            "updated_at": _now_jst_iso(),
            "actor_id": actor_id,
        }

        entity = NWFObject(
            subject_id=subject_id,
            entity_type=entity_type,
            state="DRAFT",
            version="1.0.0",
            content=content,
            metadata=metadata,
            relationships=[],
        )

        # レジストリ登録
        self.registry[subject_id] = entity

        # 永続化
        self._save_entity(entity)

        # 監査ログ
        if self.audit_logger:
            self.audit_logger.log_event(
                event_type="CREATE_ENTITY",
                actor_id=actor_id,
                target_id=subject_id,
                payload={"entity_type": entity_type},
            )

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
            Optional[NWFObject]: Entity オブジェクト
        """
        if subject_id in self.registry:
            return self.registry[subject_id]

        entity_path = self._get_entity_path(subject_id)
        if not os.path.exists(entity_path):
            return None

        with open(entity_path, "r", encoding="utf-8") as f:
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
    ) -> Optional[NWFObject]:
        """
        Entity を更新する（Immutable 原則に基づき version 更新）。

        Args:
            subject_id (str): Entity ID
            updates (Dict[str, Any]): 更新内容
            actor_id (str): 更新者 ID

        Returns:
            Optional[NWFObject]: 更新後 Entity
        """
        entity = self.get_entity(subject_id)
        if not entity:
            return None

        # content 更新
        entity.content.update(updates)
        entity.metadata["updated_at"] = _now_jst_iso()
        entity.metadata["actor_id"] = actor_id

        # version patch increment
        entity.version = self._increment_patch_version(entity.version)

        self._save_entity(entity)

        if self.audit_logger:
            self.audit_logger.log_event(
                event_type="UPDATE_ENTITY",
                actor_id=actor_id,
                target_id=subject_id,
                payload={"updates": updates},
            )

        return entity

    # ------------------------------------------------------------------
    # Archive
    # ------------------------------------------------------------------
    def archive_entity(self, subject_id: str, actor_id: str) -> bool:
        """
        Entity を ARCHIVED 状態へ変更（論理削除）。

        Args:
            subject_id (str): Entity ID
            actor_id (str): 実行者 ID

        Returns:
            bool: 成功可否
        """
        entity = self.get_entity(subject_id)
        if not entity:
            return False

        if self.state_manager:
            self.state_manager.change_state(subject_id, "ARCHIVED", actor_id)

        entity.state = "ARCHIVED"
        self._save_entity(entity)

        if self.audit_logger:
            self.audit_logger.log_event(
                event_type="ARCHIVE_ENTITY",
                actor_id=actor_id,
                target_id=subject_id,
                payload={},
            )

        return True

    # ------------------------------------------------------------------
    # List / Search
    # ------------------------------------------------------------------
    def list_entities(
        self,
        entity_type: Optional[str] = None,
        state: Optional[str] = None,
    ) -> List[NWFObject]:
        """
        Entity 一覧取得。

        Args:
            entity_type (Optional[str]): フィルタ Entity Type
            state (Optional[str]): フィルタ State

        Returns:
            List[NWFObject]: Entity リスト
        """
        result = []
        for entity in self.registry.values():
            if entity_type and entity.entity_type != entity_type:
                continue
            if state and entity.state != state:
                continue
            result.append(entity)
        return result

    # ------------------------------------------------------------------
    # Relationship
    # ------------------------------------------------------------------
    def link_entities(
        self,
        src_id: str,
        dst_id: str,
        rel_type: str,
    ) -> bool:
        """
        Entity 間の関係を追加。

        Args:
            src_id (str): 元 Entity ID
            dst_id (str): 先 Entity ID
            rel_type (str): Relationship Type

        Returns:
            bool: 成功可否
        """
        src = self.get_entity(src_id)
        dst = self.get_entity(dst_id)

        if not src or not dst:
            return False

        relationship = {
            "target_id": dst_id,
            "rel_type": rel_type,
        }

        src.relationships.append(relationship)
        self._save_entity(src)
        return True

    def unlink_entities(
        self,
        src_id: str,
        dst_id: str,
        rel_type: str,
    ) -> bool:
        """
        Entity 間の関係を削除。

        Args:
            src_id (str): 元 Entity ID
            dst_id (str): 先 Entity ID
            rel_type (str): Relationship Type

        Returns:
            bool: 成功可否
        """
        src = self.get_entity(src_id)
        if not src:
            return False

        src.relationships = [
            r for r in src.relationships
            if not (r["target_id"] == dst_id and r["rel_type"] == rel_type)
        ]

        self._save_entity(src)
        return True

    # ------------------------------------------------------------------
    # Internal Utilities
    # ------------------------------------------------------------------
    def _get_entity_path(self, subject_id: str) -> str:
        """
        Entity ファイルパス取得。
        """
        return os.path.join(self.entity_dir, f"{subject_id}.json")

    def _save_entity(self, entity: NWFObject) -> None:
        """
        Entity を JSON として保存。
        """
        path = self._get_entity_path(entity.subject_id)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(entity.to_dict(), f, ensure_ascii=False, indent=2)

    def _increment_patch_version(self, version: str) -> str:
        """
        Patch Version をインクリメント。

        Args:
            version (str): 現在バージョン

        Returns:
            str: 更新後バージョン
        """
        parts = version.split(".")
        if len(parts) != 3:
            return version
        parts[2] = str(int(parts[2]) + 1)
        return ".".join(parts)


if __name__ == "__main__":
    # 簡易テスト用
    manager = EntityManager()
    print("EntityManager initialized.")


# [EOF]