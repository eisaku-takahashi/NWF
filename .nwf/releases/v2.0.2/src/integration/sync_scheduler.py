"""
Source: src/integration/sync_scheduler.py
Updated: 2026-04-13T09:24:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
    - docs/spec/Project_Governance/NWF_GitHub_Sync_Spec_v2.0.1.md
Docstring:
    Sync Scheduler モジュール。
    NWFの実行サイクル（Workflow / Beat / Episode）に連動し、
    RepositoryWatcher / CommitAnalyzer / GitHubSyncManager を統合制御する。
    GitHub同期処理のオーケストレーション（指揮）を担う。
"""

# import
from typing import Dict, Any, Optional
from datetime import datetime, timezone, timedelta

from src.integration.github_sync_manager import GitHubSyncManager
from src.integration.repository_watcher import RepositoryWatcher
from src.integration.commit_analyzer import CommitAnalyzer

# 定数 / 設定
JST = timezone(timedelta(hours=9))

# 公開インターフェース
__all__ = [
    "SyncScheduler"
]

# Utility Functions
def _current_timestamp() -> str:
    """
    現在時刻を ISO8601 JST 形式で取得

    Returns:
        str: JST ISO8601 タイムスタンプ
    """
    return datetime.now(JST).isoformat()


# Classes
class SyncScheduler:
    """
    NWF同期処理の指揮者（Orchestrator）

    Watcher（検知）→ Analyzer（意味付け）→ Manager（同期）
    の一連のパイプラインを統合制御する。

    Args:
        None

    Returns:
        None
    """

    def __init__(self):
        """
        各モジュールの初期化
        """
        self.manager = GitHubSyncManager()
        self.watcher = RepositoryWatcher()
        self.analyzer = CommitAnalyzer()
        self.sync_lock = False  # 同期中の再入防止ロック

    def schedule_sync(self, trigger: str) -> None:
        """
        [仕様 5.5] 同期スケジュールを登録し即時実行

        Args:
            trigger (str): トリガー種別（workflow_complete / beat_end / episode_end）

        Returns:
            None
        """
        print(f"[SCHEDULER] ({_current_timestamp()}) Trigger received: {trigger}")

        # なぜ必要か:
        # 同時に複数の同期が走ると整合性が崩れるためロック制御
        if self.sync_lock:
            print("[SCHEDULER] Sync already in progress. Skipping...")
            return

        self.execute_sync_cycle()

    def execute_sync_cycle(self) -> Dict[str, Any]:
        """
        [仕様 5.5] 同期サイクル実行

        Returns:
            Dict[str, Any]: SyncResult
        """
        print(f"[SCHEDULER] ({_current_timestamp()}) Starting Sync Cycle...")

        # 状態遷移理由:
        # 同期処理中は他の同期をブロックする
        self.sync_lock = True

        try:
            # 1. 変更検知
            changes = self.watcher.detect_changes()

            if not changes:
                print("[SCHEDULER] No changes detected.")
                return {
                    "success": True,
                    "error_code": None,
                    "message": "No changes to sync."
                }

            # 2. コミットメッセージ生成
            commit_message = self.analyzer.generate_commit_message(changes)

            print(f"[SCHEDULER] Commit Message: {commit_message}")

            # 3. GitHub同期実行
            result = self.manager.sync_push(changes)

            if result.get("success"):
                print(f"[SCHEDULER] Sync Success: {commit_message}")
            else:
                error_code = result.get("error_code", "UNKNOWN")
                print(f"[SCHEDULER] Sync Failed: {error_code}")

                # エラー処理
                self._handle_sync_error(error_code)

            return result

        except Exception as e:
            # 例外処理理由:
            # 同期処理の例外がシステム全体を停止させないようにする
            print(f"[SCHEDULER] CRITICAL ERROR: {str(e)}")

            return {
                "success": False,
                "error_code": "ERR_SYNC_999",
                "message": str(e)
            }

        finally:
            # 状態復元理由:
            # ロックを必ず解除し、次回同期を可能にする
            self.sync_lock = False

    def _handle_sync_error(self, error_code: str) -> None:
        """
        同期エラー時のフォールバック処理

        Args:
            error_code (str): エラーコード

        Returns:
            None
        """
        # なぜ必要か:
        # エラーの種類に応じて再試行や通知を制御するため
        print(f"[SCHEDULER] Handling error: {error_code}")

        if error_code == "ERR_SYNC_002":
            print("[SCHEDULER] Integrity violation detected. Abort sync.")
        elif error_code == "ERR_SYNC_003":
            print("[SCHEDULER] Conflict detected. Requires manual resolution.")
        elif error_code == "ERR_SYNC_004":
            print("[SCHEDULER] Pull validation failed. Escalating to HITL.")
        else:
            print("[SCHEDULER] Unknown error. Logging for investigation.")


# Main Guard
if __name__ == "__main__":
    scheduler = SyncScheduler()
    scheduler.schedule_sync(trigger="manual_test")


# [EOF]