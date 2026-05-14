"""
Source: src/integrity/validation_result.py
Updated: 2026-05-03T15:04:00+09:00  # ★修正: 作成日時に更新（Implementation Rules準拠）
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
    - docs/project/NWF_Phase_3.5_Debug_Work_Plan_v20260502.md
    - src/models/nwf_enums.py
Docstring:
    ValidationResult モジュール。

    Validatorの検証結果を表す immutable データクラスを定義する。
    Phase 3.5 において I/F契約の完全整合を行い、
    Validator / Engine / Evaluator 間のデータ整合性を保証する。
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any

from src.models.nwf_enums import NWFSeverity

# =========================================================
# 定数
# =========================================================
SUCCESS_CODE: str = ""

# ★追加: scopeの許可値（Spec曖昧性排除）
ALLOWED_SCOPES = {
    "SYSTEM_INTEGRITY",
}

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

    I/F契約（Phase 3.5 確定仕様）:
    - rule_id を必須識別子として使用
    - severity / scope / target_id を統一的に扱う
    - failure() / success() により完全固定I/Fを提供
    """

    # =========================================================
    # ★ rule_id（I/F契約: 必須）
    # =========================================================
    # 修正前: rule_id: str = ""
    # 修正後: 必須扱い（空文字禁止は__post_init__で検証）
    rule_id: str = ""

    # =========================================================
    # 基本フィールド
    # =========================================================
    is_valid: bool = True
    severity: NWFSeverity = NWFSeverity.INFO
    error_code: str = SUCCESS_CODE
    message: str = ""
    violated_rules: List[str] = field(default_factory=list)

    transaction_id: str = ""
    stardate: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    # =========================================================
    # Trace系
    # =========================================================
    trace_id: str = ""
    span_id: str = ""
    source: str = ""
    target_id: str = ""

    # =========================================================
    # ★互換レイヤ
    # =========================================================
    code: str = ""     # alias
    scope: str = ""    # alias

    # =========================================================
    # Post Init
    # =========================================================
    def __post_init__(self):
        """
        初期化後の整合性チェックおよび正規化処理
        """

        # -----------------------------
        # alias 正規化
        # -----------------------------
        if self.code and not self.error_code:
            object.__setattr__(self, "error_code", self.code)

        if self.error_code and not self.code:
            object.__setattr__(self, "code", self.error_code)

        # -----------------------------
        # ★ rule_id 必須チェック
        # -----------------------------
        if not self.rule_id:
            raise ValueError("rule_id is required")

        # -----------------------------
        # ★ scope 検証（Spec準拠）
        # -----------------------------
        if self.scope:
            if self.scope not in ALLOWED_SCOPES:
                raise ValueError(f"invalid scope: {self.scope}")

        # -----------------------------
        # Severity と is_valid の整合性
        # -----------------------------
        if self.severity in (NWFSeverity.ERROR, NWFSeverity.CRITICAL):
            if self.is_valid:
                raise ValueError("ERROR/CRITICAL の場合 is_valid=False 必須")

        elif self.severity == NWFSeverity.INFO:
            if not self.is_valid:
                raise ValueError("INFO の場合 is_valid=True 必須")

        # -----------------------------
        # violated_rules 制約
        # -----------------------------
        if self.is_valid and self.violated_rules:
            raise ValueError("is_valid=True の場合 violated_rules は空")

        # -----------------------------
        # ★ violated_rules と rule_id の関係明確化
        # -----------------------------
        # 理由:
        # - rule_id は単一の主識別子
        # - violated_rules は複数違反の集合
        # - failure() において最低1件は rule_id を含むことを保証
        if not self.is_valid:
            if not self.violated_rules:
                raise ValueError("violated_rules must not be empty when invalid")
            if self.rule_id not in self.violated_rules:
                raise ValueError("violated_rules must include rule_id")

        # -----------------------------
        # 型チェック
        # -----------------------------
        if not isinstance(self.metadata, dict):
            raise TypeError("metadata must be dict")

        if not isinstance(self.trace_id, str):
            raise TypeError("trace_id must be str")

        # -----------------------------
        # 正規化
        # -----------------------------
        object.__setattr__(self, "stardate", float(self.stardate))
        object.__setattr__(self, "metadata", dict(self.metadata))

    # =========================================================
    # Utility
    # =========================================================
    def to_dict(self) -> Dict[str, Any]:
        """
        dict形式に変換
        """
        result = asdict(self)
        result["severity"] = self.severity.name
        return result

    def is_blocking(self) -> bool:
        """
        CRITICAL判定
        """
        return self.severity == NWFSeverity.CRITICAL

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ValidationResult):
            return False
        return self.to_dict() == other.to_dict()

    # =========================================================
    # merge
    # =========================================================
    @classmethod
    def merge(cls, results: List["ValidationResult"]) -> "ValidationResult":
        """
        複数結果のマージ
        """

        if not results:
            raise RuntimeError("merge(): empty")

        priority = {
            NWFSeverity.INFO: 0,
            NWFSeverity.WARNING: 1,
            NWFSeverity.ERROR: 2,
            NWFSeverity.CRITICAL: 3,
        }

        max_result = max(results, key=lambda r: priority[r.severity])
        is_valid = all(r.is_valid for r in results)

        messages = [r.message for r in results if r.message]

        return cls(
            rule_id=max_result.rule_id,
            is_valid=is_valid,
            severity=max_result.severity if not is_valid else NWFSeverity.INFO,
            error_code=max_result.error_code,
            message=" | ".join(messages),
            violated_rules=[x for r in results for x in r.violated_rules],
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
    # 修正前（削除・コメント化）
    # ---------------------------------------------------------
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
    # - Spec Driven Development違反
    # - failure() との非対称性

    # ---------------------------------------------------------
    # 修正後（I/F完全固定）
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
        成功結果生成（INFO）

        修正内容:
        - failure() と完全対称なI/F構造
        - kwargs 排除
        - 必須項目を明示化
        """

        # ★必須チェック
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
        失敗結果生成（ERROR / CRITICAL）

        修正内容:
        - I/Fを完全固定（Work Planと100%一致）
        - kwargs廃止
        - rule_id / target_id / scope を必須化
        """

        if severity not in (NWFSeverity.ERROR, NWFSeverity.CRITICAL):
            raise ValueError("failure(): ERROR/CRITICAL only")

        # ★必須チェック
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