Source: docs/spec/Core_Spec/NWF_Entity_ID_System_v2.0.1.md
Updated: 2026-03-21T15:42:00+09:00
PIC: Engineer / ChatGPT

# NWF Entity ID System v2.0.1

---

## 1. 概要

本ドキュメントは  
Novel Writing Framework（NWF）における  
Entity ID システムを定義する。

NWFではすべてのストーリー要素は  
一意の ID によって識別される。

本仕様は NWF Data Model、Engine、Execution の  
すべての参照関係の基盤仕様となる。

目的：

- Entity識別の一意性確保
- Entity間参照の安定化
- データベース構造の明確化
- Engine処理の効率化
- 階層構造の明確化
- 循環参照の防止

---

## 2. ID System Overview

NWFでは以下のEntityが  
IDによって識別される。

Entity一覧：

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

すべてのEntityは一意のIDを持つ。

---

## 3. ID Naming Structure

NWF ID は以下の構造を持つ。

entity_prefix + "_" + number

例：

char_001  
thread_001  
scene_010  
event_005  
beat_003  

番号は3桁以上の連番とする。

---

## 4. Entity Prefix List

各Entityは専用のPrefixを持つ。

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

---

## 5. ID Uniqueness Scope

IDの一意性スコープは  
**Story単位で一意** とする。

つまり、同一Story Database 内では  
同じIDを持つEntityは存在してはならない。

別Storyでは同じIDを使用可能。

例：

Story A  
char_001

Story B  
char_001

これは許可される。

---

## 6. ID Generation Authority

ID生成の責任主体を以下のように定義する。

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

IDは各Engineが生成し、  
人間が手動でIDを変更してはならない。

IDは一度生成されたら変更してはならない。

---

## 7. Hierarchical ID Rules

NWF の階層構造：

Scene > Event > Beat

親子関係は parent_id によって管理する。

### Scene

Scene は Thread に属する構造単位。

Scene は複数Threadに属することができる。

Scene は parent_id を持たない（最上位イベント単位）。

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

NWFでは循環参照を防ぐため、  
**片方向参照原則** を採用する。

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

これにより循環参照を防止する。

---

## 9. Stable ID Principle

IDは一度作成されたら変更してはならない。

理由：

- Git履歴安定
- Engine参照保持
- データ整合性維持
- AI処理の安定化

ID変更が必要な場合は  
新しいEntityを作成する。

---

## 10. Human Readable Design

NWF IDは  
人間が読める形式で設計されている。

例：

char_001  
thread_003  
scene_010  
event_004  

PrefixによりEntity種類が判別できる。

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

Beat

beat_id = beat_002  
parent_event_id = event_003

---

## 12. Extensibility

将来以下のEntityが追加可能：

- Location
- Item
- Organization
- Technology
- Document
- Memory

追加する場合は  
同じ命名規則で Prefix を定義する。

例：

location_  
item_  
org_  

---

## 13. まとめ

NWF Entity ID System は  
NWFのすべてのストーリー要素を  
一意に識別する仕組みである。

本仕様では以下を定義した：

- 全EntityのID Prefix
- Story単位のID一意性
- ID生成責任Engine
- Scene > Event > Beat 階層IDルール
- parent_id による階層管理
- 片方向参照原則
- Stable ID Principle

この仕様は  
NWF Data Model と Engine Architecture の  
基盤仕様として使用される。

---

[EOF]