Source: docs/spec/Core_Spec/NWF_Thread_State_Model_v2.0.0.md
Updated: 2026-03-17T05:00:00+09:00
PIC: Engineer / ChatGPT

# NWF Thread State Model v2.0.0

---

## 1. 概要

Thread State Model は
物語内の Thread の進行状態を管理するモデルである。

Thread は常に特定の状態を持ち
Scene の進行に応じて状態が変化する。

---

## 2. Thread State の目的

Thread State は以下を管理する。

Thread の開始  
Thread の進行  
Thread の一時停止  
Thread の解決  

---

## 3. Thread State 定義

基本状態は以下である。

inactive  
Thread 未開始

active  
Thread 進行中

paused  
Thread 一時停止

resolved  
Thread 解決済

closed  
Thread 完全終了

---

## 4. State Transition

Thread 状態は以下のように遷移する。

inactive → active  
active → paused  
paused → active  
active → resolved  
resolved → closed  

---

## 5. Thread State JSON Example

例

{
  "thread_state": {
    "thread_id": "thread_main",
    "state": "active",
    "progress": 0.45,
    "related_scene_id": "scene_010"
  }
}

---

## 6. Scene との関係

Thread State は Scene の進行と連動する。

Scene が進むことで
Thread の状態が変化する。

例

Scene 1  
Thread 開始

Scene 10  
Thread 中盤

Scene 20  
Thread 解決

---

## 7. 関連 Spec

NWF_Thread_Graph_Model  
NWF_Scene_Model  
NWF_Timeline_Model  
NWF_Data_Model  

---

## 8. まとめ

Thread State Model は
物語の進行に伴う Thread の状態を管理する。

これにより
複数の物語ラインを体系的に制御できる。

---

[EOF]