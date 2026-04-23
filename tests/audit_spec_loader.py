import sys
import unittest
from unittest.mock import MagicMock, patch

# NWF Core モジュールのパスを通す
sys.path.append('./src')

class TestSpecLoaderIntegrity(unittest.TestCase):
    """
    NWF Phase 2.2 SpecLoader 整合性監査
    基準: Spec Driven Development (SDD) & 因果律チェーン
    """

    def setUp(self):
        # 未修正の依存モジュールをモック化し、I/F 期待値を定義
        self.mock_registry = MagicMock()
        self.mock_validator = MagicMock()
        self.mock_audit_mgr = MagicMock()
        
        # 検証対象のロード（依存関係を注入）
        from loader.spec_loader import SpecLoader
        self.loader = SpecLoader(
            registry=self.mock_registry,
            validator=self.mock_validator,
            audit_log_manager=self.mock_audit_mgr
        )

    def test_phase_1_root_of_truth(self):
        """[監査1] スキャンの起点が Master Index であるか"""
        expected_index = "docs/spec/Index/NWF_Spec_Master_Index_v2.0.1.md"
        # 内部プロパティまたはメソッドで定義されているか確認
        self.assertEqual(self.loader.ROOT_INDEX, expected_index, 
                         "Error: 起点が Master Index v2.0.1 ではありません。")

    def test_phase_2_causality_chain(self):
        """[監査2] transaction_id が発行され、Audit に伝播しているか"""
        # 実行
        with patch('loader.spec_loader.uuid.uuid4', return_value='TXN-TEST-123'):
            self.loader.load()
            
            # AuditLogManager への呼び出しを確認
            # 第1引数が 'SPEC_LOAD_INIT'、引数に transaction_id が含まれているか
            calls = self.mock_audit_mgr.record_event.call_args_list
            self.assertTrue(any('TXN-TEST-123' in str(c) for c in calls),
                            "Error: transaction_id が AuditLogManager に伝播していません。")

    def test_phase_3_anti_zombie_versioning(self):
        """[監査3] v2.0.1 以外のスペックを拒絶するか"""
        bad_metadata = {"id": "test", "version": "1.0.0"} # 旧バージョン
        
        # バリデーターが False を返した場合、ロードが停止するか
        self.mock_validator.validate.return_value = False
        
        with self.assertRaises(Exception): # または定義した ValidationError
            self.loader._process_spec("dummy_path.md", bad_metadata)

    def test_phase_4_d7_naming_compliance(self):
        """[監査4] 内部で subject_id が使用されているか"""
        # ソースコードを直接読み込んで 'id' 単体使用をチェック（簡易静的解析）
        with open('src/loader/spec_loader.py', 'r') as f:
            content = f.read()
            self.assertIn('subject_id', content)
            # metadata['id'] のような記述がないか（厳格な D7 規約）
            self.assertNotIn("metadata['id']", content)

if __name__ == '__main__':
    unittest.main()