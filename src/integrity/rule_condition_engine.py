"""
Source: src/integrity/rule_condition_engine.py
Updated: 2026-04-30T10:40:00+09:00  # ★更新: evaluate I/F 追加対応（Spec整合修正）
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Core_Spec/NWF_World_Rule_Model_v2.0.1.md
    - docs/spec/Core_Spec/NWF_World_Rule_Execution_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
Docstring:
    Rule Condition Engine モジュール。

    JSON Expression Tree DSL を評価し、boolean を返却する純関数エンジン。
    決定論・例外排除・副作用ゼロを保証する。

    ★修正内容（Phase 3.5）:
    - rule_evaluator との I/F 契約不整合を解消
    - evaluate() 関数を追加（Spec準拠）
"""

# imports
from typing import Any, Dict, Union

# constants
SUPPORTED_COMPARISON_OPS = {"==", "!=", ">", "<", ">=", "<="}
SUPPORTED_LOGICAL_OPS = {"AND", "OR", "NOT"}

# ★修正前:
# __all__ = [
#     "evaluate_condition",
# ]
#
# ★修正後:
# - rule_evaluator からの import evaluate に対応するため追加
__all__ = [
    "evaluate_condition",
    "evaluate",  # ★追加（I/F契約準拠）
]


# =========================================================
# Utility Functions
# =========================================================

def _resolve_path(path: str, data_root: Dict[str, Any]) -> Any:
    """
    ドット記法パスを解決する。
    """
    try:
        parts = path.split(".")
        if not parts:
            return None

        current = data_root.get(parts[0], None)

        for key in parts[1:]:
            if current is None:
                return None

            # dict 優先
            if isinstance(current, dict):
                current = current.get(key, None)
                continue

            # attribute fallback
            try:
                current = getattr(current, key)
            except Exception:
                return None

        return current
    except Exception:
        return None


def _apply_operator(op: str, actual: Any, expected: Any) -> bool:
    """
    比較演算を適用する。
    """
    try:
        if actual is None or expected is None:
            if op == "==":
                return actual is None and expected is None
            if op == "!=":
                return not (actual is None and expected is None)
            return False

        if type(actual) != type(expected):
            if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
                pass
            else:
                return True if op == "!=" else False

        if op == "==":
            return actual == expected
        if op == "!=":
            return actual != expected
        if op == ">":
            return actual > expected
        if op == "<":
            return actual < expected
        if op == ">=":
            return actual >= expected
        if op == "<=":
            return actual <= expected

        return False
    except Exception:
        return False


def _evaluate_logical(node: Dict[str, Any], data_root: Dict[str, Any]) -> bool:
    """
    論理ノード評価
    """
    op = node.get("operator")

    if op not in SUPPORTED_LOGICAL_OPS:
        return False

    if op == "AND":
        operands = node.get("operands", [])
        if not isinstance(operands, list):
            return False
        for child in operands:
            if not evaluate_condition(child, data_root):
                return False
        return True

    if op == "OR":
        operands = node.get("operands", [])
        if not isinstance(operands, list):
            return False
        for child in operands:
            if evaluate_condition(child, data_root):
                return True
        return False

    if op == "NOT":
        operand = node.get("operands")
        return not evaluate_condition(operand, data_root)

    return False


def _evaluate_exists(node: Dict[str, Any], data_root: Dict[str, Any]) -> bool:
    """
    exists ノード評価
    """
    path = node.get("exists")
    if not isinstance(path, str):
        return False

    value = _resolve_path(path, data_root)
    return value is not None


def _evaluate_comparison(node: Dict[str, Any], data_root: Dict[str, Any]) -> bool:
    """
    比較ノード評価
    """
    field = node.get("field")
    op = node.get("op")
    expected = node.get("value")

    if not isinstance(field, str):
        return False

    if op not in SUPPORTED_COMPARISON_OPS:
        return False

    actual = _resolve_path(field, data_root)

    return _apply_operator(op, actual, expected)


# =========================================================
# Main Function
# =========================================================

def evaluate_condition(
    node: Union[Dict[str, Any], None],
    data_root: Dict[str, Any],
) -> bool:
    """
    条件式を評価する純関数。
    """
    try:
        if not isinstance(node, dict):
            return False

        if "operator" in node:
            return _evaluate_logical(node, data_root)

        if "exists" in node:
            return _evaluate_exists(node, data_root)

        if "field" in node:
            return _evaluate_comparison(node, data_root)

        return False

    except Exception:
        return False


# =========================================================
# ★追加: evaluate（I/F契約準拠）
# =========================================================

def evaluate(
    node: Union[Dict[str, Any], None],
    data_root: Dict[str, Any],
) -> bool:
    """
    rule_evaluator との I/F 契約を満たすラッパー関数。

    なぜ必要か:
        - rule_evaluator.py が evaluate() を期待しているため
        - Spec Driven Development におけるI/F整合性維持

    設計:
        - evaluate_condition をそのまま委譲
        - 副作用なし（純関数維持）
        - 既存ロジックを破壊しない

    Args:
        node: JSON DSL ノード
        data_root: {"entity": ..., "context": ...}

    Returns:
        bool
    """
    # ★追加理由:
    # - Implementation Drift 修正
    # - rule_evaluator からの import evaluate を満たすため
    return evaluate_condition(node, data_root)


# =========================================================
# Main Guard
# =========================================================
if __name__ == "__main__":
    sample = {
        "operator": "AND",
        "operands": [
            {"field": "entity.value", "op": ">", "value": 10},
            {"exists": "entity.value"}
        ]
    }

    data = {
        "entity": {"value": 20},
        "context": {}
    }

    print(evaluate(sample, data))  # ★ evaluate使用に変更しても動作確認


# [EOF]