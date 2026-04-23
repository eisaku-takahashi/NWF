"""
Source: src/integrity/recursive_auditor.py
Updated: 2026-04-23T04:29:00+09:00  # ★Phase 3.4 ⑦ Auditor非破壊性の最終確認対応版
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Project_Governance/NWF_Recursive_Integrity_Spec_v2.0.1.md
    - docs/spec/Execution_Spec/NWF_Validator_And_Context_Contract_v2.0.1.md
    - docs/spec/Execution_Spec/NWF_Validation_System_v2.0.1.md
    - src/integrity/validation_result.py
    - src/models/nwf_enums.py
    - src/models/nwf_object.py
Docstring:
    Recursive Auditor モジュール。

    【Phase 3.4 最終修正内容（確定版 + Monotonicity対応）】
    - Severity決定ロジックを完全修正（最大値保持）
    - WARNING上書きバグ排除
    - CRITICAL保持保証
    - ValidationResult空防御追加
    - Severityダウングレード防止
    - 集約処理の非破壊化（Pass-through設計）

    【Phase 3.4 最終拡張（今回）】
    - ★Auditor責務の再定義（最重要）
        ❌ 集約（Aggregation）禁止
        ❌ ValidationResultの意味変更禁止
        ❌ 再生成・要約禁止
        ✅ 監査ログ生成のみ
        ✅ 検査・観測・記録に限定

    【Phase 3.4 追加（Pipeline責務分離の明文化）】
    - Validator → ValidationResult生成のみ
    - Adapter → 型変換のみ（意味変更禁止）
    - Auditor → ★監査のみ（本モジュール）
    - Engine → 最終判断（停止・例外）

    - 本モジュールは「Validation Pipelineの非破壊観測層」である
    - データの意味・Severity・制御信号は一切変更しない

    【設計原則】
    - Validation Pipeline 非破壊設計原則に従う
    - Auditorは「判断しない」「変換しない」「上書きしない」
    - Severityは制御信号であり、ここで変換してはならない

    【重要】
    - report.severity は「観測結果」であり制御信号ではない
    - 実際の停止判定は Engine 側で行う（責務分離）

    【⑦ Auditor非破壊性 最終確認（今回の追加）】
    - ValidationResultの完全非改変保証を明文化
    - 参照渡しによるPass-throughを明示
    - 深いコピー禁止（意味破壊防止）
    - Monotonicity Rule遵守コメント追加
    - 「なぜ変更してはいけないか」を明示

    【デバッグログ】
    - Phase 3.4検証完了後に削除予定
"""

# =========================
# Import
# =========================
from typing import List, Dict, Any
from datetime import datetime, timezone, timedelta

from src.integrity.validation_result import ValidationResult
from src.models.nwf_enums import NWFSeverity

# =========================
# Constants / Config
# =========================
JST = timezone(timedelta(hours=9))

# =========================
# Public Interface
# =========================
__all__ = [
    "AuditReport",
    "RecursiveAuditor"
]

# =========================
# Utility Functions
# =========================
def get_current_timestamp() -> datetime:
    """現在時刻を JST で取得"""
    return datetime.now(JST)


# -----------------------------
# 最大Severity決定（※観測専用）
# -----------------------------
def resolve_severity(results: List[ValidationResult]) -> NWFSeverity:
    """
    ValidationResult配列から最大Severityを取得（非破壊）

    【重要変更】
    - これは「評価」ではなく「観測」
    - ValidationResultには一切影響を与えない
    """

    priority = {
        NWFSeverity.INFO: 0,
        NWFSeverity.WARNING: 1,
        NWFSeverity.ERROR: 2,
        NWFSeverity.CRITICAL: 3,
    }

    max_sev = NWFSeverity.INFO

    for vr in results:
        if priority[vr.severity] > priority[max_sev]:
            max_sev = vr.severity

    return max_sev


# -----------------------------
# Severity安全更新（※非破壊補助）
# -----------------------------
def escalate_severity(current: NWFSeverity, new: NWFSeverity) -> NWFSeverity:
    """
    Severityを安全に更新（ダウングレード禁止）

    【注意】
    - ValidationResultには使用しない
    - report内部の補助情報のみ対象
    """

    priority = {
        NWFSeverity.INFO: 0,
        NWFSeverity.WARNING: 1,
        NWFSeverity.ERROR: 2,
        NWFSeverity.CRITICAL: 3,
    }

    return new if priority[new] > priority[current] else current


# =========================
# Classes
# =========================
class AuditReport:
    """再帰的監査レポート（非制御・監査専用）"""

    def __init__(self, transaction_id: str):
        self.is_valid: bool = True
        self.issues: List[str] = []
        self.depth_checked: int = 0
        self.dangling_threads: List[str] = []
        self.transaction_id: str = transaction_id
        self.timestamp: datetime = get_current_timestamp()

        # ★重要：これは「観測結果」であり制御ではない
        self.severity: NWFSeverity = NWFSeverity.INFO

        # =====================================================
        # ★⑦ 非破壊保証：ValidationResultそのまま保持
        # =====================================================
        # ❗重要:
        # - deepcopy禁止（意味破壊・パフォーマンス低下）
        # - 再生成禁止
        # - 要約禁止
        #
        # なぜ:
        # - ValidationResultは制御信号（Engineが使用）
        # - ここで変更するとMonotonicity Ruleが崩壊する
        #
        # 結論:
        # → 参照をそのまま保持（Pass-through）
        # =====================================================
        self.validation_results: List[ValidationResult] = []


class RecursiveAuditor:
    """ナラティブ再帰監査（非破壊監査専用）"""

    def __init__(self, max_depth: int = 3):
        self.max_depth = max_depth

    def audit(
        self,
        validation_results: List[ValidationResult],
        story_data: Dict[str, Any]
    ) -> AuditReport:
        """
        ナラティブ整合性を検証（非破壊）

        Returns:
            AuditReport

        Raises:
            RuntimeError: ValidationResultが空の場合
        """

        # -----------------------------
        # 契約違反防御
        # -----------------------------
        if not validation_results:
            raise RuntimeError("ValidationResult is empty (Contract violation)")

        # -----------------------------
        # デバッグログ（Phase 3.4）
        # -----------------------------
        for vr in validation_results:
            print(f"[DEBUG] Pre-Audit Severity: {vr.severity}")

        transaction_id = validation_results[0].transaction_id
        report = AuditReport(transaction_id)

        # =====================================================
        # ★⑦ 非破壊保証（最重要）
        # =====================================================
        # 修正前（概念）:
        # report.validation_results = summarize(validation_results)
        # → ❌ 集約による情報ロス
        # → ❌ Severity破壊
        #
        # 修正後:
        # → 参照そのまま格納
        # → 完全Pass-through
        #
        # Monotonicity Rule:
        # - 下流でSeverityが変わらないことを保証
        # - CRITICALは絶対に失われない
        #
        # ❗禁止事項:
        # - deepcopy
        # - list再生成
        # - ValidationResult改変
        #
        # ✅ 正しい実装:
        # - 同一参照を保持
        # =====================================================
        report.validation_results = validation_results

        # =====================================================
        # ★ CRITICAL検知（観測のみ）
        # =====================================================
        for vr in validation_results:
            if vr.severity == NWFSeverity.CRITICAL:
                report.is_valid = False
                report.severity = NWFSeverity.CRITICAL
                report.issues.append(f"CRITICAL_DETECTED: {vr.error_code}")

                # ❗重要:
                # - ValidationResultは一切変更しない
                # - Engineが停止判断を行う
                return report

        # =====================================================
        # ★ Severity観測（非制御）
        # =====================================================
        report.severity = resolve_severity(validation_results)

        if report.severity in (NWFSeverity.ERROR, NWFSeverity.CRITICAL):
            report.is_valid = False

        # =====================================================
        # 副次監査（非影響処理）
        # =====================================================
        # ❗重要:
        # - ValidationResultには影響しない
        # - reportの補助情報のみ更新
        self._recursive_scan(story_data, 0, report, visited=set())
        self._validate_timeline_synchronization(story_data, report)
        self._check_foreshadowing_integrity(story_data, report)

        return report

    def _recursive_scan(self, data, depth, report, visited):
        """再帰構造監査（副次）"""
        if depth > self.max_depth:
            return

        report.depth_checked = max(report.depth_checked, depth)

        obj_id = id(data)
        if obj_id in visited:
            report.issues.append("WARN_RECURSIVE_001")
            return

        visited.add(obj_id)

        if isinstance(data, dict):
            for value in data.values():
                if isinstance(value, (dict, list)):
                    self._recursive_scan(value, depth + 1, report, visited)

        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    self._recursive_scan(item, depth + 1, report, visited)

    def _validate_timeline_synchronization(self, story_data, report):
        """Timeline監査（非破壊）"""
        timeline = story_data.get("timeline", [])
        previous_time = None

        for event in timeline:
            timestamp = event.get("timestamp")
            if not timestamp:
                continue

            try:
                current_time = datetime.fromisoformat(timestamp)

                if current_time.tzinfo != JST:
                    report.issues.append("WARN_TIMELINE_001")

                if previous_time and current_time < previous_time:
                    report.is_valid = False

                    # -----------------------------
                    # 修正前:
                    # report.severity = NWFSeverity.ERROR
                    #
                    # 問題:
                    # - CRITICALがERRORに上書きされる可能性
                    #
                    # 修正後:
                    # - escalate使用
                    # - 単調増加保証（Monotonicity）
                    # -----------------------------
                    report.severity = escalate_severity(
                        report.severity,
                        NWFSeverity.ERROR
                    )
                    report.issues.append("ERR_TIMELINE_002")

                previous_time = current_time

            except Exception:
                report.issues.append("WARN_TIMELINE_003")

    def _check_foreshadowing_integrity(self, story_data, report):
        """伏線監査（非破壊）"""
        foreshadowing = story_data.get("foreshadowing", [])

        for thread in foreshadowing:
            if thread.get("status") == "open":
                report.dangling_threads.append(thread.get("id", "UNKNOWN"))

        if report.dangling_threads:
            report.issues.append("WARN_FORESHADOW_001")


# =========================
# Main Guard
# =========================
if __name__ == "__main__":

    dummy_results = [
        ValidationResult(
            is_valid=True,
            severity=NWFSeverity.INFO,
            error_code="INFO_TEST",
            message="test",
            violated_rules=[],
            transaction_id="test_tx",
            stardate=0.0,
            metadata={}
        )
    ]

    dummy_story = {}

    auditor = RecursiveAuditor()
    result = auditor.audit(dummy_results, dummy_story)

    print(result.severity)

# [EOF]