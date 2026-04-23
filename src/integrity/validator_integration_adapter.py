"""
Source: src/integrity/validator_integration_adapter.py
Updated: 2026-04-23T04:17:00+09:00  # ★Phase 3.4 ⑥ Adapter整合性最終確認（Severity型保証強化版）
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

    ★ Phase 3.4 修正内容（完全版）:
    - None返却禁止（契約違反 → RuntimeError）
    - 空List返却禁止（契約違反 → RuntimeError）
    - 必ず1件以上のValidationResult保証
    - ValidationResult再変換禁止
    - severity上書き禁止（Spec準拠）

    ★ 今回の追加修正（最重要）:
    - CRITICAL例外を握りつぶさず上位へ伝播
    - Adapterは「変換」のみ、制御は行わない（責務分離）

    ★ Phase 3.4 追加修正（型保証）:
    - severityが文字列の場合のEnum強制キャストを追加
    - 不正値に対する安全なフォールバック処理を実装

    ★ Phase 3.4 最終整合（⑩ Pipeline責務分離）:
    - Validator → 生成のみ
    - Adapter → 変換のみ（★ここ）
    - Auditor → 監査のみ
    - Engine → 判断のみ

    ★ Phase 3.4 ⑥ 最終確認（今回追加）:
    - severityは最終的に必ず NWFSeverity 型であることを保証
    - 変換責務の範囲内で「型の正規化」のみを実施
    - 意味変更は禁止（Monotonicity Rule維持）

    ❗重要:
    - Adapterは絶対に「制御」を行わない
    - Severity変更・集約・フィルタリングは禁止
    - 情報は非破壊で上位へ伝播する（Pass-through思想）
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
        """
        fallback用途のみ

        なぜ必要か:
        - severityが欠損した場合の最低限の補完
        - Adapterは「推定」はするが「変更」はしない
        """
        if is_valid:
            return NWFSeverity.INFO
        return NWFSeverity.CRITICAL


# -------------------------------
# main adapter class
# -------------------------------
class ValidatorIntegrationAdapter:
    """
    Validator Integration Adapter

    役割:
    - Validator結果の正規化（型変換のみ）

    ❗責務分離（最重要）:
    - Validator: 生成
    - Adapter: 変換（ここ）
    - Auditor: 監査
    - Engine: 判断

    ❗禁止事項:
    - Severityの変更
    - 結果の集約
    - フィルタリング
    - 制御ロジック（停止判断など）
    """

    def __init__(self, validator: Union[ConsistencyValidator, List[ConsistencyValidator]]) -> None:
        """
        Args:
            validator: 単体 or 複数 Validator
        """

        # -------------------------------
        # 修正前
        # -------------------------------
        # self.validators = [validator]

        # -------------------------------
        # 修正後（複数対応）
        # -------------------------------
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

        Returns:
            List[ValidationResult]

        Raises:
            RuntimeError: Contract違反時
        """

        results: List[ValidationResult] = []

        for validator in self.validators:
            try:
                raw_result = validator.validate(context, target)

                # -------------------------------
                # Contract防御
                # -------------------------------
                if raw_result is None:
                    raise RuntimeError("Validator returned None (Contract violation)")

                # -------------------------------
                # list処理
                # -------------------------------
                if isinstance(raw_result, list):

                    if not raw_result:
                        raise RuntimeError("Validator returned empty list (Contract violation)")

                    for r in raw_result:

                        # -------------------------------
                        # 非破壊Pass-through
                        # -------------------------------
                        if isinstance(r, ValidationResult):
                            results.append(r)
                        else:
                            results.append(self._convert_result(context, r))

                # -------------------------------
                # 単体処理
                # -------------------------------
                else:

                    if isinstance(raw_result, ValidationResult):
                        results.append(raw_result)
                    else:
                        results.append(self._convert_result(context, raw_result))

            except Exception:
                # -------------------------------
                # ★ 修正前（問題点）
                # -------------------------------
                # 例外を握りつぶす可能性あり

                # -------------------------------
                # ★ 修正後（最重要）
                # -------------------------------
                # CRITICALは絶対に握りつぶさない
                raise

        # -------------------------------
        # Contract保証
        # -------------------------------
        if not results:
            raise RuntimeError("ValidationResult list is empty after execution (Contract violation)")

        return results

    def _convert_result(self, context: WorkflowContext, result: Any) -> ValidationResult:
        """
        任意型 → ValidationResult 変換

        ❗重要:
        - これは「変換」のみ
        - 意味変更は禁止
        """

        # -------------------------------
        # bool
        # -------------------------------
        if isinstance(result, bool):
            is_valid = result
            raw_code = ""
            message = ""
            violated_rules: List[str] = []
            severity = None

        # -------------------------------
        # dict
        # -------------------------------
        elif isinstance(result, dict):
            is_valid = result.get("is_valid", True)
            raw_code = result.get("error_code", "")
            message = result.get("message", "")
            violated_rules = result.get("violated_rules", [])

            severity_str = result.get("severity", None)

            # =========================================================
            # ★ 修正前
            # =========================================================
            # severity = NWFSeverity(severity_str)

            # =========================================================
            # ★ 修正後（Phase 3.4）
            # =========================================================
            # - 安全キャスト
            # - fallbackあり
            # =========================================================
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

        # -------------------------------
        # ValidationResult互換
        # -------------------------------
        else:
            try:
                is_valid = result.is_valid
                raw_code = result.error_code
                message = result.message
                violated_rules = result.violated_rules

                severity = result.severity

                # -------------------------------
                # ★ Phase 3.4 ⑥ 追加（型保証強化）
                # -------------------------------
                # 修正前:
                # if isinstance(severity, str):
                #     severity = NWFSeverity[severity]
                #
                # 問題:
                # - 不正文字列で例外発生
                #
                # 修正後:
                # - try/exceptで安全キャスト
                # - 失敗時はNone→fallbackへ
                # -------------------------------
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

        # -------------------------------
        # ★ Phase 3.4 ⑥ 追加（最重要）
        # -------------------------------
        # severity最終保証
        #
        # なぜここで保証するか:
        # - Adapterは「型の正規化責務」を持つ唯一の層
        # - Engineは純粋な判断ロジックに集中させるため
        # - 上流の不正値をここで吸収することで
        #   Pipeline全体の安定性を担保する
        #
        # ❗重要:
        # - 意味変更ではなく「型保証」
        # - Monotonicity Ruleを破らない
        # -------------------------------
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

    def _handle_exception(self, context: WorkflowContext, exception: Exception) -> ValidationResult:
        """
        例外 → ValidationResult

        ❗注意:
        - 本メソッドは現在未使用
        - Phase 3.4では例外は握りつぶさず上位伝播が原則
        """

        error_message = str(exception)

        if "CAUSAL" in error_message:
            error_code = "ERR_WR_002"
        elif "IMMUTABILITY" in error_message:
            error_code = "ERR_WR_003"
        else:
            error_code = "ERR_LM_001"

        return ValidationResult(
            is_valid=False,
            severity=NWFSeverity.CRITICAL,
            error_code=error_code,
            message=error_message,
            violated_rules=[error_code],
            transaction_id=context.transaction_id,
            stardate=context.current_stardate,
            metadata={"exception": True}
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