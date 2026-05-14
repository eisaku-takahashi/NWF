Source: docs/spec/Data_Spec/NWF_ThreadData_v2.0.1.md
Updated: 2026-03-25T01:15:00+09:00
PIC: Engineer / ChatGPT

# NWF ThreadData v2.0.1

---

## 1. 概要

ThreadData は NWF における「Thread（スレッド）」を定義するデータ構造であり、物語における特定の目的・対立・状態変化を持つ **物語シミュレーション実行単位（Story Simulation Unit）** を表す。

NWF v2.0.0 では Thread は主に Scene の集合として扱われていたが、v2.0.1 では Story OS アーキテクチャへの移行に伴い、Thread は単なるストーリーラインではなく、物語内の状態変化を駆動する「実行パッケージ」として再定義される。

Thread は Timeline、Character、WorldState、Causality、Emotional Curve など複数のシステムを束ね、物語の進行を計算・実行するための中核単位となる。

---

## 2. Core Information

Thread の基本情報を定義する。

主な項目：

- thread_id  
  スレッドの一意識別子。

- thread_title  
  スレッドの名称。

- description  
  スレッドの概要説明。

- plot_structure_role  
  物語構造上の役割。  
  例：Setup, Inciting Incident, Rising Action, Midpoint, Climax, Resolution など。

- importance_level  
  物語全体に対する重要度（数値または段階）。

Thread は単なる補助イベントではなく、物語構造上の役割を持つ単位として扱う。

---

## 3. Simulation Constraints

Thread の開始条件および終了条件を定義する。
これは Execution Flow における実行可否判定に使用される。

### 3.1 Pre-conditions（開始条件）

Thread が開始可能になる条件。

例：

- world_state_flag
- character_state
- 他 Thread の完了フラグ
- timeline 条件
- 特定 Event の発生

### 3.2 Post-conditions（終了条件 / 成功条件）

Thread 完了時に世界やキャラクターに発生する状態変化。

例：

- world_state_change
- character_relationship_change
- new_flag_set
- item_acquired
- next_thread_unlocked

Thread は「開始条件 → 実行 → 状態変化 → 次の Thread 解放」
というシミュレーション構造を持つ。

---

## 4. Participants & Motivation

Thread に関与するキャラクターおよび、そのスレッドにおける目的を定義する。

主な要素：

- involved_characters  
  関与キャラクター ID のリスト。

- character_objectives  
  各キャラクターの目的。

- motivations  
  行動動機。

- relationships_affected  
  この Thread によって変化する人間関係。

Thread はキャラクターの目的と動機の衝突・協力によって進行する。

---

## 5. Temporal & Causal Data

Thread と Timeline、および他 Thread との因果関係を定義する。

主な要素：

- timeline_start_node
- timeline_end_node
- duration_story_time
- dependencies  
  この Thread が開始するために完了している必要がある Thread。

- unlocks_threads  
  この Thread 完了後に開始可能になる Thread。

- causality_links  
  原因・結果として関連する Event / Thread。

Thread は Timeline 上の期間を持ち、因果関係ネットワークの一部として管理される。

---

## 6. Dynamic Force Data

Thread 内で発生する対立・緊張・感情変化を定義する。

主な要素：

- conflict_type  
  対立の種類（Character vs Character, Character vs World など）。

- tension_type  
  緊張の種類（Mystery, Suspense, Action, Drama など）。

- tension_intensity  
  緊張の強度。

- emotional_arc_effect  
  Emotional Curve への影響。

Thread は物語の「力学（Dynamic Forces）」を発生させる単位として扱う。

---

## 7. Thread Lifecycle

Thread の状態遷移および分岐管理を定義する。

主な状態：

- planned
- active
- suspended
- completed
- failed
- branched

また、以下の要素を管理する：

- branch_condition  
  分岐条件。

- parallel_threads  
  並行して進行可能な Thread。

- exclusive_threads  
  同時に実行できない排他 Thread。

Thread Lifecycle は物語の進行制御および IF 分岐シミュレーションに使用される。

---

## 8. Scene & Beat Aggregation

Thread を構成する Scene および Beat を管理する。

主な要素：

- scenes  
  Thread を構成する Scene ID の順序付きリスト。

- beats  
  Scene 内の Beat（小イベント）参照。

- scene_order_logic  
  Scene の順序制御ロジック（固定 / 条件分岐 / ランダム 等）。

Thread は Scene の単なるリストではなく、
「状態変化を発生させる Scene の集合」として扱われる。

---

## 9. まとめ

NWF ThreadData v2.0.1 では Thread を

「ストーリーライン」
ではなく
「物語シミュレーション実行単位」

として再定義した。

Thread は以下を統合する中核データである。

- Timeline
- Character
- World State
- Causality
- Emotional Curve
- Plot Structure
- Scene / Beat

ThreadData は Story OS において、
物語を計算・実行・分岐・進行させるための中心的なデータモデルとなる。

---

[EOF]