Source: docs/spec/Data_Spec/NWF_SceneData_v2.0.1.md
Updated: 2026-03-25T01:55:00+09:00
PIC: Engineer / ChatGPT

# NWF SceneData v2.0.1

---

## 1. 概要

SceneData は NWF における Scene（シーン）を定義するデータ構造であり、物語シミュレーションにおける **最小実行単位（Story Execution Unit）** を表す。

NWF v2.0.0 では Scene は場面情報の記述データとして扱われていたが、v2.0.1 では Story OS アーキテクチャへの移行に伴い、Scene は入力状態（Pre-conditions）を処理し、出力状態（Post-conditions）を生成する「状態遷移命令」として再定義される。

Scene は Thread の内部で実行され、Character、World、Timeline、Causality、Emotional Curve に影響を与え、物語の状態を更新する。

---

## 2. Core Metadata

Scene の基本メタデータを定義する。

主な項目：

- scene_id  
  シーンの一意識別子。

- scene_title  
  シーンの名称。

- thread_id  
  所属する Thread ID。

- location_id  
  シーンが発生する場所 ID。

- narrative_order  
  読者に提示される順序（語り順）。

- execution_step  
  シミュレーションエンジンが実行する順序。

Scene は Narrative Order（語り順）と Execution Step（実行順）を独立して持つ。

---

## 3. Temporal & Causal Data

Scene の時間情報および因果関係を定義する。

主な要素：

- timeline_start_node  
  シーン開始の Timeline ノード。

- timeline_end_node  
  シーン終了の Timeline ノード。

- duration_story_time  
  物語内時間での継続時間。

- causality_links  
  原因となる Event / Scene、および結果として発生する Event / Scene のリンク。

Scene は Timeline 上の時間範囲を占有し、因果関係グラフのノードとして扱われる。

---

## 4. Participants

Scene に関与するキャラクターおよび、そのシーン内での目的を定義する。

主な要素：

- involved_characters  
  登場キャラクター ID のリスト。

- local_objectives  
  各キャラクターがそのシーンで達成しようとしている目標。

- relationships_affected  
  このシーンで変化する人間関係。

Scene はキャラクターの目的・対立・協力によって進行する。

---

## 5. Execution Logic

Scene 実行のための条件および実行後の状態変化を定義する。

### 5.1 Pre-conditions（開始条件）

Scene が開始されるために必要な条件。

例：

- world_state_flags
- character_status
- location_presence
- timeline_condition
- previous_scene_completed
- thread_state
- item_possession

### 5.2 Post-conditions（状態変化）

Scene 実行によって発生する状態変化（差分）。

例：

- character_state_changes
- relationship_changes
- world_state_changes
- new_flags_set
- flags_removed
- thread_progress
- timeline_updates

Scene は状態変化の差分（Delta）を生成する命令として扱う。

---

## 6. Narrative Dynamics

Scene の物語的役割および感情的影響を定義する。

主な要素：

- scene_objective  
  シーン全体として達成すべき目的。

- conflict  
  シーン内の対立構造。

- tension_level  
  緊張度（数値または段階）。

- emotional_impact  
  読者・キャラクターへの感情的影響。

- emotional_curve_effect  
  Emotional Curve への影響。

Scene は物語のテンションと感情曲線を生成する単位として扱う。

---

## 7. Event List

Scene を構成する具体的な出来事（Event / Beat）への参照を定義する。

主な要素：

- events  
  シーン内で発生するイベント ID のリスト。

- beats  
  シーン内のビート（小イベント）の順序付きリスト。

- event_order_logic  
  イベントの実行順序ロジック。

Scene は複数の Event / Beat の集合として構成される。

---

## 8. Navigation & Branching

Scene 終了後の遷移および分岐条件を定義する。

主な要素：

- next_scene_candidates  
  次に遷移可能な Scene ID のリスト。

- branch_conditions  
  分岐条件（Success / Failure / Flag / Character State など）。

- triggers  
  特定条件で自動的に開始される Scene のトリガー。

- exclusive_scenes  
  同時に発生できない Scene。

Scene は直線的な構造だけでなく、分岐・並行・条件遷移を持つ。

---

## 9. まとめ

NWF SceneData v2.0.1 では Scene を

「場面の記述」
ではなく
「状態変化を発生させる実行命令」

として再定義した。

Scene は以下の要素に影響を与える。

- Character State
- Relationship
- World State
- Thread Progress
- Timeline
- Causality Graph
- Emotional Curve
- Narrative Order

SceneData は Story OS において、
物語世界の状態を更新する最小実行単位として機能する。

---

[EOF]