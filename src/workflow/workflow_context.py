"""
Source: src/workflow/workflow_context.py
Updated: 2026-04-20T00:54:00+09:00  # ← ★更新日時を修正
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Project_Governance/NWF_Workflow_Engine_Spec_v2.0.1.md
    - docs/spec/Execution_Spec/NWF_Validator_And_Context_Contract_v2.0.1.md
Docstring:
    WorkflowContext モジュール（Phase 3.4 完全Spec準拠版）。

    修正内容（重要）：
    - WorkflowContext.__init__ を Spec Contract 準拠に変更
    - transaction_id 自動生成（UUID v7）
    - metadata / world_rules / transaction / stardate を constructor で受け取る
    - 旧I/Fはコメントアウトで保持（監査用）
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, List
import uuid  # ← ★追加（transaction_id生成用）

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

    ★ Phase 3.4 修正：
    - Spec Contract 準拠（完全一致）
    - SSoT（Single Source of Truth）
    """

    # ============================================================
    # ❌ 修正前（旧I/F） ※削除せずコメントアウト
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
    # ✅ 修正後（Spec v2.0.1 完全準拠）
    # ============================================================
    def __init__(
        self,
        metadata: Dict[str, Any],
        world_rules: Dict[str, bool],
        transaction: List[TransactionEntry],
        current_stardate: float,
    ) -> None:
        """
        初期化処理（Spec準拠）。

        Args:
            metadata (Dict[str, Any])
            world_rules (Dict[str, bool])
            transaction (List[TransactionEntry])
            current_stardate (float)
        """

        now = datetime.now(JST).isoformat()

        # --------------------------------------------------------
        # ★ 修正ポイント①：transaction_id 自動生成
        # --------------------------------------------------------
        # Spec:
        # UUID v7 を標準とする
        # ※Python標準未対応のため uuid4 を代替（将来置換）
        self.transaction_id: str = str(uuid.uuid4())

        # --------------------------------------------------------
        # ★ 修正ポイント②：Spec構造を直接保持
        # --------------------------------------------------------
        self.metadata: Dict[str, Any] = metadata
        self.world_rules: Dict[str, bool] = world_rules
        self.transaction: List[TransactionEntry] = transaction

        # ★ stardate 精度制御（Spec準拠）
        self.current_stardate: float = round(current_stardate, 6)

        # --------------------------------------------------------
        # ★ 互換レイヤ（既存コード救済）
        # --------------------------------------------------------
        # ↓旧コードが参照するため残す（将来削除可能）
        self._global_vars: Dict[str, Any] = {}
        self._local_vars: Dict[str, Any] = {}

        # ❌ 旧 _metadata → 新 metadata に統合
        # self._metadata: Dict[str, Any] = {}

        self._created_at: str = now
        self._updated_at: str = now

    # ============================================================
    # ★ 既存メソッド（互換維持）
    # ============================================================

    def get_transaction_id(self) -> str:
        # ★修正：新フィールド参照
        return self.transaction_id

    def get_metadata(self, key: str) -> Optional[Any]:
        # ★修正：_metadata → metadata
        return self.metadata.get(key)

    def set_metadata(self, key: str, value: Any) -> None:
        # ★修正：_metadata → metadata
        self.metadata[key] = value
        self._update_timestamp()

    def get_world_rule(self, key: str) -> Optional[bool]:
        return self.world_rules.get(key)

    def set_world_rule(self, key: str, value: bool) -> None:
        # ★注意：本来 immutable
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
    # ★ 安全アクセス（getattr禁止対応）
    # ============================================================
    def get_attr(self, key: str, default: Any = None) -> Any:
        # 優先順位：metadata → world_rules → global → local

        if key in self.metadata:
            return self.metadata.get(key)

        if key in self.world_rules:
            return self.world_rules.get(key)

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
            "metadata": dict(self.metadata),
            "world_rules": dict(self.world_rules),
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
    # ★ 新I/Fテスト（Spec準拠）
    ctx = WorkflowContext(
        metadata={
            "base_date": "2026-01-01",
            "time_unit": "day",
            "coordinate_system": "earth",
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