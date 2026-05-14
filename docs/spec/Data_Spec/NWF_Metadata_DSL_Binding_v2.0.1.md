Source: docs/spec/Data_Spec/NWF_Metadata_DSL_Binding_v2.0.1.md
Updated: 2026-04-26T13:49:00+09:00
PIC: Engineer / ChatGPT

# NWF Metadata DSL Binding v2.0.1

---

## 1. 概要

本ドキュメントは、NWF Phase 3.5 における JSON DSL（World Rule）評価エンジンと `metadata_schema.json` の間の**バインディング仕様**を定義する。

目的：

* JSON DSL評価エンジンが参照する **入力（Fact）フィールド**を明確化する
* 評価結果として記録される **Trace（実行記録）フィールド**を標準化する
* Evaluator群（RuleEvaluator / ConditionEngine / EscalationEvaluator）が
  metadata を介して **決定論的に動作することを保証する**
* Validator（Orchestrator）が metadata に依存して再現可能な実行を行えるようにする

---

## 2. 設計原則

本仕様は以下の原則に従う：

* **Pure Function 原則**

  * Evaluatorはmetadataを入力としてのみ使用し、副作用を持たない
* **Deterministic Execution**

  * 同一 metadata 入力に対して常に同一結果を生成
* **Traceability 完全性**

  * すべての評価は追跡可能である
* **責務分離**

  * 入力（Fact）と出力（Trace）を明確に分離
* **Spec-Code 一致**

  * 本仕様は実装と完全一致することを前提とする

---

## 3. バインディング全体構造

JSON DSL評価における metadata の役割は以下の2系統に分類される：

| 区分        | 内容               |
| --------- | ---------------- |
| Fact（入力）  | 評価エンジンが参照する不変データ |
| Trace（出力） | 評価結果および実行履歴      |

---

## 4. 入力（Fact）バインディング定義

### 4.1 audit_context

用途：トランザクション単位の整合性保証

使用フィールド：

* `audit_context.last_transaction_id`

  * Validationの基準トランザクション
* `audit_context.created_at`
* `audit_context.updated_at`

役割：

* Validation対象の**時間的一貫性の基準**
* traceability.validation_state との対応付け

---

### 4.2 workflow_context

用途：実行時コンテキスト

使用フィールド：

* `workflow_context.workflow_id`
* `workflow_context.execution_id`
* `workflow_context.validation_thresholds`

特に重要：

#### validation_thresholds

```json
"validation_thresholds": {
  "scene": 5,
  "character": 3,
  "global": 20
}
```

役割：

* EscalationEvaluator の**唯一の入力パラメータ**
* scope別ERROR上限を定義
* Evaluatorの純粋性を維持（外部設定排除）

---

### 4.3 traceability（入力としての一部利用）

以下は「前回状態」として参照される：

* `traceability.validation_state.validation_version`
* `traceability.validation_state.rule_set_hash`

役割：

* RuleEvaluatorの**差分検知**
* キャッシュキー生成の補助

---

### 4.4 DSL評価対象データ（Entity）

※metadata外だが参照必須

* entity本体（例：character, scene）
* フィールド参照（例：`entity.properties.hp`）

役割：

* ConditionEngineの主要入力

---

## 5. Trace（出力）バインディング定義

### 5.1 traceability.validation_state

JSON DSL評価結果の中核

```json
"validation_state": {
  "validation_version": "v2.0.1",
  "last_transaction_id": "uuid",
  "rule_set_hash": "sha256...",
  "evaluation_engine_version": "1.0.0",
  "is_deterministic": true
}
```

各フィールドの役割：

| フィールド                     | 内容                   |
| ------------------------- | -------------------- |
| validation_version        | Validation仕様バージョン    |
| last_transaction_id       | 対応するaudit_context    |
| rule_set_hash             | 適用されたWorld Ruleのハッシュ |
| evaluation_engine_version | Engine実装バージョン        |
| is_deterministic          | 常にtrue（保証制約）         |

---

### 5.2 DSL Context（拡張トレース）

```json
"dsl_context": {
  "applied_rule_hashes": ["sha256..."],
  "evaluation_engine_version": "1.0.0"
}
```

役割：

* Rule単位の適用履歴
* デバッグ・監査用途
* 再現性保証

---

### 5.3 audit_context との関係

整合ルール：

* `validation_state.last_transaction_id`
  == `audit_context.last_transaction_id`

これにより：

* Validationとデータ変更の完全対応を保証
* ロールバック・再実行が可能

---

## 6. Evaluator別バインディング

### 6.1 ConditionEngine

入力：

* entity
* DSL condition
* metadata（参照のみ）

使用：

* フィールド参照（dot notation）
* 型チェック（metadata依存なし）

出力：

* boolean（純関数）

---

### 6.2 RuleEvaluator

入力：

* entity
* rules
* metadata.workflow_context

使用：

* validation_thresholds（間接的）
* rule_set_hash（生成）

出力：

* ValidationResult[]
* rule_set_hash（traceへ）

---

### 6.3 EscalationEvaluator

入力：

* ValidationResult[]
* metadata.workflow_context.validation_thresholds

処理：

* scope別カウント
* threshold比較

出力：

* 新規ValidationResult（CRITICAL）

制約：

* 入力リスト不変（immutable）

---

### 6.4 Validator（Orchestrator）

入力：

* metadata（完全参照）
* entity
* rules

処理：

1. RuleEvaluator
2. TemporalEvaluator（将来）
3. EscalationEvaluator

出力：

* 結果統合
* traceability更新

---

## 7. 決定論保証仕様

以下を満たすことで完全決定論を保証：

* metadataにすべての外部依存を集約
* validation_thresholds の明示化
* rule_set_hash の固定化
* evaluation_engine_version の記録
* is_deterministic = true（強制）

---

## 8. 禁止事項

以下は厳格に禁止：

* eval / 動的コード実行
* metadata外部の暗黙依存
* ランダム値使用
* 時刻依存処理（現在時刻取得）

---

## 9. Cross-Spec Synchronization

本仕様は以下と同期される：

* Core_Spec:

  * NWF_World_Rule_Model_v2.0.1.md
* Execution_Spec:

  * NWF_World_Rule_Execution_v2.0.1.md
  * NWF_Validator_Orchestration_Spec_v2.0.1.md
* Data_Spec:

  * metadata_schema.json
  * dsl_condition_schema.json

---

## 10. まとめ

本仕様により：

* metadata は単なる付随情報ではなく
  **DSL評価の完全な入力・出力基盤**となる

* Evaluatorは：

  * 外部状態に依存せず
  * metadataのみを参照し
  * 完全決定論的に動作する

* Validatorは：

  * metadataに基づく純粋なオーケストレーターとして機能する

これにより NWF Phase 3.5 の中核要件である：

* Deterministic Validation
* Traceability
* Spec-Code 一致

が保証される。

---

[EOF]