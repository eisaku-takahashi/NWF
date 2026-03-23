Source: docs/spec/Architecture_Spec/NWF_Character_Model_v2.0.1.md
Updated: 2026-03-23T20:05:00+09:00
PIC: Engineer / ChatGPT

# NWF Character Model v2.0.1

---

## 1. 概要

NWF（Novel Writing Framework）における Character Model は、物語を駆動する主体（Actor）を定義するモデルであり、Story OS における動的エージェントとして機能する。

Character は World Model によって定義される物理・社会・文化・経済・組織の制約を受けながら行動し、Thread / Scene においてイベントを発生させ、Emotional Curve によって感情変化を持ち、Timeline 上で状態遷移を行う。

System Architecture v2.0.1 において Character Model は World Model と同じ **World & Actor Layer** に属し、Narrative Logic Layer（Thread / Scene）へ行動主体として入力される。

v2.0.1 では以下の点が強化された。

- Multi-Graph Data Architecture との統合
- Character State（動的状態）の導入
- Goal / Motivation / Conflict モデル追加
- Character Arc と Emotional Curve 連携
- Ability / Skill / Inventory の導入
- World Model 参照の必須化
- Narrative Consistency 検証フック追加
- AI Authoring Interface 用 POV メタデータ追加

---

## 2. Core Attributes（基本属性）

Character の基本情報は静的属性として管理される。

### 2.1 Character Identity

主な情報:

- character_id
- name
- age
- gender
- species
- occupation
- organization_id
- culture_id
- home_location_id
- social_class
- description

Character は以下の World Model 要素を参照する。

- organization_id
- culture_id
- location_id
- world_rule_constraint

これによりキャラクターは世界の制約下で行動する。

---

### 2.2 Character Role

CharacterRole は物語における役割を定義する。

例:
- protagonist
- antagonist
- deuteragonist
- mentor
- ally
- enemy
- narrator
- observer

1人のキャラクターは複数の Role を持つことができる。

Role は Thread / Scene の進行ロジックに影響する。

---

### 2.3 Character Trait

CharacterTrait は性格・価値観・能力傾向・弱点・信念を管理する。

例:
- personality
- moral_alignment
- strengths
- weaknesses
- beliefs
- fears
- habits
- speech_style

Trait は以下に影響する。

- 行動選択
- Goal / Motivation
- Emotional Curve
- Narrative Consistency

---

### 2.4 Character Background

CharacterBackground はキャラクターの過去を管理する。

例:
- birthplace
- family
- education
- past_events
- trauma
- turning_points
- motivation_origin

Background は Timeline Model の過去 Event と関連付けられる。

---

## 3. Dynamic State（動的状態）

v2.0.1 では Character の現在状態を **Character_State** として管理する。

Character_State は Execution Flow に伴い変化する。

主な状態情報:

- current_location_id
- current_organization_id
- health_status
- mental_state
- social_status
- inventory
- wealth
- relationships_status
- emotional_state
- active_goal
- current_thread_id
- current_scene_id

Character_State は Timeline 上の状態遷移として記録される。

---

## 4. Drive & Logic（行動原理）

Character は Goal と Motivation によって行動する。

### 4.1 Goal

Character の目標を定義する。

例:
- survival
- revenge
- love
- power
- discovery
- escape
- protect_someone
- become_king

Goal は Thread（Conflict）発生の原因となる。

---

### 4.2 Motivation

Motivation は行動の心理的理由を定義する。

例:
- desire
- fear
- belief
- duty
- guilt
- curiosity
- ambition

Motivation は CharacterTrait と CharacterBackground に依存する。

---

### 4.3 Conflict

Character は以下の Conflict を持つ。

- internal_conflict
- external_conflict
- relationship_conflict
- social_conflict
- survival_conflict

Conflict は Thread Model と連動する。

---

### 4.4 Character Arc

Character Arc は物語を通じた変化を定義する。

例:
- growth
- fall
- redemption
- corruption
- enlightenment
- relationship_change
- ideology_change

Character Arc は Emotional Curve と Timeline Event によって表現される。

---

## 5. Relationships（関係性）

CharacterRelationship は Multi-Graph 上で Edge として管理される。

Relationship Edge の情報:

- relationship_type
- emotion_intensity
- trust_level
- hostility_level
- dependency
- history
- last_event_id

Relationship は時間経過とイベントによって変化する。

Relationship Edge の例:

- family
- friend
- mentor
- lover
- rival
- enemy
- subordinate
- leader

Relationship は Story ドラマ生成の重要な要素となる。

---

## 6. Capabilities（能力・スキル・資源）

Character は能力・スキル・資源を持つ。

### 6.1 Ability

WorldRule に依存する能力。

例:
- strength
- intelligence
- magic_power
- technical_skill
- leadership
- negotiation
- stealth
- combat_skill

---

### 6.2 Skill

訓練や経験によって習得した技能。

例:
- swordsmanship
- programming
- medicine
- diplomacy
- engineering
- magic_control
- investigation

---

### 6.3 Inventory / Resource

Character が所有する資源。

例:
- money
- weapons
- tools
- documents
- keys
- vehicles
- information
- political_power

Inventory は Character_State と連動する。

---

## 7. Cross-Model Mapping（モデル間連携）

Character Model は以下のモデルと連携する。

### 7.1 World Model
- organization_id
- culture_id
- location_id
- world_rule_constraint
- economy
- social_class

### 7.2 Thread Model
- participates_in_thread
- conflict_source
- goal_related_thread

### 7.3 Scene Model
- appears_in_scene
- current_location
- relationship_event
- emotional_event

### 7.4 Timeline Model
- birth_event
- background_event
- relationship_change_event
- injury_event
- promotion_event
- death_event

### 7.5 Emotional Curve Model
- emotional_state
- emotional_peak
- emotional_drop
- relationship_emotion_change

### 7.6 Narrative Consistency Model
- trait_action_consistency
- knowledge_consistency
- timeline_consistency
- relationship_consistency

Character は複数モデルの中心ノードとして機能する。

---

## 8. AI Support（AI Authoring Interface 連携）

AI がキャラクター視点で物語を生成するために以下の情報を保持する。

- voice_style
- vocabulary_level
- knowledge_scope
- personality_voice
- moral_view
- emotional_reaction_pattern
- decision_pattern
- narration_style
- dialogue_style
- memory_scope

AI はこれらを参照して以下を行う。

- POV 描写生成
- キャラクターらしい会話生成
- 行動提案
- 感情変化予測
- 関係性変化予測
- 設定矛盾検出

Character Model は AI にとって Actor Simulation Model として機能する。

---

## 9. まとめ

Character Model v2.0.1 は、NWF におけるキャラクターを静的な設定データではなく、世界の制約下で行動し、感情変化し、関係性を変化させ、Timeline 上で状態遷移する **動的エージェント** として定義するモデルである。

本モデルは以下を統合管理する。

- Identity / Role / Trait / Background
- Character State（動的状態）
- Goal / Motivation / Conflict
- Character Arc / Emotional Curve
- Relationships（Graph Edge）
- Ability / Skill / Inventory
- World / Thread / Scene / Timeline 連携
- Narrative Consistency 検証
- AI Authoring Interface POV 情報

Character Model は World Model と並び Story OS の World & Actor Layer の中核を構成し、Thread / Scene によって物語を実行する主体として機能する。

---

[EOF]