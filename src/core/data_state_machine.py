"""
Source: src/core/data_state_machine.py
Updated: 2026-04-02T21:44:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Core_Spec/NWF_Object.md
    - docs/spec/Core_Spec/Event_Manager.md
    - docs/spec/Core_Spec/Audit_System.md
    - docs/spec/Data_Spec/Data_State_Model.md
    - docs/spec/Engine_Spec/Workflow_Engine.md
Docstring:
    Data State Machine モジュール。
    NWF システムにおけるすべてのデータ状態遷移を統治する中核コンポーネント。
    NWFObject の status を変更できる唯一のモジュールとして、
    状態遷移ルールの検証、権限チェック、イベント発行を行う。
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any

# ============================================================
# Time Policy (JST)
# ============================================================

JST = timezone(timedelta(hours=9))

# ============================================================
# Constants / State Definitions
# ============================================================

STATE_DRAFT = "DRAFT"
STATE_REVIEW = "REVIEW"
STATE_APPROVED = "APPROVED"
STATE_RELEASED = "RELEASED"
STATE_ARCHIVED = "ARCHIVED"

ALL_STATES = [
    STATE_DRAFT,
    STATE_REVIEW,
    STATE_APPROVED,
    STATE_RELEASED,
    STATE_ARCHIVED,
]

# 許可された状態遷移
ALLOWED_TRANSITIONS: Dict[str, List[str]] = {
    STATE_DRAFT: [STATE_REVIEW],
    STATE_REVIEW: [STATE_DRAFT, STATE_APPROVED],
    STATE_APPROVED: [STATE_RELEASED],
    STATE_RELEASED: [STATE_ARCHIVED],
    STATE_ARCHIVED: [],
}

# ============================================================
# Public Interface
# ============================================================

__all__ = [
    "DataStateMachine",
    "NWFStateTransitionError",
]

# ============================================================
# Exceptions
# ============================================================

class NWFStateTransitionError(Exception):
    """
    状態遷移ルール違反例外
    """
    pass

# ============================================================
# Utility Functions
# ============================================================

def now_jst_iso() -> str:
    """
    JST の現在時刻を ISO8601 形式で取得
    """
    return datetime.now(JST).isoformat()

# ============================================================
# Data State Machine
# ============================================================

class DataStateMachine:
    """
    Data State Machine

    NWFObject の状態遷移を管理する。
    状態遷移の検証、権限チェック、イベント発行を行う。

    Args:
        event_manager: EventManager インスタンス

    Methods:
        transition_to
        validate_transition
        check_authority
        execute_transition
    """

    def __init__(self, event_manager):
        """
        初期化

        Args:
            event_manager: EventManager
        """
        self.event_manager = event_manager
        self.transitions = ALLOWED_TRANSITIONS

    # --------------------------------------------------------
    # Main Transition Method
    # --------------------------------------------------------

    def transition_to(self, obj, next_state: str, actor: str, context: Optional[Dict[str, Any]] = None):
        """
        状態遷移メイン処理

        Args:
            obj: NWFObject
            next_state: 遷移先状態
            actor: 実行者ID
            context: 追加情報

        Returns:
            更新された NWFObject

        Raises:
            NWFStateTransitionError
        """

        old_state = obj.status

        # イベント: 遷移開始
        self._emit_event(
            "STATE_TRANSITION_START",
            obj,
            old_state,
            next_state,
            actor,
            context
        )

        # 遷移検証
        self.validate_transition(old_state, next_state)

        # 権限チェック
        self.check_authority(actor, next_state)

        # 遷移実行
        new_obj = self.execute_transition(obj, next_state, actor)

        # イベント: 遷移成功
        self._emit_event(
            "STATE_CHANGED",
            new_obj,
            old_state,
            next_state,
            actor,
            context
        )

        return new_obj

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    def validate_transition(self, current_state: str, next_state: str):
        """
        状態遷移が許可されているか確認

        Args:
            current_state: 現在状態
            next_state: 次状態

        Raises:
            NWFStateTransitionError
        """

        if current_state not in self.transitions:
            raise NWFStateTransitionError(f"Unknown state: {current_state}")

        allowed = self.transitions[current_state]

        if next_state not in allowed:
            raise NWFStateTransitionError(
                f"Invalid transition: {current_state} -> {next_state}"
            )

    # --------------------------------------------------------
    # Authority Check
    # --------------------------------------------------------

    def check_authority(self, actor: str, next_state: str):
        """
        権限チェック

        Args:
            actor: 実行者ID
            next_state: 遷移先状態

        Notes:
            現在は簡易チェック
            将来的には Role / Permission System と連携
        """

        # APPROVED は特別権限が必要
        if next_state == STATE_APPROVED:
            if actor is None or actor == "":
                raise NWFStateTransitionError("Approval requires actor")

    # --------------------------------------------------------
    # Execute Transition
    # --------------------------------------------------------

    def execute_transition(self, obj, next_state: str, actor: str):
        """
        状態遷移実行

        NWFObject は不変オブジェクトとして扱い、
        新しいインスタンスを生成して返す。

        Args:
            obj: NWFObject
            next_state: 次状態
            actor: 実行者

        Returns:
            新しい NWFObject
        """

        # 新しいオブジェクトをクローン
        new_obj = obj.clone()

        new_obj.status = next_state
        new_obj.updated_at = now_jst_iso()

        # 承認時の情報記録
        if next_state == STATE_APPROVED:
            new_obj.approved_by = actor
            new_obj.approved_at = now_jst_iso()

        return new_obj

    # --------------------------------------------------------
    # Event Emission
    # --------------------------------------------------------

    def _emit_event(
        self,
        event_type: str,
        obj,
        old_state: str,
        new_state: str,
        actor: str,
        context: Optional[Dict[str, Any]]
    ):
        """
        EventManager へイベント送信
        """

        event_payload = {
            "event_type": event_type,
            "object_id": obj.id,
            "old_state": old_state,
            "new_state": new_state,
            "actor": actor,
            "timestamp": now_jst_iso(),
            "context": context or {},
        }

        if self.event_manager:
            self.event_manager.emit(event_payload)


# ============================================================
# Main Guard
# ============================================================

if __name__ == "__main__":
    print("DataStateMachine module")


# [EOF]