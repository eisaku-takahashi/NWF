Source: docs/project/NWF_Phase_3.5_Work_Plan_v20260424.md
Updated: 2026-04-24T09:10:00+09:00
PIC: Engineer / ChatGPT

# NWF Phase 3.5 Work Plan v20260424

---

## 1. 概要

本ドキュメントは  
NWF Phase 3.5「World Rule Execution 強化」の実装作業計画を定義する。

目的：

- World Rule の評価ロジックを純関数として分離・再構築する
- Validator を「オーケストレーター」に限定する
- 決定論的・非副作用・高再現性のValidation Pipelineを確立する
- Phase 3.6（Temporal）への拡張性を担保する

本計画は以下を満たす：

- Pure Function
- Deterministic Execution
- 責務分離（Evaluator分割）
- Spec-Code 一致

---

## 2. 作業方針

- すべてのロジックは Evaluator に集約する
- Validator は「呼び出しと合成」のみを行う
- JSON DSL によりルールを定義する
- すべての処理は決定論的であること
- ValidationResult は immutable（frozen）とする
- 実装順序は依存関係に基づき最適化する

---

## 3. 作業一覧（実行順）

---

### 1. Rule Condition Engine 実装

ファイル:
- 新規: src/integrity/rule_condition_engine.py

作業内容:

- JSON Expression Tree を再帰的に評価するエンジンを実装
- 対応オペレータ:
  - 比較: ==, !=, >, <, >=, <=
  - 論理: AND, OR, NOT
  - 存在: exists
- フィールド参照:
  - ドット記法対応（例: entity.properties.mass）
- Null安全:
  - 欠損時は False（例外禁止）
- 型比較:
  - 異種型は False

DoD:

- 全オペレータが仕様通りに動作
- 不正フィールド参照で例外が発生しない
- 同一入力で完全一致の出力（決定論保証）

---

### 2. RuleEvaluator 実装

ファイル:
- 新規: src/integrity/rule_evaluator.py

作業内容:

- 入力:
  - context
  - entity
  - rules
- 処理:
  - scope適合ルールの評価
  - condition_engine を使用して判定
  - action を ValidationResult に変換
- ルール競合解決:
  - Specificity（scope） > priority > rule_id
- ソート:
  - 決定論的順序で評価

DoD:

- 全ルールが deterministic に評価される
- 競合解決が仕様通りに動作
- 副作用ゼロ

---

### 3. EscalationEvaluator 実装

ファイル:
- 新規: src/integrity/escalation_evaluator.py

作業内容:

- ERROR件数を scope別にカウント
- threshold超過で CRITICAL を追加
- 入力リストを変更せず新規リストを返す
- rule_id順でソートして評価

DoD:

- threshold超過時に必ずCRITICALが生成される
- Monotonicity（昇格のみ）を保証
- 同一入力で同一出力

---

### 4. ValidationResult 拡張

ファイル:
- 既存修正: src/integrity/validation_result.py

作業内容:

- dataclass(frozen=True) 化
- フィールド追加:
  - trace_id
  - span_id
  - source
  - target_id
- __eq__ による比較保証

DoD:

- 完全イミュータブル
- テスト比較可能
- Trace情報を保持

---

### 5. WorkflowContext 拡張

ファイル:
- 既存修正: src/workflow/workflow_context.py

作業内容:

- trace_id を追加（生成時固定）
- metadata に world_rules を保持
- scene_state を明確化
- execution_id を保持

DoD:

- trace_id が不変である
- Evaluator が必要な情報をすべて参照可能

---

### 6. Validator 再構築（Orchestrator化）

ファイル:
- 既存修正: src/integrity/consistency_validator.py

作業内容:

- ロジック削除（完全委譲）
- 呼び出し順序:
  1. RuleEvaluator
  2. TemporalEvaluator（空実装可）
  3. EscalationEvaluator
- 結果をフラットに結合
- 最終ソート:
  - (scope, code, target_id)

DoD:

- Validatorが純粋なオーケストレーターである
- ロジックが存在しない
- 出力順序が完全決定論

---

### 7. JSON DSL スキーマ定義

ファイル:
- 既存修正: data/schema/metadata_schema.json
- 既存修正: docs/spec/Core_Spec/NWF_World_Rule_Model_v2.0.1.md
- 既存修正: docs/spec/Core_Spec/NWF_World_Rule_Execution_v2.0.1.md

作業内容:

- condition の JSON schema 定義
- operator / operands 構造定義
- eval禁止明記

DoD:

- JSONバリデーション可能
- DSL仕様が明文化されている

---

### 8. Rule Action フォーマット定義

ファイル:
- 既存修正: docs/spec/Core_Spec/NWF_World_Rule_Model_v2.0.1.md

作業内容:

- action構造を明確化
- 必須項目:
  - severity
  - code
  - message
- プレースホルダ仕様定義

DoD:

- すべてのRuleが統一フォーマットで記述可能

---

### 9. Integration Test 実装

ファイル:
- 新規: tests/integration_phase_3_5_world_rules.py

作業内容:

- テストケース:
  1. 単一Rule評価
  2. 競合解決
  3. Escalation発動
  4. DSL異常系
  5. Deterministic検証（100回一致）

DoD:

- 全テストPASS
- 再現性100%

---

### 10. パフォーマンス最適化

ファイル:
- 新規: docs/spec/Execution_Spec/NWF_Execution_Performance_v2.0.1.md

作業内容:

- ルールインデックス化
- 評価キャッシュ設計
- ハッシュキー設計

DoD:

- O(N) → O(k) に削減（scope分割）
- キャッシュ戦略が仕様化

---

### 11. Error Model 追記

ファイル:
- 既存修正: docs/spec/Execution_Spec/NWF_Error_Model_v2.0.1.md

作業内容:

- Threshold方式Escalation定義追加
- scope別カウント仕様明記

DoD:

- Escalation仕様が完全定義される

---

## 4. 依存関係

1. Condition Engine
2. RuleEvaluator
3. EscalationEvaluator
4. ValidationResult
5. WorkflowContext
6. Validator
7. Spec更新
8. Test
9. Performance

---

## 5. Definition of Done

- Spec-Code 一致
- Integration Test PASS
- 完全決定論
- 副作用ゼロ
- Trace可能
- Engineとの責務分離維持

---

## 6. 結論

Phase 3.5 は

「World Rule を安全かつ決定論的に実行する純関数群の構築」

である。

この計画により：

- Validator は完全に分離される
- Engine は純粋な意思決定機構となる
- NWF は拡張可能なルール実行基盤を獲得する

次フェーズ（Phase 3.6 Temporal）への接続準備は完了する。

---

[EOF]