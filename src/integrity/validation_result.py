"""
Source: src/integrity/validation_result.py
Updated: 2026-06-05T09:53:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
    - docs/spec/Execution_Spec/NWF_Validation_System_v2.0.1.md
    - docs/spec/Execution_Spec/NWF_Validator_And_Context_Contract_v2.0.1.md
    - src/models/nwf_enums.py
Docstring:
    ValidationResult モジュール。

    Validator の検証結果を表す immutable データクラスを定義する。

    Phase 3.5 Validation Integration Audit Step 1 対応版。

    保証事項:
    - rule_id 必須
    - scope 必須
    - target_id 必須
    - immutable dataclass
    - strict schema enforcement
    - Severity Monotonicity
    - ValidationResult merge() 契約準拠
"""

from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Dict
from typing import List

from src.models.nwf_enums import NWFSeverity

SUCCESS_CODE: str = ""

__all__ = [
    "ValidationResult",
]


@dataclass(frozen=True)
class ValidationResult:
    """
    ValidationResult は Validator の検証結果を表す immutable データクラス。
    """

    # =========================================================
    # strict schema 必須項目
    # =========================================================

    rule_id: str = ""

    # =========================================================
    # 基本属性
    # =========================================================

    is_valid: bool = True
    severity: NWFSeverity = NWFSeverity.INFO

    error_code: str = SUCCESS_CODE
    message: str = ""

    violated_rules: List[str] = field(default_factory=list)

    # =========================================================
    # Traceability
    # =========================================================

    transaction_id: str = ""
    stardate: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    trace_id: str = ""
    span_id: str = ""
    source: str = ""

    target_id: str = ""

    # Legacy alias
    code: str = ""

    scope: str = ""

    def __post_init__(self) -> None:
        """
        strict schema 検証。
        """

        # -----------------------------------------------------
        # alias 同期
        # -----------------------------------------------------

        if self.code and not self.error_code:
            object.__setattr__(self, "error_code", self.code)

        if self.error_code and not self.code:
            object.__setattr__(self, "code", self.error_code)

        # -----------------------------------------------------
        # severity 正規化
        # -----------------------------------------------------

        if isinstance(self.severity, str):
            try:
                object.__setattr__(
                    self,
                    "severity",
                    NWFSeverity[self.severity],
                )
            except KeyError:
                object.__setattr__(
                    self,
                    "severity",
                    NWFSeverity(self.severity),
                )

        # -----------------------------------------------------
        # 必須フィールド
        # -----------------------------------------------------

        if not isinstance(self.rule_id, str):
            raise TypeError("rule_id must be str")

        if not self.rule_id.strip():
            raise ValueError("rule_id is required")

        if not isinstance(self.target_id, str):
            raise TypeError("target_id must be str")

        if not self.target_id.strip():
            raise ValueError("target_id is required")

        if not isinstance(self.scope, str):
            raise TypeError("scope must be str")

        if not self.scope.strip():
            raise ValueError("scope is required")

        # -----------------------------------------------------
        # 型検査
        # -----------------------------------------------------

        if not isinstance(self.metadata, dict):
            raise TypeError("metadata must be dict")

        if not isinstance(self.trace_id, str):
            raise TypeError("trace_id must be str")

        if not isinstance(self.span_id, str):
            raise TypeError("span_id must be str")

        if not isinstance(self.transaction_id, str):
            raise TypeError("transaction_id must be str")

        # -----------------------------------------------------
        # Severity ↔ is_valid 整合性
        # -----------------------------------------------------

        if self.severity in (
            NWFSeverity.ERROR,
            NWFSeverity.CRITICAL,
        ):
            if self.is_valid:
                raise ValueError("ERROR/CRITICAL requires is_valid=False")

        elif self.severity == NWFSeverity.INFO:
            if not self.is_valid:
                raise ValueError("INFO requires is_valid=True")

        # WARNING は valid/invalid の両方を許容

        # -----------------------------------------------------
        # violated_rules
        # -----------------------------------------------------

        if self.is_valid:
            if self.violated_rules:
                raise ValueError("violated_rules must be empty when valid")

        else:
            if not self.violated_rules:
                raise ValueError("violated_rules must not be empty when invalid")

            if self.rule_id not in self.violated_rules:
                raise ValueError("violated_rules must include rule_id")

        # -----------------------------------------------------
        # 正規化
        # -----------------------------------------------------

        object.__setattr__(
            self,
            "stardate",
            float(self.stardate),
        )

        object.__setattr__(
            self,
            "metadata",
            dict(self.metadata),
        )

    # =========================================================
    # Utility
    # =========================================================

    def to_dict(self) -> Dict[str, Any]:
        """
        dict 変換。
        """

        result = asdict(self)
        result["severity"] = self.severity.name
        return result

    def is_blocking(self) -> bool:
        """
        Engine 停止判定。

        CRITICAL のみ停止。
        """

        return self.severity == NWFSeverity.CRITICAL

    # =========================================================
    # Equality
    # =========================================================

    def __eq__(self, other: object) -> bool:
        """
        Validation System v2.0.1 §21 準拠。

        timestamp 系は比較対象外。
        """

        if not isinstance(other, ValidationResult):
            return False

        return (
            self.severity == other.severity
            and self.code == other.code
            and self.message == other.message
            and self.target_id == other.target_id
            and self.rule_id == other.rule_id
            and self.span_id == other.span_id
            and self.trace_id == other.trace_id
            and self.source == other.source
            and self.scope == other.scope
        )

    # =========================================================
    # Merge
    # =========================================================

    @classmethod
    def merge(
        cls,
        results: List["ValidationResult"],
    ) -> "ValidationResult":
        """
        ValidationResult 集約。

        Severity Monotonicity 準拠。
        """

        if not results:
            raise RuntimeError("merge(): empty")

        severity_priority = {
            NWFSeverity.INFO: 0,
            NWFSeverity.WARNING: 1,
            NWFSeverity.ERROR: 2,
            NWFSeverity.CRITICAL: 3,
        }

        max_result = max(
            results,
            key=lambda r: severity_priority[r.severity],
        )

        merged_rules: List[str] = []

        for result in results:
            for rule in result.violated_rules:
                if rule not in merged_rules:
                    merged_rules.append(rule)

        is_valid = all(r.is_valid for r in results)

        messages = [r.message for r in results if r.message]

        if is_valid:
            return cls(
                rule_id=max_result.rule_id,
                is_valid=True,
                severity=NWFSeverity.INFO,
                error_code="",
                message=" | ".join(messages),
                violated_rules=[],
                transaction_id=max_result.transaction_id,
                stardate=max_result.stardate,
                metadata={"merged": True},
                trace_id=max_result.trace_id,
                span_id=max_result.span_id,
                source="merge",
                target_id=max_result.target_id,
                scope=max_result.scope,
            )

        return cls(
            rule_id=max_result.rule_id,
            is_valid=False,
            severity=max_result.severity,
            error_code=max_result.error_code,
            message=" | ".join(messages),
            violated_rules=merged_rules,
            transaction_id=max_result.transaction_id,
            stardate=max_result.stardate,
            metadata={"merged": True},
            trace_id=max_result.trace_id,
            span_id=max_result.span_id,
            source="merge",
            target_id=max_result.target_id,
            scope=max_result.scope,
        )

    # =========================================================
    # Factory
    # =========================================================

    @staticmethod
    def success(
        rule_id: str,
        target_id: str,
        scope: str,
        message: str = "",
        metadata: Dict[str, Any] | None = None,
    ) -> "ValidationResult":
        """
        成功結果生成。
        """

        return ValidationResult(
            rule_id=rule_id,
            is_valid=True,
            severity=NWFSeverity.INFO,
            message=message,
            violated_rules=[],
            target_id=target_id,
            scope=scope,
            metadata=metadata or {},
        )

    @staticmethod
    def failure(
        severity: NWFSeverity,
        message: str,
        rule_id: str,
        target_id: str,
        scope: str,
        error_code: str = "",
        violated_rules: List[str] | None = None,
    ) -> "ValidationResult":
        """
        失敗結果生成。

        WARNING / ERROR / CRITICAL を許容。
        """

        if severity not in (
            NWFSeverity.WARNING,
            NWFSeverity.ERROR,
            NWFSeverity.CRITICAL,
        ):
            raise ValueError("failure(): WARNING/ERROR/CRITICAL only")

        return ValidationResult(
            rule_id=rule_id,
            is_valid=False,
            severity=severity,
            error_code=error_code,
            message=message,
            violated_rules=(
                violated_rules if violated_rules is not None else [rule_id]
            ),
            target_id=target_id,
            scope=scope,
        )


# [EOF]
