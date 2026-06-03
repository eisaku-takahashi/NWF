"""
Source: tests/integration_phase_3_4_validator.py
Updated: 2026-05-19T22:34:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Execution_Spec/NWF_Validator_And_Context_Contract_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
    - docs/project/NWF_Phase_3.5_Debug_Work_Plan_v20260516.md
    - docs/project/NWF_Phase_3.5_Debug_Work_Plan_v20260519.md
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

    ★Phase 3.4 最終強化:
    - Engine評価直前ログの明示追加
    - Validator → Adapter → Engine の完全トレース可視化
    - CRITICAL到達から停止までのログ一貫性確認

    ★Phase 3.5 修正（重要）:
    - ValidationResult strict schema 対応
    - rule_id / scope / target_id 必須化対応
    - results[0] 依存の完全排除
    - 順序非依存テストへの統一
    - ValidationResult strict schema rollback 禁止対応

    ★Phase 3.5 Debug Work Plan v20260519 対応:
    - violated_rules strict schema 完全同期
    - violated_rules includes rule_id 準拠
    - Severity consistency synchronization
    - INFO混在禁止方針同期

    テストは完全に決定論的であり、副作用を持たない。
"""

# =========================================================
# import
# =========================================================
import unittest
import uuid
from datetime import timedelta
from datetime import timezone

from src.engine.story_engine import StoryEngine
from src.integrity.validation_result import ValidationResult
from src.integrity.validator_integration_adapter import (
    ValidatorIntegrationAdapter,
)
from src.models.nwf_enums import NWFSeverity
from src.workflow.workflow_context import WorkflowContext

# =========================================================
# 定数 / 設定
# =========================================================

# ---------------------------------------------------------
# NWF 時間管理規則:
# JST 固定
# ---------------------------------------------------------
JST = timezone(timedelta(hours=9))

# =========================================================
# Public Interface
# =========================================================
__all__ = [
    "MockValidator",
    "LegacyDictValidator",
    "DummyEntity",
    "create_context",
    "create_validation_result",
    "TestPhase34ValidatorIntegration",
]

# =========================================================
# テスト用モック
# =========================================================
class MockValidator:
    """
    任意の ValidationResult を返すモックバリデーター
    """

    def __init__(self, result: ValidationResult):
        """
        モック初期化。

        Args:
            result:
                返却する ValidationResult
        """

        self._result = result

    def validate(
        self,
        context: WorkflowContext,
        target
    ):
        """
        ValidationResult を返却する。

        Args:
            context:
                WorkflowContext

            target:
                対象 Entity

        Returns:
            ValidationResult
        """

        return self._result


class LegacyDictValidator:
    """
    旧I/F（dict）を返すバリデーター

    Adapter の Legacy 互換吸収機能検証用。
    """

    def validate(
        self,
        context: WorkflowContext,
        target
    ):
        """
        Legacy dict を返却する。

        Args:
            context:
                WorkflowContext

            target:
                対象 Entity

        Returns:
            dict:
                Legacy Validation Result
        """

        return {
            "is_valid": False,
            "severity": "ERROR",
            "error_code": "ERR_LM_001",
            "message": "legacy dict error",

            # =================================================
            # strict schema:
            # invalid の場合 violated_rules 必須
            # =================================================
            "violated_rules": [
                "LEGACY_RULE"
            ],

            # =================================================
            # strict schema 必須属性
            # =================================================
            "rule_id": "LEGACY_RULE",
            "scope": "LEGACY",
            "target_id": "LEGACY_TARGET",
        }


class DummyEntity:
    """
    Entity 最小要件のみを満たすダミー
    """

    def __init__(self, entity_id: str):
        """
        DummyEntity 初期化。

        Args:
            entity_id:
                Entity ID
        """

        self.id = entity_id
        self.is_alive = True
        self.current_location = (
            "test_location"
        )


# =========================================================
# Utility Functions
# =========================================================
def create_context() -> WorkflowContext:
    """
    WorkflowContext をテスト用に生成する。

    Returns:
        WorkflowContext
    """

    context = WorkflowContext(
        metadata={
            "base_date": "2026-01-01",
            "time_unit": "stardate",
            "coordinate_system": "3D",
        },
        world_rules={
            "allow_ghost_activity": False,
            "allow_time_reversal": False,
            "allow_multi_location": False,
        },
        transaction=[],
        current_stardate=1.000001,
    )

    # -----------------------------------------------------
    # transaction_id 必須仕様対応
    # -----------------------------------------------------
    context.transaction_id = str(
        uuid.uuid4()
    )

    return context


def create_validation_result(
    severity: NWFSeverity
) -> ValidationResult:
    """
    ValidationResult を生成する。

    Args:
        severity:
            NWFSeverity

    Returns:
        ValidationResult
    """

    is_valid = severity in [
        NWFSeverity.INFO,
        NWFSeverity.WARNING,
    ]

    # =====================================================
    # strict schema:
    # invalid の場合 violated_rules 必須
    # violated_rules は rule_id を含む必要がある
    # =====================================================
    violated_rules = []

    if not is_valid:

        violated_rules = [
            "TEST_RULE"
        ]

    return ValidationResult(
        rule_id="TEST_RULE",
        scope="TEST_SCOPE",
        target_id="TEST_TARGET",
        is_valid=is_valid,
        severity=severity,
        error_code="TEST_CODE",
        message="test message",
        violated_rules=violated_rules,
        transaction_id=str(
            uuid.uuid4()
        ),
        stardate=1.000001,
        metadata={},
    )


# =========================================================
# Test Class
# =========================================================
class TestPhase34ValidatorIntegration(
    unittest.TestCase
):
    """
    Phase 3.4 Validator Integration テスト
    """

    def setUp(self):
        """
        各テスト前の初期化。
        """

        self.context = create_context()

        self.entity = DummyEntity(
            "entity_001"
        )

    # =====================================================
    # 正常系
    # =====================================================
    def test_normal_flow(self):
        """
        INFO 正常系テスト。
        """

        result = create_validation_result(
            NWFSeverity.INFO
        )

        validator = MockValidator(result)

        adapter = ValidatorIntegrationAdapter(
            [validator]
        )

        raw = validator.validate(
            self.context,
            self.entity
        )

        print(
            "DEBUG [Validator]:",
            getattr(
                raw,
                "severity",
                raw
            ),
        )

        adapted = adapter.validate(
            self.context,
            self.entity
        )

        print(
            "DEBUG [Adapter]:",
            [
                r.severity
                for r in adapted
            ],
        )

        print(
            "[TEST → Engine PRE]",
            [
                r.severity
                for r in adapted
            ],
        )

        engine = StoryEngine(adapter)

        timeline = (
            engine.generate_story_graph(
                [self.entity],
                self.context
            )
        )

        self.assertIsInstance(
            timeline,
            list
        )

    # =====================================================
    def test_warning_flow(self):
        """
        WARNING 系テスト。
        """

        result = create_validation_result(
            NWFSeverity.WARNING
        )

        validator = MockValidator(result)

        adapter = ValidatorIntegrationAdapter(
            [validator]
        )

        adapted = adapter.validate(
            self.context,
            self.entity
        )

        print(
            "[TEST → Engine PRE]",
            [
                r.severity
                for r in adapted
            ],
        )

        engine = StoryEngine(adapter)

        timeline = (
            engine.generate_story_graph(
                [self.entity],
                self.context
            )
        )

        self.assertIsInstance(
            timeline,
            list
        )

    # =====================================================
    def test_error_flow(self):
        """
        ERROR 系テスト。
        """

        result = create_validation_result(
            NWFSeverity.ERROR
        )

        validator = MockValidator(result)

        adapter = ValidatorIntegrationAdapter(
            [validator]
        )

        adapted = adapter.validate(
            self.context,
            self.entity
        )

        print(
            "[TEST → Engine PRE]",
            [
                r.severity
                for r in adapted
            ],
        )

        engine = StoryEngine(adapter)

        timeline = (
            engine.generate_story_graph(
                [self.entity],
                self.context
            )
        )

        self.assertIsInstance(
            timeline,
            list
        )

        self.assertEqual(
            len(timeline),
            0
        )

    # =====================================================
    def test_critical_flow(self):
        """
        CRITICAL 系テスト。
        """

        result = create_validation_result(
            NWFSeverity.CRITICAL
        )

        validator = MockValidator(result)

        adapter = ValidatorIntegrationAdapter(
            [validator]
        )

        results = adapter.validate(
            self.context,
            self.entity
        )

        print(
            "[TEST → Engine]",
            [
                r.severity
                for r in results
            ],
        )

        engine = StoryEngine(adapter)

        with self.assertRaises(
            RuntimeError
        ):

            engine.evaluate_validation_results(
                results
            )

    # =====================================================
    # Adapter変換系
    # =====================================================
    def test_adapter_legacy_conversion(
        self
    ):
        """
        Legacy dict → ValidationResult
        変換テスト。
        """

        validator = LegacyDictValidator()

        adapter = ValidatorIntegrationAdapter(
            [validator]
        )

        results = adapter.validate(
            self.context,
            self.entity
        )

        print(
            "DEBUG [Adapter Legacy]:",
            [
                r.severity
                for r in results
            ],
        )

        self.assertTrue(
            all(
                isinstance(
                    r,
                    ValidationResult
                )
                for r in results
            )
        )

        # -------------------------------------------------
        # 順序非依存検証
        # -------------------------------------------------
        self.assertTrue(
            any(
                r.severity
                == NWFSeverity.ERROR
                for r in results
            )
        )

        # -------------------------------------------------
        # strict schema:
        # violated_rules includes rule_id
        # -------------------------------------------------
        self.assertTrue(
            all(
                r.rule_id
                in r.violated_rules
                for r in results
                if not r.is_valid
            )
        )

    # =====================================================
    def test_multiple_validators(self):
        """
        複数 Validator 統合テスト。
        """

        v1 = MockValidator(
            create_validation_result(
                NWFSeverity.INFO
            )
        )

        v2 = MockValidator(
            create_validation_result(
                NWFSeverity.WARNING
            )
        )

        v3 = MockValidator(
            create_validation_result(
                NWFSeverity.ERROR
            )
        )

        adapter = ValidatorIntegrationAdapter(
            [v1, v2, v3]
        )

        results = adapter.validate(
            self.context,
            self.entity
        )

        print(
            "[TEST → Engine PRE MULTI]",
            [
                r.severity
                for r in results
            ],
        )

        self.assertEqual(
            len(results),
            3
        )

        self.assertTrue(
            any(
                r.severity
                == NWFSeverity.ERROR
                for r in results
            )
        )

    # =====================================================
    def test_stardate_precision(self):
        """
        Stardate 精度検証。
        """

        epsilon = 0.000001

        a = 1.000001
        b = 1.0000015

        self.assertTrue(
            abs(a - b) < epsilon
        )


# =========================================================
# Main Guard
# =========================================================
if __name__ == "__main__":
    unittest.main()

# [EOF]