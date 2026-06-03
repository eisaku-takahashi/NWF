"""
Source: src/integrity/validation_result.py
Updated: 2026-05-18T12:46:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
    - docs/project/NWF_Phase_3.5_Debug_Work_Plan_v20260516.md
    - docs/spec/Execution_Spec/NWF_Validation_System_v2.0.1.md
    - docs/spec/Execution_Spec/NWF_Validator_Orchestration_Spec_v2.0.1.md
    - src/models/nwf_enums.py
Docstring:
    ValidationResult モジュール。

    Validator の検証結果を表す immutable データクラスを定義する。

    Phase 3.5 において ValidationResult strict schema を維持しつつ、
    Pass-through 原則および Legacy Adapter 互換性を保証する。

    本実装では以下を保証する：

    - rule_id 必須
    - scope 必須（ただし値制限は行わない）
    - target_id 必須
    - immutable dataclass
    - strict schema enforcement
    - Validator / Adapter / Engine 間の非破壊伝播
"""

from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Dict
from typing import List

from src.models.nwf_enums import NWFSeverity

# =========================================================
# 定数
# =========================================================

SUCCESS_CODE: str = ""

# =========================================================
# 公開インターフェース
# =========================================================

__all__ = [
    "ValidationResult",
]

# =========================================================
# ValidationResult
# =========================================================


@dataclass(frozen=True)
class ValidationResult:
    """
    ValidationResult は Validator の検証結果を表す immutable データクラス。

    Phase 3.5 strict schema 仕様に基づき、
    Validator / Adapter / Engine 間で統一I/Fを提供する。

    Attributes:
        rule_id:
            ルール識別子。
            strict schema により必須。

        is_valid:
            Validation 成功可否。

        severity:
            検証結果の重大度。

        error_code:
            エラーコード。

        message:
            人間可読メッセージ。

        violated_rules:
            違反ルール一覧。

        target_id:
            対象エンティティID。

        scope:
            Validation スコープ。
            strict schema により必須。

            注意:
                Execution Spec 準拠により、
                ValidationResult 層では値制限を行わない。

                理由:
                - Pass-through 原則維持
                - Legacy Adapter 互換維持
                - TEST_SCOPE / LEGACY 許容
                - Validator 側の fallback 処理維持
    """

    # =========================================================
    # strict schema 必須属性
    # =========================================================

    # ---------------------------------------------------------
    # rule_id
    # ---------------------------------------------------------
    # 修正前:
    # rule_id: str = ""
    #
    # 修正後:
    # strict schema により必須化。
    # 空文字禁止は __post_init__ で検証する。
    # ---------------------------------------------------------
    rule_id: str = ""

    # ---------------------------------------------------------
    # 基本属性
    # ---------------------------------------------------------
    is_valid: bool = True
    severity: NWFSeverity = NWFSeverity.INFO
    error_code: str = SUCCESS_CODE
    message: str = ""
    violated_rules: List[str] = field(default_factory=list)

    # ---------------------------------------------------------
    # トレーサビリティ
    # ---------------------------------------------------------
    transaction_id: str = ""
    stardate: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    # ---------------------------------------------------------
    # Trace 系
    # ---------------------------------------------------------
    trace_id: str = ""
    span_id: str = ""
    source: str = ""

    # ---------------------------------------------------------
    # strict schema 必須属性
    # ---------------------------------------------------------
    target_id: str = ""

    # =========================================================
    # Legacy Compatibility Layer
    # =========================================================

    # ---------------------------------------------------------
    # code
    # ---------------------------------------------------------
    # 理由:
    # Legacy validator 互換。
    # error_code の alias として扱う。
    # ---------------------------------------------------------
    code: str = ""

    # ---------------------------------------------------------
    # scope
    # ---------------------------------------------------------
    # 修正前:
    # ALLOWED_SCOPES による値制限あり。
    #
    # 問題:
    # - Work Plan の TEST_SCOPE と矛盾
    # - Legacy Adapter の LEGACY と矛盾
    # - Pass-through 原則違反
    # - Execution Spec 違反
    #
    # 修正後:
    # strict schema において「非空のみ保証」へ変更。
    #
    # 理由:
    # - 任意文字列許容
    # - 意味変更禁止原則維持
    # - Legacy Adapter 互換維持
    # - Validator fallback 処理維持
    # ---------------------------------------------------------
    scope: str = ""

    # =========================================================
    # Post Init
    # =========================================================

    def __post_init__(self) -> None:
        """
        初期化後の strict schema 検証および正規化処理。

        Raises:
            ValueError:
                strict schema 違反時。

            TypeError:
                型不整合時。
        """

        # -----------------------------------------------------
        # alias 正規化
        # -----------------------------------------------------
        # 理由:
        # Legacy validator compatibility。
        # code と error_code を同期する。
        # -----------------------------------------------------

        if self.code and not self.error_code:
            object.__setattr__(self, "error_code", self.code)

        if self.error_code and not self.code:
            object.__setattr__(self, "code", self.error_code)

        # -----------------------------------------------------
        # strict schema:
        # rule_id 必須
        # -----------------------------------------------------

        if not str(self.rule_id).strip():
            raise ValueError("rule_id is required")

        # -----------------------------------------------------
        # strict schema:
        # target_id 必須
        # -----------------------------------------------------

        if not str(self.target_id).strip():
            raise ValueError("target_id is required")

        # -----------------------------------------------------
        # strict schema:
        # scope 必須
        # -----------------------------------------------------
        # 修正前（コメント化保持）:
        #
        # if self.scope:
        #     if self.scope not in ALLOWED_SCOPES:
        #         raise ValueError(f"invalid scope: {self.scope}")
        #
        # 削除理由:
        # - Execution Spec 違反
        # - Pass-through 原則違反
        # - Work Plan TEST_SCOPE と矛盾
        # - Legacy Adapter LEGACY と矛盾
        #
        # 修正後:
        # 非空のみ保証。
        # 値制限は行わない。
        # -----------------------------------------------------

        if not str(self.scope).strip():
            raise ValueError("scope is required")

        # -----------------------------------------------------
        # Severity と is_valid 整合性
        # -----------------------------------------------------

        if self.severity in (
            NWFSeverity.ERROR,
            NWFSeverity.CRITICAL,
        ):
            if self.is_valid:
                raise ValueError(
                    "ERROR/CRITICAL の場合 is_valid=False 必須"
                )

        elif self.severity == NWFSeverity.INFO:
            if not self.is_valid:
                raise ValueError(
                    "INFO の場合 is_valid=True 必須"
                )

        # -----------------------------------------------------
        # violated_rules 制約
        # -----------------------------------------------------

        if self.is_valid and self.violated_rules:
            raise ValueError(
                "is_valid=True の場合 violated_rules は空"
            )

        # -----------------------------------------------------
        # invalid 時 violated_rules 必須
        # -----------------------------------------------------

        if not self.is_valid:
            if not self.violated_rules:
                raise ValueError(
                    "violated_rules must not be empty when invalid"
                )

            if self.rule_id not in self.violated_rules:
                raise ValueError(
                    "violated_rules must include rule_id"
                )

        # -----------------------------------------------------
        # 型チェック
        # -----------------------------------------------------

        if not isinstance(self.metadata, dict):
            raise TypeError("metadata must be dict")

        if not isinstance(self.trace_id, str):
            raise TypeError("trace_id must be str")

        if not isinstance(self.target_id, str):
            raise TypeError("target_id must be str")

        if not isinstance(self.scope, str):
            raise TypeError("scope must be str")

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
        dict 形式へ変換する。

        Returns:
            Dict[str, Any]:
                dict 化された ValidationResult。
        """

        result = asdict(self)
        result["severity"] = self.severity.name

        return result

    def is_blocking(self) -> bool:
        """
        blocking 判定。

        Returns:
            bool:
                CRITICAL の場合 True。
        """

        return self.severity == NWFSeverity.CRITICAL

    def __eq__(self, other: object) -> bool:
        """
        等価判定。

        Args:
            other:
                比較対象。

        Returns:
            bool:
                等価の場合 True。
        """

        if not isinstance(other, ValidationResult):
            return False

        return self.to_dict() == other.to_dict()

    # =========================================================
    # merge
    # =========================================================

    @classmethod
    def merge(
        cls,
        results: List["ValidationResult"],
    ) -> "ValidationResult":
        """
        ValidationResult をマージする。

        Args:
            results:
                ValidationResult 一覧。

        Returns:
            ValidationResult:
                マージ済み ValidationResult。

        Raises:
            RuntimeError:
                results が空の場合。
        """

        if not results:
            raise RuntimeError("merge(): empty")

        priority = {
            NWFSeverity.INFO: 0,
            NWFSeverity.WARNING: 1,
            NWFSeverity.ERROR: 2,
            NWFSeverity.CRITICAL: 3,
        }

        max_result = max(
            results,
            key=lambda r: priority[r.severity],
        )

        is_valid = all(r.is_valid for r in results)

        messages = [
            r.message
            for r in results
            if r.message
        ]

        return cls(
            rule_id=max_result.rule_id,
            is_valid=is_valid,
            severity=(
                max_result.severity
                if not is_valid
                else NWFSeverity.INFO
            ),
            error_code=max_result.error_code,
            message=" | ".join(messages),
            violated_rules=[
                x
                for r in results
                for x in r.violated_rules
            ],
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

    # ---------------------------------------------------------
    # 修正前（コメント化保持）
    # ---------------------------------------------------------
    #
    # @staticmethod
    # def success(**kwargs) -> "ValidationResult":
    #     return ValidationResult(
    #         is_valid=True,
    #         severity=NWFSeverity.INFO,
    #         **kwargs
    #     )
    #
    # 削除理由:
    # - kwargs による I/F曖昧性
    # - strict schema 違反
    # - failure() 非対称
    # - Spec Driven Development 違反
    # ---------------------------------------------------------

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

        Args:
            rule_id:
                ルールID。

            target_id:
                対象ID。

            scope:
                Validation scope。

            message:
                メッセージ。

            metadata:
                メタデータ。

        Returns:
            ValidationResult:
                INFO ValidationResult。
        """

        if not rule_id:
            raise ValueError("rule_id is required")

        if not target_id:
            raise ValueError("target_id is required")

        if not scope:
            raise ValueError("scope is required")

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

        Args:
            severity:
                ERROR または CRITICAL。

            message:
                エラーメッセージ。

            rule_id:
                ルールID。

            target_id:
                対象ID。

            scope:
                Validation scope。

            error_code:
                エラーコード。

            violated_rules:
                違反ルール一覧。

        Returns:
            ValidationResult:
                ERROR / CRITICAL ValidationResult。
        """

        if severity not in (
            NWFSeverity.ERROR,
            NWFSeverity.CRITICAL,
        ):
            raise ValueError(
                "failure(): ERROR/CRITICAL only"
            )

        if not rule_id:
            raise ValueError("rule_id is required")

        if not target_id:
            raise ValueError("target_id is required")

        if not scope:
            raise ValueError("scope is required")

        return ValidationResult(
            rule_id=rule_id,
            is_valid=False,
            severity=severity,
            error_code=error_code,
            message=message,
            violated_rules=violated_rules or [rule_id],
            target_id=target_id,
            scope=scope,
        )


# [EOF]