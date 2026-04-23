"""
Source: src/core/metadata_manager.py
Updated: 2026-04-21T14:40:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - src/integrity/validation_result.py
    - src/models/nwf_enums.py
Docstring:
    MetadataManager（Phase 3.4対応版）
    時間整合性検証を ValidationResult ベースに統一
"""

# =========================================================
# import
# =========================================================
from src.integrity.validation_result import ValidationResult
from src.models.nwf_enums import NWFSeverity


# =========================================================
# Classes
# =========================================================
class MetadataManager:

    def __init__(self):
        self.anchor = None

    def register_anchor(self, event: dict):
        """
        基準イベント登録
        """
        self.anchor = event

    def validate_temporal_consistency(self, event: dict) -> ValidationResult:
        """
        時間整合性検証（Phase 3.4対応）

        Args:
            event (dict)

        Returns:
            ValidationResult
        """

        # =========================================================
        # ▼ 旧実装（参考として残す）
        # =========================================================
        # return TemporalResult(
        #     success=False,
        #     error_code="TEMPORAL_CAUSALITY_VIOLATION",
        #     message="Temporal paradox detected"
        # )

        # =========================================================
        # ▼ Phase 3.4 実装
        # =========================================================

        if self.anchor and event["stardate"] < self.anchor["stardate"]:
            return ValidationResult(
                is_valid=False,
                severity=NWFSeverity.CRITICAL,
                error_code="TEMPORAL_CAUSALITY_VIOLATION",
                message="Temporal paradox detected",
                violated_rules=["TEMPORAL_CAUSALITY"],
                transaction_id="N/A",  # 必要なら後でcontext連携
                stardate=event["stardate"],
                metadata={}
            )

        return ValidationResult(
            is_valid=True,
            severity=NWFSeverity.INFO,
            error_code=None,
            message="Temporal consistency OK",
            violated_rules=[],
            transaction_id="N/A",
            stardate=event["stardate"],
            metadata={}
        )

# [EOF]