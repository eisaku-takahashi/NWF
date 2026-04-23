import sys
import unittest
import os
from unittest.mock import MagicMock

# NWF Core & Loader のパスを通す
sys.path.append('./src')

class NWFPhase2IntegrationTest(unittest.TestCase):
    """
    NWF Phase 2.2 統合テスト
    目的: Loader Layer (Loader/Validator/Registry) と Core Layer (Audit/Event) 
    の物理的な疎通と、D7 規約に基づいた因果律チェーンの検証。
    """

    def setUp(self):
        """テスト環境の初期化と依存注入（Dependency Injection）"""
        # Core 5 コンポーネントのモック化（あるいは実体化）
        self.audit_mgr = MagicMock()
        self.event_mgr = MagicMock()
        
        from loader.spec_validator import SpecValidator
        from loader.spec_registry import SpecRegistry
        from loader.spec_loader import SpecLoader
        
        # コンポーネントの構築
        self.validator = SpecValidator()
        self.registry = SpecRegistry()
        # integration_phase_2_2.py 内の 29行目付近
        # もし spec_loader.py の引数名が 'spec_registry' なら：
        #
        # 修正前
        # self.loader = SpecLoader(
        #    registry=self.registry,
        #    validator=self.validator,
        #    audit_log_manager=self.audit_mgr,
        #    event_manager=self.event_mgr
        # )
        #
        # 修正後
        self.loader = SpecLoader(
            spec_registry=self.registry,  # 引数名を実態に合わせる
            spec_validator=self.validator,
            audit_log_manager=self.audit_mgr,
            event_manager=self.event_mgr
        )

    def test_pipeline_01_successful_load_chain(self):
        """[統合1] 正常なスペックが Registry に到達し、因果律が Audit に刻まれるか"""
        # 擬似的な v2.0.1 準拠スペック（D7 規約）
        test_metadata = {
            "subject_id": "NWF_Test_Spec_v2.0.1",
            "version": "v2.0.1",
            "category": "Core"
        }
        
        # 1. 内部処理のシミュレーション（Loader が Parser から受け取った想定）
        transaction_id = "TXN-INTEGRATION-TEST-001"
        self.loader._process_spec_data(test_metadata, transaction_id)
        
        # 2. Registry 検証: 正しく登録されているか
        registered_spec = self.registry.get_spec("NWF_Test_Spec_v2.0.1")
        self.assertIsNotNone(registered_spec)
        
        # 3. Audit 検証: transaction_id が AuditManager に渡されたか
        self.audit_mgr.record_event.assert_called()
        args, _ = self.audit_mgr.record_event.call_args
        self.assertIn(transaction_id, str(args))

    def test_pipeline_02_validator_gatekeeper(self):
        """[統合2] Validator が不正なスペック（旧Ver/Zombie）を物理的に阻止するか"""
        # 不正なスペック（旧バージョン）
        zombie_metadata = {
            "subject_id": "NWF_Zombie_Spec",
            "version": "v1.0.0", # 旧版は排斥対象
            "category": "Core"
        }
        
        # ロード試行 -> 失敗（Exception または False）を期待
        with self.assertRaises(Exception): # Validator の仕様により調整
            self.loader._process_spec_data(zombie_metadata, "TXN-FAIL-TEST")
            
        # Registry に登録されていないことを確認
        self.assertIsNone(self.registry.get_spec("NWF_Zombie_Spec"))

    def test_pipeline_03_registry_lock_integrity(self):
        """[統合3] ロード完了後に Registry が物理的に不変（Locked）になるか"""
        # 1. ロックの実行
        self.registry.lock()
        
        # 2. 追加登録の試行 -> 拒絶されるべき
        new_spec = {"subject_id": "NWF_Post_Lock_Spec", "version": "v2.0.1"}
        with self.assertRaises(Exception):
            self.registry.register(new_spec, "TXN-AFTER-LOCK")

if __name__ == '__main__':
    unittest.main()