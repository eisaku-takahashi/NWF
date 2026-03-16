Source: docs/spec/Core_Spec/NWF_Relationship_Model_v2.0.0.md
Updated: 2026-03-17T07:00:00+09:00
PIC: Engineer / ChatGPT

# NWF Relationship Model v2.0.0

---

## 1. 概要

Relationship Model は
NWF におけるエンティティ間の関係を定義するモデルである。

Character・Thread・Scene・Event などの
エンティティは互いに関係を持つ。

Relationship Model は
その関係を統一的に管理する。

---

## 2. Relationship の目的

Relationship は以下を表現する。

キャラクター間の関係  
キャラクターと Thread の関係  
Scene と Event の関係  
Thread と Conflict の関係  

---

## 3. Relationship 構造

Relationship は
以下の要素で構成される。

relationship_id

関係を識別するID

source_entity_id

関係の起点エンティティ

target_entity_id

関係の対象エンティティ

relationship_type

関係の種類

description

関係の説明

---

## 4. Relationship 種別

代表的な Relationship 種別

character_to_character

character_to_thread

character_to_scene

scene_to_event

thread_to_conflict

thread_to_scene

event_to_character

---

## 5. Relationship JSON Example

{
  "relationship": {
    "relationship_id": "rel_001",
    "source_entity_id": "char_001",
    "target_entity_id": "char_002",
    "relationship_type": "character_to_character",
    "description": "主人公とライバルの関係"
  }
}

---

## 6. 関連 Spec

NWF_Entity_ID_System

NWF_Character_Model

NWF_Thread_Graph_Model

NWF_Scene_Model

NWF_Event_Model

---

## 7. まとめ

Relationship Model は
NWF のエンティティ間の関係を管理するための
基盤モデルである。

これにより
物語構造をネットワークとして表現できる。

---

[EOF]