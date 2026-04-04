"""
Source: src/core/metadata_manager.py
Updated: 2026-04-04T21:27:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Core_Spec/Audit_System.md
    - docs/spec/Data_Spec/Data_Model.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
Docstring:
    Metadata Manager モジュール。
    Entity に付随する metadata の初期化・更新・検証・監査コンテキスト管理を行う。
    データ本体(content)とシステム文脈(metadata)を分離し、
    追跡可能性・監査性・因果関係(Provenance)を保証する。
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional

# JST タイムゾーン定義
JST = timezone(timedelta(hours=9))

# 公開インターフェース
__all__ = [
    "MetadataManager"
]


def get_current_timestamp() -> str:
    """
    現在時刻を ISO8601 JST 形式で取得する。

    Returns:
        str: ISO8601形式のタイムスタンプ
    """
    return datetime.now(JST).isoformat()


class MetadataManager:
    """
    MetadataManager クラス。

    Entity の metadata を管理する。
    初期化、更新、検証、監査コンテキスト管理を担当する。
    """

    def __init__(self, spec_loader=None):
        """
        MetadataManager 初期化。

        Args:
            spec_loader: Spec ID の検証に使用するローダー
        """
        self.spec_loader = spec_loader

    def initialize_metadata(
        self,
        spec_id: str,
        actor_id: str,
        parent_entity_id: Optional[str] = None,
        derivation_type: str = "MANUAL_CREATE"
    ) -> Dict[str, Any]:
        """
        新規 Entity 用 metadata を初期化する。

        Args:
            spec_id (str): 準拠 Spec ID
            actor_id (str): 操作主体 ID
            parent_entity_id (Optional[str]): 親 Entity ID
            derivation_type (str): 生成種別

        Returns:
            Dict[str, Any]: 初期化された metadata

        Raises:
            ValueError: actor_id または spec_id が不正な場合
        """

        if not actor_id:
            raise ValueError("actor_id is required for metadata initialization")

        if not spec_id:
            raise ValueError("spec_id is required for metadata initialization")

        # Spec ID 検証
        if self.spec_loader:
            if not self.spec_loader.is_valid_spec_id(spec_id):
                raise ValueError(f"Invalid spec_id: {spec_id}")

        current_time = get_current_timestamp()

        metadata = {
            "source_spec_id": spec_id,
            "actor_id": actor_id,
            "created_at": current_time,
            "updated_at": current_time,
            "audit_context": {
                "last_transaction_id": None,
                "change_reason": "Entity Created",
                "workflow_id": None
            },
            "traceability": {
                "parent_entity_id": parent_entity_id,
                "derivation_type": derivation_type
            },
            "extensions": {}
        }

        return metadata

    def update_metadata(
        self,
        current_metadata: Dict[str, Any],
        actor_id: str,
        transaction_id: str,
        reason: Optional[str] = None,
        workflow_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        metadata 更新処理。

        Args:
            current_metadata (Dict[str, Any]): 現在の metadata
            actor_id (str): 操作主体 ID
            transaction_id (str): 監査トランザクション ID
            reason (Optional[str]): 変更理由
            workflow_id (Optional[str]): Workflow ID

        Returns:
            Dict[str, Any]: 更新された metadata

        Raises:
            ValueError: actor_id 未指定など
        """

        if not actor_id:
            raise ValueError("actor_id is required for metadata update")

        if "created_at" not in current_metadata:
            raise ValueError("Invalid metadata: created_at missing")

        # updated_at 更新
        current_metadata["updated_at"] = get_current_timestamp()
        current_metadata["actor_id"] = actor_id

        # audit_context 更新
        audit_context = current_metadata.get("audit_context", {})
        audit_context["last_transaction_id"] = transaction_id

        if reason:
            audit_context["change_reason"] = reason

        if workflow_id:
            audit_context["workflow_id"] = workflow_id

        current_metadata["audit_context"] = audit_context

        return current_metadata

    def get_audit_context(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        audit_context を取得する。

        Args:
            metadata (Dict[str, Any]): metadata

        Returns:
            Dict[str, Any]: audit_context
        """
        return metadata.get("audit_context", {})

    def validate_metadata(self, metadata: Dict[str, Any]) -> bool:
        """
        metadata の整合性チェック。

        Args:
            metadata (Dict[str, Any]): metadata

        Returns:
            bool: 検証結果

        Raises:
            ValueError: 不正な metadata
        """

        required_fields = [
            "source_spec_id",
            "actor_id",
            "created_at",
            "updated_at"
        ]

        for field in required_fields:
            if field not in metadata:
                raise ValueError(f"Metadata missing required field: {field}")

        # created_at <= updated_at チェック
        created_at = metadata["created_at"]
        updated_at = metadata["updated_at"]

        if created_at > updated_at:
            raise ValueError("created_at cannot be later than updated_at")

        # Spec ID 検証
        if self.spec_loader:
            spec_id = metadata["source_spec_id"]
            if not self.spec_loader.is_valid_spec_id(spec_id):
                raise ValueError(f"Invalid spec_id in metadata: {spec_id}")

        return True


if __name__ == "__main__":
    # 簡易テスト
    manager = MetadataManager()

    metadata = manager.initialize_metadata(
        spec_id="SPEC-TEST-001",
        actor_id="USR-Test"
    )

    metadata = manager.update_metadata(
        current_metadata=metadata,
        actor_id="USR-Test",
        transaction_id="TXN-001",
        reason="Test Update"
    )

    print(metadata)

# [EOF]