Source: docs/spec/Core_Spec/NWF_Entity_ID_System_v2.0.1.md
Updated: 2026-04-04T03:07:00+09:00
PIC: Engineer / ChatGPT

# NWF Entity ID System v2.0.1

---

## 1. 概要

本ドキュメントは Novel Writing Framework（NWF）における Entity ID システムを定義する。

NWFではすべてのストーリー要素、イベント、トランザクション、監査イベントは一意のIDによって識別される。

本仕様は以下のシステムの基盤仕様となる。

- Data Model
- Engine
- Execution Pipeline
- Event Manager
- Data State Machine
- Kernel Audit System

目的：

- Entity識別の一意性確保
- Entity間参照の安定化
- データベース構造の明確化
- Engine処理の効率化
- 階層構造の明確化
- 循環参照の防止
- Transaction / Event / Audit のトレーサビリティ確保
- Kernel Audit System とのID整合性確保

---

## 2. ID System Overview

NWFでは以下のEntityが ID によって識別される。

### Story Entities

- World
- WorldRule
- Character
- Thread
- Scene
- Event
- Beat
- State
- Relationship
- Timeline

### System Entities

- Execution
- Transaction
- Audit Event
- Prompt
- Validation
- Analysis
- Engine Run
- State Transition

すべてのEntityは一意のIDを持つ。

---

## 3. ID Naming Structure

IDは用途により以下の2種類に分類される。

### 3.1 Human Readable Sequential ID

Story Entity 用 ID

構造：

entity_prefix + "_" + number

例：

char_001  
thread_001  
scene_010  
event_005  
beat_003  

番号は3桁以上の連番とする。

### 3.2 System UUID ID

System Entity 用 ID

対象：

- transaction_id
- execution_id
- audit_event_id
- prompt_id
- validation_id
- analysis_id
- state_transition_id
- engine_run_id

これらは **UUID v4** を使用する。

例：

550e8400-e29b-41d4-a716-446655440000

System レベルのIDは全システムで一意でなければならない。

---

## 4. Entity Prefix List

各Entityは専用のPrefixを持つ。

### Story Entities Prefix

World  
world_

WorldRule  
world_rule_

Character  
char_

Thread  
thread_

Scene  
scene_

Event  
event_

Beat  
beat_

State  
state_

Relationship  
rel_

Timeline  
timeline_

### System Entities Prefix（Human Readable IDが必要な場合）

Execution  
exec_

Transaction  
tx_

Audit Event  
audit_

Prompt  
prompt_

Validation  
val_

Analysis  
analysis_

Engine Run  
engine_

State Transition  
st_

---

## 5. ID Uniqueness Scope

IDの一意性スコープは以下のように定義する。

### Story Entity ID

Story単位で一意

同一Story Database 内では  
同じIDを持つEntityは存在してはならない。

別Storyでは同じIDを使用可能。

### System Entity ID

System 全体で一意（UUID）

対象：

- transaction_id
- execution_id
- audit_event_id
- prompt_id
- state_transition_id

これらはシステム全体で重複してはならない。

---

## 6. ID Generation Authority

ID生成の責任主体を以下のように定義する。

### Story Entities

World / WorldRule  
→ World Engine

Character / Relationship  
→ Character Engine

Thread  
→ Thread Engine

Scene / Event / Beat / Timeline  
→ Scene Engine

State  
→ State Engine

### System Entities

Execution ID  
→ Execution Manager

Transaction ID  
→ Kernel Transaction Manager

Audit Event ID  
→ Kernel Audit Logger

Prompt ID  
→ Prompt Manager

Validation ID  
→ Validation Engine

Analysis ID  
→ Analysis Engine

State Transition ID  
→ Data State Machine

Engine Run ID  
→ Engine Controller

IDは各システムコンポーネントが生成し、  
人間が手動でIDを変更してはならない。

IDは一度生成されたら変更してはならない。

---

## 7. Hierarchical ID Rules

NWF の階層構造：

Scene > Event > Beat

親子関係は parent_id によって管理する。

### Scene

Scene は Thread に属する構造単位。  
Scene は parent_id を持たない。

### Event

Event は Scene に属する。  
Event は必ず parent_scene_id を持つ。

例：

event_003  
parent_scene_id = scene_010

### Beat

Beat は Event に属する。  
Beat は必ず parent_event_id を持つ。

例：

beat_002  
parent_event_id = event_003

---

## 8. Reference Rules（参照ルール）

NWFでは循環参照を防ぐため、片方向参照原則を採用する。

原則：

- 子は親IDを参照する
- 親は子IDを直接保持しない
- 集合はEngineが生成する

参照方向：

Beat → Event → Scene → Thread  
Event → Character  
Scene → Character  
Thread → Character  
Scene → WorldRule  
Event → State Transition  
Transaction → Entity  
Audit Event → Transaction  
Prompt → Execution  
Execution → Event  

これにより循環参照を防止する。

---

## 9. Stable ID Principle

IDは一度作成されたら変更してはならない。

理由：

- Git履歴安定
- Engine参照保持
- データ整合性維持
- AI処理の安定化
- Audit Log の因果関係維持
- Transaction Traceability 維持

ID変更が必要な場合は  
新しいEntityを作成する。

---

## 10. Audit / Transaction / Execution ID Relationship

Kernel Audit System 導入により、以下のID関係を定義する。

ID関係構造：

audit_event_id  
    → transaction_id  
        → execution_id  
            → event_id  
                → entity_id  

このIDチェーンにより以下が可能になる：

- 誰が
- いつ
- 何を実行し
- どのイベントが発生し
- どのEntityが変更されたか

を完全に追跡できる。

これを **Traceability Chain** と呼ぶ。

---

## 11. JSON Representation Example

例：

Character

character_id = char_001

Scene

scene_id = scene_010  
participants = char_001, char_002

Event

event_id = event_003  
parent_scene_id = scene_010

Transaction

transaction_id = UUID

Audit Event

audit_event_id = UUID  
transaction_id = UUID  
actor = system  
action = create_event  
target_id = event_003

---

## 12. Extensibility

将来以下のEntityが追加可能：

- Location
- Item
- Organization
- Technology
- Document
- Memory
- Knowledge
- Emotion
- Goal
- Conflict

追加する場合は同じ命名規則で Prefix を定義する。

例：

location_  
item_  
org_  
doc_  
memory_  

---

## 13. まとめ

NWF Entity ID System は NWF のすべてのストーリー要素および  
システムイベント、トランザクション、監査ログを一意に識別する仕組みである。

本仕様では以下を定義した：

- Story Entity ID ルール
- System Entity UUID ルール
- 全EntityのID Prefix
- Story単位のID一意性
- System全体のUUID一意性
- ID生成責任コンポーネント
- Scene > Event > Beat 階層IDルール
- parent_id による階層管理
- 片方向参照原則
- Stable ID Principle
- Audit / Transaction / Execution Traceability Chain

この仕様は NWF Data Model、Engine Architecture、Kernel Audit System の  
基盤仕様として使用される。

---

[EOF]