"""
Source: src/automation/event_trigger.py
Updated: 2026-04-14T08:15:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Project_Governance/NWF_Automation_Spec_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
    - src/core/audit_log_manager.py
    - src/integration/repository_watcher.py
    - src/integrity/anomaly_detector.py
Docstring:
    NWFの神経系モジュール。
    外部・内部イベントを検知し、NWFEventとして標準化し、
    SystemOrchestratorへ通知する。
"""

from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, List

# JST タイムゾーン定義
JST = timezone(timedelta(hours=9))

# 無視対象ファイル/ディレクトリ
IGNORE_PATTERNS: List[str] = [
    ".git",
    ".tmp",
    "__pycache__",
    ".DS_Store"
]

__all__ = [
    "NWFEvent",
    "EventTrigger"
]


@dataclass(frozen=True)
class NWFEvent:
    """
    NWF標準イベントモデル

    Args:
        event_id (str): 一意のイベントID
        event_type (str): イベント種別
        source (str): 発生元
        timestamp_jst (str): JSTタイムスタンプ
        payload (Dict[str, Any]): イベント詳細情報

    Returns:
        None
    """
    event_id: str
    event_type: str
    source: str
    timestamp_jst: str
    payload: Dict[str, Any]


class EventTrigger:
    """
    イベント検知および発行を行うクラス。
    Stateless設計により状態を保持しない。
    """

    def __init__(self, orchestrator: Optional[Any] = None, audit_logger: Optional[Any] = None):
        """
        初期化

        Args:
            orchestrator: SystemOrchestratorインスタンス
            audit_logger: AuditLogManagerインスタンス
        """
        self.orchestrator = orchestrator
        self.audit_logger = audit_logger

    def _generate_event_id(self, event_type: str) -> str:
        """
        イベントID生成

        Args:
            event_type (str): イベント種別

        Returns:
            str: イベントID
        """
        timestamp = datetime.now(JST).strftime('%Y%m%d%H%M%S')
        return f"EVT-{event_type}-{timestamp}"

    def create_event(self, event_type: str, source: str, payload: Dict[str, Any]) -> NWFEvent:
        """
        NWFEvent生成

        Args:
            event_type (str): イベント種別
            source (str): 発生元
            payload (Dict[str, Any]): データ

        Returns:
            NWFEvent
        """
        return NWFEvent(
            event_id=self._generate_event_id(event_type),
            event_type=event_type,
            source=source,
            timestamp_jst=datetime.now(JST).isoformat(),
            payload=payload
        )

    def emit_event(self, event: NWFEvent) -> None:
        """
        イベント送信

        Args:
            event (NWFEvent): 発行イベント

        Returns:
            None
        """
        # Audit Log 記録
        if self.audit_logger:
            try:
                self.audit_logger.log_event(asdict(event))
            except Exception as e:
                # ログ記録失敗も監査対象
                pass

        # Orchestratorへ送信
        if self.orchestrator:
            self.orchestrator.route_event(event)

    def _is_ignored(self, path: str) -> bool:
        """
        無視対象判定

        Args:
            path (str): ファイルパス

        Returns:
            bool: 無視する場合True
        """
        for pattern in IGNORE_PATTERNS:
            if pattern in path:
                return True
        return False

    def detect_file_change(self, path: str) -> None:
        """
        ファイル変更検知

        Args:
            path (str): 変更ファイルパス

        Returns:
            None
        """
        if self._is_ignored(path):
            return

        event = self.create_event(
            event_type="FILE_CHANGE",
            source="repository_watcher",
            payload={"path": path}
        )
        self.emit_event(event)

    def detect_integrity_result(self, success: bool, details: Dict[str, Any]) -> None:
        """
        整合性検証結果イベント

        Args:
            success (bool): 成否
            details (Dict[str, Any]): 詳細

        Returns:
            None
        """
        event_type = "INTEGRITY_SUCCESS" if success else "INTEGRITY_FAIL"

        event = self.create_event(
            event_type=event_type,
            source="integrity_checker",
            payload=details
        )
        self.emit_event(event)

    def detect_temporal_event(self, event_name: str, metadata: Dict[str, Any]) -> None:
        """
        時間イベント検知

        Args:
            event_name (str): イベント名
            metadata (Dict[str, Any]): 補足情報

        Returns:
            None
        """
        event = self.create_event(
            event_type="TEMPORAL_TICK",
            source="temporal_manager",
            payload={
                "event_name": event_name,
                "metadata": metadata
            }
        )
        self.emit_event(event)

    def detect_anomaly(self, anomaly_report: Dict[str, Any]) -> None:
        """
        異常検知イベント

        Args:
            anomaly_report (Dict[str, Any]): 異常内容

        Returns:
            None
        """
        event = self.create_event(
            event_type="ANOMALY_DETECTED",
            source="anomaly_detector",
            payload=anomaly_report
        )
        self.emit_event(event)

    def detect_release_completed(self, version: str) -> None:
        """
        リリース完了イベント

        Args:
            version (str): リリースバージョン

        Returns:
            None
        """
        event = self.create_event(
            event_type="RELEASE_COMPLETED",
            source="release_manager",
            payload={"version": version}
        )
        self.emit_event(event)

    def detect_sync_completed(self, version: str) -> None:
        """
        同期完了イベント

        Args:
            version (str): 対象バージョン

        Returns:
            None
        """
        event = self.create_event(
            event_type="SYNC_COMPLETED",
            source="github_sync_manager",
            payload={"version": version}
        )
        self.emit_event(event)


if __name__ == "__main__":
    # 動作確認用簡易テスト
    trigger = EventTrigger()
    trigger.detect_file_change("data/sample.json")

# [EOF]