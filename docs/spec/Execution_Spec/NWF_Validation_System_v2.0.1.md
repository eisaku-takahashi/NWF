Source: docs/spec/Execution_Spec/NWF_Validation_System_v2.0.1.md
Updated: 2026-04-22T11:53:00+09:00
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

---

## 12. Severity Monotonicity Rule（Validation System適用・新規追加）

### 12.1 追加理由

Error Model 側で導入された Monotonicity Rule を Validation System にも適用する必要があるため。

また、Phase 3.4 において以下の問題が確認された：

- CRITICAL が途中で消失する
- Adapter / Auditor における情報破壊
- Pipeline が非可逆構造になっている

---

### 12.2 ルール定義

一度発生した Severity は Validation Pipeline 内で減衰してはならない。

---

### 12.3 適用範囲

- Validator
- Adapter
- Auditor
- Engine

---

### 12.4 禁止事項

- CRITICAL → ERROR / WARNING / INFO
- ERROR → WARNING / INFO
- WARNING → INFO
- 集約による downgrade
- 型変換時の誤変換

---

### 12.5 許可事項

- Severity の昇格のみ許可

---

### 12.6 実装指針

- Pass-through を基本とする
- merge時のみ最大Severityを選択

---

### 12.7 設計上の意味

旧:
集約型（情報破壊構造）

新:
伝播型（情報非破壊構造）

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

---

### 14.2 新仕様

CRITICAL:
- 即時停止
- RuntimeError

ERROR:
- continue
- 出力スキップ（Edge未生成）

---

### 14.3 削除理由（明示）

ERROR例外化は以下の理由で無効化：

- Partial Execution 不可能
- Pipeline停止過剰
- Validation思想違反

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

[EOF]