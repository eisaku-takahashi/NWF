Source: docs/spec/Data_Spec/NWF_TimelineData_v2.0.1.md
Updated: 2026-03-25T00:38:00+09:00
PIC: Engineer / ChatGPT

# NWF TimelineData v2.0.1

---

## 1. 概要

TimelineData は Story OS（Narrative World Framework v2.0.1）における時間構造を管理するデータモデルである。

本バージョンでは TimelineData を、従来の「出来事や Scene の時間配置を管理するデータ」ではなく、
物語の実行、因果関係、語りの順序、並行イベント、分岐シミュレーションを統合的に制御する
**時間シミュレーション・データモデル（Temporal Simulation Data Model）** として再定義する。

TimelineData は Story OS において以下の役割を持つ。

- 物語世界の時間構造の定義
- Scene / Event / Thread の時間配置
- 因果関係の管理
- 回想・倒叙など語り順序の管理
- 並行イベントの管理
- 分岐タイムライン・IF シミュレーションの管理
- Temporal Consistency（時間整合性）の検証
- Execution Step と連動した時間更新

TimelineData は Story OS の時間的整合性と物語構造を支える基盤データである。

---

## 2. Time System Definitions（時間システム定義）

Story OS では時間を 4 種類の時間軸として管理する。

### 2.1 Absolute Time

世界設定上の絶対時間（暦・年・月・日・時刻など）を表す。
世界史、文明、季節、年齢計算などに使用される。

主な用途：

- キャラクターの年齢計算
- 歴史イベント管理
- 季節・昼夜・環境変化
- 世界設定との整合性

---

### 2.2 Story Time

物語内でキャラクターが体験する時間の流れを表す。
Scene や Event の経過時間、移動時間、待機時間などを管理する。

主な用途：

- Scene の時間長
- Thread の経過時間
- キャラクターの行動時間
- 移動時間や休息時間
- ストーリー全体の時間経過

---

### 2.3 Narrative Order

読者に提示される順序（語りの順序）を表す。
回想、倒叙、時間跳躍などを管理する。

主な用途：

- Flashback（回想）
- Flashforward（未来描写）
- 非線形ストーリー構造
- ミステリの情報提示順序
- 伏線提示タイミング

Narrative Order は Story Time や Absolute Time と一致しない場合がある。

---

### 2.4 Execution Step

Story OS のシミュレーション実行ステップを表す時間軸である。
Execution Flow の各ステップで Story State が更新される。

主な用途：

- Simulation Step
- Engine 実行順序管理
- State Update タイミング
- What-if Simulation
- Story Branch Simulation

Execution Step は Story OS の内部時間である。

---

## 3. Timeline Graph Architecture

TimelineData は Timeline Graph として管理される。

Timeline Graph は以下の要素で構成される。

### 3.1 Timeline Node

Timeline Node は時間上の点または期間を表す。

主なノードタイプ：

- event_node: 出来事
- scene_node: Scene
- thread_node: Thread 区間
- time_marker_node: 時点
- flashback_anchor_node: 回想アンカー
- branch_point_node: 分岐点

Node の主な属性：

- node_id
- node_type
- absolute_time
- story_time_start
- story_time_end
- narrative_order_index
- execution_step
- location
- related_characters

---

### 3.2 Timeline Edge

Timeline Node 同士を接続する Edge を定義する。

主な Edge タイプ：

- sequence_edge: 時系列順序
- causality_edge: 因果関係
- parallel_edge: 並行イベント
- branch_edge: 分岐タイムライン
- flashback_edge: 回想リンク
- flashforward_edge: 未来リンク

Edge の主な属性：

- edge_id
- edge_type
- source_node_id
- target_node_id
- causality_strength
- time_offset
- dependency_type

Timeline Graph により時間構造と因果関係を統合的に管理する。

---

## 4. Temporal State Data

TimelineData では以下の時間状態データを管理する。

### 4.1 Scene / Event Time Range

- scene_id
- start_story_time
- end_story_time
- duration
- location
- participating_characters

### 4.2 Character Personal Time

各キャラクターの個別時間を管理する。

主な項目：

- character_id
- age
- personal_time_elapsed
- last_appearance_time
- subjective_time
- sleep_time
- travel_time

Character Personal Time により
キャラクターごとの時間整合性を管理する。

### 4.3 Thread Time

Thread 単位の時間範囲を管理する。

主な項目：

- thread_id
- start_time
- end_time
- total_duration
- related_scenes

---

## 5. Causality & Consistency

TimelineData は因果関係と時間整合性を管理する。

### 5.1 Causality Links

出来事の原因と結果をリンクする。

主な項目：

- cause_event_id
- effect_event_id
- causality_type
- dependency_strength
- required_conditions
- blocking_conditions

これにより因果関係の破綻を検出できる。

---

### 5.2 Temporal Consistency Data

時間整合性チェックのためのデータ。

主なチェック項目：

- 同時刻の重複行動
- 移動時間の不足
- 年齢・時間経過の矛盾
- 因果逆転
- 存在しない時間でのイベント
- Flashback の論理矛盾

主なデータ項目：

- time_constraints
- location_constraints
- character_availability
- paradox_flags
- timeline_consistency_state

---

## 6. Multi-Track Management

TimelineData は複数の時間トラックを管理する。

### 6.1 Parallel Events

同時進行イベントの管理。

- parallel_event_group_id
- event_list
- synchronization_point
- merge_event

### 6.2 Branch Timeline

分岐タイムラインや IF シミュレーションを管理する。

- branch_id
- branch_point_node
- branch_condition
- branch_timeline_reference
- merge_condition

### 6.3 Flashback / Flashforward

回想や未来描写を管理する。

- flashback_anchor_node
- flashforward_anchor_node
- narrative_position
- actual_time_reference
- memory_owner_character

Narrative Order と Story Time の不一致をここで管理する。

---

## 7. Execution Flow Integration

TimelineData は Execution Flow と連動する。

Execution Step ごとに以下が更新される。

- current_execution_step
- current_story_time
- active_scenes
- active_events
- character_current_time
- scheduled_events
- next_event_queue

Execution Flow における時間更新の流れ：

Execution Step
→ Time Advance
→ Scheduled Event Check
→ Scene Start / End
→ Character Time Update
→ Emotional Timeline Update
→ Story State Update

TimelineData は Story Simulation の時間制御システムとして機能する。

---

## 8. AI Interface Metadata

AI Authoring Interface で時間経過を表現するためのメタデータ。

主な項目：

- time_of_day
- season
- weather
- environment_state
- character_age_stage
- fatigue_level
- time_skip_flag
- pacing_control_parameter

これらは文章生成時の描写制御に使用される。

---

## 9. まとめ

TimelineData v2.0.1 は
従来の時間管理データではなく、
Story OS における時間シミュレーションシステムの中核データモデルである。

TimelineData は以下を統合する。

- Absolute Time（世界時間）
- Story Time（物語時間）
- Narrative Order（語り順序）
- Execution Step（シミュレーション時間）
- Timeline Graph（時間ノード・因果関係）
- Character Personal Time（キャラクター時間）
- Parallel / Branch Timeline（並行・分岐）
- Flashback / Flashforward（時間跳躍）
- Temporal Consistency（時間整合性）
- Execution Scheduling（時間スケジューリング）

TimelineData は Story OS における
時間・因果・順序・整合性を統合的に管理する基盤データである。

---

[EOF]