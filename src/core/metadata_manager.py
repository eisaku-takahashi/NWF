"""
Source: src/core/metadata_manager.py
Updated: 2026-04-15T12:00:00+09:00  # 修正後更新
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Core_Spec/Audit_System.md
    - docs/spec/Data_Spec/Data_Model.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
    - docs/spec/Kernel_Spec/NWF_Temporal_Management_v2.0.1.md  # 追加（時間管理）
    - docs/spec/Kernel_Spec/NWF_Kernel_Core_Concept_v2.0.1.md  # 追加（因果律）
Docstring:
    Metadata Manager モジュール。
    Entity に付随する metadata の初期化・更新・検証・監査コンテキスト管理を行う。
    データ本体(content)とシステム文脈(metadata)を分離し、
    追跡可能性・監査性・因果関係(Provenance)を保証する。

    Phase 3.1 拡張:
    - JST と Timeline のデュアル時間管理
    - 時間変換インターフェース
    - 時間逆転矛盾（Temporal Paradox）検知
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
    """
    return datetime.now(JST).isoformat()


class MetadataManager:
    """
    MetadataManager クラス。
    """

    def __init__(self, spec_loader=None, timeline_anchor: int = 0):
        """
        初期化処理

        修正前:
            spec_loader のみ

        修正後:
            timeline_anchor を追加
            → Timelineの基準点（Anchor Point）として使用

        Args:
            spec_loader: Spec検証用
            timeline_anchor (int): Timeline基準値
        """
        self.spec_loader = spec_loader
        self.timeline_anchor = timeline_anchor  # Phase 3.1追加
        self.timeline_map: Dict[str, int] = {}  # transaction_id → timeline_index

    # ------------------------------
    # Phase 3.1 追加: 時間変換
    # ------------------------------
    def convert_to_timeline_date(self, jst_time: str) -> int:
        """
        JST → Timeline 変換

        なぜ必要か：
        - 現実時間と作中時間を対応させるため

        実装方針：
        - 簡易的にUNIX秒ベース → 整数インデックスへ変換
        """
        dt = datetime.fromisoformat(jst_time)
        return int(dt.timestamp())

    def convert_to_real_time(self, timeline_index: int) -> str:
        """
        Timeline → JST 変換
        """
        dt = datetime.fromtimestamp(timeline_index, JST)
        return dt.isoformat()

    def initialize_metadata(
        self,
        spec_id: str,
        actor_id: str,
        parent_entity_id: Optional[str] = None,
        derivation_type: str = "MANUAL_CREATE"
    ) -> Dict[str, Any]:
        """
        metadata 初期化
        """

        if not actor_id:
            raise ValueError("actor_id is required")

        if not spec_id:
            raise ValueError("spec_id is required")

        if self.spec_loader:
            if not self.spec_loader.is_valid_spec_id(spec_id):
                raise ValueError(f"Invalid spec_id: {spec_id}")

        current_time = get_current_timestamp()

        # ------------------------------
        # 修正前:
        # metadata = {...}
        #
        # 修正後:
        # timeline_index を追加
        # ------------------------------
        timeline_index = self.convert_to_timeline_date(current_time)

        metadata = {
            "source_spec_id": spec_id,
            "actor_id": actor_id,
            "created_at": current_time,
            "updated_at": current_time,

            # Phase 3.1追加
            "timeline": {
                "chronological_index": timeline_index,
                "anchor": self.timeline_anchor
            },

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
        metadata 更新
        """

        if not actor_id:
            raise ValueError("actor_id is required")

        if "created_at" not in current_metadata:
            raise ValueError("Invalid metadata: created_at missing")

        # ------------------------------
        # 修正前:
        # updated_at のみ更新
        #
        # 修正後:
        # timeline も更新
        # ------------------------------
        new_time = get_current_timestamp()
        new_timeline = self.convert_to_timeline_date(new_time)

        # ------------------------------
        # Phase 3.1: Temporal Paradox Check
        # ------------------------------
        old_timeline = current_metadata.get("timeline", {}).get("chronological_index")

        if old_timeline is not None:
            if new_timeline < old_timeline:
                raise ValueError("TEMPORAL_CAUSALITY_VIOLATION: Timeline reversal detected")

        current_metadata["updated_at"] = new_time
        current_metadata["actor_id"] = actor_id

        # timeline更新
        current_metadata.setdefault("timeline", {})
        current_metadata["timeline"]["chronological_index"] = new_timeline

        # audit更新
        audit_context = current_metadata.get("audit_context", {})
        audit_context["last_transaction_id"] = transaction_id

        if reason:
            audit_context["change_reason"] = reason

        if workflow_id:
            audit_context["workflow_id"] = workflow_id

        current_metadata["audit_context"] = audit_context

        return current_metadata

    def validate_metadata(self, metadata: Dict[str, Any]) -> bool:
        """
        metadata 検証
        """

        required_fields = [
            "source_spec_id",
            "actor_id",
            "created_at",
            "updated_at"
        ]

        for field in required_fields:
            if field not in metadata:
                raise ValueError(f"Missing field: {field}")

        created_at = metadata["created_at"]
        updated_at = metadata["updated_at"]

        if created_at > updated_at:
            raise ValueError("created_at > updated_at")

        # ------------------------------
        # Phase 3.1: Timeline検証追加
        # ------------------------------
        timeline = metadata.get("timeline")

        if timeline:
            index = timeline.get("chronological_index")
            anchor = timeline.get("anchor")

            if index is None:
                raise ValueError("Timeline index missing")

            if index < anchor:
                raise ValueError("TEMPORAL_CAUSALITY_VIOLATION: before anchor point")

        if self.spec_loader:
            spec_id = metadata["source_spec_id"]
            if not self.spec_loader.is_valid_spec_id(spec_id):
                raise ValueError(f"Invalid spec_id: {spec_id}")

        return True


if __name__ == "__main__":
    manager = MetadataManager()

    metadata = manager.initialize_metadata(
        spec_id="SPEC-TEST-001",
        actor_id="USR-Test"
    )

    metadata = manager.update_metadata(
        current_metadata=metadata,
        actor_id="USR-Test",
        transaction_id="TXN-001"
    )

    print(metadata)

# [EOF]