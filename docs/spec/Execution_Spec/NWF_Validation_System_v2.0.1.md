Source: docs/spec/Execution_Spec/NWF_Validation_System_v2.0.1.md
Updated: 2026-04-04T02:12:00+09:00
PIC: Engineer / ChatGPT

# NWF Validation System v2.0.1

---

## 1. 概要

NWF Validation System は、NWF v2.0.1（Story OS）における品質保証（Quality Assurance）および論理整合性検証（Logical Integrity Verification）を統治するシステムである。本システムは単なるエラーチェック機構ではなく、「Validation-Driven Generation（検証駆動型生成）」という設計思想の中核を担う。

Story OS においては、すべての Engine 出力、Data 生成、Timeline 生成、Event 生成、Simulation 結果、Narrative 生成は、必ず Validation を通過しなければならない。Validation System は WorldRule、Causality、Timeline、State、Emotion、Narrative の整合性を多層的に検証し、Analysis Engine および Error Model と連携して自己修復ループを構成する。

また本バージョンでは **NWF Kernel Audit System と統合** され、Validation Failure、Warning、Integrity Score、Rollback などのすべての重要イベントは **監査ログ（Audit Log）に記録される**。これにより Validation System は品質保証システムであると同時に、システムの説明責任（Accountability）を担保する証拠生成システムとして機能する。

---

## 2. Validation Layer Architecture

Validation System は以下の 5 層 Validation 構造を持つ。

### 2.1 Level 1: Schema Validation
データ形式、型、必須フィールド、JSON 構造の正当性を検証する。

検証対象:
- JSON 構造
- データ型
- 必須フィールド
- 値範囲
- Enum 値
- フィールド単位整合性

Schema Validation Failure は **VALIDATION_ERROR イベント** として Audit Logger に送信される。

---

### 2.2 Level 2: Reference Validation
ID 参照、依存関係、リンク関係、外部参照の整合性を検証する。

検証対象:
- character_id の存在確認
- event_id の参照整合性
- timeline_id の存在確認
- dependency_graph の循環参照チェック
- relation / link の整合性

Reference Validation Failure は **REFERENCE_ERROR イベント** として監査ログへ記録される。

---

### 2.3 Level 3: Engine Logic Validation
各 Engine が実行した演算結果の正当性を検証する。

対象 Engine:
- Timeline Engine
- Event Engine
- Simulation Engine
- State Engine
- Emotion Engine
- Narrative Engine
- WorldRule Engine
- Causality Engine

検証例:
- Temporal Validation
- Causal Validation
- State Validation
- Emotional Validation
- Physics / WorldRule 違反
- Event Dependency 不整合

Engine Logic Failure は **ENGINE_VALIDATION_ERROR イベント** として記録される。

---

### 2.4 Level 4: Cross Engine Validation
複数 Engine 間の整合性を検証する。Analysis Engine が担当する。

検証例:
- Timeline と Event の整合性
- Event と Causality の整合性
- Simulation と State の整合性
- Emotion と Narrative の整合性
- WorldRule と Event の整合性
- Character State と Timeline の整合性

Cross Engine Validation Failure は **CROSS_ENGINE_VALIDATION_ERROR** として記録される。

---

### 2.5 Level 5: Narrative Integrity Validation
Story 全体の整合性、テーマ整合性、感情曲線、物語構造の完成度を検証する。

検証対象:
- Narrative Arc
- Emotional Curve
- Character Development
- Theme Consistency
- Plot Consistency
- Narrative Closure
- Logical Consistency
- World Consistency

Integrity Score は監査ログに記録され、Story Generation の品質証拠として保存される。

---

## 3. Audit Logging Integration（重要）

Validation System は NWF Kernel Audit System と完全統合される。

### 3.1 Audit Logging 必須イベント

Validation System は以下のイベントを必ず Audit Logger に送信する。

- VALIDATION_START
- VALIDATION_SUCCESS
- VALIDATION_WARNING
- VALIDATION_ERROR
- INTEGRITY_SCORE_CALCULATED
- ROLLBACK_TRIGGERED
- RECALCULATION_TRIGGERED
- VALIDATION_RETRY
- VALIDATION_FINAL_FAILURE

### 3.2 Audit Log に記録する情報

Validation Audit Log Fields:
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

Validation Failure は単なるエラーではなく、**監査対象イベント**として必ず記録される。

---

## 4. Engine-Level Validation Responsibilities

各 Engine は Self-Validation を実施する責任を持つ。

### 4.1 Timeline Engine
- Temporal Order Validation
- Time Overlap Validation
- Timeline Gap Detection
- Event Timestamp Consistency

### 4.2 Event Engine
- Event Dependency Validation
- Event Preconditions Validation
- Event Outcome Consistency
- Event Reference Validation

### 4.3 Simulation Engine
- State Transition Validation
- Physics / WorldRule Validation
- Resource Consistency
- Probability Consistency

### 4.4 State Engine
- Character State Validation
- Object State Validation
- Attribute Range Validation
- State Dependency Validation

### 4.5 Emotion Engine
- Emotional Curve Validation
- Emotion Transition Validation
- Emotional Intensity Range Validation
- Emotional Continuity Validation

### 4.6 Narrative Engine
- Plot Structure Validation
- Narrative Flow Validation
- Character Arc Validation
- Theme Consistency Validation

---

## 5. Validation Gates in Execution Pipeline

Execution Pipeline の各フェーズ間に Validation Gate を設置する。

Validation Gates:
1. Plan Validation Gate
2. Structure Validation Gate
3. Timeline Validation Gate
4. Event Validation Gate
5. Simulation Validation Gate
6. Emotion Validation Gate
7. Integrity Validation Gate
8. Narrative Validation Gate
9. Save Validation Gate

各 Validation Gate の通過・失敗は **Audit Log に記録される**。

Validation Gate Failure:
- Execution Stop
- Error Model Trigger
- Rollback
- Recalculation
- Re-Validation
- Audit Log Record

---

## 6. Validation → Error Model Flow

Validation Fail が発生した場合、以下のフローが実行される。

Validation Flow:
1. Validation Execution
2. Validation Failure Detection
3. Audit Log Record
4. Error Model Trigger
5. Error Classification
6. Analysis Engine Feedback
7. Rollback
8. Recalculation
9. Re-Validation
10. Integrity Score Recalculation
11. Execution Resume

Self-Healing Loop:
Validation → Error Detection → Audit Log → Analysis → Rollback → Recalculation → Validation

---

## 7. Data Model & Fields

Validation System は Data Model に以下のフィールドを追加する。

Validation Fields:
- validation_status
- integrity_score
- consistency_score
- validation_log
- validation_timestamp
- validated_by_engine
- validation_version
- validation_level
- validation_errors
- validation_warnings
- last_validation_transaction_id

validation_status:
- valid
- warning
- invalid
- pending

integrity_score_unit: 0.0_to_1.0

last_validation_transaction_id は Audit Log の transaction_id と一致する必要がある。

---

## 8. Logging & Traceability

Validation System はすべての Validation 結果を Validation Log として保存する。

Validation Log:
- validation_id
- object_id
- engine_name
- validation_level
- validation_result
- integrity_score
- error_code
- error_message
- timestamp
- dependency_objects
- recalculation_flag
- transaction_id

Execution Log、Validation Log、Audit Log は統合され、
**Execution Trace / Validation Trace / Audit Trace** を完全追跡可能とする。

---

## 9. Maintenance & Versioning

Versioning ルール:
- Engine 仕様変更時は Validation Rule 更新
- Data Model 変更時は Schema Validation 更新
- Execution Pipeline 変更時は Validation Gate 更新
- Integrity Score Algorithm 更新時は Version Increment
- Audit Event 変更時は Validation System 更新

Validation System は Story OS の品質、整合性、論理性、説明責任を保証する中核システムである。

---

## 10. まとめ

NWF Validation System v2.0.1 は Story OS における品質保証および論理整合性維持のための多層検証システムである。

Validation System の主要概念:
- Validation Driven Generation
- 5 Layer Validation Architecture
- Engine Self Validation
- Analysis Engine Cross Validation
- Integrity Score Decision System
- Validation Gates in Execution Pipeline
- Validation → Error Model → Rollback → Recalculation Loop
- Logging & Traceability
- Audit Logging Integration
- Story Integrity Assurance
- Accountability & Traceability

本システムにより Story OS は自己修復能力を持つ論理生成システムであると同時に、すべての判断・失敗・修正履歴を証拠として保存する監査対応システムとして動作する。

---

[EOF]