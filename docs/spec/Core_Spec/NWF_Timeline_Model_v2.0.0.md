Source: docs/spec/Core_Spec/NWF_Timeline_Model_v2.0.0.md
Updated: 2026-03-17T05:00:00+09:00
PIC: Engineer / ChatGPT

# NWF Timeline Model v2.0.0

---

## 1. 概要

Timeline Model は NWF における物語時間構造を管理するためのデータモデルである。

Thread、Scene、Event を時間軸上に配置し、
物語の進行順序と因果関係を管理する。

Timeline は以下の用途で使用される。

・物語の時系列管理  
・Scene順序の検証  
・伏線と回収の時間関係の確認  
・並行Threadの同期  

---

## 2. Timeline 構造

Timeline は Event の集合として構成される。

基本構造

timeline
  ├ events
  └ timeline_metadata

---

## 3. Timeline Event

Timeline Event は物語時間上の1つの出来事を表す。

主に以下のエンティティと関連付けられる。

・Scene  
・Thread  
・Character  
・World Event  

---

## 4. Event 属性

主な属性は以下である。

event_id  
イベントID

related_scene_id  
関連Scene

related_thread_id  
関連Thread

timestamp_story  
物語時間

timestamp_order  
物語表示順序

event_type  
イベント種別

description  
イベント概要

---

## 5. Timeline JSON Example

例

{
  "timeline": {
    "timeline_id": "timeline_main",
    "events": [
      {
        "event_id": "event_001",
        "related_scene_id": "scene_001",
        "related_thread_id": "thread_main",
        "timestamp_story": "year_001_day_001",
        "timestamp_order": 1,
        "event_type": "scene_start",
        "description": "物語開始"
      }
    ]
  }
}

---

## 6. NWF 内での役割

Timeline Model は以下の Spec と連携する。

NWF_Data_Model  
NWF_Thread_Graph_Model  
NWF_Scene_Model  
NWF_Entity_ID_System  

---

## 7. まとめ

Timeline Model は NWF における
物語の時間構造を管理する中核モデルである。

Thread・Scene・Event を時間軸に配置することで
物語の因果関係と進行順序を明確にする。

---

[EOF]