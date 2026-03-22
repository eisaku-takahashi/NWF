Source: docs/spec/Core_Spec/NWF_Thread_State_Model_v2.0.1.md
Updated: 2026-03-22T13:43:00+09:00
PIC: Engineer / ChatGPT

# NWF Thread State Model v2.0.1

---

## Validation Result

### 1. Terminology Issues
Thread State / Scene / Timeline / State Transition などの用語は Glossary v2.0.1 に統一。
「進行」「解決」などの曖昧語は状態名ではなく説明文に限定。

### 2. ID / Reference Issues
すべての参照IDは Entity ID System v2.0.1 の Prefix を使用する。
thread_id
scene_id
timeline_id
state_id
parent_thread_id

### 3. Data Structure Issues
Thread の実行状態と履歴ログを分離する必要がある。
execution_control と history_log を分離した構造に変更。

### 4. State Machine Logic Issues
Thread State は State Model + State Transition Model に従う。
Thread 固有の状態は State Entity のインスタンスとして扱う。

### 5. Dependency Issues
本モデルは以下 Spec に依存する。
NWF_State_Model
NWF_State_Transition_Model
NWF_Scene_Model
NWF_Thread_Graph_Model
NWF_Timeline_Model
NWF_Story_Database

### 6. Missing Fields / Concepts
以下の概念を追加した。
current_scene_id
parent_thread_id
branch_condition
timeline_id
priority
execution_pointer
state_history

### 7. Required Changes for v2.0.1
Thread を「Scene Graph 上を移動するポインタ」として再定義。
Thread State を State Machine に統合。
Timeline との同期機構を追加。
Execution Control / History Log 分離。

### 8. Updated Model Proposal (v2.0.1)
Thread は Scene Graph 上を移動する実行ポインタであり、
状態(State)・現在位置(Scene)・時間軸(Timeline)・分岐情報を保持する。

### 9. Updated JSON Example
下記参照。

### 10. Summary
Thread State Model は
Thread の状態管理モデルから
Thread Execution Control Model へ拡張された。

---

## 1. 概要

Thread State Model は
Thread の状態・進行位置・時間軸・分岐情報を管理するモデルである。

Thread は Scene Graph 上を移動するポインタとして動作する。

---

## 2. Thread State の目的

Thread State Model は以下を管理する。

Thread の状態
現在の Scene
Timeline 位置
Thread 分岐
実行優先度
実行履歴
状態履歴

---

## 3. Thread の基本概念

Thread は以下の要素を持つ。

Thread = Execution Pointer + State + Timeline + Branch Info

Thread は Scene Graph 上を移動するポインタであり、
Scene 遷移によって物語が進行する。

---

## 4. Thread State 定義

Thread の基本状態は以下とする。

latent
開始待機状態

active
実行中

paused
一時停止

resolved
解決済

closed
終了

これらの状態は State Model により管理され、
State Transition Model に従って遷移する。

---

## 5. Thread Execution Control

Thread Execution Control は以下の情報を管理する。

thread_id
state_id
current_scene_id
timeline_id
parent_thread_id
branch_condition
priority
execution_pointer

---

## 6. Timeline との同期

Thread は必ず Timeline に紐付く。

1 Thread = 1 Timeline

Timeline によって
Scene の時間順序
Thread の実行順序
Event 発生順序
が管理される。

---

## 7. Thread History / Log

Thread は以下の履歴を保持する。

scene_history
state_history
event_history
transition_history

これにより
物語進行ログを完全に再現可能になる。

---

## 8. Thread State JSON Schema

例

{
  "thread_state": {
    "thread_id": "thread_main_001",
    "execution_control": {
      "state_id": "state_active",
      "current_scene_id": "scene_010",
      "timeline_id": "timeline_main",
      "parent_thread_id": null,
      "branch_condition": null,
      "priority": 1,
      "execution_pointer": "scene_010"
    },
    "history_log": {
      "scene_history": [
        "scene_001",
        "scene_005",
        "scene_010"
      ],
      "state_history": [
        "state_latent",
        "state_active"
      ],
      "event_history": [],
      "transition_history": []
    }
  }
}

---

## 9. 関連 Spec

NWF_State_Model
NWF_State_Transition_Model
NWF_Scene_Model
NWF_Thread_Graph_Model
NWF_Timeline_Model
NWF_Story_Database_Model

---

## 10. まとめ

Thread State Model v2.0.1 では
Thread を単なる状態管理ではなく
Scene Graph 上を移動する実行ポインタとして定義した。

Thread は以下の要素を統合管理する。

State
Scene Position
Timeline
Branch
Execution Control
History Log

これにより
マルチスレッド物語制御
分岐物語
時間軸分離
物語シミュレーション
が可能になる。

---

[EOF]