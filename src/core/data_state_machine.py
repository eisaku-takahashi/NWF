"""
Source: src/core/data_state_machine.py
Updated: 2026-04-07T05:10:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Core_Spec/NWF_State_Transition_Model_v2.0.1.md
    - docs/spec/Data_Spec/NWF_StateData_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
Docstring:
    Data State Machine モジュール。
    NWF システムにおける状態遷移の正典（Single Source of Truth）を提供する。

    本モジュールは純粋な遷移判定ロジックのみを担当し、
    データ更新・ログ記録・永続化は一切行わない。

    因果律（Causality）を保証するため、
    定義された状態遷移以外はすべて例外として扱う。
"""

from typing import Dict, List

# ============================================================
# Constants / State Definitions
# ============================================================

STATE_DRAFT = "DRAFT"
STATE_REVIEW = "REVIEW"
STATE_APPROVED = "APPROVED"
STATE_RELEASED = "RELEASED"
STATE_ARCHIVED = "ARCHIVED"

ALL_STATES: List[str] = [
    STATE_DRAFT,
    STATE_REVIEW,
    STATE_APPROVED,
    STATE_RELEASED,
    STATE_ARCHIVED,
]

# ============================================================
# 正典状態遷移テーブル
# ============================================================

# なぜこの構造か：
# 状態遷移の唯一の正解をここに集中させることで、
# DataStateManager / EntityManager の分岐ロジックの不整合を防ぐため
TRANSITIONS: Dict[str, List[str]] = {
    STATE_DRAFT: [STATE_REVIEW, STATE_ARCHIVED],
    STATE_REVIEW: [STATE_APPROVED, STATE_DRAFT, STATE_ARCHIVED],
    STATE_APPROVED: [STATE_RELEASED, STATE_DRAFT, STATE_ARCHIVED],
    STATE_RELEASED: [STATE_ARCHIVED],
    STATE_ARCHIVED: [],
}

# ============================================================
# Public Interface
# ============================================================

__all__ = [
    "DataStateMachine",
    "InvalidStateTransitionError",
    "ALL_STATES",
]

# ============================================================
# Exceptions
# ============================================================

class InvalidStateTransitionError(Exception):
    """
    状態遷移違反例外

    なぜ必要か：
    不正な状態遷移は因果律の破壊に直結するため、
    即時例外として検出し、上位レイヤーに通知する。
    """
    def __init__(self, current_state: str, next_state: str):
        message = f"Invalid state transition: {current_state} -> {next_state}"
        super().__init__(message)


# ============================================================
# Data State Machine
# ============================================================

class DataStateMachine:
    """
    DataStateMachine（状態遷移判定専用クラス）

    責務:
        - 状態遷移の妥当性チェックのみを行う
        - データ更新・ログ記録は行わない

    Notes:
        本クラスは「状態遷移の熱力学法則」を担う。
        一度 ARCHIVED に入ったエンティティは復元できない。
    """

    _TRANSITIONS = TRANSITIONS

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    @classmethod
    def validate_transition(cls, current_state: str, next_state: str) -> bool:
        """
        状態遷移の妥当性を検証する

        Args:
            current_state (str): 現在状態
            next_state (str): 遷移先状態

        Returns:
            bool: 遷移可能な場合 True

        Raises:
            InvalidStateTransitionError: 不正な遷移の場合
        """

        # 状態の存在チェック
        if current_state not in cls._TRANSITIONS:
            raise InvalidStateTransitionError(current_state, next_state)

        # 許可された遷移リスト取得
        allowed_states = cls._TRANSITIONS[current_state]

        # 遷移可能か判定
        if next_state not in allowed_states:
            raise InvalidStateTransitionError(current_state, next_state)

        return True

    # --------------------------------------------------------
    # Helper
    # --------------------------------------------------------

    @classmethod
    def get_allowed_transitions(cls, current_state: str) -> List[str]:
        """
        指定状態から遷移可能な状態一覧を取得

        Args:
            current_state (str): 現在状態

        Returns:
            List[str]: 遷移可能状態一覧
        """

        return cls._TRANSITIONS.get(current_state, [])

# ============================================================
# Main Guard
# ============================================================

if __name__ == "__main__":
    # 簡易テスト
    print(DataStateMachine.validate_transition("DRAFT", "REVIEW"))

# [EOF]