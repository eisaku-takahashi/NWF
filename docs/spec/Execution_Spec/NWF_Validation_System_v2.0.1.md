Source: docs/spec/Execution_Spec/NWF_Validation_System_v2.0.1.md
Updated: 2026-05-13T17:43:00+09:00
PIC: Engineer / ChatGPT

# NWF Validation System v2.0.1

---

## 1. 概要

NWF Validation System は、NWF v2.0.1（Story OS）における品質保証（Quality Assurance）、論理整合性検証（Logical Integrity Verification）、および物語因果整合性維持を目的とした多層検証システムである。

本システムは単なるデータ検証機構ではなく、NWF の Execution Pipeline、Engine System、Data Model、Audit System、Error Model と統合され、Validation Driven Generation（検証駆動型生成）を実現する中核システムとして設計される。

NWF においては、すべての Engine 出力、データ生成、Timeline 更新、Event 発生、State 変更、Emotion 変化、Narrative 生成は Validation を通過しなければならない。

Validation に失敗した場合、Error Model が起動し、Rollback、Recalculation、Re-Validation の自己修復ループ（Self-Healing Loop）が実行される。

---

## 2. Validation 対象

Validation System は NWF に存在するすべての Entity および構造データを検証対象とする。

### 2.1 Foundation Entities
- Metadata
- Version
- Transaction
- Audit Log Reference
- Execution Result

検証内容:
- ID 重複
- Version 整合性
- Transaction 順序
- Timestamp 整合性
- Metadata Schema

### 2.2 Structural Entities
- Timeline
- Scene
- Thread
- Beat
- Thread Graph
- Story Structure

検証内容:
- Timeline 連続性
- Scene 順序
- Thread Graph 循環参照
- Beat Sequence 整合性
- Structure Gap Detection

### 2.3 Dynamic Entities
- Event
- State
- Emotion
- Conflict
- Simulation Result

検証内容:
- Event Preconditions
- State Transition
- Emotion Curve
- Conflict Resolution
- Simulation Consistency

### 2.4 Relational Entities
- Character
- Relationship
- WorldRule
- Dependency
- Reference ID

検証内容:
- Character 設定整合性
- Relationship 整合性
- WorldRule 違反
- Reference 存在確認

### 2.5 Output Entities
- Narrative
- Query
- Execution Result
- Analysis Result

検証内容:
- Narrative と Event の整合性
- Query Syntax
- Output Consistency
- Narrative Integrity

---

## 3. Validation Fields

各 Entity および Data Model には以下の Validation 関連フィールドを持たせる。

Validation Fields:
- validation_status
- integrity_score
- consistency_score
- validation_log
- validation_errors
- validation_warnings
- validation_timestamp
- validated_by_engine
- validation_version
- dependency_ids
- recalculation_flag
- rollback_flag
- last_validation_transaction_id

### 3.1 validation_status
状態:
- pending
- valid
- warning
- invalid
- dirty

### 3.2 integrity_score
範囲:
0.0 ～ 1.0

Story、Timeline、Thread、Narrative 全体の整合性評価に使用する。

### 3.3 consistency_score
他 Entity との整合性スコア。

---

## 4. Validation Layer Architecture

Validation System は多層検証構造を持つ。

### 4.1 Level 1: Schema Validation
JSON Schema による形式検証。

検証内容:
- JSON 構造
- 型
- 必須フィールド
- Enum
- 値範囲
- Schema 適合性

対象:
- entity_schema.json
- metadata_schema.json

### 4.2 Level 2: Reference Validation
参照整合性検証。

検証内容:
- entity_id 存在確認
- dependency_ids 整合性
- reference_id 整合性
- graph 循環参照検出
- orphan entity 検出

### 4.3 Level 3: Engine Logic Validation
各 Engine が実行した結果の論理検証。

対象 Engine:
- Timeline Engine
- Event Engine
- Simulation Engine
- State Engine
- Emotional Curve Engine
- Narrative Engine
- Story Engine
- Query Engine
- Analysis Engine

### 4.4 Level 4: Cross Engine Validation
Engine 間の整合性検証。

検証例:
- Timeline と Event
- Event と State
- State と Emotion
- Emotion と Narrative
- WorldRule と Simulation
- Character と Event
- Narrative と Timeline

### 4.5 Level 5: Narrative Integrity Validation
Story 全体の整合性検証。

検証対象:
- Narrative Arc
- Emotional Curve
- Character Development
- Theme Consistency
- Plot Consistency
- Foreshadowing Resolution
- Narrative Closure
- Logical Consistency
- World Consistency

---

## 5. Engine Validation Responsibilities

各 Engine は Self Validation の責任を持つ。

### 5.1 Timeline Engine
- Temporal Order Validation
- Time Overlap Validation
- Timeline Gap Detection
- Event Timestamp Consistency

### 5.2 Event Engine
- Event Preconditions
- Event Dependency
- Event Outcome Consistency
- Event Reference Validation

### 5.3 Simulation Engine
- Physics / WorldRule Validation
- Resource Consistency
- Probability Consistency
- State Transition Validation

### 5.4 State Engine
- Character State Validation
- Object State Validation
- Attribute Range Validation
- State Dependency Validation

### 5.5 Emotional Curve Engine
- Emotional Curve Validation
- Emotion Transition Validation
- Emotional Continuity Validation

### 5.6 Narrative Engine
- Plot Structure Validation
- Narrative Flow Validation
- Character Arc Validation
- Theme Consistency Validation

### 5.7 Analysis Engine
- Cross Engine Validation
- Consistency Analysis
- Integrity Score Calculation

---

## 6. Validation Gates in Execution Pipeline

Execution Pipeline の各フェーズに Validation Gate を設置する。

Validation Gates:
1. Input Validation Gate
2. Plan Validation Gate
3. Structure Validation Gate
4. Timeline Validation Gate
5. Event Validation Gate
6. Simulation Validation Gate
7. State Validation Gate
8. Emotion Validation Gate
9. Cross Engine Validation Gate
10. Integrity Validation Gate
11. Narrative Validation Gate
12. Save Validation Gate
13. Commit Validation Gate

Validation Gate Failure 時:
- Execution Stop
- Error Model Trigger
- Rollback
- Recalculation
- Re-Validation
- Audit Log Record

---

## 7. Validation → Error Model Flow

Validation Failure 発生時のフロー。

Validation Flow:
1. Validation Execution
2. Validation Failure Detection
3. Validation Log Record
4. Audit Log Record
5. Error Model Trigger
6. Error Classification
7. Analysis Engine Feedback
8. Rollback
9. Recalculation
10. Re-Validation
11. Integrity Score Recalculation
12. Execution Resume

Self-Healing Loop:
Validation → Error Detection → Audit → Analysis → Rollback → Recalculation → Validation

---

## 8. Audit Log Integration

Validation System は Kernel Audit System と統合される。

### 8.1 Audit Event
Validation 関連イベント:
- VALIDATION_START
- VALIDATION_SUCCESS
- VALIDATION_WARNING
- VALIDATION_ERROR
- INTEGRITY_SCORE_CALCULATED
- ROLLBACK_TRIGGERED
- RECALCULATION_TRIGGERED
- VALIDATION_RETRY
- VALIDATION_FINAL_FAILURE

### 8.2 Audit Log Fields
Validation Audit Log:
- transaction_id
- validation_id
- object_id
- engine_name
- validation_level
- validation_result
- integrity_score
- error_code
- error_message
- actor
- timestamp_jst
- related_objects
- rollback_flag
- recalculation_flag

Validation Failure は必ず Audit Log に記録される。

---

## 9. Logging & Traceability

NWF は以下のログを統合管理する。

Log Types:
- Execution Log
- Validation Log
- Audit Log
- Analysis Log

Trace Types:
- Execution Trace
- Validation Trace
- Audit Trace
- Version Trace
- Transaction Trace

これにより、以下を完全追跡可能とする。
- いつ
- 誰が
- どの Engine が
- 何を変更し
- なぜ Validation に失敗し
- どの Rollback が実行されたか

---

## 10. Validation System Architecture Summary

NWF Validation System は Story OS における整合性維持システムであり、以下の役割を持つ。

Validation System Roles:
- Data Integrity Assurance
- Logical Consistency Verification
- Narrative Consistency Verification
- Execution Safety Control
- Rollback Trigger System
- Recalculation Trigger System
- Integrity Score Evaluation
- Audit Evidence Generation
- Self-Healing Loop Control
- Story Integrity Assurance

Validation System は NWF Kernel、Engine System、Execution Pipeline、Error Model、Audit System と連携し、Story OS 全体の整合性と説明責任を保証する。

---

## 11. ValidationResult 集約ルール（Phase 3.4 拡張・修正）

### 11.1 背景（不具合の発生原因）

従来の実装では、複数の ValidationResult を集約する際に以下のような問題が存在した。

- all() や boolean ベースで is_valid を評価
- severity が間接的に上書き・消失
- CRITICAL が WARNING / INFO に劣化する

これは以下の問題を引き起こした。

- Engine が停止すべきケースで継続する
- Error Model が起動しない
- Audit の信頼性が崩壊する

また、Phase 3.5 Debug Work Plan において以下が追加確認された：

- Validator / Engine / Mock 間で Severity が意味論的制御信号として使用されている
- CRITICAL は Engine 停止制御に直結する
- INFO 混在禁止仕様が Integration Test において明示検証対象となった

そのため、ValidationResult の集約は
「論理圧縮」ではなく「非破壊伝播」でなければならない。

---

### 11.2 【重要修正】旧仕様の扱い（削除ではなく無効化）

以下の旧仕様は削除せず「仕様外」として保持する。

旧仕様:
- 任意ロジックによる集約
- is_valid ベースの判定
- boolean圧縮

理由:
- 過去の実装との互換性検証のため
- Audit / Debug 時の比較参照のため

追加理由（Phase 3.5）:
- 過去の Validation Trace の比較検証
- Historical Audit Diff の整合性維持
- Integration Test の後方互換性確認

ただしこれらは現在の仕様では使用禁止とする。

---

### 11.3 新ルール（必須）

#### ■ ルール1：merge() のみ使用可能

ValidationResult の集約は ValidationResult.merge() のみで行う。

#### ■ ルール2：最大Severity保持（Monotonicity適用）

CRITICAL > ERROR > WARNING > INFO

最も高いSeverityを必ず保持する。

#### ■ ルール3：Severity圧縮禁止

boolean変換禁止  
is_valid は補助情報

#### ■ ルール4：Adapterでの再生成禁止

変換のみ許可  
意味変更禁止

#### ■ ルール5（Phase 3.5追加）：ValidationResult の非破壊伝播

Validation Pipeline 内において：

- ValidationResult の再生成禁止
- Severity の再評価禁止
- Adapter / Auditor における downgrade 禁止

を正式仕様として固定する。

---

### 11.4 ValidationResult 集約と Engine 制御（追記）

ValidationResult は単なる検証結果ではなく、
以下の Runtime Control Signal として扱う。

- Engine停止制御
- Rollback Trigger
- Recalculation Trigger
- Audit Priority
- Self-Healing Loop 制御

そのため：

- CRITICAL の消失
- ERROR の downgrade
- WARNING の圧縮

は Runtime Integrity Violation とみなす。

---

### 11.5 Integration Test 整合性（Phase 3.5追加）

以下の Integration Test と完全一致する必要がある：

- tests/integration_phase_3_4_validator.py
- tests/integration_phase_3_5_world_rules.py
- tests/unit/test_validator_critical_only.py

特に以下を保証する：

- CRITICAL は必ず Engine まで到達
- violation 存在時に INFO を混在させない
- merge() 以外で Severity が変化しない
- ValidationResult の順序が決定論的である

---

### 11.6 設計上の意味（更新）

旧：
集約型（情報破壊構造）

新：
伝播型（情報非破壊構造）

Phase 3.5以降：
「ValidationResult を完全再現可能な制御信号として扱う」

---

## 12. Severity Monotonicity Rule（Validation System適用・新規追加）

### 12.1 追加理由

Error Model 側で導入された Monotonicity Rule を Validation System にも適用する必要があるため。

また、Phase 3.4 において以下の問題が確認された：

- CRITICAL が途中で消失する
- Adapter / Auditor における情報破壊
- Pipeline が非可逆構造になっている

さらに Phase 3.5 において：

- Validator が Orchestrator 化された
- ValidationResult が Engine Control Signal 化された
- Deterministic Validation が必須化された

ため、Severity の完全非破壊伝播を正式仕様として固定する。

---

### 12.2 ルール定義

一度発生した Severity は Validation Pipeline 内で減衰してはならない。

---

### 12.3 適用範囲

- Validator
- Adapter
- Auditor
- Engine
- Mock
- Integration Test Layer

---

### 12.4 禁止事項

- CRITICAL → ERROR / WARNING / INFO
- ERROR → WARNING / INFO
- WARNING → INFO
- 集約による downgrade
- 型変換時の誤変換
- ValidationResult 再生成によるSeverity消失
- Mock層でのSeverity変換

---

### 12.5 許可事項

- Severity の昇格のみ許可

---

### 12.6 実装指針

- Pass-through を基本とする
- merge時のみ最大Severityを選択
- Adapter は意味変更を行わない
- Auditor は ValidationResult を変更しない
- Engine のみが最終制御判断を行う

---

### 12.7 Phase 3.5 Debug Work Plan 整合性（追記）

以下の仕様と一致しなければならない：

- violation が存在する場合：
  - INFO を生成しない
- CRITICAL は Engine.evaluate() 到達時に停止条件となる
- ERROR は continue 可能
- ValidationResult は merge() 以外で集約禁止

---

### 12.8 設計上の意味

旧:
集約型（情報破壊構造）

新:
伝播型（情報非破壊構造）

Phase 3.5以降：
Validation Pipeline は「制御信号の完全伝播システム」となる。

---

## 13. Severity伝播保証ルール（強化版）

### 13.1 修正前

- 一部層で変換・圧縮が発生
- CRITICAL消失の可能性あり

---

### 13.2 修正後

- 完全な非破壊伝播を保証

---

### 13.3 追加明文化

Severity は以下の役割を持つ：

- 制御信号（Control Signal）
- Engine停止トリガー
- Rollbackトリガー
- Audit重要度決定要素

---

## 14. ERROR挙動仕様（明確化・修正履歴付き）

### 14.1 旧仕様（保持）

- ERRORで例外発生（実装依存）

問題:
- Self-Healing Loop破壊
- 実装不統一

追加問題（Phase 3.5）:
- Partial Execution 不可能
- Validator Orchestrator 原則違反
- Integration Test の決定論性破壊

---

### 14.2 新仕様

CRITICAL:
- 即時停止
- RuntimeError
- Engine.evaluate() 停止
- Rollback Trigger

ERROR:
- continue
- 出力スキップ（Edge未生成）
- ValidationResult は保持
- Self-Healing Loop 継続

WARNING:
- continue
- Audit記録

INFO:
- continue
- violation 非存在時のみ生成可能

---

### 14.3 INFO生成禁止仕様（Phase 3.5追加）

以下を正式仕様として固定する：

```text
violation が1件でも存在する場合：
Validation OK（INFO）は生成しない
```

対象：

* Validator
* Engine
* Mock
* Integration Test

理由：

* Signal Ambiguity 防止
* Engine停止判定の単純化
* Deterministic Validation 保証

---

### 14.4 削除理由（明示）

ERROR例外化は以下の理由で無効化：

* Partial Execution 不可能
* Pipeline停止過剰
* Validation思想違反
* Self-Healing Loop 非互換
* Orchestrator責務違反

---

### 14.5 Engine 制御仕様（追記）

Engine.evaluate() において：

* CRITICAL:

  * 停止
  * Rollback可能
  * Audit必須

* ERROR:

  * continue
  * Edge生成スキップ
  * ValidationResult保持

* WARNING:

  * continue

* INFO:

  * continue
  * violation非存在時のみ許可

---

### 14.6 設計上の意味

旧：
Validation = 例外制御

新：
Validation = Runtime Control Signal

Phase 3.5以降：
Validation は Execution Pipeline の制御層として動作する。

---

## 15. Validation Pipeline 非破壊設計原則（新規追加）

### 15.1 定義

Validation Pipeline は「情報を変換するものではなく、伝播するもの」である。

---

### 15.2 各層の責務

Validator:
- ValidationResult を生成する

Adapter:
- 型変換のみ行う（意味変更禁止）

Auditor:
- 監査ログを生成する（ValidationResult不変）

Engine:
- 最終判断を行う

---

### 15.3 禁止事項

- ValidationResult の再生成
- Severity の変更
- 再評価ロジックの挿入
- 集約ロジックの独自実装

---

## 16. まとめ（Phase 3.4 最終）

本アップデートにより以下が確定：

- Severity Monotonicity Rule 完全適用
- ValidationResult 非破壊伝播
- ERROR挙動の統一
- Pipeline責務分離

---

### 最重要ルール

1. Severityは減衰させるな
2. 集約するな（merge以外禁止）
3. ERRORは停止ではない

---

### 最終状態

- CRITICALは必ずEngineに到達
- Validationは完全トレーサブル
- Self-Healing Loopが安定動作

---

## 17. ソートとScopeの重み付け定義（Phase 3.5対応）【修正・追記】

### 17.1 追加背景

Phase 3.5 において Validator の完全オーケストレーター化が行われた結果、
ValidationResult の最終出力順序が「仕様として決定論的に固定される必要」が発生した。

従来の仕様では以下の問題が存在した：

- scope の優先順位がファイルごとに散発的に定義されていた
- 実装依存で順序が変動する可能性があった
- Integration Test における完全一致検証が不安定
- priority と出力順が混在していた
- rule_id が意味順序として誤用されていた

このため、Scopeの重み付けおよび ValidationResult の整列仕様を
本仕様にて統一的に定義する。

---

### 17.2 Scope 定義（再確認）

Scope は ValidationResult.scope に格納される分類である。

想定値：
- global
- regional
- scene
- character
- entity（将来拡張）
- SYSTEM_INTEGRITY（Phase 3.5追加）

補足：
- SYSTEM_INTEGRITY は Immutability / Structural Integrity 用
- CRITICAL Runtime Integrity Violation に使用する

---

### 17.3 【新ルール】Scope 重み付け順序（決定論仕様）

以下の順序を正式仕様として固定する：

global < regional < scene < character

SYSTEM_INTEGRITY:
- 現時点ではソート未使用
- 意味分類専用

補足：
- 小さいほど優先度が高い（先にソートされる）
- entity は将来拡張用であり、現時点では未使用（後方互換維持のため削除しない）

---

### 17.4 ソートキー定義（確定仕様）【修正】

#### 修正前（保持・仕様外化）

ソートキー：

```text
(scope_weight, severity_weight, code, target_id)
````

問題点：

* 実装依存
* rule_id順序が不安定
* Integration Test 不一致
* Evaluator責務との混在

---

#### 修正後（新仕様・必須）

Validator における最終ソートキーは以下とする：

```text
(severity, code, target_id)
```

補足：

* tests/integration_phase_3_5_world_rules.py に完全準拠
* scope_weight は将来拡張用
* priority は出力順に使用禁止
* rule_id は意味順序を持たない

---

#### 設計理由（追加）

* Validator は Orchestrator であり「意味順序」を持たない
* 出力順は「安定していればよい（Deterministic）」のであり「意味順序」ではない
* rule_id / priority に依存すると責務分離違反となる

---

### 17.5 評価順と出力順の完全分離（強化）

RuleEvaluator:

* priority に基づき評価順を制御

Validator:

* 決定論的整列のみ担当
* 意味順序を持たない

禁止事項：

* priority を出力順に使用
* 評価順を出力順として扱う
* rule_id に意味順序を持たせる

---

### 17.6 Integration Test 整合性（追記）

以下を保証する：

* 入力順が異なっても出力一致
* priority に依存しない
* severity downgrade が存在しない
* ValidationResult の順序が完全決定論

確認対象：

* tests/integration_phase_3_5_world_rules.py
* tests/integration_phase_3_4_validator.py

---

### 17.7 実装指針

- scope_weight はハードコードまたはEnumで定義
- Validator のみが最終ソートを行う
- Evaluator は順序を保証しない（責務分離）

---

### 17.8 設計上の意味

旧：
曖昧順序（実装依存）

新：
完全決定論順序（Spec保証）

Phase 3.5以降：
「ValidationResult は比較可能な証明出力」となる。

---

## 17.9 【新規追加】評価順と出力順の分離（重要設計原則）

### 定義

NWF においては以下を厳密に分離する：

| 概念  | 担当            | 意味             |
| --- | ------------- | -------------- |
| 評価順 | RuleEvaluator | ルール適用の実行順序     |
| 出力順 | Validator     | 結果の整列（決定論保証のみ） |

---

### 仕様

* RuleEvaluator は priority に基づき評価順を制御する
* Validator は評価順を**一切保証しない**
* Validator は**決定論的であることのみを保証する**

---

### 禁止事項（新規明文化）

* priority を出力順に使用すること
* rule_id に意味順序を持たせること
* 評価順を出力順として扱うこと

---

### 設計上の意味

旧：

* 評価順 ≒ 出力順（混在）

新：

* 評価順 ≠ 出力順（完全分離）

---

## 17.10 【新規追加】priorityの扱い明文化

### 仕様

priority は以下の用途のみに使用する：

* RuleEvaluator における評価順制御

---

### 非適用範囲

priority は以下には**一切影響しない**：

* ValidationResult の出力順
* ValidationResult の比較
* Deterministic Execution

---

### 理由

* Validator の責務は「整列」であり「意味付け」ではない
* priority を出力順に使用すると Orchestrator 原則違反となる

---

### テスト整合性

tests/integration_phase_3_5_world_rules.py において：

* 入力順が異なっても出力が一致することを検証
* priority に依存しないことを保証

---

## 18. Phase 3.5 における影響範囲

本変更は以下に影響する：

- consistency_validator.py（最終ソート処理）
- Integration Test（完全一致検証）
- Audit Log（順序安定化）

---

## 19. 後方互換性

- 旧データはそのまま使用可能
- ソート順のみ変更される（意味変更なし）

---

## 20. 最終まとめ（Phase 3.5 反映）【更新】

追加確定事項：

* Validator の出力順は `(severity, code, target_id)` により決定される
* priority は出力順に影響しない
* 評価順と出力順は完全に分離される
* Deterministic Execution は「順序の意味」ではなく「順序の安定性」で定義される

---

### 最重要追加ルール（更新）

1. Scope順序は設計上保持するが、現時点のソートには使用しない
2. ソートはValidatorのみが行う
3. Evaluatorは順序を持つが、Validatorは意味順序を持たない
4. priorityは出力順に影響させてはならない
5. 評価順と出力順を混同するな

---

## 21. 【追記】ValidationResult 比較仕様（__eq__）定義（Integration Test 対応）

### 21.1 追加背景

Phase 3.5 Integration Test において、ValidationResult の比較が決定論的かつ完全一致である必要が生じた。

従来仕様では以下の問題が存在した：

- 比較対象フィールドの明確な定義が存在しない
- timestamp の非決定性によりテストが不安定
- 実装依存で equality 判定が変化する
- Mock と本番実装で比較挙動が異なる

---

### 21.2 新仕様（必須）

ValidationResult の __eq__ 比較は以下のフィールドの完全一致を条件とする：

必須一致フィールド：

- severity
- code
- message
- target_id
- rule_id
- span_id
- trace_id
- source

追加仕様（Phase 3.5）：

- scope
- validation_version

も比較対象として扱うことを推奨する。

ただし後方互換性維持のため、
必須要件とはしない。

---

### 21.3 timestamp の扱い（重要）

#### 修正前（旧仕様・保持）

- timestamp を完全一致比較対象とする（実装依存）

問題：
- 実行ごとに値が変動
- Integration Test 不安定化
- Runtime依存差異発生

---

#### 修正後（新仕様）

- timestamp は比較対象外
- または「存在確認のみ」を行う

追加仕様：

```text
timestamp の論理意味は
「発生時刻記録」であり
「ValidationResult の論理同一性」ではない
```

---

### 21.4 Integration Test 特例（追記）

以下を固定化する：

```text
transaction_id = "test-fixed-tx"
```

理由：

* span_id 再現性
* trace 一致性
* Audit deterministic replay

---

### 21.5 理由

* Deterministic Test 保証
* Runtime依存値排除
* Equality の意味を論理一致へ限定
* ValidationResult を証明可能出力へ昇格

---

### 21.6 設計上の意味

旧：
物理的同一性比較（非安定）

新：
論理的同一性比較（完全決定論）

Phase 3.5以降：
ValidationResult は「再現可能な監査証跡」として扱う。

---

## 22. 【追記】span_id 決定論的生成アルゴリズム

### 22.1 追加背景

Traceability 強化および Integration Test の完全一致検証のため、
span_id の生成方法を仕様として固定する必要がある。

従来仕様では：

- 実装依存
- 一意性のみ保証
- 決定論性なし

さらに Phase 3.5 において：

- ValidationResult equality
- Audit replay
- Deterministic Execution

が正式要求となった。

---

### 22.2 新仕様（必須）

span_id は以下の入力を用いたハッシュで決定論的に生成する：

```text
span_id = hash(
rule_id +
action_index +
target_id +
transaction_id
)
```

---

### 22.3 各要素定義

* rule_id:
  ルール識別子

* action_index:
  同一ルール内での action 順序（0-based）

* target_id:
  対象エンティティID（必ず str）

* transaction_id:
  WorkflowContext から取得

---

### 22.4 ハッシュ仕様

* 使用関数：
  SHA-256 または同等の決定論的ハッシュ

* 出力：
  hex string

* エンコード：
  UTF-8

---

### 22.5 Entity ID 正規化仕様との同期（Phase 3.5追加）

span_id の決定論性を保証するため：

```text
target_id は必ず str に正規化する
```

これは以下仕様と同期する：

* docs/spec/Core_Spec/NWF_Entity_ID_System_v2.0.1.md
* docs/spec/Core_Spec/NWF_Story_Database_v2.0.1.md

また：

* UUID object を外部I/Fへ露出してはならない
* story_db.get() は str を受け取る

---

### 22.6 テスト環境における特例（重要）

transaction_id を含めることでテストごとに値が変化するため：

```text
transaction_id = "test-fixed-tx"
```

を Integration Test で固定する。

---

### 22.7 修正前仕様（保持）

* span_id 生成方法未定義
* 実装依存

理由：

* 後方互換性
* Audit比較用途

ただし現仕様では使用禁止。

---

### 22.8 設計上の意味

旧：
非決定論ID（追跡のみ）

新：
決定論ID（比較可能・再現可能）

Phase 3.5以降：
span_id は Trace / Audit / Equality の統合基盤となる。

---

## 23. 【追記】Deterministic Validation Guarantee（強化）

### 23.1 定義

同一入力に対して ValidationResult は以下を満たす：

- 完全一致
- 順序一致
- span_id 一致

---

### 23.2 比較精度（浮動小数点）

内部比較は以下を採用：

```

abs(a - b) < 1e-9

```

---

### 23.3 禁止事項

- ランダム値の使用
- 実行時依存値の混入
- 非決定的順序処理

---

### 23.4 設計上の意味

Validation System は：

「検証システム」から  
「再現可能な証明システム」へ進化する

---

## 24. 最終まとめ（Phase 3.5 + Integration Test 完全対応）

本追記により以下が確定：

- ValidationResult の比較仕様完全定義
- span_id の決定論的生成
- テスト環境の完全再現性
- Traceability と Determinism の統合

---

### 最重要追加ルール（統合版）

1. ValidationResult は論理一致で比較せよ
2. span_id は必ず決定論生成せよ
3. timestamp は比較するな
4. transaction_id はテスト時固定せよ

---

### 最終状態

- Validation は完全再現可能
- Integration Test は100%一致
- Trace / Audit / Test が統一基盤で動作

---

[EOF]