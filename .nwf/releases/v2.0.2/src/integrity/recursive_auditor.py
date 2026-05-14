"""
Source: src/integrity/recursive_auditor.py
Updated: 2026-04-12T08:08:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Project_Governance/NWF_Recursive_Integrity_Spec_v2.0.1.md
    - src/integrity/consistency_validator.py
    - src/models/nwf_object.py
Docstring:
    Recursive Auditor モジュール。
    ナラティブ整合性（Level 3）を検証するために、物語構造を再帰的に監査する。
    階層構造、タイムライン、伏線の整合性を検証し、物語全体の一貫性を保証する。
"""

from typing import List, Dict, Any
from datetime import datetime, timezone, timedelta
from src.integrity.consistency_validator import ConsistencyResult

# JST 定義
JST = timezone(timedelta(hours=9))

__all__ = [
    "AuditReport",
    "RecursiveAuditor"
]


# Utility Functions

def get_current_timestamp() -> datetime:
    """
    現在時刻を JST で取得する

    Returns:
        datetime: JST の現在時刻
    """
    return datetime.now(JST)


# Classes

class AuditReport:
    """
    再帰的監査レポートコンテナ（仕様 5.4 準拠）

    Attributes:
        is_valid (bool): ナラティブ整合性の成否
        issues (List[str]): 検出された問題
        depth_checked (int): チェックした最大深度
        dangling_threads (List[str]): 未回収スレッド
        transaction_id (str): トランザクションID
        timestamp (datetime): 監査時刻
    """

    def __init__(self, transaction_id: str):
        self.is_valid: bool = True
        self.issues: List[str] = []
        self.depth_checked: int = 0
        self.dangling_threads: List[str] = []
        self.transaction_id: str = transaction_id
        self.timestamp: datetime = get_current_timestamp()


class RecursiveAuditor:
    """
    ナラティブ再帰監査クラス

    Args:
        max_depth (int): 再帰探索の最大深度
    """

    def __init__(self, max_depth: int = 3):
        self.max_depth = max_depth

    def audit(self, consistency_result: ConsistencyResult, story_data: Dict[str, Any]) -> AuditReport:
        """
        [監査] ナラティブ整合性（Level 3）を検証

        Args:
            consistency_result (ConsistencyResult): 論理整合性結果
            story_data (dict): 物語データ

        Returns:
            AuditReport: 監査結果
        """

        report = AuditReport(consistency_result.transaction_id)

        # L2エラーがある場合は監査スキップ
        if not consistency_result.is_consistent:
            report.is_valid = False
            report.issues.append("SKIP: Causal consistency failure.")
            return report

        # 再帰スキャン開始
        self._recursive_scan(story_data, 0, report, visited=set())

        # タイムライン整合性チェック
        self._validate_timeline_synchronization(story_data, report)

        # 伏線整合性チェック
        self._check_foreshadowing_integrity(story_data, report)

        return report

    def _recursive_scan(self, data: Dict[str, Any], depth: int, report: AuditReport, visited: set):
        """
        階層構造を再帰的にスキャン

        Args:
            data (dict): 対象データ
            depth (int): 現在の深度
            report (AuditReport): レポート
            visited (set): 循環参照検知用
        """

        # 深度制限チェック
        if depth > self.max_depth:
            return

        report.depth_checked = max(report.depth_checked, depth)

        # 循環参照防止
        obj_id = id(data)
        if obj_id in visited:
            report.issues.append("WARN_RECURSIVE_001: Circular reference detected.")
            return
        visited.add(obj_id)

        # 階層構造の整合性チェック
        if isinstance(data, dict):
            for key, value in data.items():
                # 下位構造へ再帰
                if isinstance(value, (dict, list)):
                    self._recursive_scan(value, depth + 1, report, visited)

        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    self._recursive_scan(item, depth + 1, report, visited)

    def _validate_timeline_synchronization(self, story_data: Dict[str, Any], report: AuditReport):
        """
        タイムライン整合性チェック

        Args:
            story_data (dict): 物語データ
            report (AuditReport): レポート
        """

        timeline = story_data.get("timeline", [])

        # 時系列チェック
        previous_time = None

        for event in timeline:
            timestamp = event.get("timestamp")

            if not timestamp:
                continue

            try:
                current_time = datetime.fromisoformat(timestamp)

                # JSTチェック
                if current_time.tzinfo != JST:
                    report.issues.append("WARN_TIMELINE_001: Non-JST timestamp detected.")

                # 時系列逆転チェック
                if previous_time and current_time < previous_time:
                    report.is_valid = False
                    report.issues.append("ERR_TIMELINE_002: Timeline inconsistency detected.")

                previous_time = current_time

            except Exception:
                report.issues.append("WARN_TIMELINE_003: Invalid timestamp format.")

    def _check_foreshadowing_integrity(self, story_data: Dict[str, Any], report: AuditReport):
        """
        伏線・スレッド整合性チェック

        Args:
            story_data (dict): 物語データ
            report (AuditReport): レポート
        """

        foreshadowing = story_data.get("foreshadowing", [])

        for thread in foreshadowing:
            status = thread.get("status")
            thread_id = thread.get("id", "UNKNOWN")

            # 未回収伏線検知
            if status == "open":
                report.dangling_threads.append(thread_id)

        if report.dangling_threads:
            report.issues.append(
                f"WARN_FORESHADOW_001: Dangling threads detected: {report.dangling_threads}"
            )


# Main Guard

if __name__ == "__main__":
    # テスト用簡易実行
    dummy_consistency = ConsistencyResult("test_tx")
    dummy_story = {
        "timeline": [
            {"timestamp": "2026-04-12T08:00:00+09:00"},
            {"timestamp": "2026-04-12T08:05:00+09:00"}
        ],
        "foreshadowing": [
            {"id": "thread_1", "status": "open"},
            {"id": "thread_2", "status": "closed"}
        ]
    }

    auditor = RecursiveAuditor()
    result = auditor.audit(dummy_consistency, dummy_story)

    print(result.is_valid)
    print(result.issues)
    print(result.dangling_threads)

# [EOF]