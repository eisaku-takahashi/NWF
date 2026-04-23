"""
Source: src/integrity/validation_result.py
Updated: 2026-04-23T04:06:00+09:00  # ★Phase 3.4 契約再確認（is_blocking責務明文化・将来拡張コメント追加）
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Execution_Spec/NWF_Validator_And_Context_Contract_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
    - src/models/nwf_enums.py
Docstring:
    ValidationResult データクラス。

    Validator の検証結果を immutable な形式で保持し、
    Engine / Adapter / IntegrityChecker 間のインターフェース統一を保証する。

    ★ Phase 3.4 最終修正内容:
    - Strict Return Contract 完全準拠
    - Severity と is_valid の双方向整合性強制（強化）
    - 成功時の violated_rules 非空禁止（追加）
    - failure() の severity 制限強化（ERROR/CRITICALのみ許可）
    - stardate 精度保証（float正規化）
    - metadata の防御コピー化（外部参照防止）
    - JSON変換の安定性向上

    ★ Phase 3.4 追加（最重要）:
    - merge() メソッド導入（唯一の集約手段）
    - ValidationResult の手動集約禁止ルール明文化

    ★ Phase 3.4 追加修正:
    - is_blocking() の責務を ValidationResult に統一
    - Enum依存排除（設計安定化）

    ★ Phase 3.4 契約再確認（今回）:
    - is_blocking() を「唯一の停止判定契約」として明文化
    - Engine は severity を直接参照せず、本メソッドを信頼する設計を推奨
    - 将来のポリシー変更（ERROR昇格等）に対する拡張ポイントを明示
"""

# =========================
# import
# =========================
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any

from src.models.nwf_enums import NWFSeverity

# =========================
# 定数 / 設定
# =========================

SUCCESS_CODE: str = ""

# =========================
# __all__
# =========================

__all__ = [
    "ValidationResult",
]

# =========================
# Classes
# =========================


@dataclass(frozen=True)
class ValidationResult:
    """
    ValidationResult は Validator の検証結果を表す immutable データクラス。

    【⚠️ 重要設計ルール（Phase 3.4）】
    --------------------------------------------------
    ❌ 以下は禁止:
        - 複数 ValidationResult を all()/any() 等で集約
        - 手動で新しい ValidationResult を再生成（集約用途）

    ✅ 必須:
        - 集約は ValidationResult.merge() のみ使用すること

    なぜ:
        - Severity の欠落（今回の重大バグ原因）
        - error_code / message の消失防止
    --------------------------------------------------
    """

    is_valid: bool
    severity: NWFSeverity
    error_code: str = SUCCESS_CODE
    message: str = ""
    violated_rules: List[str] = field(default_factory=list)

    transaction_id: str = ""
    stardate: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """
        不変オブジェクトの整合性を保証するための検証処理。
        """

        # -----------------------------
        # Severity と is_valid の整合性保証
        # -----------------------------
        if self.severity in (NWFSeverity.ERROR, NWFSeverity.CRITICAL):
            if self.is_valid:
                raise ValueError(
                    "ERROR/CRITICAL の場合 is_valid は False でなければならない"
                )
        elif self.severity == NWFSeverity.INFO:
            if not self.is_valid:
                raise ValueError(
                    "INFO の場合 is_valid は True でなければならない"
                )

        # -----------------------------
        # 成功時の error_code 正規化
        # -----------------------------
        if self.is_valid and not self.error_code:
            object.__setattr__(self, "error_code", SUCCESS_CODE)

        # -----------------------------
        # 成功時 violated_rules 禁止
        # -----------------------------
        if self.is_valid and self.violated_rules:
            raise ValueError(
                "is_valid=True の場合 violated_rules は空でなければならない"
            )

        # -----------------------------
        # 型保証
        # -----------------------------
        if not isinstance(self.violated_rules, list):
            raise TypeError("violated_rules は List[str] である必要がある")

        if not isinstance(self.metadata, dict):
            raise TypeError("metadata は Dict[str, Any] である必要がある")

        if not isinstance(self.transaction_id, str):
            raise TypeError("transaction_id は str である必要がある")

        if not isinstance(self.stardate, (float, int)):
            raise TypeError("stardate は float である必要がある")

        # -----------------------------
        # 正規化処理
        # -----------------------------
        object.__setattr__(self, "stardate", float(self.stardate))
        object.__setattr__(self, "metadata", dict(self.metadata))

    # =========================
    # Utility Methods
    # =========================

    def to_dict(self) -> Dict[str, Any]:
        """JSONシリアライズ"""
        result = asdict(self)
        result["severity"] = self.severity.name
        return result

    def is_blocking(self) -> bool:
        """
        ★ Phase 3.4 修正（最重要）
        ★ Phase 3.4 契約再確認（今回）

        【修正前】
        return self.severity.is_blocking()

        【問題点】
        - Enumにロジックを委譲している
        - ValidationResultの責務が不明確
        - Engineとの結合が強くなる

        【修正後】
        - ValidationResult自身がblocking判定を持つ
        - 単一責務原則に従う
        - Engineは本メソッドのみを参照すべき（推奨）

        【現在仕様】
        - CRITICALのみがシステム停止条件

        【設計意図（重要）】
        - Engineは「停止判定ロジック」を持たない
        - ValidationResultが「停止信号」を保持する
        → Pipelineの責務分離を維持

        【将来拡張余地】
        - ERRORを条件付きでblockingに昇格可能
        - Policy注入（設定ファイル・Context依存）へ拡張可能

        【注意】
        - Engine側にフォールバックとして severity 比較が残っていてもよいが、
          最終的には本メソッドへ完全統一することが望ましい
        """

        # -----------------------------
        # ★ 現行実装（単純判定）
        # -----------------------------
        return self.severity == NWFSeverity.CRITICAL

        # -----------------------------
        # ★ 将来拡張例（コメントとして保持）
        # -----------------------------
        # if self.severity == NWFSeverity.CRITICAL:
        #     return True
        #
        # if self.severity == NWFSeverity.ERROR:
        #     return self.metadata.get("escalate_to_blocking", False)
        #
        # return False

    # =========================
    # ★ Phase 3.4 追加（最重要）
    # =========================
    @classmethod
    def merge(cls, results: List["ValidationResult"]) -> "ValidationResult":

        # -----------------------------
        # 空配列防御（契約違反）
        # -----------------------------
        if not results:
            raise RuntimeError("ValidationResult.merge(): empty results")

        # -----------------------------
        # Severity優先度定義
        # -----------------------------
        priority = {
            NWFSeverity.INFO: 0,
            NWFSeverity.WARNING: 1,
            NWFSeverity.ERROR: 2,
            NWFSeverity.CRITICAL: 3,
        }

        # -----------------------------
        # 最大Severity選択
        # -----------------------------
        max_result = max(results, key=lambda r: priority[r.severity])
        is_valid = all(r.is_valid for r in results)

        # -----------------------------
        # メッセージ統合
        # -----------------------------
        messages = [r.message for r in results if r.message]
        combined_message = " | ".join(messages) if messages else ""

        # -----------------------------
        # violated_rules 統合
        # -----------------------------
        all_rules: List[str] = []
        for r in results:
            all_rules.extend(r.violated_rules)

        # -----------------------------
        # 新規インスタンス生成（唯一の合法集約）
        # -----------------------------
        return cls(
            is_valid=is_valid,
            severity=max_result.severity if not is_valid else NWFSeverity.INFO,
            error_code=max_result.error_code,
            message=combined_message,
            violated_rules=all_rules,
            transaction_id=max_result.transaction_id,
            stardate=max_result.stardate,
            metadata={"merged": True}
        )

    # =========================
    # Factory Methods
    # =========================

    @staticmethod
    def success(
        message: str = "",
        transaction_id: str = "",
        stardate: float = 0.0,
        metadata: Dict[str, Any] | None = None,
    ) -> "ValidationResult":
        return ValidationResult(
            is_valid=True,
            severity=NWFSeverity.INFO,
            error_code=SUCCESS_CODE,
            message=message,
            violated_rules=[],
            transaction_id=transaction_id,
            stardate=stardate,
            metadata=metadata or {},
        )

    @staticmethod
    def failure(
        severity: NWFSeverity,
        error_code: str,
        message: str,
        violated_rules: List[str] | None = None,
        transaction_id: str = "",
        stardate: float = 0.0,
        metadata: Dict[str, Any] | None = None,
    ) -> "ValidationResult":

        # -----------------------------
        # severity制約（契約）
        # -----------------------------
        if severity not in (NWFSeverity.ERROR, NWFSeverity.CRITICAL):
            raise ValueError(
                "failure() では severity は ERROR または CRITICAL のみ許可される"
            )

        return ValidationResult(
            is_valid=False,
            severity=severity,
            error_code=error_code,
            message=message,
            violated_rules=violated_rules or [],
            transaction_id=transaction_id,
            stardate=stardate,
            metadata=metadata or {},
        )


# =========================
# Main Guard
# =========================

if __name__ == "__main__":

    r1 = ValidationResult.success(message="ok1")
    r2 = ValidationResult.failure(
        severity=NWFSeverity.ERROR,
        error_code="ERR_TEST",
        message="error occurred"
    )

    merged = ValidationResult.merge([r1, r2])
    print(merged.to_dict())

# [EOF]