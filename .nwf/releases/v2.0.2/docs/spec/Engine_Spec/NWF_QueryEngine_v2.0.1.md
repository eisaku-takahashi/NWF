Source: docs/spec/Engine_Spec/NWF_QueryEngine_v2.0.1.md
Updated: 2026-03-27T14:22:00+09:00
PIC: Engineer / ChatGPT

# NWF Query Engine v2.0.1
(Data Access & Interface Layer Specification)

---

## 1. 概要

Query Engine は NWF v2.0.1（Story OS）において、全物語データの検索・参照・関係探索を担当する Data Access & Interface Layer の中核エンジンである。

本エンジンは単なる検索機能ではなく、Story OS における「物語データ・ゲートウェイ（Narrative Data Gateway）」として機能する。

Thread、Scene、Event、Timeline、Character、State など、Story OS 内のすべての構造化データを横断的に検索・抽出・関係探索し、他エンジンおよび Interface Layer に対して必要な情報を提供する。

Query Engine は Story OS におけるデータ検索基盤、データ参照 API、関係探索エンジンとして機能する。

---

## 2. System Architecture 上の位置づけ

Query Engine は System Architecture において Data Access & Interface Layer に配置される。

Layer 構造：

- Data Layer（物理ストレージ）
- Data Access & Interface Layer（Query Engine）
- Engine Layer（Story / Scene / Event / Timeline Engine）
- Intelligence Layer（Analysis / Simulation Engine）
- Interface Layer（UI / Visualization / External API）

Query Engine の役割：

- Data Layer と Engine / Intelligence Layer の仲介
- データ参照 API の提供
- 検索・フィルタリング・集計
- 因果関係・時間関係の探索
- UI / 外部 API 向けデータ提供

Query Engine は Service ではなく、Story OS 内部標準 API エンジンとして定義される。

---

## 3. Core Architecture

### 3.1 Data Access Scope

Query Engine は以下のデータに対して読み取りアクセス権限を持つ。

- Thread Data
- Scene Data
- Event Data
- Timeline Data
- Character Data
- Character State Data
- EmotionalCurve Data
- WorldRule Data
- Foreshadowing Data
- Analysis Result Data
- Structure Data

Story OS 内のすべての構造化データを検索対象とする。

---

### 3.2 Query Engine の役割

Query Engine は以下の機能を提供する。

- ID 検索
- 条件検索
- 範囲検索
- 関係検索
- 因果関係探索
- Timeline 検索
- Cross Reference 検索
- 集計・統計
- グラフ探索
- インデックス検索
- キャッシュ検索

Query Engine は Story OS のデータ検索基盤として機能する。

---

## 4. Query Language Specification（NWF-QL）

Query Engine は NWF-QL（NWF Query Language）を使用して検索を行う。

NWF-QL は JSON ベースのクエリ形式または DSL（Domain Specific Language）として定義される。

クエリの基本構成：

- target（検索対象）
- filter（条件）
- range（範囲）
- relation（関係）
- aggregation（集計）
- sort（並び替え）
- limit（件数制限）

検索演算子例：

- equals
- not_equals
- greater_than
- less_than
- between
- contains
- in
- before
- after
- related_to
- caused_by
- causes
- appears_in
- belongs_to

NWF-QL は Story OS 全体の標準検索言語となる。

---

## 5. Query Types（検索種別）

Query Engine は以下の検索種別をサポートする。

### 5.1 Point Query
ID を指定して単一データを取得する。

例：
Scene ID、Event ID、Character ID など。

### 5.2 Range Query
時間、Scene 範囲、Event 範囲などの範囲検索。

例：
Timeline Day 5 ～ Day 10
Scene 20 ～ Scene 40

### 5.3 Relational Query
関係性を条件に検索する。

例：
Character A が登場する Scene
Thread X に属する Event
Character A と Character B が同時に登場する Scene

### 5.4 Analytical Query
統計・集計・メトリクス取得。

例：
Event 数
Thread 出現頻度
Character 登場回数
Event Density

---

## 6. Search & Discovery Modules

Query Engine は以下の検索モジュールを持つ。

### 6.1 Temporal Discovery（時間軸検索）

Timeline を基準に検索を行う。

検索例：

- 特定日付の Event
- Scene の前後 Event
- 同時発生 Event
- Timeline 範囲内 Event
- Climax 付近 Event

---

### 6.2 Causal Explorer（因果・グラフ探索）

Event の因果関係グラフを探索する。

探索例：

- Event A の原因イベント
- Event A の結果イベント
- 因果チェーン
- 因果ループ検出
- Thread 因果構造
- Character 行動の因果連鎖

Causal Explorer はグラフ探索アルゴリズムを使用する。

---

### 6.3 Relational Filter（関係フィルタ）

Character、Thread、Scene、Event の関係を条件に検索する。

検索例：

- Character A が登場する Scene
- Thread X に属する Scene
- Event を含む Scene
- 特定 Emotional 状態の Scene
- 特定 Theme に関係する Thread

---

## 7. Output Data Structures

Query Engine は以下の結果形式を返す。

### 7.1 QueryResult
単一オブジェクトを返す。

### 7.2 ResultSet
複数結果のリスト。

### 7.3 GraphResult
関係グラフデータ。

内容：

- nodes
- edges
- relations
- weights

### 7.4 MetricsSummary
統計・集計結果。

例：

- Event Count
- Scene Count
- Thread Coverage
- Character Appearance Count
- Event Density
- Emotional Average

---

## 8. Performance & Indexing

大規模な物語データに対応するため、Query Engine は以下の機構を持つ。

### 8.1 Index

主なインデックス：

- Scene ID Index
- Event ID Index
- Character ID Index
- Thread ID Index
- Timeline Index
- Event Time Index
- Character Appearance Index
- Thread Scene Index
- Causal Graph Index

Index により高速検索を実現する。

### 8.2 Cache

頻繁に使用されるクエリ結果をキャッシュする。

キャッシュ対象例：

- Character Appearance List
- Scene Event List
- Thread Coverage
- Timeline Event Range
- Emotional Curve Data

Cache により Story OS 全体のパフォーマンスを向上させる。

---

## 9. Internal / External Dual Interface

Query Engine は 2 種類のインターフェースを提供する。

### 9.1 Internal Interface（Engine 用）

対象：

- Story Engine
- Analysis Engine
- Simulation Engine
- Event Engine
- Timeline Engine

特徴：

- 生データ
- 高精度
- 完全データ
- 高速アクセス

### 9.2 External Interface（UI / API 用）

対象：

- Visualization Tool
- Editor UI
- External API
- Export Tool

特徴：

- 軽量データ
- フィルタ済み
- 集計済み
- Graph Data
- Preview Data

Query Engine は Story OS の内部 API と外部 API の両方を提供する。

---

## 10. Execution Lifecycle

Query Engine の実行フロー：

1. Query Request 受信
2. Query Parser
3. Query Planner
4. Index Search
5. Data Fetch
6. Relation Join
7. Graph Construction
8. Aggregation / Metrics
9. Result Formatting
10. Result Return
11. Cache Update

Query Engine は検索要求に応じて動的に実行される。

---

## 11. Maintenance & Versioning

Query Engine は以下の仕様に強く依存する。

- Data_Spec v2.0.1
- ID System v2.0.1
- Reference System v2.0.1
- Timeline Spec v2.0.1
- Event Spec v2.0.1
- Thread Spec v2.0.1
- Character Spec v2.0.1
- Analysis Spec v2.0.1

データ構造・ID体系変更時は Query Engine の Index および Query Format を更新する必要がある。

---

## 12. まとめ

Query Engine は以下の役割を持つ。

- Story OS 全データの検索
- 条件検索・範囲検索
- 関係検索
- 因果関係探索
- Timeline 検索
- Cross Reference 検索
- 集計・統計
- Graph データ生成
- Index 管理
- Cache 管理
- Internal API 提供
- External API 提供

Query Engine は Story OS における

「データ検索基盤」
「データ参照 API」
「関係探索エンジン」
「物語データ・ゲートウェイ」

として機能する。

NWF v2.0.1 において Query Engine は
Story OS のデータアクセス中枢を担う基盤エンジンである。

---

[EOF]