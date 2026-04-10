"""
Source: src/workflow/workflow_state_machine.py
Updated: 2026-04-11T06:19:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Project_Governance/NWF_Workflow_Engine_Spec_v2.0.1.md
Docstring:
    WorkflowStateMachine モジュール。
    NWF Workflow Engine における状態遷移を厳密に管理する。
    不正遷移を防止し、因果律・非矛盾性を保証する。
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, Set

# JST タイムゾーン定義
JST = timezone(timedelta(hours=9))

# 状態定義
STATE_IDLE = "IDLE"
STATE_READY = "READY"
STATE_RUNNING = "RUNNING"
STATE_SUSPEND = "SUSPEND"
STATE_COMPLETED = "COMPLETED"
STATE_FAILED = "FAILED"
STATE_ABORTED = "ABORTED"

# 公開インターフェース
__all__ = [
    "WorkflowStateMachine",
]

class WorkflowStateMachine:
    """
    Workflow の状態遷移を管理するクラス。

    状態遷移は必ず本クラスを経由して行う必要がある。
    不正な遷移が発生した場合は RuntimeError を発生させる。
    """

    # 許可遷移定義
    _ALLOWED_TRANSITIONS: Dict[str, Set[str]] = {
        STATE_IDLE: {STATE_READY},
        STATE_READY: {STATE_RUNNING},
        STATE_RUNNING: {STATE_COMPLETED, STATE_FAILED, STATE_SUSPEND},
        STATE_SUSPEND: {STATE_RUNNING, STATE_ABORTED},
        STATE_COMPLETED: {STATE_IDLE},
        STATE_FAILED: {STATE_IDLE},
        STATE_ABORTED: {STATE_IDLE},
    }

    def __init__(self) -> None:
        """
        初期化処理。

        初期状態は IDLE とする。
        """
        self._current_state: str = STATE_IDLE
        self._last_updated: str = datetime.now(JST).isoformat()

    def get_state(self) -> str:
        """
        現在の状態を取得する。

        Returns:
            str: 現在の状態
        """
        return self._current_state

    def get_last_updated(self) -> str:
        """
        最終更新時刻を取得する。

        Returns:
            str: ISO8601形式のタイムスタンプ
        """
        return self._last_updated

    def can_transition(self, target_state: str) -> bool:
        """
        指定状態へ遷移可能かを判定する。

        Args:
            target_state (str): 遷移先状態

        Returns:
            bool: 遷移可能な場合 True
        """
        allowed = self._ALLOWED_TRANSITIONS.get(self._current_state, set())
        return target_state in allowed

    def transition_to(self, target_state: str) -> None:
        """
        状態遷移を実行する。

        Args:
            target_state (str): 遷移先状態

        Raises:
            RuntimeError: 不正な状態遷移の場合
        """
        # なぜ必要か：
        # 状態遷移の整合性を保証し、不正なフロー（例: READY → COMPLETED）を防ぐため
        if not self.can_transition(target_state):
            raise RuntimeError(
                f"Invalid state transition: {self._current_state} -> {target_state}"
            )

        # 状態更新（atomic）
        self._current_state = target_state
        self._last_updated = datetime.now(JST).isoformat()

    def reset(self) -> None:
        """
        状態を IDLE にリセットする。

        主にワークフロー終了後に使用する。
        """
        # なぜ必要か：
        # COMPLETED / FAILED / ABORTED 後に再利用可能にするため
        self._current_state = STATE_IDLE
        self._last_updated = datetime.now(JST).isoformat()

    def is_terminal_state(self) -> bool:
        """
        終了状態かどうかを判定する。

        Returns:
            bool: 終了状態なら True
        """
        return self._current_state in {
            STATE_COMPLETED,
            STATE_FAILED,
            STATE_ABORTED,
        }

    def is_running(self) -> bool:
        """
        実行中かどうかを判定する。

        Returns:
            bool: RUNNING 状態なら True
        """
        return self._current_state == STATE_RUNNING


if __name__ == "__main__":
    # 簡易動作確認
    sm = WorkflowStateMachine()
    print("Initial:", sm.get_state())

    sm.transition_to(STATE_READY)
    sm.transition_to(STATE_RUNNING)
    sm.transition_to(STATE_COMPLETED)

    print("Final:", sm.get_state())

# [EOF]