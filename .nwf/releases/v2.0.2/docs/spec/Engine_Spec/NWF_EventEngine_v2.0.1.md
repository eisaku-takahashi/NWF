Source: docs/spec/Engine_Spec/NWF_EventEngine_v2.0.1.md
Updated: 2026-03-27T11:34:00+09:00
PIC: Engineer / ChatGPT

# NWF Event Engine v2.0.1

---

## 1. 概要

Event Engine は、NWF v2.0.1 (Story OS) における因果律の最小確定単位を生成する Dynamics Layer の中核エンジンである。

本エンジンは単なる出来事管理システムではなく、Story OS における「因果確定ノード生成器（Causal Node Generator）」として機能する。

Simulation Engine や Character 行動、Conflict 状態などから発生する「可能性」を、確定した事実（Event）へと変換し、以下のエンジンへ波及させる。

- Timeline Engine
- State Engine
- Beat Engine
- EmotionalCurve Engine
- Narrative Engine（間接的）
- Analysis Engine

Event Engine は Story OS における「変化の起点」「歴史の確定点」「因果連鎖のノード」を生成するエンジンである。

---

## 2. Core Architecture

### 2.1 Event Engine の役割

Event Engine の責務は以下である。

1. Event（確定した出来事）の生成
2. Event の分類
3. Event の発生条件判定
4. 因果リンクの構築
5. State Delta の算出
6. Timeline への Event 登録
7. Beat Engine への表現トリガー送信
8. EmotionalCurve Engine への Intensity 通知
9. Simulation Engine の確率イベントの確定
10. Event Chain（Thread）の形成

Event は Story OS における「確定した事実」を表す。

---

### 2.2 Event と Beat の責務分離

NWF v2.0.1 において Event と Beat は明確に分離される。

Event = 原因（Fact）
Beat = 表現（Action / Reaction）

例：

Event:
A が B を撃った

Beat:
銃を構える
引き金を引く
弾丸が飛ぶ
着弾する
B が倒れる
周囲が叫ぶ

構造モデル：

Event 発生 → Beat Engine が複数 Beat を生成 → Scene 内で表現

つまり、

Event = 論理構造
Beat = 演出構造

である。

---

### 2.3 Event と State の関係

Event は State Delta（状態差分）を算出し、State Engine に更新を要求する。

責務分離：

Event Engine:
- 何が起きたか
- 何がどう変わるべきか（State Delta）

State Engine:
- StateData の更新
- State 履歴管理
- Snapshot 管理
- 永続化

State Change の決定権は Event Engine が持つ。

---

### 2.4 Event の粒度と階層

Event は階層構造を持つ。

#### Atomic Event
最小単位の Event

例：
- 発言
- 攻撃
- 移動
- 発見
- 告白
- 裏切り
- 情報取得

#### Composite Event
複数の Atomic Event から構成される Event

例：
- 戦闘
- 交渉
- 逃走
- 革命
- 結婚
- 戦争
- 旅

Composite Event は内部に複数の Atomic Event を持つ。

---

### 2.5 Event と Thread / Scene の関係

関係定義：

Thread = Event Chain
Scene = Event Container

#### Thread
因果によって連結された Event の連鎖

Event A → Event B → Event C → Event D

これが Thread となる。

#### Scene
特定の時間・場所で発生する Event 群の容器

Scene 内に複数 Event が存在する。

Scene は空間時間単位
Event は因果単位

---

### 2.6 因果リンク構造（Causality Graph）

Event 同士は因果リンクで接続される。

構造は原則として DAG（有向非巡回グラフ）とする。

Event A → Event B → Event C
Event A → Event D
Event C → Event E

循環因果は禁止する。

これにより Timeline Engine と Analysis Engine が因果整合性を検証できる。

---

## 3. Event Data Specification

### 3.1 EventData フィールド定義

EventData は以下のフィールドを持つ。

- event_id
- event_type
- trigger_source
- participants
- location
- timestamp
- state_delta
- causality_link_id
- intensity
- importance
- scene_id
- thread_id
- branch_id
- atomic_or_composite
- parent_event_id
- child_event_ids

---

### 3.2 Event Classification（分類体系）

Event は以下の分類を持つ。

#### Physical Event
物理的変化
例：
- 攻撃
- 破壊
- 移動
- 死亡
- 負傷

#### Psychological Event
心理的変化
例：
- 恋に落ちる
- 決意する
- 絶望する
- 疑う
- 信じる

#### Social Event
社会的変化
例：
- 結婚
- 裏切り
- 同盟
- 昇進
- 逮捕
- 戦争開始

#### Information Event
情報変化
例：
- 秘密を知る
- 正体がバレる
- 手紙を読む
- 記録を発見
- 嘘を知る

この分類は EmotionalCurve や Analysis Engine で使用される。

---

### 3.3 Event 制約ルール

EventData は以下の制約を持つ。

1. 全 Event は timestamp を持つ
2. 全 Event は thread_id を持つ
3. Event は最低 1 つの causality_link を持つ（最初の Event を除く）
4. Atomic Event は親 Event を持つ場合がある
5. Composite Event は child_event_ids を持つ
6. State Delta を持たない Event も存在可能
7. intensity は 0.0 〜 1.0
8. importance は 0.0 〜 1.0
9. Event は必ず Scene に属する
10. Event は Branch Timeline に属する

---

## 4. Operational Algorithms

### 4.1 Event 生成アルゴリズム

Event 生成の基本フロー：

1. Trigger Condition 検出
2. Condition Check
3. Event Type 決定
4. Participants 決定
5. Location 決定
6. Timestamp 取得（Timeline Engine）
7. Causality Link 作成
8. State Delta 算出
9. Event Intensity 計算
10. Event Importance 計算
11. EventData 生成
12. Timeline Engine へ登録
13. State Engine へ State Delta 送信
14. Beat Engine へ表現トリガー送信
15. EmotionalCurve Engine へ通知
16. Thread 更新

この処理により Event が確定した歴史として登録される。

---

### 4.2 State Delta 算出プロセス

State Delta とは Event による状態差分である。

例：

HP: 100 → 40
Relationship: Friendly → Enemy
Location: City → Forest
Status: Alive → Dead
Knowledge: Unknown → Known

State Delta は以下の形式を持つ。

- state_id
- old_value
- new_value
- change_magnitude
- affected_entity

State Engine はこの Delta を適用して StateData を更新する。

---

### 4.3 因果リンク構築ロジック

Event Engine は Event 間の因果関係を管理する。

リンク種類：

- cause_of
- triggered_by
- enables
- prevents
- parallel_to
- consequence_of

因果グラフは DAG として管理される。

---

## 5. Engine Integration

### 5.1 Timeline Engine 連携

Event Engine → Timeline Engine

送信データ：
- event_id
- timestamp
- causality_order
- branch_id
- scene_id
- thread_id

Timeline Engine は時間整合性を保証する。

---

### 5.2 State Engine 連携

Event Engine → State Engine

送信データ：
- state_delta
- event_id
- timestamp

State Engine は State を更新し履歴を保存する。

---

### 5.3 Beat Engine 連携

Event 発生後、Beat Engine が表現用 Beat を生成する。

Event → Beat Generator → Beat Sequence → Scene

Event は Beat の原因となる。

---

### 5.4 EmotionalCurve Engine 連携

Event Engine は EmotionalCurve Engine に以下を送信する。

- event_intensity
- event_importance
- state_delta
- event_type
- conflict_relation

EmotionalCurve Engine はこれを用いて感情曲線を更新する。

---

### 5.5 Simulation Engine 連携

Simulation Engine は確率的未来を生成する。

Event Engine は以下を行う。

- 確率イベントの確定
- 分岐 Event の生成
- Branch Timeline 作成
- Event Chain 分岐
- 非採用 Event のアーカイブ

つまり、

Simulation = 可能性
Event = 確定した歴史

という関係になる。

---

## 6. Execution Lifecycle

Event Engine の実行サイクル：

1. Trigger 発生
2. Condition Check
3. Event 生成
4. Causality Link 構築
5. State Delta 算出
6. Timeline 登録
7. State 更新要求
8. Beat Trigger
9. EmotionalCurve 通知
10. Thread 更新
11. Branch 処理
12. Consistency Check
13. Event 確定
14. History 登録

このサイクルにより世界の歴史が形成される。

---

## 7. Maintenance & Versioning

Event Engine は以下の Data Spec に依存する。

- Data_Spec_v2.0.1
- EventData
- StateData
- TimelineData
- ThreadData
- SceneData
- CharacterData
- BranchData
- ConflictData

以下の変更があった場合 Version を更新する。

- EventData 構造変更
- Event Classification 変更
- State Delta 構造変更
- Causality Graph 構造変更
- Simulation Integration 変更
- Thread/Event 関係変更

---

## 8. まとめ

Event Engine は Story OS において以下を担う。

- 出来事の確定
- 因果連鎖の構築
- State Change の起点
- Timeline の構成単位生成
- Beat の原因生成
- EmotionalCurve のトリガー生成
- Simulation の確率未来を歴史へ変換
- Thread（Event Chain）の形成

Event Engine は Story OS における「因果の心臓」であり、
世界の不確実性を確定した歴史へ変換する最重要 Dynamics Engine である。

---

[EOF]