Source: docs/spec/Core_Spec/NWF_Event_Model_v2.0.0.md
Updated: 2026-03-17T05:10:00+09:00
PIC: Engineer / ChatGPT

# NWF Event Model v2.0.0

---

## 1. 概要

Event Model は NWF において
物語内で発生する出来事を表現するためのデータモデルである。

Event は Scene・Thread・Character と関連付けられ
物語の因果関係を構成する基本単位となる。

---

## 2. Event の役割

Event は以下の目的で使用される。

物語の出来事の記録  
Timeline への配置  
Thread 進行のトリガー  
Character 状態変化の原因  

---

## 3. Event 属性

event_id

イベントを識別する一意ID

event_type

イベントの種類

related_scene_id

関連する Scene

related_thread_id

関連する Thread

timestamp_story

物語時間

description

イベント概要

---

## 4. Event 種別

代表的な Event 種別

scene_start  
scene_end  
character_action  
world_event  
conflict_trigger  
thread_resolution

---

## 5. Event JSON Example

{
  "event": {
    "event_id": "event_001",
    "event_type": "scene_start",
    "related_scene_id": "scene_001",
    "related_thread_id": "thread_main",
    "timestamp_story": "year_001_day_001",
    "description": "物語の開始"
  }
}

---

## 6. 関連 Spec

NWF_Timeline_Model  
NWF_Scene_Model  
NWF_Thread_Graph_Model  
NWF_Character_Model

---

## 7. まとめ

Event Model は
物語における出来事を管理する基本モデルである。

Timeline と組み合わせることで
物語の因果関係と時間構造を明確にする。

---

[EOF]