"""
tests/integration_phase_2_6.py
NWF Phase 2.6: GitHub Sync 統合テスト
"""

import unittest
from unittest.mock import MagicMock, patch
from src.integration.sync_scheduler import SyncScheduler

class NWFPhase2_6SyncIntegrationTest(unittest.TestCase):
    def setUp(self):
        # 実際のリポジトリを汚さないようモック化
        self.scheduler = SyncScheduler()
        self.scheduler.manager = MagicMock()
        self.scheduler.watcher = MagicMock()
        self.scheduler.analyzer = MagicMock()

    def test_sync_pipeline_full_success(self):
        """[監査1] 正常系：変更検知から同期完了までのパイプライン"""
        print("\n[監査1] 正常系パイプライン検証中...")
        
        # 1. Watcherが変更を検知したと仮定
        mock_event = [{
            "event_id": "EVT-SYNC-TEST-001",
            "entity_id": "CHR-018ed123-4567-789a-bcde-f0123456789a",
            "event_type": "UPDATE",
            "entity_type": "CHARACTER",
            "timeline_point": "SCENE-001"
        }]
        self.scheduler.watcher.detect_changes.return_value = mock_event
        
        # 2. Analyzerがメッセージを生成したと仮定
        self.scheduler.analyzer.generate_commit_message.return_value = "[NWF-SYNC] UPDATE: CHARACTER at SCENE-001"
        
        # 3. Managerが成功を返したと仮定
        self.scheduler.manager.sync_push.return_value = {"success": True, "message": "Push OK"}

        # 実行
        result = self.scheduler.execute_sync_cycle()

        # 検証
        self.assertTrue(result["success"])
        self.scheduler.watcher.detect_changes.assert_called_once()
        self.scheduler.analyzer.generate_commit_message.assert_called_with(mock_event)
        self.scheduler.manager.sync_push.assert_called_once()
        print(" -> [OK] 正常系パイプラインの導通を確認しました。")

    def test_sync_aborted_when_no_changes(self):
        """[監査2] 正常系：変更がない場合に同期をスキップ"""
        print("\n[監査2] 空同期スキップ検証中...")
        
        self.scheduler.watcher.detect_changes.return_value = []
        
        result = self.scheduler.execute_sync_cycle()
        
        self.assertTrue(result["success"])
        self.assertEqual(result["message"], "No changes to sync.")
        self.scheduler.manager.sync_push.assert_not_called()
        print(" -> [OK] 変更なしの際に安全にスキップされることを確認しました。")

if __name__ == "__main__":
    unittest.main()