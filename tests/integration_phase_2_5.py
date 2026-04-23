"""
tests/integration_phase_2_5.py
NWF Phase 2.5: Recursive Integrity 最終統合監査テスト (UUIDv7 厳格準拠)
"""

import unittest
from datetime import datetime, timezone, timedelta
from src.integrity.integrity_checker import IntegrityChecker
from src.integrity.consistency_validator import ConsistencyValidator
from src.integrity.recursive_auditor import RecursiveAuditor
from src.integrity.anomaly_detector import AnomalyDetector, IntegrityStatus

JST = timezone(timedelta(hours=+9))

# --- 本物として認識されるための基底クラス定義 ---
class NWFObject:
    """門番が求める基底クラス"""
    def __init__(self):
        pass

class MockContext:
    def __init__(self, tx_id):
        self.transaction_id = tx_id
        self.created_at = datetime.now(JST)
        self.updated_at = datetime.now(JST)
        self.metadata = {"actor_id": "SYS-001"}

class NWFObjectSimulation(NWFObject):
    """
    NWF Entity Schema v2.0.1 の全制約をクリアする。
    UUIDv7 Regex: ^[A-Z]{3,5}-[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$
    """
    def __init__(self):
        super().__init__()
        # 正規表現を完全にパスする UUIDv7 形式 ID (第4: 7, 第5: 8)
        valid_uuid = "CHR-018ed123-4567-789a-8bcd-0123456789ab"
        now_jst = datetime.now(JST).isoformat()
        
        # 必須属性の網羅
        self.id = valid_uuid
        self.entity_id = valid_uuid
        self.subject_id = "USER-001"
        self.type = "CHARACTER"
        self.title = "Final Verified Actor"
        self.content = {"data": "verified"}
        self.status = "DRAFT"
        self.version = "1.0.0"
        self.metadata = {
            "source_spec_id": "SPEC-001",
            "actor_id": "USER-001",
            "audit_context": {"last_transaction_id": "TXN-000"}
        }
        self.created_at = now_jst
        self.updated_at = now_jst
        self.created_by = "USER-001"
        self.timestamp = datetime.now(JST)

class MockExecutionResult:
    def __init__(self, data):
        self.data = data
        self.transaction_id = "TXN-2.5-PASS-FINAL"
        self.status = "SUCCESS"
        self.timestamp = datetime.now(JST)

class NWFPhase2_5IntegrityIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.checker = IntegrityChecker()
        self.validator = ConsistencyValidator()
        self.auditor = RecursiveAuditor(max_depth=3)
        self.detector = AnomalyDetector(confidence_threshold=0.85)
        self.mock_context = MockContext("TXN-2.5-PASS-FINAL")

    def test_full_integrity_pipeline_success(self):
        """[監査1] 全レイヤー通過パス (正常系)"""
        print("\n[監査1] 正常系パイプライン検証中...")
        mock_obj = NWFObjectSimulation()
        exec_res = MockExecutionResult(mock_obj)

        # L1: Structural
        val_res = self.checker.check(exec_res)
        if not val_res.is_valid:
            print(f" -> [DEBUG] L1 Errors: {val_res.errors}")
            # もし type 判定で落ちるなら dict に変換して再試行するロジックも検討
        self.assertTrue(val_res.is_valid, "L1 Check Failed")

        # L2: Causal
        con_res = self.validator.validate(self.mock_context, val_res)
        self.assertTrue(con_res.is_consistent, "L2 Check Failed")

        # L3 & L4
        aud_rep = self.auditor.audit(con_res, {"test": "data"})
        final = self.detector.detect(aud_rep, {"confidence": 0.95})

        self.assertEqual(final.status, IntegrityStatus.SUCCESS)
        print(" -> [OK] すべての厳格な検証を完全に突破しました。")

    def test_structural_failure_cascade(self):
        """[監査2] 不正データによる停止"""
        print("\n[監査2] 不正データによる停止検証中...")
        exec_res = MockExecutionResult({"invalid": "type"}) 
        val_res = self.checker.check(exec_res)
        con_res = self.validator.validate(self.mock_context, val_res)
        self.assertFalse(con_res.is_consistent)
        print(" -> [OK] 期待通り L1 で不正をブロックしました。")

if __name__ == "__main__":
    unittest.main()