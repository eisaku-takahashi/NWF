Source: docs/spec/Core_Spec/NWF_Story_Database_v2.0.0.md
Updated: 2026-03-17T05:00:00+09:00
PIC: Engineer / ChatGPT

# NWF Story Database v2.0.0

---

## 1. 概要

Story Database は NWF における
物語データを統合管理する論理データベースである。

NWF のすべての物語要素は
Story Database 内のデータとして管理される。

---

## 2. データ管理対象

Story Database は以下のデータを管理する。

Thread  
Scene  
Character  
WorldRule  
Event  
Timeline  

---

## 3. データ構造

Story Database は以下の論理構造を持つ。

story_database
  ├ threads
  ├ scenes
  ├ characters
  ├ world_rules
  ├ events
  └ timeline

---

## 4. Story Database JSON Example

例

{
  "story_database": {
    "threads": [],
    "scenes": [],
    "characters": [],
    "world_rules": [],
    "events": [],
    "timeline": {}
  }
}

---

## 5. データ管理方針

Story Database の設計方針

一意IDによる参照  
JSONベースの構造  
ファイル分割可能設計  
エンジンによるクエリ可能  

---

## 6. 関連 Spec

NWF_Data_Model  
NWF_Entity_ID_System  
NWF_Timeline_Model  
NWF_Thread_Graph_Model  
NWF_Query_Language  

---

## 7. まとめ

Story Database は
NWF における物語情報の統合データ基盤である。

すべての物語要素は
このデータベース内のエンティティとして管理される。

---

[EOF]