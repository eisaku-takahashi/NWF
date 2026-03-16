Source: docs/spec/Core_Spec/NWF_Conflict_Model_v2.0.0.md
Updated: 2026-03-17T05:10:00+09:00
PIC: Engineer / ChatGPT

# NWF Conflict Model v2.0.0

---

## 1. 概要

Conflict Model は
物語における対立構造を管理するモデルである。

Conflict は Thread の中心となる問題を表す。

---

## 2. Conflict の役割

Conflict は以下を定義する。

物語の問題  
対立構造  
解決目標  

---

## 3. Conflict 属性

conflict_id

Conflict ID

conflict_type

対立の種類

related_thread_id

関連 Thread

participants

関係する Character

description

対立内容

---

## 4. Conflict 種別

代表的な Conflict

character_vs_character  
character_vs_society  
character_vs_self  
character_vs_nature  
character_vs_system

---

## 5. Conflict JSON Example

{
  "conflict": {
    "conflict_id": "conflict_001",
    "conflict_type": "character_vs_system",
    "related_thread_id": "thread_main",
    "participants": [
      "char_001"
    ],
    "description": "主人公が監視社会システムに対抗する"
  }
}

---

## 6. 関連 Spec

NWF_Thread_Graph_Model  
NWF_Event_Model  
NWF_Character_Model  
NWF_World_Rule_Model

---

## 7. まとめ

Conflict Model は
物語の中心問題を定義するモデルである。

Thread は
この Conflict を解決する過程として構築される。

---

[EOF]