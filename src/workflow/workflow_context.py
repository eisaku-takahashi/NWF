"""
Source: src/workflow/workflow_context.py
Updated: 2026-04-25T12:02:00+09:00  # ★Phase 3.5 拡張対応
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Project_Governance/NWF_Workflow_Engine_Spec_v2.0.1.md
    - docs/spec/Execution_Spec/NWF_Validator_And_Context_Contract_v2.0.1.md
Docstring:
    WorkflowContext モジュール（Phase 3.5 拡張版）。

    修正内容（重要）：
    - Phase 3.4 Spec Contract 維持
    - Phase 3.5 拡張:
        - trace_id 追加（生成時固定・不変）
        - execution_id 追加（実行単位識別子）
        - scene_state 明確化（metadata依存から分離）
        - Evaluatorが参照可能な構造強化
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, List
import uuid

# JST タイムゾーン定義
JST = timezone(timedelta(hours=9))

# Stardate 比較用 epsilon（Spec準拠）
EPSILON = 0.000001

# 公開インターフェース
__all__ = [
    "WorkflowContext",
    "TransactionEntry",
]


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
        self.timestamp = timestamp
        self.target_id = target_id
        self.op_type = op_type
        self.field = field
        self.old_val = old_val
        self.new_val = new_val

    def to_dict(self) -> Dict[str, Any]:
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

    ★ Phase 3.4:
    - Spec Contract 準拠
    - SSoT

    ★ Phase 3.5:
    - Traceability 強化
    - Evaluator 対応構造
    """

    # ============================================================
    # ❌ 修正前（旧I/F） ※削除せず保持
    # ============================================================
    """
    def __init__(self, transaction_id: str) -> None:
        now = datetime.now(JST).isoformat()

        self._transaction_id: str = transaction_id
        self._global_vars: Dict[str, Any] = {}
        self._local_vars: Dict[str, Any] = {}
        self._metadata: Dict[str, Any] = {}

        self._world_rules: Dict[str, bool] = {}
        self._transaction: List[TransactionEntry] = []
        self._current_stardate: float = 0.0

        self._created_at: str = now
        self._updated_at: str = now
    """

    # ============================================================
    # ✅ 修正後（Phase 3.5 拡張版）
    # ============================================================
    def __init__(
        self,
        metadata: Dict[str, Any],
        world_rules: Dict[str, bool],
        transaction: List[TransactionEntry],
        current_stardate: float,
    ) -> None:
        """
        初期化処理（Spec準拠 + Phase 3.5 拡張）

        Args:
            metadata (Dict[str, Any])
            world_rules (Dict[str, bool])
            transaction (List[TransactionEntry])
            current_stardate (float)
        """

        now = datetime.now(JST).isoformat()

        # --------------------------------------------------------
        # ★ Phase 3.4: transaction_id
        # --------------------------------------------------------
        self.transaction_id: str = str(uuid.uuid4())

        # --------------------------------------------------------
        # ★ Phase 3.5 追加①: trace_id（不変）
        # --------------------------------------------------------
        # ★設計意図:
        # - 全Workflowのトレースを一意に識別
        # - Evaluator / Validator / Engine 全体で共有
        self.trace_id: str = str(uuid.uuid4())

        # --------------------------------------------------------
        # ★ Phase 3.5 追加②: execution_id
        # --------------------------------------------------------
        # ★設計意図:
        # - 実行単位の識別（再実行・リトライ区別）
        self.execution_id: str = str(uuid.uuid4())

        # --------------------------------------------------------
        # ★ Phase 3.4: Spec構造
        # --------------------------------------------------------
        self.metadata: Dict[str, Any] = metadata
        self.world_rules: Dict[str, bool] = world_rules
        self.transaction: List[TransactionEntry] = transaction

        # --------------------------------------------------------
        # ★ Phase 3.5 追加③: scene_state 明確化
        # --------------------------------------------------------
        # ❌ 旧: metadata内に曖昧に存在
        # ✅ 新: 明示フィールド化
        self.scene_state: Dict[str, Any] = metadata.get("scene_state", {})

        # --------------------------------------------------------
        # stardate（Spec準拠）
        # --------------------------------------------------------
        self.current_stardate: float = round(current_stardate, 6)

        # --------------------------------------------------------
        # 互換レイヤ
        # --------------------------------------------------------
        self._global_vars: Dict[str, Any] = {}
        self._local_vars: Dict[str, Any] = {}

        self._created_at: str = now
        self._updated_at: str = now

    # ============================================================
    # ★ 既存メソッド（互換維持）
    # ============================================================

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

    def add_transaction(self, entry: TransactionEntry) -> None:
        self.transaction.append(entry)
        self._update_timestamp()

    def get_transaction(self) -> List[TransactionEntry]:
        return list(self.transaction)

    def set_stardate(self, stardate: float) -> None:
        self.current_stardate = round(stardate, 6)
        self._update_timestamp()

    def get_stardate(self) -> float:
        return self.current_stardate

    # ============================================================
    # ★ Phase 3.5 追加: Trace取得API
    # ============================================================

    def get_trace_id(self) -> str:
        return self.trace_id

    def get_execution_id(self) -> str:
        return self.execution_id

    def get_scene_state(self) -> Dict[str, Any]:
        return dict(self.scene_state)

    # ============================================================
    # ★ 安全アクセス
    # ============================================================
    def get_attr(self, key: str, default: Any = None) -> Any:

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

    # ============================================================
    # ★ Snapshot
    # ============================================================
    def snapshot(self) -> Dict[str, Any]:
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

    # ============================================================
    # ★ 内部
    # ============================================================
    def _update_timestamp(self) -> None:
        self._updated_at = datetime.now(JST).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return self.snapshot()


if __name__ == "__main__":

    ctx = WorkflowContext(
        metadata={
            "base_date": "2026-01-01",
            "time_unit": "day",
            "coordinate_system": "earth",
            "scene_state": {"location": "tokyo"},
        },
        world_rules={
            "allow_ghost_activity": False,
            "allow_time_reversal": False,
            "allow_multi_location": False,
        },
        transaction=[],
        current_stardate=123.456789,
    )

    print(ctx.to_dict())

# [EOF]