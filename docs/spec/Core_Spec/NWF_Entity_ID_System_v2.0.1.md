Source: docs/spec/Core_Spec/NWF_Entity_ID_System_v2.0.1.md
Updated: 2026-05-11T15:23:00+09:00
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

### 3.3 Entity ID Normalization Rule（追加仕様）

Phase 3.5 Validation Integrity 修正に伴い、
Entity ID の型揺れ防止仕様を正式定義する。

#### 基本原則

- Entity ID は外部I/Fでは常に `str` として扱う
- Validator / StoryDB / Engine / Audit / Transaction Pipeline は
  すべて `str` ID を使用する
- UUID オブジェクトを直接比較・保持・公開してはならない
- UUID を利用する場合も、I/F境界では `str(UUID)` に正規化する

---

#### 修正前仕様（保持）

従来仕様では：

- UUID v4 を使用する

のみが定義されており、

- Python UUID object を許可するのか
- I/F上の型を `UUID` と `str` のどちらに統一するのか

が未定義であった。

このため：

- UUID / str 混在
- dict key 不一致
- StoryDB lookup failure
- Validator immutability false negative

などが発生しうる構造であった。

---

#### 修正後仕様（正式採用）

すべての Entity ID / System ID は：

- 保存時
- 比較時
- DBアクセス時
- Validation時
- Audit時
- Engine連携時

において `str` に正規化しなければならない。

必須実装例：

target_id = str(entity.id)

StoryDB I/F：

get(entity_id: str) -> Optional[Entity]

UUID比較例：

str(previous.uuid) != str(current.uuid)

---

#### UUID Object カプセル化原則（追加仕様）

UUID object は内部実装詳細としてのみ許可される。

許可される場所：

- ID生成直後
- UUID生成ユーティリティ内部
- ORM内部
- DB Driver内部

禁止事項：

- UUID object の外部返却
- UUID object のAPI公開
- UUID object の比較I/F使用
- UUID object をdict keyとして共有
- UUID object をValidation境界へ渡すこと

理由：

- Python runtime 差異防止
- JSON serialization 安定化
- StoryDB I/F 安定化
- Mock / Production 一貫性維持
- Validation deterministic behavior 保証
- Recursive Integrity 安定化

---

#### Cross-Spec Synchronization

本仕様は以下と同期しなければならない：

- docs/spec/Core_Spec/NWF_Story_Database_v2.0.1.md
- docs/spec/Execution_Spec/NWF_Consistency_Validator_Spec_v2.0.1_Phase_3.5.md
- docs/spec/Execution_Spec/NWF_Validation_System_v2.0.1.md
- docs/spec/Execution_Spec/NWF_Mock_Design_Guideline_v2.0.1.md
- docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md

---

#### Phase 3.5 DoD

本仕様追加により：

- ID型揺れが排除される
- StoryDB I/F が安定化される
- Mock / Production 差異が排除される
- Validation immutability 判定が deterministic 化される
- UUID比較失敗による false negative が排除される

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

---

### Story Entity ID

Story単位で一意

同一Story Database 内では  
同じIDを持つEntityは存在してはならない。

別Storyでは同じIDを使用可能。

---

追加仕様（Phase 3.5）：

Story Entity ID は
I/F上では必ず `str` として扱う。

許可例：

"char_001"
"scene_010"

禁止例：

UUID("550e8400-e29b-41d4-a716-446655440000")

理由：

- StoryDB lookup 安定化
- Validation deterministic behavior 維持
- Engine I/F 統一
- Mock / Production 差異防止

---

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

修正前仕様（保持）：

「UUID を使用する」とのみ定義されていた。

---

修正後仕様（正式採用）：

UUIDを利用する場合でも、
外部I/Fでは必ず `str(UUID)` に正規化する。

例：

transaction_id: str

許可：

"550e8400-e29b-41d4-a716-446655440000"

非推奨：

UUID("550e8400-e29b-41d4-a716-446655440000")

禁止：

- UUID object のI/F公開
- UUID object の永続比較
- UUID object のValidation入力

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

### Phase 3.5 Immutability Synchronization（追加仕様）

本仕様は
Phase 3.5 Consistency Validator の
Immutability Check と同期する。

同期対象：

- docs/spec/Execution_Spec/NWF_Consistency_Validator_Spec_v2.0.1_Phase_3.5.md
- src/integrity/consistency_validator.py

Validator は：

- ID を `str` に正規化した上で
- previous entity を StoryDB から取得し
- UUID比較を行う

必須原則：

- ID型揺れを許可しない
- UUID object をI/F境界へ露出しない
- Stable ID Principle を Validation Layer でも保証する

---

削除しなかった理由：

旧仕様の

「IDは変更してはならない」

という原則自体は現在も有効であり、
Phase 3.5 ではその原則を
Validation Pipeline にまで拡張・厳格化した。

そのため旧仕様は削除せず、
Immutability Enforcement 仕様として補強する。

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