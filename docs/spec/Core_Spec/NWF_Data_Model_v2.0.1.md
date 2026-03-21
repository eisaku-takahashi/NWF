Source: docs/spec/Core_Spec/NWF_Data_Model_v2.0.1.md
Updated: 2026-03-21T16:41:00+09:00
PIC: Engineer / ChatGPT

# NWF Data Model v2.0.1

---

## 1. 問題点と不足Entityの特定

NWF_Data_Model_v2.0.0 では、Glossary v2.0.1 および Entity ID System v2.0.1 と比較して以下の問題が存在していた。

### 1.1 不足していたEntity

v2.0.0 に存在しなかったEntity：

Event  
State  
Relationship  
Timeline  
World  

これにより、物語構造・状態変化・人間関係・時系列の管理が不完全であった。

### 1.2 階層構造の問題

旧構造：

WorldRule → Character → Thread → Scene → Beat

この構造は物語構造として不適切であり、
特に Scene / Event / Beat の関係が未定義であった。

### 1.3 データモデルの問題

- Entity関係が階層モデルに偏っていた
- 多対多関係の表現ができない
- Character ↔ Scene ↔ Thread の関係が不明確
- Timeline が独立概念として扱われていない
- State の管理場所が定義されていない

これらを解決するため、
v2.0.1 では Graph 指向データモデルを採用する。

---

## 2. 新データ構造図（Graph指向モデル）

NWF v2.0.1 のデータ構造は以下の論理構造を持つ。

Story
 ├── World
 │    └── WorldRule
 │
 ├── Characters
 │    ├── Character
 │    ├── State
 │    └── Relationship
 │
 ├── Threads
 │    └── Thread
 │         └── Scene
 │              └── Event
 │                   └── Beat
 │
 ├── Timeline
 │    └── Scene Timeline / Event Timeline
 │
 └── Links
      ├── character_scene_links
      ├── character_event_links
      ├── thread_scene_links
      └── relationship_links

### 2.1 構造軸（Narrative Structure Axis）

Thread  
↓  
Scene  
↓  
Event  
↓  
Beat  

これは物語の構造軸である。

### 2.2 動態要素（Dynamic Elements）

Character  
State  
Relationship  
Timeline  

これらは構造軸とは独立した動的要素として存在し、
Graph構造で接続される。

---

## 3. Entity関係マトリックス

各Entityが参照するIDの関係を定義する。

World
- world_rule_ids

WorldRule
- world_id

Character
- world_id
- state_ids
- relationship_ids
- thread_ids
- scene_ids
- event_ids

Thread
- related_character_ids
- scene_ids

Scene
- thread_ids
- location
- participant_character_ids
- event_ids
- timeline_id

Event
- scene_id
- involved_character_ids
- beat_ids
- state_change_ids
- timeline_id

Beat
- event_id

State
- character_id
- related_event_id

Relationship
- character_id_1
- character_id_2

Timeline
- scene_ids
- event_ids

---

## 4. Story Database 実装ガイドライン

### 4.1 Database Model

NWF Story Data Store は以下のモデルを採用する。

Document-Graph Hybrid Model

特徴：

- EntityはJSONドキュメントとして保存
- Entity間の関係はID参照で接続
- Linkテーブルで多対多関係を管理
- Graph構造として物語関係を表現

### 4.2 JSON保存単位

推奨JSON単位：

worlds.json  
world_rules.json  
characters.json  
relationships.json  
states.json  
threads.json  
scenes.json  
events.json  
beats.json  
timeline.json  
links.json  

### 4.3 Link Table 概念

多対多関係を管理するため、
Link Table 概念を導入する。

例：

character_scene_links
character_id
scene_id

character_event_links
character_id
event_id

thread_scene_links
thread_id
scene_id

relationship_links
relationship_id
character_id

これにより循環参照を防ぎつつ、
Graph構造を表現できる。

### 4.4 ID参照原則

すべてのEntity参照は以下の原則に従う。

- Entityは他EntityをIDで参照する
- 子Entityは親IDを持つ
- 多対多関係はLinkテーブルで管理する
- Entity本体に配列参照を持たせすぎない
- 循環参照は禁止
- 参照方向は原則として構造軸の上から下

---

## 5. Data Model 設計原則

NWF Data Model v2.0.1 は以下の原則に基づく。

Graph指向データモデル  
ID参照ベース設計  
Document Database 互換  
Git管理可能構造  
AI解析適合構造  
拡張可能設計  
循環参照防止設計  

---

## 6. まとめ

NWF Data Model v2.0.1 では以下を実現した。

- Glossary v2.0.1 の全Entity統合
- Thread > Scene > Event > Beat 構造軸確立
- Character / State / Relationship / Timeline の動態要素化
- Document-Graph Hybrid Database Model 採用
- Link Table による多対多関係管理
- ID参照によるEntity結合
- 循環参照防止設計

この Data Model は
NWF Story Database、
Engine Architecture、
AI Authoring System
の基盤データ構造となる。

---

[EOF]