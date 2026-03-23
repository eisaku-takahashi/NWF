Source: docs/spec/Architecture_Spec/NWF_Story_Database_Model_v2.0.1.md
Updated: 2026-03-23T17:27:00+09:00
PIC: Engineer / ChatGPT

# NWF Story Database Model v2.0.1

---

## 1. Overview (Database as a Story State Engine)

NWF（Novel Writing Framework）における Story Database Model は、物語に関するすべてのデータ、状態、関係、時間、因果、履歴を統合管理する中核データ基盤である。本データベースは単なる保存領域ではなく、Story Operating System（Story OS）における **Story State Engine（物語状態管理エンジン）** として機能する。

Story Database は以下を担う。

- 全エンティティの永続化
- Entity ID System による統合管理
- Dual-Axis Timeline の保持
- 因果関係・相関関係のグラフ管理
- Simulation State の履歴管理
- Narrative Query Language（NQL）による検索基盤
- Narrative Consistency の検証用データ供給
- AI Engine / Rendering Engine へのデータ供給

Story Database は NWF Foundation Layer における **Single Source of Truth（唯一の真実の源泉）** である。

---

## 2. Data Storage Strategy (Markdown, JSON, Graph-DB Mapping)

Story Database は複数のデータ形式を組み合わせた **Graph-Document Hybrid Architecture** を採用する。

### 2.1 Document Storage

以下の要素は文書構造として保存される。

- Thread
- Scene
- Beat
- World
- Character
- Rule
- Lore
- Dialogue
- Note

保存形式:

- Markdown
- JSON
- YAML

これらは人間が編集しやすい形式で保持される。

### 2.2 Structured Data Storage

構造化データとして保存されるもの:

- Entity Metadata
- Timeline Index
- Emotional Curve Data
- Foreshadowing State
- Consistency Check Results
- Simulation Snapshot

保存形式:

- JSON
- SQLite / Document DB / Key-Value Store

### 2.3 Graph Data Storage

関係性データはグラフ構造として管理される。

グラフ種類:

- Causal Graph
- Thread Graph
- Relationship Graph
- Location Graph
- Organization Graph
- Knowledge Graph

Graph DB（Neo4j 等）または内部 Graph 構造で管理される。

---

## 3. Core Entity Schema (ID, Meta, Payload)

Core Spec v2.0.1 の全 19 要素は共通スキーマで管理される。

### 3.1 Entity 共通構造

各エンティティは以下の構造を持つ。

- entity_id
- entity_type
- metadata
- payload
- relationships
- timeline_index
- state_history

### 3.2 Entity Metadata

Metadata に含まれる情報:

- name
- description
- tags
- created_time
- updated_time
- author
- version
- status

### 3.3 Payload

Payload はエンティティ固有データを格納する。

例:

- Character → personality, background, goal
- World → rules, geography, culture
- Scene → location, characters, summary
- Beat → action, dialogue, emotion_change
- Rule → constraint, effect
- Event → event_description
- Emotion → emotion_value

Story Database はすべての Core Entity を ID ベースで正規化し管理する。

---

## 4. Timeline Architecture (ST / NT Indexing)

Story Database は Dual-Axis Timeline を採用する。

### 4.1 Story Time (ST)

- 物語世界内部の時間
- 年、日付、時刻、経過時間
- キャラクターの年齢、歴史、イベント発生時刻などに使用

### 4.2 Narrative Time (NT)

- 物語が語られる順序
- 回想
- 未来
- 並行ストーリー
- 視点切替
- 編集順序

### 4.3 Timeline Index

各 Scene / Beat / Event は以下を持つ。

- story_time_start
- story_time_end
- narrative_time_order
- timeline_thread_id

Timeline Resolution Engine はこのインデックスを使用して物語の時間整合性を解決する。

---

## 5. Multi-Graph Schema

Story Database は複数のグラフを同時に管理する。

### 5.1 Causal Graph

ノード:
- Event
- Beat
- Scene

エッジ:
- causes
- enables
- prevents
- reveals
- foreshadows

物語の因果関係を表現する。

### 5.2 Thread Graph

構造:

Thread → Scene → Beat

物語構造およびストーリーライン管理に使用される。

### 5.3 Relationship Graph

ノード:
- Character
- Organization
- Location

エッジ:
- friend
- enemy
- family
- belongs_to
- located_in
- controls
- loves
- hates

社会関係・感情関係・所属関係を管理する。

### 5.4 World Rule Influence Graph

World Rule が Event / Character / Organization / Technology に与える影響範囲を管理する。

---

## 6. State & Conflict Persistence (Simulation Snapshot Management)

Story OS は物語をシミュレーションとして扱うため、状態遷移を保存する必要がある。

### 6.1 Simulation State

State に含まれる情報:

- character_state
- world_state
- relationship_state
- organization_state
- location_state
- conflict_state
- resource_state
- knowledge_state

### 6.2 Snapshot

特定の Story Time / Narrative Time における状態を Snapshot として保存する。

Snapshot により:

- 物語の任意時点の状態復元
- 分岐ストーリー
- What-if シミュレーション
- 矛盾検出
- 状態遷移分析

が可能になる。

---

## 7. Query & Analysis Support (NQL Backend Logic)

Story Database は Narrative Query Language（NQL）による検索・分析を想定して設計される。

### 7.1 NQL の用途

例:

- 特定キャラクターが登場する Scene を取得
- 未回収伏線を検索
- 因果関係チェーンを取得
- 特定期間のイベント一覧
- 感情曲線のピークを検索
- Character 関係ネットワークを取得
- Timeline 上の矛盾を検索
- Conflict 状態の変化を取得

### 7.2 Index 設計

検索高速化のためのインデックス:

- entity_id index
- entity_type index
- story_time index
- narrative_time index
- thread_id index
- character_id index
- location_id index
- relationship index
- causal link index
- foreshadowing status index

Story Database は **NQL 最適化インデックス** を前提に設計される。

---

## 8. Data Integrity & Validation

Story Database は Story OS の整合性基盤であるため、データ整合性検証機能を持つ。

検証対象:

- Entity ID 重複
- 参照切れ ID
- Timeline 矛盾
- 因果関係ループ
- 未回収伏線
- Character 行動と Personality の矛盾
- World Rule 違反イベント
- Thread 構造不整合
- State Transition 矛盾

Narrative Consistency Engine は Story Database のデータを使用して整合性を検証する。

---

## 9. まとめ

Story Database Model v2.0.1 は、NWF における物語データ、関係、時間、状態、因果、履歴を統合管理する **Narrative Graph Data Store** であり、Story Operating System の Foundation Layer における Single Source of Truth として機能する。

本データベースは以下を統合する。

- Document Storage
- Structured Data Storage
- Graph Data Storage
- Timeline Storage
- Simulation State Storage
- Query Engine Index
- Consistency Validation Data

Story Database は NWF 全体の基盤であり、Core Spec の全 19 要素、System Architecture、AI Engine、Rendering Engine、Analysis Engine はすべて本データベースを中心に動作する。

Story Database Model は Story OS のデータ基盤であり、物語を「保存する」のではなく、「状態として管理し、解析し、生成し、シミュレーションする」ためのデータエンジンとして設計される。

---

[EOF]