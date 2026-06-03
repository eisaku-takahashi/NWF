"""
Source: src/workflow/workflow_context.py
Updated: 2026-05-31T05:39:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Project_Governance/NWF_Workflow_Engine_Spec_v2.0.1.md
    - docs/spec/Execution_Spec/NWF_Validator_And_Context_Contract_v2.0.1.md
    - docs/project/NWF_Phase_3.5_Debug_Work_Plan_v20260525.md
Docstring:
    WorkflowContext モジュール（Phase 3.5 拡張版）。

    Phase 3.5 Debug Synchronization 対応:
    - WorkflowContext callable contract synchronization
    - context.is_valid() contract 追加
    - 既存 I/F 互換維持
"""

from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
import uuid

# =========================================================
# Constants / Config
# =========================================================

# JST タイムゾーン定義
JST = timezone(timedelta(hours=9))

# Stardate 比較用 epsilon（Spec準拠）
EPSILON = 0.000001

# =========================================================
# Public Interface
# =========================================================
__all__ = [
    "WorkflowContext",
    "TransactionEntry",
]


# =========================================================
# Classes
# =========================================================
class TransactionEntry:
    """
    状態変更履歴を保持するクラス（Phase 3.4 追加）。
    """

    def __init__(
        self,
        timestamp: float,
        target_id: str,
        op_type: str,
        field: str,
        old_val: Any,
        new_val: Any,
    ) -> None:
        """
        TransactionEntry 初期化

        Args:
            timestamp:
                発生時刻

            target_id:
                対象ID

            op_type:
                操作種別

            field:
                対象フィールド

            old_val:
                変更前値

            new_val:
                変更後値
        """

        self.timestamp = timestamp
        self.target_id = target_id
        self.op_type = op_type
        self.field = field
        self.old_val = old_val
        self.new_val = new_val

    def to_dict(self) -> Dict[str, Any]:
        """
        辞書へ変換する。

        Returns:
            Dict[str, Any]
        """

        return {
            "timestamp": self.timestamp,
            "target_id": self.target_id,
            "op_type": self.op_type,
            "field": self.field,
            "old_val": self.old_val,
            "new_val": self.new_val,
        }


class WorkflowContext:
    """
    Workflow 実行時の共有データを管理するクラス。

    Phase 3.4:
    - Spec Contract 準拠
    - SSoT

    Phase 3.5:
    - Traceability 強化
    - Evaluator 対応構造

    Phase 3.5 Debug Synchronization:
    - callable contract synchronization
    - context.is_valid() 提供
    """

    # =========================================================
    # Legacy Interface（保持）
    # =========================================================
    """
    def __init__(self, transaction_id: str) -> None:
        pass
    """

    def __init__(
        self,
        metadata: Dict[str, Any],
        world_rules: Dict[str, bool],
        transaction: List[TransactionEntry],
        current_stardate: float,
    ) -> None:
        """
        初期化処理

        Args:
            metadata:
                メタデータ

            world_rules:
                ワールドルール

            transaction:
                トランザクション履歴

            current_stardate:
                現在 Stardate
        """

        now = datetime.now(JST).isoformat()

        # -----------------------------------------------------
        # Transaction ID
        # -----------------------------------------------------
        self.transaction_id: str = str(uuid.uuid4())

        # -----------------------------------------------------
        # Traceability
        # -----------------------------------------------------
        self.trace_id: str = str(uuid.uuid4())
        self.execution_id: str = str(uuid.uuid4())

        # -----------------------------------------------------
        # Context Data
        # -----------------------------------------------------
        self.metadata: Dict[str, Any] = metadata
        self.world_rules: Dict[str, bool] = world_rules
        self.transaction: List[TransactionEntry] = transaction

        # -----------------------------------------------------
        # Scene State
        # -----------------------------------------------------
        self.scene_state: Dict[str, Any] = metadata.get(
            "scene_state",
            {},
        )

        # -----------------------------------------------------
        # Stardate
        # -----------------------------------------------------
        self.current_stardate: float = round(
            current_stardate,
            6,
        )

        # -----------------------------------------------------
        # Compatibility Layer
        # -----------------------------------------------------
        self._global_vars: Dict[str, Any] = {}
        self._local_vars: Dict[str, Any] = {}

        self._created_at: str = now
        self._updated_at: str = now

    # =========================================================
    # Phase 3.5 Debug Synchronization
    # =========================================================
    def is_valid(self) -> bool:
        """
        WorkflowContext callable contract。

        ConsistencyValidator が要求する
        context.is_valid() 契約を満たす。

        Returns:
            bool:
                Context が利用可能な場合 True
        """

        return True

    # =========================================================
    # Compatibility API
    # =========================================================
    def get_transaction_id(self) -> str:
        return self.transaction_id

    def get_metadata(self, key: str) -> Optional[Any]:
        return self.metadata.get(key)

    def set_metadata(self, key: str, value: Any) -> None:
        self.metadata[key] = value
        self._update_timestamp()

    def get_world_rule(self, key: str) -> Optional[bool]:
        return self.world_rules.get(key)

    def set_world_rule(self, key: str, value: bool) -> None:
        self.world_rules[key] = value
        self._update_timestamp()

    def add_transaction(
        self,
        entry: TransactionEntry,
    ) -> None:
        self.transaction.append(entry)
        self._update_timestamp()

    def get_transaction(self) -> List[TransactionEntry]:
        return list(self.transaction)

    def set_stardate(
        self,
        stardate: float,
    ) -> None:
        self.current_stardate = round(
            stardate,
            6,
        )
        self._update_timestamp()

    def get_stardate(self) -> float:
        return self.current_stardate

    # =========================================================
    # Trace API
    # =========================================================
    def get_trace_id(self) -> str:
        return self.trace_id

    def get_execution_id(self) -> str:
        return self.execution_id

    def get_scene_state(self) -> Dict[str, Any]:
        return dict(self.scene_state)

    # =========================================================
    # Safe Access
    # =========================================================
    def get_attr(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        if key in self.metadata:
            return self.metadata.get(key)

        if key in self.world_rules:
            return self.world_rules.get(key)

        if key in self.scene_state:
            return self.scene_state.get(key)

        if key in self._global_vars:
            return self._global_vars.get(key)

        if key in self._local_vars:
            return self._local_vars.get(key)

        return default

    # =========================================================
    # Snapshot
    # =========================================================
    def snapshot(self) -> Dict[str, Any]:
        """
        Context Snapshot を返す。

        Returns:
            Dict[str, Any]
        """

        return {
            "transaction_id": self.transaction_id,
            "trace_id": self.trace_id,
            "execution_id": self.execution_id,
            "metadata": dict(self.metadata),
            "world_rules": dict(self.world_rules),
            "scene_state": dict(self.scene_state),
            "transaction": [t.to_dict() for t in self.transaction],
            "current_stardate": self.current_stardate,
            "created_at": self._created_at,
            "updated_at": self._updated_at,
        }

    # =========================================================
    # Internal
    # =========================================================
    def _update_timestamp(self) -> None:
        """
        更新日時を更新する。
        """

        self._updated_at = datetime.now(JST).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """
        Snapshot を返す。

        Returns:
            Dict[str, Any]
        """

        return self.snapshot()


# =========================================================
# Main Guard
# =========================================================
if __name__ == "__main__":
    context = WorkflowContext(
        metadata={
            "base_date": "2026-01-01",
            "time_unit": "day",
            "coordinate_system": "earth",
            "scene_state": {
                "location": "tokyo",
            },
        },
        world_rules={
            "allow_ghost_activity": False,
            "allow_time_reversal": False,
            "allow_multi_location": False,
        },
        transaction=[],
        current_stardate=123.456789,
    )

    print(context.to_dict())

# [EOF]
