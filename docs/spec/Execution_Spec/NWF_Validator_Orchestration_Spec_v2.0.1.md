Source: docs/spec/Execution_Spec/NWF_Validator_Orchestration_Spec_v2.0.1.md
Updated: 2026-05-13T22:40:00+09:00
PIC: Engineer / ChatGPT

# NWF Validator Orchestration Spec v2.0.1

---

## 1. 概要

本ドキュメントは
NWF Phase 3.5 における Validator の「完全オーケストレーター化」を実現するための実行仕様を定義する。

本仕様は以下を目的とする：

* Validator の責務を「制御（Orchestration）」のみに限定する
* Evaluator 群の統合実行フローを明確化する
* Validation Pipeline の決定論性（Determinism）を保証する
* ValidationResult の非破壊伝播を保証する
* Phase 3.6（Temporal）への拡張性を確保する

---

## 2. 設計原則

### 2.1 Orchestrator 原則

Validator は以下のみを行う：

* 入力データの分配
* Evaluator 呼び出し
* 結果の統合
* 決定論的ソート

追記（2026-05-13）:

* Validator は StoryDB / Entity / ValidationResult の内部構造へ直接依存してはならない
* Validator は Evaluator の実行順序制御のみを責務とする
* ValidationResult は Evaluator が生成したものをそのまま伝播する
* ValidationResult の再構築・変換・補正は禁止
* Validator は StoryDB の実装差異を吸収してはならず、公開I/Fのみに依存する

### 2.2 禁止事項

Validator において以下は完全禁止：

* 条件分岐による検証ロジック
* if/else による整合性判定
* ValidationResult の再生成
* Severity の変更
* 再評価処理

追記（2026-05-13）:

* DB内部辞書・内部キャッシュへの直接アクセス
* UUID比較等のドメイン検証ロジックの直接実装
* ValidationResult の mutable 操作
* ValidationResult のフィルタリングによる意味変更
* INFO生成条件などの検証ポリシーの直接実装

理由:
これらは Evaluator 層または Validation Policy 層の責務であり、
Validator が保持すると責務分離違反および Determinism 破壊を引き起こすため。

---

## 3. 入出力仕様

### 3.1 入力

Validator は以下を入力とする：

* target: Entity（単一）
* context: WorkflowContext

追記（2026-05-13）:

* target.id は外部I/F上必ず `str`
* Validator は ID型として UUID object を扱わない
* context 経由で取得される StoryDB は以下I/Fに準拠している必要がある：

```python
get(entity_id: str) -> Optional[Entity]
```

* Validator は StoryDB 実装の内部構造に依存してはならない

### 3.2 出力

* List[ValidationResult]

追記（2026-05-13）:

* 出力される ValidationResult は Evaluator が生成した immutable object をそのまま保持する
* Validator は ValidationResult の属性変更を行わない
* ValidationResult は pass-through 原則に従う

---

## 4. 実行フロー（基本シーケンス）

Validator は以下の順序で Evaluator を実行する：

1. RuleEvaluator
2. TemporalEvaluator
3. EscalationEvaluator

---

## 5. 詳細オーケストレーション仕様

### 5.1 Step 1: RuleEvaluator

#### 入力生成

Validator は以下を取得・生成する：

* context.metadata.world_rules
* target に適用可能な rule のフィルタリング

追記（2026-05-13）:

* Rule の適用判定は Evaluator 呼び出し準備としてのみ許可される
* Rule内容そのものの評価・整合性判定は禁止
* Validator は Rule 実行結果を変更してはならない

#### 実行

```python
rule_results = RuleEvaluator.process(rules, target, context)
```

#### 出力

* List[ValidationResult]

追記（2026-05-13）:

* ValidationResult は immutable object として扱う
* Validator による Severity 変更は禁止
* Validator による code / scope / target_id の補正は禁止

---

### 5.2 Step 2: TemporalEvaluator（Phase 3.5暫定）

#### 入力生成

* current_entity: target
* history: context から取得

追記（2026-05-13）:

* TemporalEvaluator は Phase 3.5 時点では暫定 no-op evaluator として扱う
* Validator は TemporalEvaluator の空配列結果に対し特別処理を行わない

#### 実行

```python
temporal_results = TemporalEvaluator.evaluate(target, history, context)
```

#### 出力

* Phase 3.5 では必ず空配列 `[]`

追記（2026-05-13）:

* Validator は空配列であることを前提とした条件分岐を実装してはならない
* 将来の Phase 3.6 Temporal 拡張との互換性維持を優先する

---

### 5.3 Step 3: EscalationEvaluator

#### 入力

* rule_results + temporal_results

追記（2026-05-13）:

* 入力 ValidationResult は merge 前の immutable object をそのまま使用する
* Validator は escalation 条件を実装しない
* CRITICAL 判定は EscalationEvaluator の責務とする

#### 実行

```python
escalated_results = EscalationEvaluator.evaluate(all_results, context)
```

#### 出力

* CRITICAL を追加した新規リスト

追記（2026-05-13）:

* EscalationEvaluator は追加 ValidationResult のみを返す
* 既存 ValidationResult の変更は禁止
* Validator は escalated_results の再評価を行わない

---

## 6. 結果統合

Validator は以下の順序で結果を統合する：

```python
all_results = (
    rule_results
    + temporal_results
    + escalated_results
)
```

※注意：

* 元リストの破壊は禁止
* 必ず新規リストで統合

追記（2026-05-13）:

* merge 処理は immutable merge とする
* append による原本変更は禁止
* ValidationResult の順序変更は sort phase のみで許可される
* Validator は merge 時に ValidationResult の削除を行ってはならない
* INFO suppression 等の validation policy は Evaluator 側責務であり、Validator は関与しない

理由:
ValidationResult の pass-through 原則および非破壊伝播を保証するため。

---

## 7. ソート仕様（決定論保証）

### 7.1 ソートキー

最終出力は以下でソートする：

```python
(scope_weight, severity_weight, code, target_id)
```

追記（2026-05-13）:

* target_id は必ず `str`
* code は deterministic string とする
* Python object id 等の runtime 依存値は禁止
* ソートキー生成時に mutable state を参照してはならない

---

### 7.2 Scope Weight 定義

以下の順序を厳密に適用する：

```text
global < regional < scene < character < entity
```

対応マッピング例：

| scope     | weight |
| --------- | ------ |
| global    | 0      |
| regional  | 1      |
| scene     | 2      |
| character | 3      |
| entity    | 4      |

追記（2026-05-13）:

* Scope Weight は固定値であり runtime変更禁止
* Spec外 scope の暗黙追加は禁止
* 未定義scopeを Validator が補正してはならない

---

### 7.3 Severity Weight 定義

```text
INFO < WARNING < ERROR < CRITICAL
```

追記（2026-05-13）:

* Severity Weight は deterministic ordering 用固定定義である
* Validator は severity の変換・補正・再分類を行わない

---

### 7.4 決定論性保証

* 同一入力に対し完全一致の出力を保証
* ソート順は完全固定
* Python の sort 安定性に依存しない設計

追記（2026-05-13）:

* runtime memory address への依存禁止
* hash randomization 依存禁止
* dict iteration order 依存禁止
* 並列実行順依存禁止

理由:
Execution環境差異による ValidationResult 順序揺れを完全排除するため。

---

## 8. シーケンス図

```text
[Validator]
|
|-- fetch rules from context
|
|-- filter rules by target
|
|-- RuleEvaluator.process()
|       ↓
|   rule_results
|
|-- TemporalEvaluator.evaluate()
|       ↓
|   temporal_results ([])
|
|-- merge(rule + temporal)
|
|-- EscalationEvaluator.evaluate()
|       ↓
|   escalated_results
|
|-- merge(all)
|
|-- sort()
|
|-- return final_results
```

---

## 9. 単位処理モデル

### 9.1 処理単位

* Validator は「単一 Entity」単位で実行される

### 9.2 非対応（Phase 3.5）

* バッチ処理
* 並列処理

---

## 10. Determinism 保証

以下を満たす：

* 同一入力 → 同一出力
* 副作用なし
* 時刻依存なし
* ランダム性なし

追記（2026-05-13）:

* StoryDB内部構造依存なし
* import順依存なし
* Python implementation差異依存なし
* ValidationResult mutable state依存なし
* object identity 比較禁止
* UUID object の直接比較依存禁止

追記理由:
Debug Work Plan v20260502 において、
Entity ID の str 正規化および StoryDB I/F統一が Single Source of Truth として確定したため。

---

## 11. ValidationResult 取り扱い規約

### 11.1 不変性

* ValidationResult は frozen dataclass
* 変更不可

追記（2026-05-13）:

* Validator は ValidationResult を mutate してはならない
* ValidationResult の shallow copy / deep copy による再生成は禁止
* Severity / scope / rule_id / target_id の変更は禁止

### 11.2 伝播

* Pass-through 原則
* 変換禁止

追記（2026-05-13）:

* Evaluator 出力はそのまま merge/sort のみに使用する
* Validator は ValidationResult の意味変更を行わない
* ValidationResult.failure() の呼び出し責務は Evaluator 側に存在する

理由:
Validator を純粋 orchestration layer として維持するため。

---

## 12. 拡張性（Phase 3.6 以降）

### 12.1 TemporalEvaluator 拡張

* Timeline整合性
* 因果律検証
* 状態遷移検証

### 12.2 Evaluator追加

将来的に以下追加可能：

* DependencyEvaluator
* ResourceEvaluator
* ProbabilityEvaluator

---

## 13. エラーハンドリング

### 13.1 CRITICAL

* EscalationEvaluator により生成
* Validatorは例外処理を行わない

追記（2026-05-13）:

* Validator は CRITICAL を suppress してはならない
* Validator は Severity escalation を直接実装しない
* CRITICAL の生成責務は Evaluator 層に限定される

### 13.2 ERROR

* 出力として保持
* 実行継続

追記（2026-05-13）:

* ERROR 存在時でも Validator は deterministic pipeline を継続する
* Validator は ERROR の意味解析を行わない

---

## 14. Legacyロジックの扱い

### 14.1 廃止対象

* consistency_validator.py 内の if/else ロジック

追記（2026-05-13）:

* StoryDB内部構造直接参照
* mutable ValidationResult 更新
* Validator 内 UUID比較ロジック
* INFO suppression の直接実装
* validation policy の inline 実装

### 14.2 理由

* 責務分離違反
* Determinism破壊
* Validation思想違反

追記（2026-05-13）:

* Single Source of Truth 原則違反
* Evaluator責務との重複
* StoryDB I/F抽象化違反
* immutable pipeline 違反
* Phase 3.6 拡張阻害

削除不要とした理由:
Legacy禁止事項は将来的な実装逸脱防止に必要なため、
履歴を保持したまま追記形式で管理する。

---

## 15. Validatorの最終定義

Validatorとは：

「Evaluatorを順序付きで実行し、結果を統合・整列する純粋制御層である」

追記（2026-05-13）:
Validator は：

* Validation policy を持たない
* ドメイン整合性判定を持たない
* ValidationResult を生成しない
* ValidationResult を変更しない
* StoryDB内部構造へ依存しない
* deterministic orchestration のみを責務とする

また以下を保証する：

* immutable Validation pipeline
* pass-through ValidationResult propagation
* StoryDB interface abstraction
* Entity ID str normalization compatibility
* Phase 3.6 Temporal extension compatibility

---

## 16. まとめ

本仕様により以下が保証される：

* Validator の完全オーケストレーター化
* Validation Pipeline の決定論性
* ValidationResult の非破壊伝播
* Scope順序の明確化
* Phase 3.6 への拡張準備

追記（2026-05-13）:
さらに以下を保証する：

* StoryDB I/F抽象化の徹底
* Entity ID型揺れの排除
* immutable ValidationResult pipeline
* Evaluator責務との完全分離
* Single Source of Truth の維持
* Python runtime差異による非決定性排除

これにより Validator は、
「検証ロジックを持たない純粋 orchestration layer」
として Phase 3.5 正式仕様に整合する。

---

[EOF]