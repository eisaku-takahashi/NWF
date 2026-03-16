Source: docs/spec/Core_Spec/NWF_Character_Model_v2.0.0.md
Updated: 2026-03-17T05:10:00+09:00
PIC: Engineer / ChatGPT

# NWF Character Model v2.0.0

---

## 1. 概要

Character Model は
物語に登場するキャラクター情報を管理するデータモデルである。

キャラクターは Scene・Thread・Event と関連付けられ
物語の行動主体として扱われる。

---

## 2. Character の役割

Character は以下を担う。

行動主体  
Conflict の発生源  
Thread 進行の推進力  

---

## 3. Character 属性

character_id

キャラクターID

name

キャラクター名

role

物語内での役割

description

キャラクター説明

status

現在状態

---

## 4. Character JSON Example

{
  "character": {
    "character_id": "char_001",
    "name": "主人公",
    "role": "protagonist",
    "status": "active",
    "description": "物語の主人公"
  }
}

---

## 5. 関連 Spec

NWF_Event_Model  
NWF_Scene_Model  
NWF_Thread_Graph_Model  
NWF_Conflict_Model

---

## 6. まとめ

Character Model は
物語に登場する人物を管理する基本モデルである。

すべての行動と Conflict は
Character を中心に発生する。

---

[EOF]