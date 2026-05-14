Source: docs/spec/Core_Spec/NWF_World_Rule_Model_v2.0.1.md
Updated: 2026-04-26T19:00:00+09:00
PIC: Engineer / ChatGPT

# NWF World Rule Model v2.0.1（Revised: DSL / Action 完全統合版）

---

## 1. 概要

本ドキュメントは
NWF v2.0.1 における World Rule Model の完全定義を示す。

World Rule は単なる静的設定ではなく、

* Story Engine
* Event Engine
* Conflict Engine

を制御する **世界制約エンジン（World Rule Engine）** として機能する。

本改訂では以下を達成する：

* JSON DSL による完全決定論的条件評価
* Rule Action の統一フォーマット定義
* ValidationResult との完全対応
* 実行仕様とデータ仕様の一致（Spec = Code）

---

## 2. 基本構造

World Rule は以下の2要素で構成される：

1. Static Settings（静的設定）
2. Dynamic Constraints（動的制約 + Action）

---

## 3. 基本属性

* world_rule_id
* rule_name
* rule_type
* description

---

## 4. スコープ属性

scope は階層構造を持つ：

* global
* regional
* character
* scene

優先順位：

scene > character > regional > global

属性：

* scope_level
* priority
* override_allowed

---

## 5. 静的設定属性

* settings
* tags

---

## 6. 動的制約構造（DSL統合）

### 6.1 評価構造

Rule は以下の論理構造で評価される：

trigger_logic（WHEN）
AND
constraint_conditions（IF）

両方が true の場合のみ action が発火する。

---

### 6.2 評価順序（決定論）

1. trigger_logic を評価
2. true の場合のみ constraint_conditions を評価（短絡評価）
3. true の場合 action 実行

---

### 6.3 DSL ノード構造

■ Comparison Node

{
"field": string,
"op": "==" | "!=" | ">" | "<" | ">=" | "<=",
"value": any
}

■ Logical Node

{
"operator": "AND" | "OR",
"operands": [node, ...]
}

■ NOT Node

{
"operator": "NOT",
"operands": node
}

■ Exists Node

{
"exists": string
}

---

### 6.4 評価仕様

* 優先順位：NOT > AND > OR
* operands は配列順に評価
* 最大ネスト深さ：16

---

### 6.5 exists の定義

* フィールドが存在し null でない → true
* "" / [] / {} → true
* 未定義 or null → false

---

### 6.6 エラー時挙動（例外禁止）

| ケース      | 挙動              |
| -------- | --------------- |
| フィールド未存在 | False           |
| 型不一致     | False（!=のみTrue） |
| None比較   | False           |
| 不正オペレータ  | False           |
| 不正構造     | False           |
| ネスト深度超過  | False           |

---

### 6.7 評価制約

* Pure Function
* Deterministic
* No Exception
* No Side Effect

---

## 7. Rule Action フォーマット

### 7.1 基本仕様

Rule は 1:N Actions を持つ。

actions は配列順に実行されるが、互いに独立である。

---

### 7.2 Action 属性

必須：

* severity
* code
* message

任意：

* primary_target
* params

---

### 7.3 Severity

* INFO
* WARNING
* ERROR
* CRITICAL

---

### 7.4 Code 命名規則

形式：

[SCOPE_INITIAL]-[CATEGORY]-[SEQUENCE]

例：

* G-GEN-001
* C-STA-002

---

### 7.5 Message テンプレート

プレースホルダ：

* {field}
* {value}
* {rule_id}
* {target_id}

未解決時：

→ そのまま文字列として残す

---

### 7.6 Params

params は DSL評価コンテキストから値を取得する。

例：

"params": {
"value": "$.character.hp"
}

---

### 7.7 primary_target

* 明示指定可能
* 未指定時は root entity の target_id

---

## 8. ValidationResult 変換仕様

| Action   | ValidationResult |
| -------- | ---------------- |
| severity | severity         |
| code     | code             |
| message  | 解決済み message     |
| N/A      | trace_id         |
| N/A      | span_id          |
| N/A      | source           |
| N/A      | target_id        |

---

### 8.1 固定値

* source = "rule_evaluator"
* trace_id = context.trace_id

---

### 8.2 span_id 生成

span_id = hash(rule_id + action_index + target_id + execution_id)

---

## 9. 実行順序（決定論）

Rule 実行順：

1. scope 適用
2. priority
3. rule_id（ASCII昇順）

---

## 10. Escalation 仕様

条件：

* 同一 scope 内 ERROR 件数 > threshold

結果：

* CRITICAL を1件追加

制約：

* Monotonic（降格なし）
* 入力不変

---

## 11. フル JSON スキーマ

{
"$schema": "[http://json-schema.org/draft-07/schema#](http://json-schema.org/draft-07/schema#)",
"title": "NWF World Rule Full Schema",
"type": "object",
"required": ["rule_id", "actions"],
"properties": {
"rule_id": { "type": "string", "pattern": "^RULE-[A-Z0-9_-]+$" },
"enabled": { "type": "boolean", "default": true },
"trigger_logic": { "$ref": "dsl_condition_schema.json#" },
"constraint_conditions": { "$ref": "dsl_condition_schema.json#" },
"actions": {
"type": "array",
"minItems": 1,
"items": {
"type": "object",
"required": ["severity", "code", "message"],
"properties": {
"severity": {
"enum": ["INFO", "WARNING", "ERROR", "CRITICAL"]
},
"code": { "type": "string" },
"message": { "type": "string" },
"primary_target": { "type": "string" },
"params": {
"type": "object",
"additionalProperties": { "type": "string" }
}
}
}
}
},
"additionalProperties": false
}

---

## 12. Story Engine 連携フロー

Event Candidate
→ Rule Check
→ Constraint Evaluation
→ Violation Detection
→ Action Execution
→ Conflict Generation
→ Event Finalization

---

## 13. World Rule の責務

* Event 発生制御
* Character 行動制約
* Conflict 生成
* 世界整合性維持
* シミュレーション制御

---

## 14. セキュリティ制約

禁止：

* eval / exec / import
* JSONPath ワイルドカード（$, .., *）

許可：

* ドット記法のみ

---

## 15. 非推奨要素

constraint_conditions（文字列形式）

理由：

* 非決定論
* 実行不能

---

## 16. Cross-Spec Synchronization

本仕様は以下と同期：

* NWF_World_Rule_Execution_v2.0.1.md
* NWF_Rule_Data_Binding_Spec_v2.0.1.md
* NWF_Validator_And_Context_Contract_v2.0.1.md

---

## 17. 結論

本仕様により World Rule Model は：

* 完全決定論的 DSL を持つ
* Action を通じて ValidationResult を生成する
* Engine と完全一致する実行モデルとなる

これにより NWF は：

「仕様＝実行可能コード」

という状態に到達する。

---

[EOF]