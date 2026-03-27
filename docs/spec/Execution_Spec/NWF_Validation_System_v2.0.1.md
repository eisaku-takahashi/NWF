Source: docs/spec/Execution_Spec/NWF_Validation_System_v2.0.1.md
Updated: 2026-03-28T00:09:00+09:00
PIC: Engineer / ChatGPT

# NWF Validation System v2.0.1

---

## 1. 概要

NWF Validation System は、NWF v2.0.1（Story OS）における品質保証（Quality Assurance）および論理整合性検証（Logical Integrity Verification）を統治するシステムである。本システムは単なるエラーチェック機構ではなく、「Validation-Driven Generation（検証駆動型生成）」という設計思想の中核を担う。

Story OS においては、すべての Engine 出力、Data 生成、Timeline 生成、Event 生成、Simulation 結果、Narrative 生成は、必ず Validation を通過しなければならない。Validation System は WorldRule、Causality、Timeline、State、Emotion、Narrative の整合性を多層的に検証し、Analysis Engine および Error Model と連携して自己修復ループを構成する。

Validation に失敗した場合、Execution Pipeline は Error Model を通じて Rollback および Recalculation を実行し、再度 Validation を実施する。このループにより Story OS の論理性、整合性、物語品質を維持する。

---

## 2. Validation Layer Architecture

Validation System は以下の 5 層 Validation 構造を持つ。

### 2.1 Level 1: Schema Validation
データ形式、型、必須フィールド、JSON 構造の正当性を検証する。  
Data Layer における最下層 Validation であり、すべての Data Object は Schema Validation を通過しなければならない。

検証対象:
- JSON 構造
- データ型
- 必須フィールド
- 値範囲
- Enum 値
- フィールド単位整合性

---

### 2.2 Level 2: Reference Validation
ID 参照、依存関係、リンク関係、外部参照の整合性を検証する。

検証対象:
- character_id の存在確認
- event_id の参照整合性
- timeline_id の存在確認
- dependency_graph の循環参照チェック
- relation / link の整合性

Data Layer と Query Layer の整合性を保証する。

---

### 2.3 Level 3: Engine Logic Validation
各 Engine が実行した演算結果の正当性を検証する。  
これは各 Engine が実施する Self-Validation に相当する。

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
- Temporal Validation（時間矛盾）
- Causal Validation（因果矛盾）
- State Validation（属性矛盾）
- Emotional Validation（感情曲線矛盾）
- Physics / WorldRule 違反
- Event Dependency 不整合

---

### 2.4 Level 4: Cross Engine Validation
複数 Engine 間の整合性を検証する。  
この Validation は主に Analysis Engine が担当する。

検証例:
- Timeline と Event の整合性
- Event と Causality の整合性
- Simulation と State の整合性
- Emotion と Narrative の整合性
- WorldRule と Event の整合性
- Character State と Timeline の整合性

Cross Engine Validation により、単一 Engine では検出できない論理矛盾を検出する。

---

### 2.5 Level 5: Narrative Integrity Validation
Story 全体の整合性、テーマ整合性、感情曲線、物語構造の完成度を検証する。  
これは Validation System の最上位層であり、Analysis Engine が Integrity Score を算出する。

検証対象:
- Narrative Arc
- Emotional Curve
- Character Development
- Theme Consistency
- Plot Consistency
- Narrative Closure
- Logical Consistency
- World Consistency

---

## 3. Engine-Level Validation Responsibilities

各 Engine は Self-Validation を実施する責任を持つ。

### 3.1 Timeline Engine
- Temporal Order Validation
- Time Overlap Validation
- Timeline Gap Detection
- Event Timestamp Consistency

### 3.2 Event Engine
- Event Dependency Validation
- Event Preconditions Validation
- Event Outcome Consistency
- Event Reference Validation

### 3.3 Simulation Engine
- State Transition Validation
- Physics / WorldRule Validation
- Resource Consistency
- Probability Consistency

### 3.4 State Engine
- Character State Validation
- Object State Validation
- Attribute Range Validation
- State Dependency Validation

### 3.5 Emotion Engine
- Emotional Curve Validation
- Emotion Transition Validation
- Emotional Intensity Range Validation
- Emotional Continuity Validation

### 3.6 Narrative Engine
- Plot Structure Validation
- Narrative Flow Validation
- Character Arc Validation
- Theme Consistency Validation

---

## 4. Analysis Engine Integration

Analysis Engine は Validation System の Cross-Validation および Integrity Evaluation を担当する中核 Engine である。

Analysis Engine の役割:
- Cross Engine Validation 実行
- Integrity Score 算出
- Consistency Score 算出
- Validation Result Aggregation
- Error Detection
- Recalculation Trigger 判定
- Narrative Integrity Evaluation

Integrity Score は 0.0 から 1.0 の範囲で算出される。

Integrity Score の例:
- 0.90 - 1.00 : Perfect Integrity
- 0.75 - 0.89 : Acceptable
- 0.50 - 0.74 : Warning
- 0.00 - 0.49 : Validation Failure

Integrity Score が Threshold 未満の場合、Error Model が起動する。

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

特に Narrative Engine 実行前に Final Integrity Gate を通過する必要がある。

Validation Gate を通過できない場合:
- Execution Stop
- Error Model Trigger
- Rollback
- Recalculation
- Re-Validation

---

## 6. Validation → Error Model Flow

Validation Fail が発生した場合、以下のフローが実行される。

Validation Flow:
1. Validation Execution
2. Validation Failure Detection
3. Error Model Trigger
4. Error Classification
5. Analysis Engine Feedback
6. Rollback
7. Recalculation
8. Re-Validation
9. Integrity Score Recalculation
10. Execution Resume

このループを Self-Healing Loop と呼ぶ。

Self-Healing Loop:
Validation → Error Detection → Analysis → Rollback → Recalculation → Validation

---

## 7. Data Model & Fields

Validation System は Data_Spec v2.0.1 の Data Model に以下のフィールドを追加する。

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

validation_status:
- valid
- warning
- invalid
- pending

integrity_score_unit: 0.0_to_1.0

Validation Log は Execution Log に統合され、Query Engine から追跡可能とする。

---

## 8. Logging & Traceability

Validation System はすべての Validation 結果を Validation Log として保存する。

Validation Log に含まれる情報:
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

Execution Log と Validation Log は統合され、Execution Trace を完全追跡可能とする。

---

## 9. Maintenance & Versioning

Validation System は Story OS の品質保証層であり、全 Engine、Data Model、Execution Pipeline の変更に合わせて更新される必要がある。

Versioning ルール:
- Engine 仕様変更時は Validation Rule を更新
- Data Model 変更時は Schema Validation 更新
- Execution Pipeline 変更時は Validation Gate 更新
- Integrity Score Algorithm 更新時は Version Increment
- Validation Rule は Version 管理される

Validation System は Story OS の品質、整合性、論理性を保証する中核システムである。

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
- Story Integrity Assurance

本システムにより Story OS は自己修復能力を持つ論理生成システムとして動作し、物語の整合性と品質を自律的に維持する。

---

[EOF]