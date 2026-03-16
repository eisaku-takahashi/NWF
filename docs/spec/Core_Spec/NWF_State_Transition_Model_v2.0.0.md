Source: docs/spec/Core_Spec/NWF_State_Transition_Model_v2.0.0.md
Updated: 2026-03-17T05:10:00+09:00
PIC: Engineer / ChatGPT

# NWF State Transition Model v2.0.0

---

## 1. 概要

State Transition Model は
NWF における状態変化のルールを定義するモデルである。

Thread・Character・World などの状態は
Event によって変化する。

---

## 2. 状態遷移の目的

状態遷移は以下を管理する。

Thread 進行  
Character 状態変化  
世界状態の変化  

---

## 3. State Transition 構造

基本構造

state_transition

  source_state  
  trigger_event  
  target_state  

---

## 4. State Transition JSON Example

{
  "state_transition": {
    "source_state": "active",
    "trigger_event": "conflict_resolved",
    "target_state": "resolved"
  }
}

---

## 5. 関連 Spec

NWF_Thread_State_Model  
NWF_Event_Model  
NWF_Conflict_Model

---

## 6. まとめ

State Transition Model は
物語の状態変化ルールを定義する。

Event をトリガーとして
Thread や Character の状態が変化する。

---

[EOF]