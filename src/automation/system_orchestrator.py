"""
Source: src/automation/system_orchestrator.py
Updated: 2026-04-14T09:41:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Project_Governance/NWF_Automation_Spec_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
Docstring:
    NWFの司令塔モジュール。
    EventTrigger・WorkflowAutomation・AutoRepairEngineを統合し、
    イベントルーティング、排他制御、システム監視（Heartbeat）を実行する。
"""

# --- import ---
import threading
import time
from datetime import datetime, timezone, timedelta
from typing import Dict

from src.automation.event_trigger import NWFEvent, EventTrigger
from src.automation.workflow_automation import WorkflowAutomation
from src.automation.auto_repair_engine import AutoRepairEngine

# --- 定数 / 設定 ---
JST = timezone(timedelta(hours=9))

GLOBAL_LOCK = "GLOBAL_LOCK"
RELEASE_LOCK = "RELEASE_LOCK"
REPAIR_LOCK = "REPAIR_LOCK"

HEARTBEAT_INTERVAL_SEC = 60

# --- 公開インターフェース ---
__all__ = [
    "SystemOrchestrator"
]

# --- Utility Functions ---
def _now_jst() -> str:
    """
    JST現在時刻をISO8601形式で取得

    Returns:
        str: JSTタイムスタンプ
    """
    return datetime.now(JST).isoformat()

# --- Classes ---
class SystemOrchestrator:
    """
    全自動化モジュールの統括クラス。

    EventTriggerからのイベントを受信し、
    WorkflowAutomation または AutoRepairEngine に振り分ける。

    また、排他制御・Heartbeat・起動制御を担う。
    """

    def __init__(self) -> None:
        """
        システム構成モジュールの初期化
        """
        # モジュール初期化
        self.trigger = EventTrigger(orchestrator=self)
        self.workflow = WorkflowAutomation(orchestrator=self)
        self.repair = AutoRepairEngine(orchestrator=self)

        # ロック管理（排他制御）
        self.locks: Dict[str, threading.Lock] = {
            GLOBAL_LOCK: threading.Lock(),
            RELEASE_LOCK: threading.Lock(),
            REPAIR_LOCK: threading.Lock()
        }

        # 実行状態
        self.is_running: bool = False

    # --- Public I/F ---
    def start(self) -> None:
        """
        システム起動（Bootstrap）

        - Specロード
        - Repository監視開始（将来）
        - Heartbeat開始
        """
        # なぜ必要か：
        # システム全体の起動ポイントを一元管理し、初期状態を保証するため
        self.is_running = True

        # Heartbeatスレッド起動
        threading.Thread(
            target=self._heartbeat_loop,
            daemon=True
        ).start()

    def route_event(self, event: NWFEvent) -> None:
        """
        イベントを適切なモジュールへ振り分ける

        Args:
            event (NWFEvent): 発生したイベント
        """
        # なぜ必要か：
        # 全イベントの唯一の入口として、整合性ある処理分配を保証するため

        # 異常系イベントは最優先で修復へ
        if event.event_type in ["ANOMALY_DETECTED", "INTEGRITY_FAIL"]:
            if self.acquire_lock(REPAIR_LOCK):
                try:
                    self.repair.execute_repair(event)
                finally:
                    self.release_lock(REPAIR_LOCK)
            return

        # 通常ワークフロー処理
        if self.locks[RELEASE_LOCK].locked():
            # なぜスキップするか：
            # RELEASE中は状態不整合を防ぐため新規処理を抑止
            return

        self.workflow.handle_event(event)

    def acquire_lock(self, lock_type: str) -> bool:
        """
        ロック取得

        Args:
            lock_type (str): ロック種別

        Returns:
            bool: 取得成功可否
        """
        if lock_type in self.locks:
            return self.locks[lock_type].acquire(blocking=False)
        return False

    def release_lock(self, lock_type: str) -> None:
        """
        ロック解放

        Args:
            lock_type (str): ロック種別
        """
        if lock_type in self.locks:
            lock = self.locks[lock_type]
            if lock.locked():
                lock.release()

    def stop(self) -> None:
        """
        システム停止

        - Heartbeat停止
        - 新規イベント受付停止
        """
        # なぜ必要か：
        # 安全なシャットダウンを実現し、状態破壊を防ぐため
        self.is_running = False

    # --- Internal ---
    def _heartbeat_loop(self) -> None:
        """
        Heartbeat処理

        60秒間隔でシステムの生存確認ログを出力する
        """
        while self.is_running:
            # 本来は audit_log_manager を使用
            # なぜprintしないか：
            # Spec上は audit_log_manager 経由が必須のため（現段階は暫定）
            timestamp = _now_jst()

            # TODO: audit_log_manager.log("HEARTBEAT", timestamp)
            _ = timestamp  # 未使用防止（将来ログ実装予定）

            time.sleep(HEARTBEAT_INTERVAL_SEC)


# --- Main Guard ---
if __name__ == "__main__":
    orchestrator = SystemOrchestrator()
    orchestrator.start()

# [EOF]