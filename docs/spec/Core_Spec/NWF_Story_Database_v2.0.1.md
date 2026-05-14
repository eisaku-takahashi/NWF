Source: docs/spec/Core_Spec/NWF_Story_Database_v2.0.1.md
Updated: 2026-05-11T17:39:00+09:00
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

### 2.2 StoryDB Interface Specification（Phase 3.5 追記）

【追記理由】
Phase 3.5 Debug Work Plan において、
Validator と StoryDB 間の I/F 不整合が
Immutability Validator の誤動作原因となったため、
StoryDB の最小必須 I/F を正式仕様として固定する。

【追加仕様】

StoryDB 実装は最低限以下の Interface を必須とする。

```python
get(entity_id: str) -> Optional[Entity]
```

### 2.2.1 get() の定義

* 引数 `entity_id` は必ず `str`
* StoryDB 実装内部で UUID object 等を使用していても、
  外部 Interface は `str` に正規化する
* Validator / Engine / Mock は
  必ず本 Interface 経由で Entity を取得する
* 内部辞書構造や storage layout に直接依存してはならない

### 2.2.2 非存在 Entity の扱い

`entity_id` に対応する Entity が存在しない場合：

```python
None
```

を返す。

例：

```python
entity = story_db.get("char_001")

if entity is None:
    # Entity not found
```

### 2.2.3 Validator Compatibility Rule（Phase 3.5 追加）

ConsistencyValidator は
以下の I/F 契約に完全準拠しなければならない。

```python
target_id = str(getattr(target, "id", ""))
previous = story_db.get(target_id)
```

【追加理由】

旧実装では：

* Mock DB の内部 dict に直接依存
* UUID / str 混在
* get() 未実装 Mock の存在

によって `previous is None` が誤発生し、
Immutability Check がスキップされる問題が存在した。

本仕様追加により：

* DB 実装差異
* Mock 実装差異
* ID 型差異

を完全に吸収する。

### 2.2.4 MockStoryDB Compatibility Requirement（Phase 3.5 追加）

MockStoryDB を含む
全テスト用 DB 実装も
本 Interface に準拠しなければならない。

最低要件：

```python
class MockStoryDB:
    def __init__(self, data: dict):
        self._data = data

    def get(self, entity_id: str):
        return self._data.get(str(entity_id))
```

【補足】

これは実装例であり、
内部構造は自由である。

ただし：

* `get(entity_id: str)`
* 非存在時 `None`
* ID の `str` 正規化

は必須契約とする。

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

【Phase 3.5 追記】

Entity ID は
外部 Interface 上では必ず `str` とする。

例：

```python
"char_001"
"scene_010"
```

UUID object や内部 DB key format は
StoryDB 内部でカプセル化し、
外部へ露出してはならない。

【追加理由】

Phase 3.5 において：

* UUID 型
* str 型

の混在により
Validator の参照失敗が発生したため。

### 5.2 参照整合性

Link が参照する source_id と target_id は
必ず既存の Entity ID でなければならない。

存在しない ID へのリンクは禁止。

【Phase 3.5 追記】

参照確認時の Entity 解決は
必ず StoryDB Interface を経由する。

```python
story_db.get(entity_id)
```

内部 storage 構造への直接アクセスは禁止。

【追加理由】

Validator / Engine / Mock 間で
I/F 契約を統一するため。

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

* 全 Entity を独立 Document として保存
* Entity 間関係を Link（Edge）として管理
* Document-Graph Hybrid Database 構造採用
* Git に適したファイル分割構造
* 多対多関係管理
* データ整合性ルール定義

【Phase 3.5 追記】

さらに以下を正式仕様化した。

* `get(entity_id: str) -> Optional[Entity]`
* 非存在時 `None` を返す
* Validator は `story_db.get()` のみを使用
* ID は外部 Interface 上 `str` に統一
* Mock DB を含む全 DB 実装の I/F 統一

これにより：

* Validator の純粋性
* StoryDB 実装交換可能性
* Mock / Production 間整合性
* Immutability Check の安定性

を保証する。

Story Database は
NWF における物語データの永続記憶層であり、
NWF Engine および AI Authoring System の基盤となる。

---

[EOF]