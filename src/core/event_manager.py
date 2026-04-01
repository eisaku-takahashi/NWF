"""
Source: src/core/event_manager.py
Updated: 2026-04-02T08:09:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Engine_Spec/NWF_State_Machine_Spec_v2.0.1.md
    - docs/spec/Data_Spec/NWF_Data_Model_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
    - src/models/nwf_object.py
Docstring:
    Event Manager モジュール。
    NWF システム内で発生するイベントを管理し、登録されたハンドラへ配信する。
    Publish-Subscribe パターンに基づき、StateMachine や ExecutionEngine から発行された
    イベントを AuditLogger、WorkflowEngine、外部同期システム等へ通知する。
"""

# --------------------------------------------------
# import
# --------------------------------------------------
from datetime import datetime, timezone, timedelta
from typing import Callable, Dict, List, Any
import uuid
import logging

# --------------------------------------------------
# 定数 / 設定
# --------------------------------------------------
JST = timezone(timedelta(hours=9))

# ロガー設定
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# --------------------------------------------------
# __all__
# --------------------------------------------------
__all__ = [
    "Event",
    "EventManager"
]

# --------------------------------------------------
# Utility Functions
# --------------------------------------------------
def generate_event_id() -> str:
    """
    イベントIDを生成する。

    Returns:
        str: UUID形式のイベントID
    """
    return str(uuid.uuid4())


def get_jst_timestamp() -> str:
    """
    JSTの現在時刻をISO 8601形式で取得する。

    Returns:
        str: JST ISO 8601 タイムスタンプ
    """
    return datetime.now(JST).isoformat()


# --------------------------------------------------
# Classes
# --------------------------------------------------
class Event:
    """
    Event データモデルクラス。
    システム内で発生した状態遷移や処理結果を表現する不変オブジェクト。
    """

    def __init__(
        self,
        event_type: str,
        object_id: str,
        object_type: str,
        old_state: str = None,
        new_state: str = None,
        actor: str = "System",
        payload: Dict[str, Any] = None,
        version: str = None
    ):
        """
        Event を初期化する。

        Args:
            event_type (str): イベント種別
            object_id (str): 対象オブジェクトID
            object_type (str): 対象オブジェクトタイプ
            old_state (str): 遷移前状態
            new_state (str): 遷移後状態
            actor (str): イベント実行主体
            payload (dict): 追加データ
            version (str): オブジェクトバージョン
        """
        self.event_id = generate_event_id()
        self.event_type = event_type
        self.object_id = object_id
        self.object_type = object_type
        self.old_state = old_state
        self.new_state = new_state
        self.timestamp = get_jst_timestamp()
        self.actor = actor
        self.payload = payload or {}
        self.version = version

    def to_dict(self) -> Dict[str, Any]:
        """
        Event を辞書形式に変換する。

        Returns:
            dict: Event データ
        """
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "object_id": self.object_id,
            "object_type": self.object_type,
            "old_state": self.old_state,
            "new_state": self.new_state,
            "timestamp": self.timestamp,
            "actor": self.actor,
            "payload": self.payload,
            "version": self.version
        }


class EventManager:
    """
    Event Manager クラス。
    イベントの購読登録、イベント発行、イベント配信を管理する。
    """

    def __init__(self):
        """
        EventManager を初期化する。
        handlers は event_type ごとのハンドラ一覧を保持する。
        """
        self.handlers: Dict[str, List[Callable]] = {}
        self.event_history: Dict[str, List[Event]] = {}

        logger.info("EventManager initialized")

    # --------------------------------------------------
    # Handler Registration
    # --------------------------------------------------
    def subscribe(self, event_type: str, handler: Callable):
        """
        イベントハンドラを登録する。

        Args:
            event_type (str): イベントタイプ
            handler (Callable): ハンドラ関数
        """
        if event_type not in self.handlers:
            self.handlers[event_type] = []

        self.handlers[event_type].append(handler)

        logger.info(f"Handler subscribed to event type: {event_type}")

    # --------------------------------------------------
    # Event Emit
    # --------------------------------------------------
    def emit(self, event: Event):
        """
        イベントを発行し、登録されたハンドラへ配信する。

        Args:
            event (Event): 発行するイベント
        """
        logger.info(f"Event emitted: {event.event_type}")

        # イベント履歴保存
        if event.object_id not in self.event_history:
            self.event_history[event.object_id] = []

        self.event_history[event.object_id].append(event)

        # 配信処理
        self._dispatch(event)

    # --------------------------------------------------
    # Internal Dispatch
    # --------------------------------------------------
    def _dispatch(self, event: Event):
        """
        登録されたハンドラへイベントを配信する。

        Args:
            event (Event): 配信するイベント
        """
        handlers = self.handlers.get(event.event_type, [])

        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                # イベント処理中の例外がシステム停止を引き起こさないようにする
                logger.error(f"Error in event handler: {e}")

    # --------------------------------------------------
    # Event History
    # --------------------------------------------------
    def get_history(self, object_id: str) -> List[Event]:
        """
        指定オブジェクトのイベント履歴を取得する。

        Args:
            object_id (str): オブジェクトID

        Returns:
            List[Event]: イベント履歴
        """
        return self.event_history.get(object_id, [])


# --------------------------------------------------
# Main Guard
# --------------------------------------------------
if __name__ == "__main__":
    """
    簡易テスト用。
    """

    def sample_handler(event: Event):
        print("Event received:", event.to_dict())

    manager = EventManager()
    manager.subscribe("STATE_CHANGED", sample_handler)

    event = Event(
        event_type="STATE_CHANGED",
        object_id="obj-001",
        object_type="Task",
        old_state="Draft",
        new_state="Review"
    )

    manager.emit(event)


# [EOF]