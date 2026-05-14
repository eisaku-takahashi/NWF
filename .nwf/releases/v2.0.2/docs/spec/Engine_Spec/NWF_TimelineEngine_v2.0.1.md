Source: docs/spec/Engine_Spec/NWF_TimelineEngine_v2.0.1.md
Updated: 2026-03-27T10:46:00+09:00
PIC: Engineer / ChatGPT

# NWF Timeline Engine v2.0.1

---

## 1. 概要

Timeline Engine は、NWF v2.0.1 (Story OS) における時間管理システムであり、物語世界の時間そのものを統治する Structural Layer の中核エンジンである。

本エンジンは単なる年表生成機能ではなく、Story OS における Temporal OS Kernel（時間カーネル）として機能し、以下を実現する。

- 物語世界の実時間（Story Time）の管理
- 語りの順序（Narrative Time）の管理
- Scene / Event 内の局所時間（Local Time）の管理
- 状態変化の時間履歴管理（State History）
- 時間的因果関係の整合性検証
- 分岐タイムラインの管理
- Narrative Engine への時間表現メタデータ提供

Timeline Engine は Story OS において「歴史」「因果律」「時間整合性」を保証する基盤システムである。

---

## 2. Core Architecture

### 2.1 Timeline Engine の役割

Timeline Engine は以下のデータを統治する。

- TimelineData
- EventData
- SceneData
- StateData の時間履歴
- Branch Timeline
- Narrative Time Mapping

本エンジンは Structural Layer に属し、世界の時間構造そのものを管理する。

---

### 2.2 Multilayer Temporal Structure（多層時間構造）

Timeline Engine は時間を以下の 3 層で管理する。

1. Story Time（物語世界の実時間）
2. Narrative Time（語り順・提示順）
3. Local Time（Scene / Event 内部時間）

#### Story Time
- 世界内で実際に起きた順序
- 因果関係の基準時間
- 年月日・時刻などの絶対時間

#### Narrative Time
- 読者に提示される順序
- 回想、予兆、並行描写を含む
- Scene の並び順

#### Local Time
- Scene 内の時間
- Event 内の時間
- 戦闘、会話、数分間の出来事など

これら 3 層は独立して管理されるが、Timeline Engine によって相互にマッピングされる。

---

### 2.3 Chronological vs Narrative Mapping

Timeline Engine は以下の対応関係を管理する。

- Scene → Story Time 上の位置
- Scene → Narrative Order
- Event → Story Time
- Event → Scene

これにより以下を実現する。

- Flashback（回想）
- Flashforward（未来描写）
- Parallel Events（並行イベント）
- Non-linear Story（非線形物語）

提示順序が変更されても、Story Time 上の因果関係は常に維持される。

---

### 2.4 TimelineData

Timeline Engine が扱う主要データ。

TimelineData に含まれる情報：

- event_id
- story_time_timestamp
- narrative_order
- scene_id
- branch_id
- state_change_log
- relative_time_tags
- time_gap
- character_age
- calendar_date
- weekday

TimelineData は Story OS における時間情報の単一ソース（Single Source of Truth）となる。

---

## 3. Operational Algorithms

### 3.1 Timeline Data Operations

Timeline Engine は以下の基本操作を提供する。

#### Time Assignment
新規 Event に対して Story Time のタイムスタンプを割り当てる。

処理内容：
- 前後イベントとの整合性確認
- 年齢計算
- Time Gap 計算
- Calendar Date 更新

#### Chronological Sorting
全 Event を Story Time 順に並び替える。

用途：
- 年表生成
- 歴史順確認
- 因果関係検証

#### Narrative Mapping
Scene / Event を Narrative Time にマッピングする。

用途：
- 回想配置
- 並行描写
- 章構成
- 物語テンポ調整

---

### 3.2 State History Tracking（状態履歴追跡）

Timeline Engine は StateData の全変更履歴を時間と共に記録する。

対象 State：
- Character State
- World State
- Relationship State
- Political State
- Technology State
- Location Control State

記録内容：
- state_id
- old_value
- new_value
- change_event_id
- story_time
- branch_id

これにより以下が可能になる。

- 任意時点の世界状態復元
- キャラクター状態履歴確認
- 分岐世界の状態比較
- Simulation Engine の履歴管理

これを State Snapshot System と呼ぶ。

---

### 3.3 Branch & Merge Management

Simulation Engine により IF 分岐が発生した場合、Timeline Engine は分岐タイムラインを生成する。

#### Branch Timeline
- branch_id
- parent_timeline_id
- branch_start_time
- branch_events
- branch_states

#### Merge Timeline
特定ルート確定時に以下を行う。

- 採用 Timeline の確定
- 非採用 Timeline のアーカイブ
- StateData の統合
- TimelineData の再構築

これにより Story Simulation と Timeline の整合性が維持される。

---

### 3.4 Temporal Calculation Engine

Timeline Engine は時間に関する計算機能を持つ。

計算対象：

- Character Age Calculation
- Time Gap Calculation
- Calendar Date Calculation
- Weekday Calculation
- Duration Calculation
- Relative Time Calculation

例：

- Event A → Event B の経過日数
- キャラクター年齢
- 戦争期間
- 旅の所要時間
- 季節
- 曜日

これにより世界の時間リアリティが維持される。

---

### 3.5 Relative Time Tags

Narrative Engine に時間表現を渡すため、Timeline Engine は Relative Time Tags を生成する。

例：

- three_days_later
- the_previous_night
- at_the_same_time
- one_year_ago
- meanwhile
- immediately_after
- long_after
- during_the_war
- before_the_accident

Narrative Engine はこれを利用して文章中の時間表現を生成する。

---

## 4. Consistency & Validation

Timeline Engine は時間的整合性を検証するガードレール機能を持つ。

### 4.1 Temporal Consistency Check

検出対象：

- 死亡後に行動している
- 怪我前に治っている
- 存在しない場所にいる
- 生まれる前に登場している
- Event の因果順序が逆
- 並行イベントの時間衝突
- 年齢計算矛盾
- 技術レベル矛盾
- 歴史改変矛盾
- 分岐 Timeline の整合性崩壊

エラーは Analysis Engine に送信される。

---

### 4.2 Guardrail Rules

Timeline Engine の基本ルール：

1. Event は必ず Story Time を持つ
2. State Change は必ず Event に紐付く
3. Narrative Order は Story Time を変更しない
4. Flashback は Story Time を過去に配置する
5. Parallel Event は同一 Story Time を共有可能
6. Branch Timeline は親 Timeline を継承する
7. Merge 時に State 矛盾を解決する
8. Character Age は Story Time に依存する
9. Calendar は Story Time から自動計算
10. TimelineData は全 Engine の参照基準となる

---

## 5. Engine Integration

### 5.1 Simulation Engine 連携

Simulation Engine → Timeline Engine

- 分岐イベント生成
- Timeline Branch 作成
- 状態履歴記録
- Merge Timeline
- シミュレーション履歴保存

Timeline Engine → Simulation Engine

- 過去状態復元
- Timeline 分岐位置提供
- 因果関係情報提供

---

### 5.2 Narrative Engine 連携

Timeline Engine → Narrative Engine

提供データ：

- Narrative Order
- Relative Time Tags
- Calendar Date
- Character Age
- Time Gap
- 同時イベント情報
- 時系列メタデータ

Narrative Engine はこれを利用して自然な時間表現を生成する。

---

### 5.3 Analysis Engine 連携

Timeline Engine → Analysis Engine

- Temporal Consistency Error
- Timeline Conflict
- Age Conflict
- Event Order Conflict
- Parallel Event Conflict
- Branch Conflict

Analysis Engine は物語構造上の問題として報告する。

---

## 6. Execution Lifecycle

Timeline Engine の実行サイクル：

1. Event 作成
2. Time Assignment
3. Chronological Sorting
4. State Change 記録
5. State History 更新
6. Temporal Calculation
7. Narrative Mapping
8. Relative Time Tag 生成
9. Consistency Check
10. TimelineData 更新
11. Engine 連携
12. 年表・履歴更新

このサイクルにより Story OS の時間構造が維持される。

---

## 7. Maintenance & Versioning

Timeline Engine は以下の Data Spec に依存する。

- Data_Spec_v2.0.1
- TimelineData
- EventData
- SceneData
- StateData
- BranchData
- CalendarData
- CharacterData

データ構造変更時は Timeline Engine のバージョンを更新する。

Version 管理対象：

- TimelineData Structure
- Temporal Algorithms
- Consistency Rules
- Branch Management Logic
- Relative Time Tag System
- Calendar System
- Age Calculation System

---

## 8. Summary

Timeline Engine は Story OS における時間管理カーネルであり、以下を統治する。

- Story Time（実時間）
- Narrative Time（語り順）
- Local Time（局所時間）
- Event Timeline
- State History
- Branch Timeline
- Temporal Calculation
- Relative Time Expression
- Temporal Consistency
- Historical Integrity

Timeline Engine は Story OS の「歴史」「因果律」「時間整合性」を保証する最も基盤的な Structural Engine である。

---

[EOF]