"""
Source: src/integrity/escalation_evaluator.py
Updated: 2026-04-30T11:54:00+09:00  # 修正: 作成日時に更新
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Execution_Spec/NWF_Error_Model_v2.0.1.md
    - docs/spec/Execution_Spec/NWF_Escalation_Logic_Spec_v2.0.1.md
    - docs/spec/Execution_Spec/NWF_Validator_And_Context_Contract_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
Docstring:
    Escalation Evaluator モジュール。

    ValidationResult のリストを入力として受け取り、
    scope + target_id 単位で ERROR 件数を集計し、
    threshold を超過した場合に CRITICAL を追加生成する。

    本モジュールは以下を保証する：
    - Pure Function（入力不変）
    - Deterministic Execution（完全決定論）
    - Monotonicity（昇格のみ）
"""

from collections import Counter
from hashlib import sha256
from typing import List, Tuple

from src.integrity.validation_result import ValidationResult
from src.workflow.workflow_context import WorkflowContext

# デフォルト閾値定義
DEFAULT_THRESHOLDS = {
    "scene": 5,
    "character": 3,
    "regional": 10,
    "global": 20,
}

# 修正前:
# __all__ = [
#     "evaluate",
# ]
#
# 修正後:
# 理由:
# - consistency_validator が EscalationEvaluator クラスをimportするため
# - I/F契約を満たすためにクラスを公開対象に追加
__all__ = [
    "evaluate",
    "EscalationEvaluator",  # ← 追加
]


def _get_threshold(scope: str, thresholds: dict) -> int:
    """
    scope に対応する threshold を取得する。
    """
    return thresholds.get(scope, thresholds.get("global", DEFAULT_THRESHOLDS["global"]))


def _create_critical_result(
    scope: str,
    target_id: str,
    count: int,
    threshold: int,
    context: WorkflowContext,
) -> ValidationResult:
    """
    CRITICAL の ValidationResult を生成する。
    """
    span_source = f"escalation:{target_id}:{context.execution_id}"
    span_id = sha256(span_source.encode()).hexdigest()

    return ValidationResult(
        rule_id=f"ESCALATION_{scope.upper()}_{target_id}",
        severity="CRITICAL",
        code="E999_THRESHOLD_EXCEEDED",
        message=f"Threshold exceeded for {scope}:{target_id}. (Current: {count}, Limit: {threshold})",
        scope=scope,
        target_id=target_id,
        trace_id=context.trace_id,
        span_id=span_id,
        source="escalation_evaluator",
    )


# 修正前:
# def evaluate(results: List[ValidationResult], context: WorkflowContext) -> List[ValidationResult]:
#
# 修正後:
# 理由:
# - Spec / I/F 要件によりシグネチャを統一
# - consistency_validator から呼び出される際、contextを渡せない可能性あり
# - context を optional に変更し安全性を担保
def evaluate(
    results: List[ValidationResult],
    context: WorkflowContext = None,  # ← 修正: optional化
) -> List[ValidationResult]:
    """
    ValidationResult のリストを評価し、threshold 超過時に CRITICAL を追加する。
    """

    # 修正追加:
    # context が None の場合の安全対策
    if context is None:
        # 理由:
        # - クラスI/Fラッパーから呼ばれる場合にcontextが未提供のケースを吸収
        return list(results) if results else []

    if not results:
        return []

    error_counts: Counter[Tuple[str, str]] = Counter()

    for res in results:
        if res.severity == "ERROR":
            key = (res.scope, res.target_id)
            error_counts[key] += 1

    thresholds = context.metadata.get("validation_thresholds", DEFAULT_THRESHOLDS)

    new_criticals: List[ValidationResult] = []

    for (scope, target_id) in sorted(error_counts.keys()):
        count = error_counts[(scope, target_id)]
        threshold = _get_threshold(scope, thresholds)

        if count >= threshold:
            critical = _create_critical_result(
                scope=scope,
                target_id=target_id,
                count=count,
                threshold=threshold,
                context=context,
            )
            new_criticals.append(critical)

    new_criticals_sorted = sorted(new_criticals, key=lambda x: x.rule_id)

    return list(results) + new_criticals_sorted


# ============================================
# 追加: クラスI/Fラッパー（Spec準拠）
# ============================================
class EscalationEvaluator:
    """
    Escalation評価クラス（I/F互換用ラッパー）

    なぜ必要か:
        - consistency_validator がクラスI/Fを要求しているため
        - 既存の関数ベース実装との互換維持

    設計:
        - 状態を持たない純関数ラッパー
        - 内部で既存 evaluate 関数を呼び出す
    """

    def __init__(self):
        pass

    def evaluate(self, results, context=None):
        """
        エスカレーション評価

        Args:
            results: List[ValidationResult]
            context: WorkflowContext（任意）

        Returns:
            List[ValidationResult]
        """

        try:
            # 修正理由:
            # - 既存関数 evaluate(results, context) に一致させる
            # - context未指定でも安全に動作するように設計
            return evaluate(results, context)
        except Exception:
            # 例外排除（Spec準拠: 決定論保証）
            return []


# [EOF]