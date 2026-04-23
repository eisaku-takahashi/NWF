"""
Source: src/integrity/anomaly_detector.py
Updated: 2026-04-21T11:40:00+09:00  # ★Phase 3.4 CRITICAL検知強化対応
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Project_Governance/NWF_Recursive_Integrity_Spec_v2.0.1.md
    - docs/spec/Execution_Spec/NWF_Validator_And_Context_Contract_v2.0.1.md
    - src/integrity/recursive_auditor.py
    - src/integrity/validation_result.py
    - src/models/nwf_enums.py
Docstring:
    Anomaly Detector モジュール。

    【Phase 3.4 最終修正内容】
    - CRITICAL検知の拡張（時間逆行・存在矛盾）
    - ValidationResultのSeverity保証強化
    - 修正前ロジック保持＋差分明示
"""

# =========================
# Import
# =========================
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime, timezone, timedelta

from src.integrity.recursive_auditor import AuditReport
from src.integrity.validation_result import ValidationResult
from src.models.nwf_enums import NWFSeverity
from src.workflow.workflow_context import WorkflowContext

# =========================
# Constants / Config
# =========================
JST = timezone(timedelta(hours=9))
DEFAULT_CONFIDENCE_THRESHOLD = 0.85

# =========================
# Public Interface
# =========================
__all__ = [
    "IntegrityStatus",
    "FinalIntegrityResult",
    "AnomalyDetector"
]

# =========================
# Classes
# =========================
class IntegrityStatus(Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    SUSPEND = "SUSPEND"


class FinalIntegrityResult:
    def __init__(self, transaction_id: str):
        self.status: IntegrityStatus = IntegrityStatus.SUCCESS
        self.anomalies: List[str] = []
        self.requires_hitl: bool = False
        self.transaction_id: str = transaction_id
        self.timestamp: datetime = datetime.now(JST)

    def add_anomaly(self, message: str):
        self.anomalies.append(message)
        self.requires_hitl = True


class AnomalyDetector:
    """
    異常検知クラス（Validator）

    ★ 修正ポイント:
    - CRITICAL条件が不足していたため追加
    """

    def __init__(self, confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD):
        self.threshold = confidence_threshold

    def validate(
        self,
        context: WorkflowContext,
        target: Any
    ) -> List[ValidationResult]:

        if not isinstance(target, AuditReport):
            return [
                ValidationResult.failure(
                    severity=NWFSeverity.ERROR,
                    error_code="ERR_AD_TYPE",
                    message="Invalid target type for AnomalyDetector",
                    violated_rules=["TYPE_CONSTRAINT"],
                    transaction_id="",
                    stardate=context.current_stardate,
                    metadata={"received_type": str(type(target))}
                )
            ]

        audit_report: AuditReport = target
        results: List[ValidationResult] = []

        # -------------------------
        # 上流監査チェック（既存）
        # -------------------------
        if not audit_report.is_valid:
            results.append(
                self._create_result(
                    context,
                    audit_report,
                    severity=NWFSeverity.CRITICAL,
                    error_code="ERR_AD_001",
                    message="Upstream audit failed",
                    violated_rules=["RECURSIVE_INTEGRITY"]
                )
            )
            return results

        # -------------------------
        # metadata取得
        # -------------------------
        metadata = {}
        if hasattr(audit_report, "metadata"):
            metadata = audit_report.metadata

        # =========================================================
        # ★ Phase 3.4 追加: CRITICAL検知（時間逆行）
        # =========================================================
        # ❌ 修正前: 存在しない
        # ✅ 修正後: 明示的検知
        timeline = metadata.get("timeline", [])
        for i in range(1, len(timeline)):
            if timeline[i] < timeline[i - 1]:
                results.append(
                    self._create_result(
                        context,
                        audit_report,
                        NWFSeverity.CRITICAL,
                        "ERR_AD_TIME",
                        "Time reversal detected",
                        ["TIME_MONOTONICITY"]
                    )
                )
                return results  # CRITICALは即返却

        # =========================================================
        # ★ Phase 3.4 追加: CRITICAL検知（存在矛盾）
        # =========================================================
        # ❌ 修正前: ERROR扱い（弱すぎ）
        # ✅ 修正後: CRITICAL昇格
        known = metadata.get("known_entities", [])
        generated = metadata.get("generated_entities", [])

        for entity in generated:
            if entity not in known:
                # ★変更点:
                # 以前: ERROR
                # 今回: CRITICAL（世界破綻）
                results.append(
                    self._create_result(
                        context,
                        audit_report,
                        NWFSeverity.CRITICAL,
                        "ERR_AD_EXISTENCE",
                        f"Non-existent entity detected -> {entity}",
                        ["ENTITY_EXISTENCE"]
                    )
                )
                return results

        # -------------------------
        # 通常検知（既存）
        # -------------------------
        results.extend(self._check_narrative_spikes(context, audit_report, metadata))
        results.extend(self._check_confidence(context, audit_report, metadata))

        # -------------------------
        # 空結果禁止
        # -------------------------
        if not results:
            results.append(
                ValidationResult.success(
                    message="No anomalies detected",
                    transaction_id=audit_report.transaction_id,
                    stardate=context.current_stardate,
                    metadata={"detector": "AnomalyDetector"}
                )
            )

        return results

    # =========================================
    # ValidationResult生成
    # =========================================
    def _create_result(
        self,
        context: WorkflowContext,
        audit_report: AuditReport,
        severity: NWFSeverity,
        error_code: str,
        message: str,
        violated_rules: List[str]
    ) -> ValidationResult:

        return ValidationResult(
            is_valid=(severity in [NWFSeverity.INFO, NWFSeverity.WARNING]),
            severity=severity,
            error_code=error_code,
            message=message,
            violated_rules=violated_rules,
            transaction_id=audit_report.transaction_id,
            stardate=context.current_stardate,
            metadata={
                "detector": "AnomalyDetector",
                "timestamp": datetime.now(JST).isoformat()
            }
        )

    # =========================================
    # 既存ロジック
    # =========================================
    def _check_narrative_spikes(self, context, report, metadata):
        results = []
        curve = metadata.get("emotion_curve", [])

        for i in range(1, len(curve)):
            diff = abs(curve[i] - curve[i - 1])
            if diff > 0.7:
                results.append(
                    self._create_result(
                        context,
                        report,
                        NWFSeverity.WARNING,
                        "ERR_AD_003",
                        f"Emotion spike Δ={diff:.2f}",
                        ["EMOTION_CONTINUITY"]
                    )
                )
        return results

    def _check_confidence(self, context, report, metadata):
        results = []
        confidence = metadata.get("confidence_score")

        if confidence is not None and confidence < self.threshold:
            results.append(
                self._create_result(
                    context,
                    report,
                    NWFSeverity.WARNING,
                    "ERR_AD_004",
                    f"Low confidence {confidence:.2f}",
                    ["CONFIDENCE_THRESHOLD"]
                )
            )
        return results


# =========================
# Main Guard
# =========================
if __name__ == "__main__":
    dummy_report = AuditReport(transaction_id="test_tx")
    detector = AnomalyDetector()
    print("AnomalyDetector ready (Phase 3.4 FINAL)")



# [EOF]