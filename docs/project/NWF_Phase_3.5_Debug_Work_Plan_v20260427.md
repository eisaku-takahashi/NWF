Source: docs/project/NWF_Phase_3.5_Debug_Work_Plan_v20260427.md
Updated: 2026-04-27T14:08:00+09:00
PIC: Engineer / ChatGPT

# NWF Phase 3.5 Debug Work Plan v20260427

---

## 1. 概要

本ドキュメントは  
NWF Phase 3.5 における統合テスト `test_conflict_resolution` の失敗に関する原因修正および検証作業計画を定義する。

本計画は以下に基づく：

- docs/project/NWF_Phase_3.5_Work_Plan_v20260424.md
- docs/spec/Core_Spec/NWF_World_Rule_Execution_v2.0.1.md
- docs/spec/Execution_Spec/NWF_Validation_System_v2.0.1.md
- 統合テスト実行ログ
- 調査レポート（Gemini作成）
- ChatGPTによる設計整合性検証結果

目的：

- テストと仕様の不整合を解消する
- 決定論的実行（Deterministic Execution）の検証を正しく実装する
- Phase 3.5 の Definition of Done を完全達成する

---

## 2. 問題定義

### 2.1 発生事象

以下テストが失敗：

- test_conflict_resolution

エラー内容：

- results[0]["rule_id"] の値が期待と一致しない

---

### 2.2 根本原因

仕様上：

- RuleEvaluator → priority順で評価
- Validator → (scope, code, target_id) で再ソート

したがって：

👉 priorityは最終出力順に影響しない

---

### 2.3 問題の本質

テストの誤り：

- 「評価順」を「出力順」と誤認している
- 決定論の定義が誤っている

---

## 3. 修正方針

### 採用方針

✅ テストコードを仕様に合わせて修正する

理由：

- Validatorは順序ロジックを持たない（Orchestrator原則）
- 出力順は決定論的であればよい
- priorityは出力順保証対象ではない

---

## 4. 作業一覧（実行順）

---

### 1. テスト仕様の再定義

ファイル:
- 既存修正: tests/integration_phase_3_5_world_rules.py

作業内容:

- test_conflict_resolution のテスト目的を以下に変更：

  旧：
  - priority順で先頭に来ることの検証

  新：
  - 出力の決定論性（Deterministic Execution）の検証

- 検証項目：
  1. 同一入力で同一出力になること
  2. 入力順序を変えても同一出力になること
  3. 全ルールが評価されること

根拠:

- NWF_World_Rule_Execution_v2.0.1.md
- Validator最終ソート仕様（scope, code, target_id）

DoD:

- priority依存の検証が完全削除されている
- 決定論テストに置き換えられている

---

### 2. test_conflict_resolution 実装修正

ファイル:
- 既存修正: tests/integration_phase_3_5_world_rules.py

作業内容:

以下コードへ修正：

    def test_conflict_resolution(self):
        """競合解決（決定論的出力の保証）"""
        rule_high = deepcopy(self.rule)
        rule_high["rule_id"] = "RULE-HIGH"
        rule_high["priority"] = 1

        rule_low = deepcopy(self.rule)
        rule_low["rule_id"] = "RULE-LOW"
        rule_low["priority"] = 100

        # 実行1
        results_1 = self.validator.validate(self.context, self.entity, [rule_low, rule_high])
        rule_ids_1 = [r["rule_id"] for r in results_1]

        # 実行2（順序入替）
        results_2 = self.validator.validate(self.context, self.entity, [rule_high, rule_low])
        rule_ids_2 = [r["rule_id"] for r in results_2]

        # 決定論保証
        self.assertEqual(rule_ids_1, rule_ids_2)

        # 全ルール評価保証
        self.assertCountEqual(rule_ids_1, ["RULE-HIGH", "RULE-LOW"])

根拠:

- 決定論定義（同一入力→同一出力）
- Orchestrator責務分離

DoD:

- テストが仕様完全準拠となる
- 不定順序への依存が消える

---

### 3. 全テスト再実行

ファイル:
- tests/integration_phase_3_5_world_rules.py

作業内容:

以下コマンド実行：

python -m pytest tests/integration_phase_3_5_world_rules.py -v

検証項目:

- 5テストすべてPASS
- FAILが0であること

DoD:

- 全テストPASS
- 実行結果が安定している

---

### 4. Deterministic再検証（強化確認）

ファイル:
- tests/integration_phase_3_5_world_rules.py

作業内容:

- test_deterministic_execution が以下を満たすこと確認：

  - 100回実行で完全一致
  - span_id含め一致

DoD:

- 再現性100%確認
- 不一致ゼロ

---

### 5. 仕様整合性レビュー

ファイル:
- docs/spec/Execution_Spec/NWF_Validation_System_v2.0.1.md
- docs/spec/Core_Spec/NWF_World_Rule_Execution_v2.0.1.md

作業内容:

- 以下を確認：

  - Validatorソート仕様が明文化されている
  - priorityが出力順に影響しないことが明示されている

必要に応じて追記：

- 「評価順と出力順の分離」明文化

DoD:

- Spec-Code完全一致
- 曖昧性ゼロ

---

### 6. 回帰テスト確認

ファイル:
- 全テスト

作業内容:

- 他テストへの影響確認：

  - test_single_rule_evaluation
  - test_escalation_trigger
  - test_dsl_error_handling
  - test_deterministic_execution

DoD:

- 全テストPASS維持
- 副作用ゼロ

---

## 5. Definition of Done

本デバッグ作業の完了条件：

- test_conflict_resolution 修正完了
- 全テストPASS
- 再現性100%
- 決定論保証成立
- Spec-Code一致
- 責務分離維持

---

## 6. 結論

本問題は：

「実装の不具合ではなく、テスト仕様の誤り」

である。

修正により：

- NWFの設計原則（責務分離）が維持される
- 決定論的実行が正しく検証される
- Phase 3.5 の品質保証が完成する

---

## 7. 重要設計原則（再確認）

| 概念 | 担当 |
|------|------|
| 評価順 | RuleEvaluator |
| 出力順 | Validator |

👉 この分離がNWFの核心である

---

[EOF]