Source: docs/spec/Core_Spec/NWF_World_Rule_Execution_v2.0.1.md
Updated: 2026-04-28T11:08:00+09:00
PIC: Engineer / ChatGPT

# NWF World Rule Execution v2.0.1

---

## 1. 概要

本仕様書は、NWF World Rule Model v2.0.1 を実行時に適用するための  
「World Rule Execution Protocol」を定義する。

本仕様は以下を目的とする：

- World Rule の決定論的実行
- JSON DSL による条件評価の統合
- Action → ValidationResult の完全マッピング
- ConsistencyValidator / Story Engine との統合

---

## 2. 設計原則

### Principle: Narrative Relativity

「因果律は絶対ではない。世界設定によって相対化される」

---

## 3. 実行フロー

## 3.1 実行パイプライン（追記・修正）

1. Fetching  
   context.metadata から world_rules を取得

2. Merge  
   デフォルトルール + コンテキストルールを統合

3. Sorting（決定論保証）  
   以下のキーで完全順序ソート：

   sort_key = (scope_weight, priority, rule_id)

4. Evaluation  
   RuleConditionEngine による DSL 評価

5. Action Execution  
   条件成立時に actions を順次実行

6. Mapping  
   Action → ValidationResult 変換

7. Logging  
   違反時 AuditLog に記録

---

### 【追記】評価順と出力順の分離（Phase 3.5対応）

本仕様において以下を厳密に分離する：

* 評価順：RuleEvaluator が制御（priority を使用）
* 出力順：Validator が制御（決定論保証のみ）

#### 修正前

Sorting（決定論保証）：

```
sort_key = (scope_weight, priority, rule_id)
```

→ 評価順と出力順の区別が曖昧

#### 修正後

* 上記 sort は「評価順」にのみ適用される
* 出力順には一切影響しない

---

## 4. World Rule 取得仕様

world_rules = context.metadata.get("world_rules", {})

---

## 5. World Rule パラメータ（標準）

- allow_resurrection
- allow_ghost_activity
- allow_time_reversal
- physics_override

---

## 6. ルール適用スコープと優先順位

### 6.1 スコープ階層

global < regional < character < scene

### 6.2 scope_weight

| scope     | weight |
|----------|--------|
| scene    | 10     |
| character| 20     |
| regional | 30     |
| global   | 40     |

※ 小さいほど優先

---

## 7. 競合解決アルゴリズム（重要修正）

### 修正前（保持・仕様外化）

```
sort_key = (scope_weight, priority, rule_id)
```

- 完全順序保証
- Python Timsort に依存可能
- 同一入力 → 同一出力

---

問題点：

* 出力順にも影響すると誤解される可能性
* Phase 3.5 テスト仕様と不整合

---

### 修正後（必須仕様）

本ソートは「RuleEvaluator内の評価順」にのみ適用する：

```
evaluation_sort_key = (scope_weight, priority, rule_id)
```

---

### 【新規追加】Validator出力順仕様（明文化）

Validator の最終出力は以下でソートされる：

```
(severity, code, target_id)
```

#### 重要ルール

* priority は出力順に一切影響しない
* scope_weight も出力順に影響しない
* rule_id も順序意味を持たない

---

### 設計原則

* RuleEvaluator：意味順序（評価順）を持つ
* Validator：意味順序を持たない（決定論のみ）

---

## 8. DSL Condition 評価仕様

### 8.1 評価順序

1. trigger_logic を評価
2. true の場合のみ constraint_conditions を評価

（短絡評価）

---

### 8.2 演算子優先順位

NOT > AND > OR

同一階層は operands のインデックス順

---

### 8.3 型安全

- number vs number → OK
- string vs string → OK
- boolean vs boolean → OK
- その他 → False

例外禁止

---

### 8.4 exists

- フィールド存在かつ null でない → True
- 未存在 / null → False
- "", [], {} → True

---

### 8.5 フィールド参照

- ドット記法のみ許可
- 未存在 → False
- 例外禁止

---

### 8.6 Null安全

- None を含む評価 → False

---

### 8.7 ネスト制限

- 最大深さ：16
- 超過時：False

---

### 8.8 禁止事項

- eval / exec / import 禁止
- ワイルドカード JSONPath 禁止

---

## 9. Action 実行仕様

### 9.1 基本構造

- 1 Rule : N Actions
- actions はインデックス順に実行
- 各 Action は独立

---

### 9.2 Action フィールド

必須：

- severity
- code
- message

任意：

- primary_target
- params

---

### 9.3 Severity

- INFO
- WARNING
- ERROR
- CRITICAL

---

### 9.4 Code 命名規則

形式：

[SCOPE_INITIAL]-[CATEGORY]-[SEQUENCE]

例：

- G-GEN-001
- C-STA-002

---

### 9.5 プレースホルダ展開

対応：

- {entity.id}
- {entity.properties.*}
- {context.scene_id}
- {target_id}
- {value}
- {rule_id}

仕様：

- ドット記法対応
- 未解決 → 空文字
- 例外禁止

---

### 9.6 primary_target

- 明示指定可能
- 未指定時：entity.id

---

### 9.7 params

- JSON パス指定（ドット記法のみ）
- 値取得失敗時：
  → プレースホルダ未置換

---

## 10. Action → ValidationResult 変換

### 10.1 マッピング

| Action | ValidationResult |
|--------|----------------|
| severity | severity |
| code | code |
| message | message |
| N/A | trace_id |
| N/A | span_id |
| N/A | source |
| N/A | target_id |

---

### 10.2 固定値

source = "rule_evaluator"

---

### 10.3 trace_id

context.trace_id を使用

---

### 10.4 span_id 生成

sha256(
  f"{trace_id}:{execution_id}:{rule_id}:{entity.id}:{action_index}"
)

- 完全決定論
- hash() 使用禁止

---

## 11. regional スコープ判定

条件：

rule.scope.target_id == entity.location_id

- location_id 未定義 → False
- 例外禁止

---

## 12. Escalation 連携

- scope単位で ERROR 数を集計
- threshold 超過時：

CRITICAL を1件追加

- Monotonicity 保証

---

## 13. ConsistencyValidator 連携（追記）

Validator は以下を実行：

1. RuleEvaluator 呼び出し
2. EscalationEvaluator 呼び出し
3. 結果統合

責務：

- オーケストレーションのみ
- ロジック禁止

---

### 【追記】出力順責務

Validator は以下を保証する：

* 決定論的順序
* 入力順非依存
* priority 非依存

#### 禁止事項

* priority を使用した出力順制御
* RuleEvaluator の順序の引き継ぎ

---

## 14. Story Engine 連携

- エッジ生成可否判定
- イベント合法性確認
- Timeline整合性検証

---

## 15. 決定論保証ルール（強化）

### 【追記】決定論の定義（Phase 3.5）

決定論とは：

* 同一入力 → 同一出力（順序含む）
* 入力順変更 → 出力不変

必須条件：

1. 入力不変
2. 完全順序ソート
3. 外部状態禁止
4. 時刻依存禁止
5. 例外禁止（Falseフォールバック）

---

### 【新規追加】決定論条件

6. 評価順と出力順が分離されていること
7. 出力順が `(severity, code, target_id)` によること
8. priority が出力順に影響しないこと

---

## 16. 削除仕様

削除対象：

- 固定因果律（ERR_CAUSAL）

理由：

- Narrative Relativity に反する

---

## 17. 影響範囲

影響あり：

- ConsistencyValidator
- Story Engine
- Event Engine（将来）
- Conflict Engine（将来）

影響なし：

- Data Model
- Entity Schema

---

## 18. セキュリティポリシー

- DSL は純関数として実行
- 動的コード実行禁止
- 実行コスト予測可能性保証
- JSON Schema 準拠必須

---

## 19. まとめ

本仕様により NWF は以下を実現する：

- World Rule による動的ストーリー制御
- JSON DSL による安全な条件評価
- Action → ValidationResult の完全決定論変換
- トレーサブルな実行基盤

本仕様は NWF における「物語の憲法」であり、  
すべての実行エンジンは本仕様に従う必要がある。

---

## 20. 【新規追加】評価順と出力順の分離（明文化）

### 定義

| 概念  | 担当            | 説明            |
| --- | ------------- | ------------- |
| 評価順 | RuleEvaluator | ルール実行順        |
| 出力順 | Validator     | 結果整列（決定論保証のみ） |

---

### 仕様

* RuleEvaluator は priority を使用して評価順を決定する
* Validator は priority を一切使用しない
* Validator は決定論的順序のみ保証する

---

### 禁止事項

* priority を出力順に使用すること
* 評価順を出力順とみなすこと
* rule_id に順序意味を持たせること

---

### 設計上の意味

旧：
評価順 ≒ 出力順（混在）

新：
評価順 ≠ 出力順（完全分離）

---

## 21. 【新規追加】テスト整合性保証（Integration Test対応）

### 対象

tests/integration_phase_3_5_world_rules.py

### 保証内容

* 入力順序を変更しても出力が一致する
* 全ルールが評価される
* Escalation が決定論的に追加される

---

### 整合条件

* DummyValidator の以下仕様と一致すること：

```
sorted(results, key=lambda r: (r["severity"], r["code"], r["target_id"]))
```

---

### 結論

* Spec と Test は完全一致
* priority は出力順に影響しないことが明示された
* 曖昧性は完全に排除された

---

[EOF]