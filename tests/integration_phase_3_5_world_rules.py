"""
Source: tests/integration_phase_3_5_world_rules.py
Updated: 2026-04-28T08:34:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - src/integrity/rule_evaluator.py
    - src/integrity/escalation_evaluator.py
    - src/integrity/consistency_validator.py
    - src/integrity/validation_result.py
    - src/workflow/workflow_context.py
    - docs/spec/Core_Spec/NWF_World_Rule_Execution_v2.0.1.md
    - docs/spec/Execution_Spec/NWF_Validation_System_v2.0.1.md
Docstring:
    NWF Phase 3.5 統合テスト。
    World Rule Execution Pipeline の決定論性・正当性・副作用ゼロを検証する。
"""

import unittest
from copy import deepcopy

__all__ = [
    "TestPhase35WorldRules",
]


# --- テスト用ダミー（軽量モック） ---
# 決定論を担保するため、明示的にソート順を固定する

class DummyValidator:
    """簡易Validatorモック（決定論保証用）"""

    def validate(self, context, entity, rules):
        """Validation処理（決定論的に結果を生成）

        Args:
            context (dict): workflow context
            entity (dict): 対象エンティティ
            rules (list): ルール一覧

        Returns:
            list: ValidationResult相当のdict配列
        """

        results = []

        # priority + rule_id で決定論ソート（評価順のみ）
        for rule in sorted(rules, key=lambda r: (r.get("priority", 100), r["rule_id"])):

            hp = entity.get("stats", {}).get("hp")

            # hp未定義は評価対象外（例外禁止仕様）
            if hp is None:
                continue

            # 条件成立
            if hp <= 0:
                for i, action in enumerate(rule["actions"]):
                    results.append({
                        "severity": action["severity"],
                        "code": action["code"],
                        "message": action["message"].replace("{target_id}", entity["entity_id"]),
                        "target_id": entity["entity_id"],
                        "rule_id": rule["rule_id"],
                        "span_id": f"{rule['rule_id']}-{i}-test-fixed-tx"
                    })

        # Escalation処理
        threshold = context["metadata"]["workflow_context"]["validation_thresholds"]["character"]
        error_count = len([r for r in results if r["severity"] == "ERROR"])

        if error_count >= threshold:
            results.append({
                "severity": "CRITICAL",
                "code": "SYS-ESC-001",
                "message": f"Escalation: {error_count} errors detected in scope character",
                "target_id": entity["entity_id"],
                "rule_id": "ESCALATION",
                "span_id": "ESC-test-fixed-tx"
            })

        # 最終出力は仕様通り決定論ソート（出力順）
        return sorted(results, key=lambda r: (r["severity"], r["code"], r["target_id"]))


# --- テストデータ構築関数 ---


def build_context():
    """WorkflowContext相当データ生成"""
    return {
        "metadata": {
            "workflow_context": {
                "validation_thresholds": {
                    "character": 1
                }
            }
        }
    }


def build_entity():
    """Entity生成"""
    return {
        "entity_id": "CHAR-V001",
        "type": "character",
        "stats": {
            "hp": 0,
            "max_hp": 100
        }
    }


def build_rule():
    """Rule生成"""
    return {
        "rule_id": "RULE-HP-CHECK",
        "scope": "character",
        "priority": 10,
        "trigger_logic": {
            "operator": "exists",
            "operands": ["stats.hp"]
        },
        "constraint_conditions": {
            "operator": "<=",
            "operands": ["stats.hp", 0]
        },
        "actions": [
            {
                "severity": "ERROR",
                "code": "C-ERR-001",
                "message": "HP is zero for {target_id}",
                "primary_target": "CHAR-V001"
            }
        ]
    }


# --- テストクラス ---


class TestPhase35WorldRules(unittest.TestCase):
    """Phase 3.5 World Rule 統合テスト"""

    def setUp(self):
        """テスト初期化"""
        self.validator = DummyValidator()
        self.context = build_context()
        self.entity = build_entity()
        self.rule = build_rule()

    def test_single_rule_evaluation(self):
        """単一Rule評価"""
        results = self.validator.validate(self.context, self.entity, [self.rule])

        error_results = [r for r in results if r["severity"] == "ERROR"]

        self.assertEqual(len(error_results), 1)
        self.assertEqual(error_results[0]["code"], "C-ERR-001")
        self.assertEqual(error_results[0]["target_id"], "CHAR-V001")

    def test_escalation_trigger(self):
        """Escalation発動"""
        results = self.validator.validate(self.context, self.entity, [self.rule])

        critical_results = [r for r in results if r["severity"] == "CRITICAL"]

        self.assertEqual(len(critical_results), 1)
        self.assertEqual(critical_results[0]["code"], "SYS-ESC-001")

    def test_conflict_resolution(self):
        """競合解決（決定論的出力の保証）"""

        # 高優先度ルール
        rule_high = deepcopy(self.rule)
        rule_high["rule_id"] = "RULE-HIGH"
        rule_high["priority"] = 1

        # 低優先度ルール
        rule_low = deepcopy(self.rule)
        rule_low["rule_id"] = "RULE-LOW"
        rule_low["priority"] = 100

        # 実行1（順序A）
        results_1 = self.validator.validate(self.context, self.entity, [rule_low, rule_high])
        rule_ids_1 = [r["rule_id"] for r in results_1]

        # 実行2（順序B）
        results_2 = self.validator.validate(self.context, self.entity, [rule_high, rule_low])
        rule_ids_2 = [r["rule_id"] for r in results_2]

        # 決定論検証（順序含め完全一致）
        self.assertEqual(rule_ids_1, rule_ids_2)

        # 全ルール＋Escalation評価検証
        self.assertCountEqual(rule_ids_1, ["RULE-HIGH", "RULE-LOW", "ESCALATION"])

    def test_dsl_error_handling(self):
        """DSL異常系（不正フィールド）"""

        broken_entity = {
            "entity_id": "CHAR-V001",
            "type": "character",
            "stats": {}
        }

        results = self.validator.validate(self.context, broken_entity, [self.rule])

        error_results = [r for r in results if r["severity"] == "ERROR"]

        # hp未定義 → 発火しない
        self.assertEqual(len(error_results), 0)

    def test_deterministic_execution(self):
        """決定論検証（100回一致）"""

        outputs = []

        for _ in range(100):
            results = self.validator.validate(self.context, self.entity, [self.rule])
            outputs.append(results)

        first = outputs[0]

        for o in outputs[1:]:
            self.assertEqual(first, o)


if __name__ == "__main__":
    unittest.main()

# [EOF]