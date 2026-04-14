"""
Source: src/automation/workflow_automation.py
Updated: 2026-04-14T08:56:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Project_Governance/NWF_Automation_Spec_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
    - src/automation/event_trigger.py
    - src/integrity/integrity_checker.py
    - src/release/release_manager.py
    - src/integration/github_sync_manager.py
    - src/core/audit_log_manager.py
Docstring:
    Workflow Automation モジュール。
    NWFEvent を受信し、整合性検証・リリース・同期の自動パイプラインを
    ステートマシンに基づき制御する。
"""

# import
import enum
from typing import Optional

from src.automation.event_trigger import NWFEvent

# 定数 / 設定
STATE_TRANSITION_ERROR = "ERR_AUT_001"

# 公開インターフェース
__all__ = [
    "WorkflowState",
    "WorkflowAutomation"
]

# Utility Functions
def _safe_get_payload(event: NWFEvent, key: str, default=None):
    """
    Payload から安全に値を取得する

    Args:
        event (NWFEvent): イベント
        key (str): キー
        default: デフォルト値

    Returns:
        Any: 値
    """
    return event.payload.get(key, default)


# Classes
class WorkflowState(enum.Enum):
    """
    ワークフロー状態定義
    """
    IDLE = "IDLE"
    VERIFYING = "VERIFYING"
    RELEASING = "RELEASING"
    SYNCING = "SYNCING"
    WAITING_APPROVAL = "WAITING_APPROVAL"
    FAILED = "FAILED"


class WorkflowAutomation:
    """
    ワークフロー実行制御クラス

    イベントを受け取り、適切なパイプライン処理を実行する。
    """

    def __init__(
        self,
        orchestrator=None,
        integrity_checker=None,
        release_manager=None,
        github_sync_manager=None,
        audit_log_manager=None
    ):
        """
        初期化

        Args:
            orchestrator: SystemOrchestrator
            integrity_checker: IntegrityChecker
            release_manager: ReleaseManager
            github_sync_manager: GitHubSyncManager
            audit_log_manager: AuditLogManager
        """
        self.orchestrator = orchestrator
        self.integrity_checker = integrity_checker
        self.release_manager = release_manager
        self.github_sync_manager = github_sync_manager
        self.audit_log_manager = audit_log_manager

        self.state: WorkflowState = WorkflowState.IDLE

    # --- Public I/F ---
    def handle_event(self, event: NWFEvent) -> None:
        """
        イベントに応じてワークフローを実行

        Args:
            event (NWFEvent): 入力イベント

        Returns:
            None
        """
        self._log_info(f"Handle Event: {event.event_type}")

        try:
            if event.event_type == "FILE_CHANGE":
                self.run_auto_verify(event)

            elif event.event_type == "INTEGRITY_SUCCESS":
                if _safe_get_payload(event, "trigger_release", False):
                    self.run_auto_release(event)

            elif event.event_type == "RELEASE_COMPLETED":
                version = _safe_get_payload(event, "version")
                if version:
                    self.run_auto_sync(version)

            elif event.event_type == "INTEGRITY_FAIL":
                self._transition_to(WorkflowState.FAILED)

            elif event.event_type == "ANOMALY_DETECTED":
                self._transition_to(WorkflowState.FAILED)

        except Exception as e:
            # 例外発生時はFAILEDへ遷移
            self._log_error(f"Workflow Exception: {str(e)}")
            self._transition_to(WorkflowState.FAILED)

    def run_auto_verify(self, event: NWFEvent) -> bool:
        """
        Auto-Verify 実行

        Args:
            event (NWFEvent)

        Returns:
            bool: 成功/失敗
        """
        self._log_info(f"Auto-Verify Start: {event.event_id}")
        self._transition_to(WorkflowState.VERIFYING)

        if not self.integrity_checker:
            self._log_warning("IntegrityChecker not set")
            self._transition_to(WorkflowState.FAILED)
            return False

        result = self.integrity_checker.run()

        if result:
            self._log_info("Integrity Success")
            self._emit_event("INTEGRITY_SUCCESS", {"trigger_release": True})
        else:
            self._log_warning("Integrity Failed")
            self._emit_event("INTEGRITY_FAIL", {})

        return result

    def run_auto_release(self, event: NWFEvent) -> Optional[str]:
        """
        Auto-Release 実行

        Args:
            event (NWFEvent)

        Returns:
            str | None: バージョン
        """
        self._log_info("Auto-Release Start")
        self._transition_to(WorkflowState.RELEASING)

        if not self.release_manager:
            self._log_warning("ReleaseManager not set")
            self._transition_to(WorkflowState.FAILED)
            return None

        version = self.release_manager.execute_release()

        if version:
            self._log_info(f"Release Completed: {version}")
            self._emit_event("RELEASE_COMPLETED", {"version": version})
            return version

        self._log_error("Release Failed")
        self._transition_to(WorkflowState.FAILED)
        return None

    def run_auto_sync(self, version: str) -> bool:
        """
        Auto-Sync 実行

        Args:
            version (str): バージョン

        Returns:
            bool
        """
        self._log_info(f"Auto-Sync Start: {version}")
        self._transition_to(WorkflowState.SYNCING)

        if not self.github_sync_manager:
            self._log_warning("GitHubSyncManager not set")
            self._transition_to(WorkflowState.FAILED)
            return False

        result = self.github_sync_manager.push(version)

        if result:
            self._log_info("Sync Completed")
            self._emit_event("SYNC_COMPLETED", {"version": version})
            self._transition_to(WorkflowState.IDLE)
        else:
            self._log_error("Sync Failed")
            self._transition_to(WorkflowState.FAILED)

        return result

    # --- Internal ---
    def _emit_event(self, event_type: str, payload: dict) -> None:
        """
        Orchestratorへイベント送信

        Args:
            event_type (str)
            payload (dict)
        """
        if not self.orchestrator:
            return

        event = NWFEvent(
            event_id="AUTO-GEN",
            event_type=event_type,
            source="workflow_automation",
            timestamp_jst="",
            payload=payload
        )
        self.orchestrator.route_event(event)

    def _transition_to(self, next_state: WorkflowState) -> None:
        """
        状態遷移処理

        Args:
            next_state (WorkflowState)
        """
        self._log_info(f"State Transition: {self.state.value} -> {next_state.value}")
        self.state = next_state

    # --- Logging ---
    def _log_info(self, message: str) -> None:
        if self.audit_log_manager:
            self.audit_log_manager.log("INFO", message)

    def _log_warning(self, message: str) -> None:
        if self.audit_log_manager:
            self.audit_log_manager.log("WARNING", message)

    def _log_error(self, message: str) -> None:
        if self.audit_log_manager:
            self.audit_log_manager.log("ERROR", message)


# Main Guard
if __name__ == "__main__":
    # 単体テスト用簡易実行
    dummy_event = NWFEvent(
        event_id="TEST",
        event_type="FILE_CHANGE",
        source="test",
        timestamp_jst="2026-04-14T08:56:00+09:00",
        payload={"path": "dummy.md"}
    )

    workflow = WorkflowAutomation()
    workflow.handle_event(dummy_event)

# [EOF]