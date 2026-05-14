Source: docs/spec/Data_Spec/NWF_CharacterData_v2.0.1.md
Updated: 2026-03-24T15:42:00+09:00
PIC: Engineer / ChatGPT

# NWF CharacterData v2.0.1

---

## 1. 概要

CharacterData は Story OS（Narrative World Framework v2.0.1）におけるキャラクターを定義するデータモデルである。

本バージョンでは CharacterData を、従来の「キャラクター設定プロフィール」ではなく、
物語シミュレーション上で状態が更新され続ける **動的シミュレーション用エージェント・データ（Character Agent Data）** として再定義する。

Character は Story OS 内では Actor / Agent として扱われ、
Story Simulation、Narrative Logic、Emotional Dynamics、Conflict Dynamics など
複数のエンジンの演算対象となる中心ノードである。

CharacterData は以下の情報を統合的に管理する。

- 静的プロフィール情報
- 動的状態（位置・健康・社会状態など）
- 心理・動機・意思決定パラメータ
- 感情状態
- 物語上の役割・キャラクターアーク状態
- 伏線・秘密フラグ
- タイムライン履歴・行動履歴
- グラフ関係（Relationship / Conflict / Narrative Links）

CharacterData は Story State の中心ノードとなるデータ構造である。

---

## 2. データ構造階層（Data Structure Hierarchy）

CharacterData は以下の階層構造を持つ。

### 2.1 Static Core（静的コア情報）

キャラクターの基本プロフィール情報を保持する。
これらの情報は通常、物語中で頻繁には変化しない。

主な項目：

- character_id: キャラクター一意識別子
- name: 名前
- role: 物語上の役割（Protagonist, Antagonist, Support など）
- personality: 性格特性
- background: 背景・経歴
- origin: 出身・所属
- abilities: 能力・技能
- traits: 特徴・属性タグ

Static Core は Character の基本設定を定義する。

---

### 2.2 Dynamic State（動的状態）

物語の進行に伴い変化する「現在の状態」を保持する。

主な項目：

- status: 現在の状態（normal, injured, missing, dead など）
- health: 健康度・体力
- location: 現在位置
- inventory: 所持品
- social_rank: 社会的地位・身分
- reputation: 評判・社会的評価
- knowledge_state: 知っている情報・秘密
- affiliation: 所属組織・グループ

Dynamic State は Execution Flow によって Scene / Thread / Event ごとに更新される。

---

### 2.3 Psychological Dynamics（心理・動機パラメータ）

キャラクターの意思決定・行動選択に影響を与える心理パラメータを管理する。

主な項目：

- motivation: 根本動機
- goal: 現在の目標
- desire: 欲望
- fear: 恐怖
- belief: 信念・価値観
- stress: ストレス値
- mental_state: 精神状態
- relationship_bias: 対人感情バイアス

これらの値は Dynamic Force Layer の演算対象となる。

---

### 2.4 Emotional Data（感情データ）

Emotional Curve Model と連動する感情状態データを管理する。

主な項目：

- emotional_valence: 感情の快・不快値
- emotional_arousal: 覚醒度
- emotional_state: 現在の感情状態（joy, anger, fear, sadness など）
- emotional_momentum: 感情遷移の慣性
- emotional_stability: 感情安定度
- emotional_history_ref: 感情履歴参照

感情データは Emotional Engine により更新される。

---

### 2.5 Narrative Attributes（物語属性）

物語構造上の役割や進行状況に関するデータを管理する。

主な項目：

- narrative_role: 物語役割
- current_thread_id: 現在参加している Thread
- current_scene_id: 現在の Scene
- character_arc_state: キャラクターアーク進行状態
- arc_progress: アーク進行度
- conflict_participation: 関与している Conflict
- narrative_flags: 物語フラグ（裏切り予定、死亡予定など）

これらは Narrative Logic Layer の演算対象となる。

---

## 3. Graph Relationship Specification

Story OS ではキャラクター間の関係は独立したデータではなく、
Graph 構造における Edge として管理する。

Character は Graph Node として定義され、
関係性は Relationship Edge として接続される。

Relationship Edge の主なプロパティ：

- relationship_type: 関係タイプ（friend, enemy, family, lover, rival など）
- relationship_intensity: 関係強度
- trust_level: 信頼度
- hostility_level: 敵対度
- relationship_history_ref: 関係履歴参照
- last_interaction_time: 最終相互作用時刻
- relationship_state: 現在の関係状態

Character Node は以下の Edge と接続される：

- relationship_edge（人間関係）
- conflict_edge（対立関係）
- narrative_edge（物語上の関係）
- foreshadowing_edge（伏線関係）

Character は Story Graph の中心ノードの一つである。

---

## 4. Execution Flow との統合

Execution Flow の各ステップ（Beat / Scene / Event）で
CharacterData の以下の項目が更新対象となる。

更新対象の例：

- location
- health
- status
- emotional_state
- stress
- goal
- relationship_intensity
- conflict_participation
- narrative_flags
- character_arc_state

Execution Flow における Character 更新の流れ：

Event / Scene 発生
→ Character Action / Interaction
→ Emotional Update
→ Relationship Update
→ Conflict Update
→ Narrative State Update
→ Character State 保存（Story State）

CharacterData は Story Simulation における状態更新単位となる。

---

## 5. Serialization & Database Mapping

CharacterData は以下のデータベース構造にマッピングされる。

### 5.1 Graph Database

Graph DB では以下の構造で保存される。

- character_node
- relationship_edge
- conflict_edge
- narrative_edge
- foreshadowing_edge

Character は Node、
関係性は Edge として保存される。

### 5.2 Document Database

Document DB では CharacterData は 1 キャラクター 1 ドキュメントとして保存される。

主な保存ブロック：

- static_core
- dynamic_state
- psychological_dynamics
- emotional_data
- narrative_attributes
- timeline_history_ref
- action_history_ref
- flags
- metadata

Graph DB と Document DB を併用して CharacterData を管理する。

---

## 6. AI Rendering Metadata

AI による文章生成・視点描写・会話生成のため、
CharacterData には Rendering 用メタデータを持たせる。

主な項目：

- pov_style: 視点描写スタイル
- vocabulary_level: 語彙レベル
- speech_style: 話し方・口調
- knowledge_scope: 知識範囲（キャラクターが知っている情報）
- perception_bias: 認知バイアス
- narrative_voice: 語りの声
- inner_monologue_style: 内面描写スタイル

これにより AI Authoring Interface で
キャラクター視点の文章生成を制御することができる。

---

## 7. まとめ

CharacterData v2.0.1 は
従来のキャラクター設定データではなく、
Story OS 上で動作するキャラクターエージェントの状態空間データである。

CharacterData は以下を統合する中心データである。

- Static Character Profile
- Dynamic Character State
- Psychological / Motivation Parameters
- Emotional State Data
- Narrative Role / Character Arc
- Relationship Graph Connections
- Timeline / Action History
- AI Rendering Metadata

Character は Story OS において
物語を動かす主体（Actor / Agent）であり、
CharacterData は Story Simulation における最重要データモデルの一つである。

---

[EOF]