"""
Source: src/integrity/validator_integration_adapter.py
Updated: 2026-06-04T03:56:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Execution_Spec/NWF_Validator_And_Context_Contract_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
    - docs/project/NWF_Phase_3.5_Debug_Work_Plan_v20260516.md
    - docs/project/NWF_Phase_3.5_Debug_Work_Plan_v20260519.md
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
    - Legacy validator の互換吸収責務を保持
    - ValidationResult strict schema 対応

    ★ Phase 3.5 Debug Work Plan v20260519 対応:
    - violated_rules strict schema 完全同期
    - violated_rules includes rule_id 準拠
    - Severity consistency synchronization
    - rollback 非実施
"""

# =========================================================
# imports
# =========================================================
from typing import Any
from typing import Dict
from typing import List
from typing import Union

from src.integrity.consistency_validator import (
    ConsistencyValidator,
)
from src.integrity.validation_result import (
    NWFSeverity,
)
from src.integrity.validation_result import (
    ValidationResult,
)
from src.workflow.workflow_context import (
    WorkflowContext,
)

# =========================================================
# constants
# =========================================================

# ---------------------------------------------------------
# Legacy error code mapping
#
# なぜ必要か:
# Legacy validator が返却する旧 error_code を
# NWF標準エラーコードへ統一するため。
# ---------------------------------------------------------
ERROR_CODE_MAPPING: Dict[str, str] = {
    "ERR_CAUSAL_001": "ERR_WR_002",
    "IMMUTABILITY_BREACH": "ERR_WR_003",
}

# ---------------------------------------------------------
# strict schema fallback constants
#
# なぜ必要か:
# Legacy validator が strict schema 必須属性を
# 未返却の場合でも Adapter責務として補完するため。
#
# ValidationResult 本体へ互換責務を持ち込まない。
# ---------------------------------------------------------
LEGACY_RULE_ID = "LEGACY_RULE"
LEGACY_SCOPE = "LEGACY"
LEGACY_TARGET_ID = ""

# =========================================================
# public interface
# =========================================================
__all__ = [
    "ValidatorIntegrationAdapter",
    "ValidatorErrorMapper",
]

# =========================================================
# utility classes
# =========================================================
class ValidatorErrorMapper:
    """
    エラーコード変換ユーティリティ。
    """

    @staticmethod
    def map_error_code(raw_code: str) -> str:
        """
        Legacy error code を
        NWF標準 error code へ変換する。

        Args:
            raw_code:
                Legacy validator が返却した
                元エラーコード。

        Returns:
            str:
                NWF標準エラーコード。
        """

        return ERROR_CODE_MAPPING.get(
            raw_code,
            "ERR_LM_001",
        )

    @staticmethod
    def infer_severity(
        is_valid: bool
    ) -> NWFSeverity:
        """
        Validation状態から severity を推定する。

        Args:
            is_valid:
                Validation成否。

        Returns:
            NWFSeverity:
                推定された severity。

        Notes:
            Work Plan v20260519 に基づき、
            invalid は CRITICAL へ統一する。
        """

        if is_valid:
            return NWFSeverity.INFO

        return NWFSeverity.CRITICAL


# =========================================================
# main adapter class
# =========================================================
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

    ★ Phase 3.5 strict schema:
    - ValidationResult strict schema を維持
    - Legacy validator 互換吸収は Adapter責務
    - violated_rules includes rule_id を保証
    """

    def __init__(
        self,
        validator: Union[
            ConsistencyValidator,
            List[ConsistencyValidator],
        ],
    ) -> None:
        """
        Adapter初期化。

        Args:
            validator:
                Validator または Validatorリスト。
        """

        if isinstance(validator, list):
            self.validators = validator
        else:
            self.validators = [validator]

        self.error_mapper = ValidatorErrorMapper()

    def validate(
        self,
        context: WorkflowContext,
        target: Any,
    ) -> List[ValidationResult]:
        """
        Validation実行ラッパー。

        Args:
            context:
                WorkflowContext。

            target:
                Validation対象。

        Returns:
            List[ValidationResult]:
                Validation結果一覧。
        """

        return self.execute(
            context,
            target,
        )

    def execute(
        self,
        context: WorkflowContext,
        target: Any,
    ) -> List[ValidationResult]:
        """
        Validation実行本体。

        ❗重要:
        - results の順序は保証されない
        - 呼び出し側は順序依存禁止

        Args:
            context:
                WorkflowContext。

            target:
                Validation対象。

        Returns:
            List[ValidationResult]:
                Validation結果一覧。

        Raises:
            RuntimeError:
                Validator Contract違反時。
        """

        results: List[ValidationResult] = []

        for validator in self.validators:

            try:
                raw_result = validator.validate(
                    target,
                    context,
                )

                # -------------------------------------------------
                # None は Contract violation
                #
                # なぜ必要か:
                # Validation pipeline 崩壊を
                # 即時検出するため。
                # -------------------------------------------------
                if raw_result is None:
                    raise RuntimeError(
                        "Validator returned None "
                        "(Contract violation)"
                    )

                if isinstance(raw_result, list):

                    # ---------------------------------------------
                    # 空listは禁止
                    #
                    # なぜ必要か:
                    # Validation実行済みか未実行かを
                    # 判定不能にするため。
                    # ---------------------------------------------
                    if not raw_result:
                        raise RuntimeError(
                            "Validator returned empty list "
                            "(Contract violation)"
                        )

                    for result_item in raw_result:

                        if isinstance(
                            result_item,
                            ValidationResult,
                        ):
                            results.append(
                                result_item
                            )

                        else:
                            results.append(
                                self._convert_result(
                                    context=context,
                                    result=result_item,
                                )
                            )

                else:

                    if isinstance(
                        raw_result,
                        ValidationResult,
                    ):
                        results.append(
                            raw_result
                        )

                    else:
                        results.append(
                            self._convert_result(
                                context=context,
                                result=raw_result,
                            )
                        )

            except Exception:
                # ---------------------------------------------
                # Exception透過仕様
                #
                # なぜ必要か:
                # Validator debugging 時に
                # stack trace を保持するため。
                #
                # rollback禁止方針に基づき、
                # Adapter側で例外を握り潰さない。
                # ---------------------------------------------
                raise

        # -------------------------------------------------
        # ValidationResult未生成は禁止
        #
        # なぜ必要か:
        # Validation pipeline の
        # silent failure を防止するため。
        # -------------------------------------------------
        if not results:
            raise RuntimeError(
                "ValidationResult list is empty "
                "after execution "
                "(Contract violation)"
            )

        # -------------------------------------------------
        # ❗ Phase 3.5 順序安全性保証
        #
        # DO NOT:
        # - results[0] を意味的に使用
        # - sort による優先順位制御
        #
        # MUST:
        # - 呼び出し側で severity/code 判定
        # -------------------------------------------------

        return results

    def _convert_result(
        self,
        context: WorkflowContext,
        result: Any,
    ) -> ValidationResult:
        """
        Legacy validator result を
        ValidationResult へ正規化する。

        Args:
            context:
                WorkflowContext。

            result:
                Legacy validator result。

        Returns:
            ValidationResult:
                strict schema 準拠結果。
        """

        if isinstance(result, bool):

            is_valid = result
            raw_code = ""
            message = ""
            violated_rules: List[str] = []
            severity = None

            # ---------------------------------------------
            # strict schema fallback
            # ---------------------------------------------
            rule_id = LEGACY_RULE_ID
            scope = LEGACY_SCOPE
            target_id = LEGACY_TARGET_ID

        elif isinstance(result, dict):

            is_valid = result.get(
                "is_valid",
                True,
            )

            raw_code = result.get(
                "error_code",
                "",
            )

            message = result.get(
                "message",
                "",
            )

            violated_rules = result.get(
                "violated_rules",
                [],
            )

            rule_id = result.get(
                "rule_id",
                LEGACY_RULE_ID,
            )

            scope = result.get(
                "scope",
                LEGACY_SCOPE,
            )

            target_id = result.get(
                "target_id",
                LEGACY_TARGET_ID,
            )

            severity_str = result.get(
                "severity",
                None,
            )

            if severity_str:

                try:

                    if isinstance(
                        severity_str,
                        str,
                    ):
                        severity = NWFSeverity[
                            severity_str
                        ]

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

                violated_rules = getattr(
                    result,
                    "violated_rules",
                    [],
                )

                severity = result.severity

                rule_id = getattr(
                    result,
                    "rule_id",
                    LEGACY_RULE_ID,
                )

                scope = getattr(
                    result,
                    "scope",
                    LEGACY_SCOPE,
                )

                target_id = getattr(
                    result,
                    "target_id",
                    LEGACY_TARGET_ID,
                )

                if isinstance(
                    severity,
                    str,
                ):

                    try:
                        severity = NWFSeverity[
                            severity
                        ]

                    except Exception:
                        severity = None

            except Exception:

                # -----------------------------------------
                # Legacy object fallback
                #
                # なぜ必要か:
                # 旧 validator 実装互換を
                # Adapter責務として吸収するため。
                # -----------------------------------------
                is_valid = getattr(
                    result,
                    "is_valid",
                    True,
                )

                raw_code = getattr(
                    result,
                    "error_code",
                    "",
                )

                message = getattr(
                    result,
                    "message",
                    "",
                )

                violated_rules = getattr(
                    result,
                    "violated_rules",
                    [],
                )

                severity = None

                rule_id = getattr(
                    result,
                    "rule_id",
                    LEGACY_RULE_ID,
                )

                scope = getattr(
                    result,
                    "scope",
                    LEGACY_SCOPE,
                )

                target_id = getattr(
                    result,
                    "target_id",
                    LEGACY_TARGET_ID,
                )

        # -------------------------------------------------
        # severity 正規化
        #
        # なぜ必要か:
        # Legacy validator が severity 未返却時でも
        # Severity consistency を維持するため。
        # -------------------------------------------------
        if not isinstance(
            severity,
            NWFSeverity,
        ):
            severity = (
                self.error_mapper.infer_severity(
                    is_valid
                )
            )

        mapped_code = (
            self.error_mapper.map_error_code(
                raw_code
            )
        )

        # -------------------------------------------------
        # ★ Step 3:
        # violated_rules includes rule_id 同期
        #
        # なぜ必要か:
        # strict schema:
        # violated_rules must include rule_id
        #
        # Legacy validator が violated_rules を
        # 未返却/不完全返却した場合でも
        # Adapter責務として補完する。
        # -------------------------------------------------
        if not isinstance(
            violated_rules,
            list,
        ):
            violated_rules = []

        normalized_violated_rules = [
            str(rule)
            for rule in violated_rules
            if rule is not None
        ]

        if not is_valid:

            # ---------------------------------------------
            # invalid時 violated_rules 空禁止
            # ---------------------------------------------
            if not normalized_violated_rules:
                normalized_violated_rules = [
                    str(rule_id)
                ]

            # ---------------------------------------------
            # violated_rules must include rule_id
            # ---------------------------------------------
            if (
                str(rule_id)
                not in normalized_violated_rules
            ):
                normalized_violated_rules.append(
                    str(rule_id)
                )

        # -------------------------------------------------
        # strict schema 完全準拠
        # -------------------------------------------------
        return ValidationResult(
            rule_id=str(rule_id),
            scope=str(scope),
            target_id=str(target_id),
            is_valid=is_valid,
            severity=severity,
            error_code=mapped_code,
            message=message,
            violated_rules=(
                normalized_violated_rules
            ),
            transaction_id=(
                context.transaction_id
            ),
            stardate=(
                context.current_stardate
            ),
            metadata={
                "adapter":
                    "ValidatorIntegrationAdapter",
                "original_error_code":
                    raw_code,
                "legacy_conversion":
                    True,
            },
        )


# =========================================================
# main guard
# =========================================================
if __name__ == "__main__":

    # -----------------------------------------------------
    # main guard は実運用対象外
    #
    # なぜ必要か:
    # Optional DI化後に
    # story_db 未指定失敗を防止するため。
    # -----------------------------------------------------

    print(
        "ValidatorIntegrationAdapter "
        "main guard is disabled."
    )

# [EOF]
