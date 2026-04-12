"""
Source: src/integrity/anomaly_detector.py
Updated: 2026-04-12T09:47:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Project_Governance/NWF_Recursive_Integrity_Spec_v2.0.1.md
    - src/integrity/recursive_auditor.py
Docstring:
    Anomaly Detector モジュール。
    Recursive Integrity の最終層として、ハルシネーション検知・感情異常検知・信頼度評価を行い、
    最終的な整合性判定（SUCCESS / FAILURE / SUSPEND）を決定する。
"""

# =========================
# Import
# =========================
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime, timezone, timedelta

from src.integrity.recursive_auditor import AuditReport

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
    """
    最終整合性ステータス定義

    - SUCCESS: 問題なし
    - FAILURE: 上流監査で致命的エラー
    - SUSPEND: 異常検知により停止
    """
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    SUSPEND = "SUSPEND"


class FinalIntegrityResult:
    """
    最終整合性結果コンテナ（Spec 5.5準拠）

    Args:
        transaction_id (str): トランザクションID
    """

    def __init__(self, transaction_id: str):
        self.status: IntegrityStatus = IntegrityStatus.SUCCESS
        self.anomalies: List[str] = []
        self.requires_hitl: bool = False
        self.transaction_id: str = transaction_id
        self.timestamp: datetime = datetime.now(JST)

    def add_anomaly(self, message: str):
        """
        異常を追加し、状態を更新する

        Args:
            message (str): 異常内容
        """
        self.anomalies.append(message)
        # 異常が1つでもあればHITL検討対象
        self.requires_hitl = True


class AnomalyDetector:
    """
    異常検知クラス

    Args:
        confidence_threshold (float): 信頼度閾値
    """

    def __init__(self, confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD):
        self.threshold = confidence_threshold

    def detect(
        self,
        audit_report: AuditReport,
        ai_output_metadata: Optional[Dict] = None
    ) -> FinalIntegrityResult:
        """
        [監査] 最終監査レポートとAI生成メタデータを照合し異常を検知する

        Args:
            audit_report (AuditReport): 再帰監査結果
            ai_output_metadata (dict): AI生成メタデータ

        Returns:
            FinalIntegrityResult: 最終整合性結果
        """
        result = FinalIntegrityResult(audit_report.transaction_id)

        # -------------------------
        # 1. 上流監査チェック
        # -------------------------
        if not audit_report.is_valid:
            result.status = IntegrityStatus.FAILURE
            result.add_anomaly("CRITICAL: Upstream audit failed.")
            return result

        # metadata が無い場合は空辞書として扱う
        metadata = ai_output_metadata or {}

        # -------------------------
        # 2. ハルシネーション検知
        # -------------------------
        self._detect_hallucinations(metadata, result)

        # -------------------------
        # 3. 感情・トーン異常検知
        # -------------------------
        self._check_narrative_spikes(metadata, result)

        # -------------------------
        # 4. 信頼度評価
        # -------------------------
        self._check_confidence(metadata, result)

        # -------------------------
        # 5. 最終判定
        # -------------------------
        if result.anomalies or result.requires_hitl:
            result.status = IntegrityStatus.SUSPEND

        return result

    # =========================
    # Internal Methods
    # =========================
    def _detect_hallucinations(self, metadata: Dict, result: FinalIntegrityResult):
        """
        未定義エンティティ（ハルシネーション）検知

        Args:
            metadata (dict): AIメタデータ
            result (FinalIntegrityResult): 出力結果
        """
        known_entities = metadata.get("known_entities", [])
        generated_entities = metadata.get("generated_entities", [])

        for entity in generated_entities:
            if entity not in known_entities:
                result.add_anomaly(f"HALLUCINATION: Unknown entity detected -> {entity}")

    def _check_narrative_spikes(self, metadata: Dict, result: FinalIntegrityResult):
        """
        感情スパイク検知

        Args:
            metadata (dict): AIメタデータ
            result (FinalIntegrityResult): 出力結果
        """
        emotion_curve = metadata.get("emotion_curve", [])

        if len(emotion_curve) < 2:
            return

        # 差分ベースの簡易スパイク検知
        for i in range(1, len(emotion_curve)):
            diff = abs(emotion_curve[i] - emotion_curve[i - 1])

            # なぜこの閾値か：
            # 急激な感情変化はナラティブ破綻の兆候であるため
            if diff > 0.7:
                result.add_anomaly(
                    f"EMOTION_SPIKE: abrupt change detected (Δ={diff:.2f}) at index {i}"
                )

    def _check_confidence(self, metadata: Dict, result: FinalIntegrityResult):
        """
        信頼度チェック

        Args:
            metadata (dict): AIメタデータ
            result (FinalIntegrityResult): 出力結果
        """
        confidence = metadata.get("confidence_score")

        if confidence is None:
            return

        if confidence < self.threshold:
            result.add_anomaly(
                f"LOW_CONFIDENCE: score={confidence:.2f} below threshold={self.threshold}"
            )
            # 低信頼度はHITL必須
            result.requires_hitl = True


# =========================
# Main Guard
# =========================
if __name__ == "__main__":
    # 簡易テスト（開発用）
    dummy_report = AuditReport(transaction_id="test_tx")
    detector = AnomalyDetector()

    test_metadata = {
        "known_entities": ["Alice", "Bob"],
        "generated_entities": ["Alice", "UnknownX"],
        "emotion_curve": [0.1, 0.9],
        "confidence_score": 0.6
    }

    result = detector.detect(dummy_report, test_metadata)
    print(result.status, result.anomalies)

# [EOF]