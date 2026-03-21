Source: docs/spec/Core_Spec/NWF_Story_Database_v2.0.1.md
Updated: 2026-03-21T18:47:00+09:00
PIC: Engineer / ChatGPT

# NWF Story Database v2.0.1

---

## 1. v2.0.0 の構造的問題点の特定

NWF_Story_Database_v2.0.0 には以下の構造的問題が存在していた。

### 1.1 Entity不足

v2.0.0 では以下のEntityがデータベース管理対象に含まれていなかった。

World  
Beat  
State  
Relationship  

これにより Data Model v2.0.1 と整合していなかった。

### 1.2 多対多関係の管理構造が存在しない

Character ↔ Scene  
Character ↔ Event  
Thread ↔ Scene  
Character ↔ Character  
Event ↔ State  

などの多対多関係を管理する仕組みが存在しなかった。

### 1.3 Graph構造非対応

Story Database v2.0.0 は単純なコレクション構造であり、
Graph構造（Entity + Relationship Edge）を表現できなかった。

これらの問題を解決するため、
v2.0.1 では Document-Graph Hybrid Database を採用する。

---

## 2. 新・物理ディレクトリ構造案

Story Database は以下の物理ディレクトリ構造で管理する。

story_database/
  worlds/
  world_rules/
  characters/
  states/
  relationships/
  threads/
  scenes/
  events/
  beats/
  timelines/
  links/

### 2.1 Entity Document 保存方針

各Entityは独立したJSONファイルとして保存する。

例：

story_database/characters/char_001.json  
story_database/scenes/scene_010.json  
story_database/events/event_003.json  

これにより Git による差分管理を容易にする。

---

## 3. Link Table (Edge Collection) の詳細設計

links ディレクトリでは Entity 間の関係を Edge として管理する。

主な Link Collection：

char_at_scene  
char_in_event  
thread_contains_scene  
event_contains_beat  
event_impacts_state  
char_relationship  
scene_on_timeline  
event_on_timeline  

### 3.1 Link Schema 基本構造

Link JSON の基本構造：

link_id  
link_type  
source_id  
target_id  
metadata  

### 3.2 Link Type 詳細

char_at_scene
Character が Scene に参加する関係

source_id = character_id  
target_id = scene_id  

char_in_event
Character が Event に関与する関係

source_id = character_id  
target_id = event_id  

thread_contains_scene
Thread が Scene を含む関係

source_id = thread_id  
target_id = scene_id  

event_contains_beat
Event が Beat を含む関係

source_id = event_id  
target_id = beat_id  

event_impacts_state
Event が State に影響を与える関係

source_id = event_id  
target_id = state_id  

char_relationship
Character 同士の関係

source_id = character_id  
target_id = character_id  

scene_on_timeline
Scene の時系列配置

source_id = scene_id  
target_id = timeline_id  

event_on_timeline
Event の時系列配置

source_id = event_id  
target_id = timeline_id  

---

## 4. JSON データ記述サンプル

### 4.1 Character JSON 例

{
  "character_id": "char_001",
  "name": "Alice",
  "role": "Protagonist"
}

### 4.2 Scene JSON 例

{
  "scene_id": "scene_010",
  "location": "Library"
}

### 4.3 Link JSON 例（Character → Scene）

{
  "link_id": "link_001",
  "link_type": "char_at_scene",
  "source_id": "char_001",
  "target_id": "scene_010"
}

### 4.4 Link JSON 例（Thread → Scene）

{
  "link_id": "link_002",
  "link_type": "thread_contains_scene",
  "source_id": "thread_001",
  "target_id": "scene_010"
}

---

## 5. データ整合性（Integrity）ガイドライン

Story Database のデータ整合性を維持するため、
以下のルールを定義する。

### 5.1 ID 一意性

すべての Entity ID は Story Database 内で一意でなければならない。

### 5.2 参照整合性

Link が参照する source_id と target_id は
必ず既存の Entity ID でなければならない。

存在しない ID へのリンクは禁止。

### 5.3 親子関係制約

Beat は必ず Event に属する。  
Event は必ず Scene に属する。  
Scene は必ず Thread に属する。  

孤立した Beat / Event / Scene は存在してはならない。

### 5.4 削除ルール

Entity を削除する場合：

1. 関連する Link を削除
2. 子 Entity を削除
3. 親 Entity を更新

参照が残ったまま Entity を削除してはならない。

### 5.5 Link 整合性

同一の source_id / target_id / link_type の
重複 Link を作成してはならない。

---

## 6. まとめ

NWF Story Database v2.0.1 では以下を実現した。

- 全 Entity を独立 Document として保存
- Entity 間関係を Link（Edge）として管理
- Document-Graph Hybrid Database 構造採用
- Git に適したファイル分割構造
- 多対多関係管理
- データ整合性ルール定義

Story Database は
NWF における物語データの永続記憶層であり、
NWF Engine および AI Authoring System の基盤となる。

---

[EOF]