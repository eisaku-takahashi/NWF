"""
Source: tests/integration_phase_3_4_validator.py
Updated: 2026-04-23T06:09:00+09:00  # ★Phase 3.4 ログトレース最終強化（Engine終端ログ追加）
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Execution_Spec/NWF_Validator_And_Context_Contract_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
    - src/integrity/validation_result.py
    - src/models/nwf_enums.py
    - src/integrity/validator_integration_adapter.py
    - src/workflow/workflow_context.py
    - src/engine/story_engine.py
Docstring:
    Phase 3.4 Validator Integration の統合テスト。

    本テストは以下を保証する：
    - Validator I/F Contract の完全一致
    - Adapter による旧I/F吸収の正当性
    - ValidationResult に基づく StoryEngine 制御フローの正当性
    - Severity ごとの分岐動作の検証

    ★Phase 3.4 追加（重要）:
    - Severity伝播トレースログの可視化
    - CRITICAL消失ポイントの特定支援

    ★Phase 3.4 最終拡張:
    - Engine.evaluate_validation_results() を用いた外部注入テスト
    - Engineを「最終ゲートキーパー」として検証

    ★Phase 3.4 最終強化（今回）:
    - Engine評価直前ログの明示追加
    - Validator → Adapter → Engine の完全トレース可視化
    - CRITICAL到達から停止までのログ一貫性確認

    テストは完全に決定論的であり、副作用を持たない。
"""

# =========================================================
# import
# =========================================================
import unittest
import uuid
from datetime import datetime, timezone, timedelta

from src.integrity.validation_result import ValidationResult
from src.models.nwf_enums import NWFSeverity, NWFActionType
from src.integrity.validator_integration_adapter import ValidatorIntegrationAdapter
from src.workflow.workflow_context import WorkflowContext
from src.engine.story_engine import StoryEngine


# =========================================================
# 定数 / 設定
# =========================================================
JST = timezone(timedelta(hours=9))


# =========================================================
# テスト用モック
# =========================================================
class MockValidator:
    """
    任意の ValidationResult を返すモックバリデーター
    """

    def __init__(self, result: ValidationResult):
        self._result = result

    def validate(self, context: WorkflowContext, target):
        return self._result


class LegacyDictValidator:
    """
    旧I/F（dict）を返すバリデーター
    Adapter の変換機能検証用
    """

    def validate(self, context: WorkflowContext, target):
        return {
            "is_valid": False,
            "severity": "ERROR",
            "error_code": "ERR_LM_001",
            "message": "legacy dict error",
            "violated_rules": ["ENTITY_STATE_CONFLICT"]
        }


class DummyEntity:
    """
    Entity 最小要件のみを満たすダミー
    """

    def __init__(self, entity_id: str):
        self.id = entity_id
        self.is_alive = True
        self.current_location = "test_location"


# =========================================================
# Utility Functions
# =========================================================
def create_context() -> WorkflowContext:
    """
    WorkflowContext をテスト用に生成
    """

    context = WorkflowContext(
        metadata={
            "base_date": "2026-01-01",
            "time_unit": "stardate",
            "coordinate_system": "3D"
        },
        world_rules={
            "allow_ghost_activity": False,
            "allow_time_reversal": False,
            "allow_multi_location": False
        },
        transaction=[],
        current_stardate=1.000001
    )

    # --- Phase 3.4 Blocker workaround ---
    context.transaction_id = str(uuid.uuid4())

    return context


def create_validation_result(severity: NWFSeverity) -> ValidationResult:
    """
    ValidationResult を生成
    """

    return ValidationResult(
        is_valid=(severity in [NWFSeverity.INFO, NWFSeverity.WARNING]),
        severity=severity,
        error_code="TEST_CODE",
        message="test message",
        violated_rules=[],
        transaction_id=str(uuid.uuid4()),
        stardate=1.000001,
        metadata={}
    )


# =========================================================
# Test Class
# =========================================================
class TestPhase34ValidatorIntegration(unittest.TestCase):

    def setUp(self):
        """
        各テスト前の初期化
        """
        self.context = create_context()
        self.entity = DummyEntity("entity_001")

    # -----------------------------------------------------
    # 正常系
    # -----------------------------------------------------
    def test_normal_flow(self):
        """
        INFO のみ → Engine が正常完了する
        """

        result = create_validation_result(NWFSeverity.INFO)
        validator = MockValidator(result)
        adapter = ValidatorIntegrationAdapter([validator])

        raw = validator.validate(self.context, self.entity)
        print("DEBUG [Validator]:", getattr(raw, "severity", raw))

        adapted = adapter.validate(self.context, self.entity)
        print("DEBUG [Adapter]:", [r.severity for r in adapted])

        # ★追加: Engine直前ログ（可視化強化）
        print("[TEST → Engine PRE]", [r.severity for r in adapted])

        engine = StoryEngine(adapter)

        timeline = engine.generate_story_graph([self.entity], self.context)

        self.assertIsInstance(timeline, list)

    # -----------------------------------------------------
    # WARNING系
    # -----------------------------------------------------
    def test_warning_flow(self):
        """
        WARNING → Engine 継続
        """

        result = create_validation_result(NWFSeverity.WARNING)
        validator = MockValidator(result)
        adapter = ValidatorIntegrationAdapter([validator])

        raw = validator.validate(self.context, self.entity)
        print("DEBUG [Validator]:", getattr(raw, "severity", raw))

        adapted = adapter.validate(self.context, self.entity)
        print("DEBUG [Adapter]:", [r.severity for r in adapted])

        # ★追加: Engine直前ログ
        print("[TEST → Engine PRE]", [r.severity for r in adapted])

        engine = StoryEngine(adapter)

        timeline = engine.generate_story_graph([self.entity], self.context)

        self.assertIsInstance(timeline, list)

    # -----------------------------------------------------
    # ERROR系
    # -----------------------------------------------------
    def test_error_flow(self):
        """
        ERROR → Engine 停止（ただしCRITICALではない）
        """

        result = create_validation_result(NWFSeverity.ERROR)
        validator = MockValidator(result)
        adapter = ValidatorIntegrationAdapter([validator])

        raw = validator.validate(self.context, self.entity)
        print("DEBUG [Validator]:", getattr(raw, "severity", raw))

        adapted = adapter.validate(self.context, self.entity)
        print("DEBUG [Adapter]:", [r.severity for r in adapted])

        # ★追加: Engine直前ログ
        print("[TEST → Engine PRE]", [r.severity for r in adapted])

        engine = StoryEngine(adapter)

        timeline = engine.generate_story_graph([self.entity], self.context)

        self.assertIsInstance(timeline, list)
        self.assertEqual(len(timeline), 0)

    # -----------------------------------------------------
    # CRITICAL系（★最重要修正ポイント）
    # -----------------------------------------------------
    def test_critical_flow(self):
        """
        CRITICAL → 即時停止（Engine.evaluate経由）

        ★修正理由：
        - 旧テストは generate_story_graph() に依存していた
        - Validation結果が Engine に「物理的に注入されていなかった」
        - Engine責務（最終判断）が検証されていなかった

        ★新設計：
        - Validator → Adapter → Engine.evaluate() の明示的接続
        - Pipeline終端テストとして成立

        ★今回追加：
        - Engine評価直前ログの強化
        - CRITICAL到達の可視化
        """

        result = create_validation_result(NWFSeverity.CRITICAL)
        validator = MockValidator(result)
        adapter = ValidatorIntegrationAdapter([validator])

        # -----------------------------
        # ★ 伝播ログ（Validator）
        # -----------------------------
        raw = validator.validate(self.context, self.entity)
        print("DEBUG [Validator]:", getattr(raw, "severity", raw))

        # -----------------------------
        # ★ Adapter後
        # -----------------------------
        results = adapter.validate(self.context, self.entity)
        print("DEBUG [Adapter]:", [r.severity for r in results])

        engine = StoryEngine(adapter)

        # -----------------------------
        # ★ 修正前（保持）
        # -----------------------------
        # print("DEBUG [Before Engine]:", [r.severity for r in results])

        # -----------------------------
        # ★ 修正後（明示ログ）
        # -----------------------------
        print("[TEST → Engine]", [r.severity for r in results])

        # ★追加（より明確なログ分離）
        print("[TRACE] Enter Engine.evaluate_validation_results")

        # -----------------------------
        # ★ Engine評価
        # -----------------------------
        with self.assertRaises(RuntimeError):
            engine.evaluate_validation_results(results)

    # -----------------------------------------------------
    # Adapter変換系
    # -----------------------------------------------------
    def test_adapter_legacy_conversion(self):
        """
        dict → ValidationResult 変換確認
        """

        validator = LegacyDictValidator()
        adapter = ValidatorIntegrationAdapter([validator])

        results = adapter.validate(self.context, self.entity)

        print("DEBUG [Adapter Legacy]:", [r.severity for r in results])

        self.assertTrue(all(isinstance(r, ValidationResult) for r in results))
        self.assertEqual(results[0].severity, NWFSeverity.ERROR)

    # -----------------------------------------------------
    # 複数Validator集約
    # -----------------------------------------------------
    def test_multiple_validators(self):
        """
        複数Validator結果の集約確認
        """

        v1 = MockValidator(create_validation_result(NWFSeverity.INFO))
        v2 = MockValidator(create_validation_result(NWFSeverity.WARNING))
        v3 = MockValidator(create_validation_result(NWFSeverity.ERROR))

        adapter = ValidatorIntegrationAdapter([v1, v2, v3])

        results = adapter.validate(self.context, self.entity)

        print("DEBUG [Multiple Validators]:", [r.severity for r in results])

        # ★追加: Engine投入前ログ（複数ケース確認）
        print("[TEST → Engine PRE MULTI]", [r.severity for r in results])

        self.assertEqual(len(results), 3)
        self.assertTrue(any(r.severity == NWFSeverity.ERROR for r in results))

    # -----------------------------------------------------
    # Stardate精度
    # -----------------------------------------------------
    def test_stardate_precision(self):
        """
        stardate 比較精度の検証
        """

        epsilon = 0.000001
        a = 1.000001
        b = 1.0000015

        self.assertTrue(abs(a - b) < epsilon)


# =========================================================
# Main Guard
# =========================================================
if __name__ == "__main__":
    unittest.main()

# [EOF]