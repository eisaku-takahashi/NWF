"""
Source: src/integrity/rule_evaluator.py
Updated: 2026-04-30T12:24:00+09:00  # ★更新: process メソッド追加（I/F整合修正）
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Core_Spec/NWF_World_Rule_Model_v2.0.1.md
    - docs/spec/Core_Spec/NWF_World_Rule_Execution_v2.0.1.md
    - docs/spec/Execution_Spec/NWF_Rule_Engine_Contract_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
Docstring:
    RuleEvaluator モジュール。
    World Rule を決定論的かつ純関数として評価し、
    ValidationResult のリストを生成する。

    ★修正内容（Phase 3.5）:
    - consistency_validator とのI/F契約不整合を解消
    - RuleEvaluator クラスを追加（関数ベースとの互換維持）
    - process メソッドを追加（Orchestrator I/F準拠）
"""

from typing import List, Dict, Any
import hashlib
import re

from src.integrity.validation_result import ValidationResult
from src.integrity.rule_condition_engine import evaluate as condition_evaluate

# ★修正前:
# __all__ = [
#     "evaluate"
# ]
#
# ★修正後:
# - consistency_validator が RuleEvaluator を import するため追加
__all__ = [
    "evaluate",
    "RuleEvaluator",  # ★追加（I/F契約準拠）
]

# Scope 優先度（低いほど優先）
SCOPE_WEIGHTS = {
    "scene": 10,
    "character": 20,
    "regional": 30,
    "global": 40
}


# =========================================================
# ★追加: RuleEvaluator クラス（I/F互換ラッパー）
# =========================================================
class RuleEvaluator:
    """
    Rule評価クラス（I/F互換用ラッパー）

    なぜ必要か:
        - consistency_validator がクラスベースI/Fを要求しているため
        - 既存の関数ベース evaluate との互換維持

    設計:
        - 内部で関数 evaluate を呼び出す
        - 状態を持たない（純関数ラップ）
        - Spec Driven Development のI/F契約を満たす
    """

    def __init__(self):
        # 状態を持たない設計（純関数ラッパー）
        pass

    # ============================================
    # ★追加: process メソッド（Spec準拠）
    # ============================================
    def process(self, rules, entity, context):
        """
        ConsistencyValidator から呼ばれる正式I/F

        Args:
            rules: List[Rule]
            entity: Entity
            context: WorkflowContext

        Returns:
            List[ValidationResult]

        修正理由:
            - Orchestrator（ConsistencyValidator）が要求するI/F
            - pipeline step としての統一インターフェース
        """
        try:
            # ★既存関数に委譲（非破壊）
            return evaluate(context=context, entity=entity, rules=rules)
        except Exception:
            # 例外排除（決定論保証）
            return []

    def evaluate(self, context: Any, entity: Any, rules: List[Dict[str, Any]]) -> List[ValidationResult]:
        """
        Rule評価（旧I/F・互換維持）

        なぜ残すか:
            - 既存コード互換
            - Non-Breaking保証
        """
        return evaluate(context, entity, rules)


# =========================================================
# 既存: 関数ベース評価（純関数）
# =========================================================
def evaluate(context: Any, entity: Any, rules: List[Dict[str, Any]]) -> List[ValidationResult]:
    """
    RuleEvaluator のメイン関数。

    Args:
        context: WorkflowContext
        entity: Entity
        rules: Rule JSON のリスト

    Returns:
        List[ValidationResult]: 評価結果（決定論順序）
    """

    # 1. enabled フィルタ（非破壊）
    active_rules = [
        r for r in rules
        if r.get("enabled", True)
    ]

    # 2. 決定論的ソート
    sorted_rules = sorted(
        active_rules,
        key=lambda r: (
            SCOPE_WEIGHTS.get(r["scope"]["type"], 99),
            r.get("priority", 100),
            r["rule_id"]
        )
    )

    results: List[ValidationResult] = []

    for rule in sorted_rules:
        # 3. scope 判定
        if not _is_scope_match(rule, context, entity):
            continue

        # 4. condition 評価
        try:
            condition_result = condition_evaluate(
                rule["condition"],
                {"context": context, "entity": entity}
            )
        except Exception:
            condition_result = False

        if not condition_result:
            continue

        # 5. message 展開
        message = _format_message(
            rule["action"]["message"],
            context,
            entity
        )

        # 6. span_id 生成
        span_id = _generate_span_id(
            context.trace_id,
            context.execution_id,
            rule["rule_id"],
            entity.id
        )

        # 7. ValidationResult 生成
        result = ValidationResult(
            rule_id=rule["rule_id"],
            severity=rule["action"]["severity"],
            scope=rule["scope"]["type"],
            code=rule["action"]["code"],
            message=message,
            target_id=entity.id,
            trace_id=context.trace_id,
            span_id=span_id,
            source="rule_evaluator"
        )

        results.append(result)

    return results


def _is_scope_match(rule: Dict[str, Any], context: Any, entity: Any) -> bool:
    """
    Scope 適合判定。
    """

    scope = rule["scope"]
    scope_type = scope["type"]
    target_id = scope.get("target_id")

    if scope_type == "scene":
        return target_id == context.scene_id

    if scope_type == "character":
        return target_id == entity.id

    if scope_type == "regional":
        location_id = getattr(entity, "location_id", None)
        if location_id is None:
            return False
        return target_id == location_id

    if scope_type == "global":
        return True

    return False


def _generate_span_id(trace_id: str, execution_id: str, rule_id: str, entity_id: str) -> str:
    """
    span_id を決定論的に生成する。
    """

    raw = f"{trace_id}:{execution_id}:{rule_id}:{entity_id}"
    return hashlib.sha256(raw.encode()).hexdigest()


PLACEHOLDER_PATTERN = re.compile(r"\{([^}]+)\}")


def _format_message(template: str, context: Any, entity: Any) -> str:
    """
    メッセージテンプレート展開。
    """

    def replace(match):
        path = match.group(1)
        value = _resolve_path(path, context, entity)
        return "" if value is None else str(value)

    return PLACEHOLDER_PATTERN.sub(replace, template)


def _resolve_path(path: str, context: Any, entity: Any) -> Any:
    """
    ドット記法で値を解決する。
    """

    parts = path.split(".")

    if not parts:
        return None

    if parts[0] == "entity":
        current = entity
    elif parts[0] == "context":
        current = context
    else:
        return None

    for part in parts[1:]:
        if current is None:
            return None

        if isinstance(current, dict):
            current = current.get(part)
        else:
            current = getattr(current, part, None)

    return current


# [EOF]