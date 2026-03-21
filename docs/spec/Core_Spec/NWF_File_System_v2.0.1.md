Source: docs/spec/Core_Spec/NWF_File_System_v2.0.1.md
Updated: 2026-03-21T19:14:00+09:00
PIC: Engineer / ChatGPT

# NWF File System v2.0.1

---

## 1. 概要

本ドキュメントは Novel Writing Framework (NWF) における
ファイルシステム構造 v2.0.1 を定義する。

NWF File System は、NWF のデータモデル、Story Database、
エンジン構造を実際のディレクトリ構造として物理的に実装するための仕様である。

本仕様では以下を定義する。

・NWF Project Root
・標準ディレクトリ構造
・data ディレクトリ構造
・links ディレクトリ構造
・engines ディレクトリ構造
・novel_projects テンプレート構造
・ファイル命名規則
・クロスプラットフォームパス規約

---

## 2. v2.0.0 の構造的問題点

File System v2.0.0 には以下の問題があった。

1. data ディレクトリが Data Model v2.0.1 の Entity を網羅していない
2. Event / Beat / State / Relationship / Timeline の保存場所が存在しない
3. Document-Graph Hybrid Model に対応する links ディレクトリが存在しない
4. engines 構造が Scene > Event > Beat の階層構造に最適化されていない
5. novel_projects テンプレートが Story Database 構造と一致していない

そのため v2.0.1 では File System 構造を全面的に拡張する。

---

## 3. 新・全体ディレクトリツリー構造

NWF Project Root の標準構造は以下とする。

<project_root>/
│
├─ docs/
│  ├─ project/
│  └─ spec/
│
├─ data/
│  ├─ worlds/
│  ├─ world_rules/
│  ├─ characters/
│  ├─ states/
│  ├─ relationships/
│  ├─ threads/
│  ├─ scenes/
│  ├─ events/
│  ├─ beats/
│  ├─ timelines/
│  └─ links/
│
├─ engines/
│  ├─ world_engine/
│  ├─ character_engine/
│  ├─ thread_engine/
│  ├─ scene_engine/
│  ├─ event_engine/
│  ├─ beat_engine/
│  ├─ timeline_engine/
│  └─ query_engine/
│
├─ novel_projects/
│  └─ project_template/
│
└─ tools/
   └─ validation/

この構造を NWF v2.0.1 の標準ファイルシステムとする。

---

## 4. data ディレクトリ構造

data ディレクトリは Story Database の物理保存領域である。

data/
│
├─ worlds/
├─ world_rules/
├─ characters/
├─ states/
├─ relationships/
├─ threads/
├─ scenes/
├─ events/
├─ beats/
├─ timelines/
└─ links/

各ディレクトリには Entity JSON ファイルが保存される。

### 4.1 ファイル命名規則

各 Entity JSON ファイルの命名規則は以下とする。

world_001.json
world_rule_001.json
character_001.json
state_001.json
relationship_001.json
thread_001.json
scene_001.json
event_001.json
beat_001.json
timeline_001.json

命名規則

entity_name + "_" + 3桁以上のID + ".json"

例

scene_012.json
character_003.json
event_045.json

---

## 5. links ディレクトリ構造

links ディレクトリは Entity 間の多対多関係を管理する
Graph Edge データを保存する。

data/links/
│
├─ character_scene_links/
├─ character_event_links/
├─ thread_scene_links/
├─ event_state_links/
├─ character_relationship_links/
└─ timeline_links/

各リンクは JSON ファイルとして保存される。

例

char_scene_001.json
thread_scene_002.json
event_state_005.json

リンクデータには以下の情報を含む。

・link_id
・source_entity_id
・target_entity_id
・link_type
・metadata

---

## 6. engines ディレクトリ構成

NWF v2.0.1 ではエンジンは Entity 階層に対応して配置する。

engines/
│
├─ world_engine/
├─ character_engine/
├─ thread_engine/
├─ scene_engine/
├─ event_engine/
├─ beat_engine/
├─ timeline_engine/
└─ query_engine/

各エンジンの責務

world_engine
世界設定と world_rules を処理

character_engine
キャラクターと state / relationship を処理

thread_engine
Thread 構造を管理

scene_engine
Scene 構造を管理

event_engine
Event 処理

beat_engine
Beat 処理

timeline_engine
Timeline 管理

query_engine
Story Database 全体の検索・クエリ処理

---

## 7. novel_projects テンプレート構造

novel_projects/project_template は
Story Database と同じ構造を持つ。

novel_projects/project_template/
│
├─ worlds/
├─ world_rules/
├─ characters/
├─ states/
├─ relationships/
├─ threads/
├─ scenes/
├─ events/
├─ beats/
├─ timelines/
├─ links/
└─ manuscript/

これにより小説プロジェクトは Story Database と
1対1対応の構造を持つ。

---

## 8. パス指定の標準規約

クロスプラットフォーム対応のため、
NWF のパス規約は以下とする。

1. すべて相対パスを使用する
2. パス区切りはスラッシュを使用する
3. ディレクトリ名はすべて小文字
4. スペースを含む名前は禁止
5. OS依存の絶対パスは禁止
6. UTF-8 文字コードを使用する
7. JSON ファイル拡張子は .json
8. Markdown ファイル拡張子は .md

パス例

docs/spec/Core_Spec/NWF_File_System_v2.0.1.md
data/scenes/scene_001.json
data/links/character_scene_links/char_scene_001.json

---

## 9. まとめ

NWF File System v2.0.1 では以下を定義した。

・Data Model v2.0.1 の全 Entity を保存する data 構造
・Document-Graph Hybrid Model に対応する links 構造
・Entity 階層に対応した engines 構造
・Story Database と同期した novel_projects テンプレート構造
・クロスプラットフォーム対応のパス規約

File System v2.0.1 は
NWF の物理構造を定義する基盤仕様であり、
Story Database と Engine System を支える
NWF の物理アーキテクチャである。

---

[EOF]