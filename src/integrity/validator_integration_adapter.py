"""
Source: src/integrity/validator_integration_adapter.py
Updated: 2026-04-29T13:18:00+09:00  # ★Phase 3.5 Adapter安全性保証対応
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Execution_Spec/NWF_Validator_And_Context_Contract_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
    - src/integrity/consistency_validator.py
    - src/integrity/validation_result.py
    - src/workflow/workflow_context.py
Docstring:
    Validator Integration Adapter モジュール。

    StoryEngine と Validator のインターフェース差異を吸収し、
    ValidationResult に正規化する責務を持つ。

    ★ Phase 3.5 追加（最重要）:
    - ValidationResultの順序に依存しないことを明示
    - Adapterは順序に一切意味を持たせない
"""

# -------------------------------
# imports
# -------------------------------
from typing import Any, Dict, List, Union

from src.integrity.consistency_validator import ConsistencyValidator
from src.integrity.validation_result import ValidationResult, NWFSeverity
from src.workflow.workflow_context import WorkflowContext

# -------------------------------
# constants
# -------------------------------
ERROR_CODE_MAPPING: Dict[str, str] = {
    "ERR_CAUSAL_001": "ERR_WR_002",
    "IMMUTABILITY_BREACH": "ERR_WR_003",
}

# -------------------------------
# __all__
# -------------------------------
__all__ = [
    "ValidatorIntegrationAdapter",
    "ValidatorErrorMapper",
]

# -------------------------------
# utility classes
# -------------------------------
class ValidatorErrorMapper:
    """エラーコード変換ユーティリティ"""

    @staticmethod
    def map_error_code(raw_code: str) -> str:
        return ERROR_CODE_MAPPING.get(raw_code, "ERR_LM_001")

    @staticmethod
    def infer_severity(is_valid: bool) -> NWFSeverity:
        if is_valid:
            return NWFSeverity.INFO
        return NWFSeverity.CRITICAL


# -------------------------------
# main adapter class
# -------------------------------
class ValidatorIntegrationAdapter:
    """
    Validator Integration Adapter

    ❗ Phase 3.5 安全性保証（最重要）:
    -----------------------------------
    DO NOT rely on order of ValidationResult list
    (ValidationResultリストの順序に依存しないでください)

    Always determine priority by severity/code explicitly
    (常に重要度/コードに基づいて明示的に優先度を決定してください)

    - resultsの順序には意味がない
    - Adapterは順序制御・優先順位決定を行わない
    - 順序はValidator実装依存であり非決定的
    """

    def __init__(self, validator: Union[ConsistencyValidator, List[ConsistencyValidator]]) -> None:
        if isinstance(validator, list):
            self.validators = validator
        else:
            self.validators = [validator]

        self.error_mapper = ValidatorErrorMapper()

    def validate(self, context: WorkflowContext, target: Any) -> List[ValidationResult]:
        return self.execute(context, target)

    def execute(self, context: WorkflowContext, target: Any) -> List[ValidationResult]:
        """
        実行本体

        ❗重要:
        - results の順序は保証されない（Spec準拠）
        - 呼び出し側は順序に依存してはならない
        """

        results: List[ValidationResult] = []

        for validator in self.validators:
            try:
                raw_result = validator.validate(context, target)

                if raw_result is None:
                    raise RuntimeError("Validator returned None (Contract violation)")

                if isinstance(raw_result, list):

                    if not raw_result:
                        raise RuntimeError("Validator returned empty list (Contract violation)")

                    for r in raw_result:
                        if isinstance(r, ValidationResult):
                            results.append(r)
                        else:
                            results.append(self._convert_result(context, r))

                else:
                    if isinstance(raw_result, ValidationResult):
                        results.append(raw_result)
                    else:
                        results.append(self._convert_result(context, raw_result))

            except Exception:
                raise

        if not results:
            raise RuntimeError("ValidationResult list is empty after execution (Contract violation)")

        # -------------------------------
        # ★ Phase 3.5 追加（安全性保証）
        # -------------------------------
        # 修正前: 明示なし
        #
        # 修正後:
        # - 順序依存禁止を明文化
        # - Adapterでは順序を加工しない（sort禁止）
        # -------------------------------
        # DO NOT:
        #   results[0] を意味的に使用
        #   sortして優先順位を決定
        #
        # MUST:
        #   呼び出し側で severity/code に基づき判断
        # -------------------------------

        return results

    def _convert_result(self, context: WorkflowContext, result: Any) -> ValidationResult:

        if isinstance(result, bool):
            is_valid = result
            raw_code = ""
            message = ""
            violated_rules: List[str] = []
            severity = None

        elif isinstance(result, dict):
            is_valid = result.get("is_valid", True)
            raw_code = result.get("error_code", "")
            message = result.get("message", "")
            violated_rules = result.get("violated_rules", [])

            severity_str = result.get("severity", None)

            if severity_str:
                try:
                    if isinstance(severity_str, str):
                        severity = NWFSeverity[severity_str]
                    else:
                        severity = severity_str
                except Exception:
                    severity = None
            else:
                severity = None

        else:
            try:
                is_valid = result.is_valid
                raw_code = result.error_code
                message = result.message
                violated_rules = result.violated_rules
                severity = result.severity

                if isinstance(severity, str):
                    try:
                        severity = NWFSeverity[severity]
                    except Exception:
                        severity = None

            except Exception:
                is_valid = getattr(result, "is_valid", True)
                raw_code = getattr(result, "error_code", "")
                message = getattr(result, "message", "")
                violated_rules = getattr(result, "violated_rules", [])
                severity = None

        if not isinstance(severity, NWFSeverity):
            severity = self.error_mapper.infer_severity(is_valid)

        mapped_code = self.error_mapper.map_error_code(raw_code)

        return ValidationResult(
            is_valid=is_valid,
            severity=severity,
            error_code=mapped_code,
            message=message,
            violated_rules=violated_rules if isinstance(violated_rules, list) else [],
            transaction_id=context.transaction_id,
            stardate=context.current_stardate,
            metadata={
                "adapter": "ValidatorIntegrationAdapter",
                "original_error_code": raw_code,
            }
        )


# -------------------------------
# main guard
# -------------------------------
if __name__ == "__main__":

    validator = ConsistencyValidator()
    adapter = ValidatorIntegrationAdapter(validator)

    context = WorkflowContext(
        metadata={
            "base_date": "2026-01-01",
            "time_unit": "stardate",
            "coordinate_system": "global"
        },
        world_rules={
            "allow_ghost_activity": False,
            "allow_time_reversal": False,
            "allow_multi_location": False
        },
        transaction=[],
        current_stardate=0.0
    )

    dummy_target = {}

    results = adapter.validate(context, dummy_target)
    for r in results:
        print(r.to_dict())

# [EOF]