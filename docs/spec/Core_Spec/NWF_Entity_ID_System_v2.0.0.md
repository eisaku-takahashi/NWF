Source: docs/spec/Core_Spec/NWF_Entity_ID_System_v2.0.0.md
Updated: 2026-03-17T04:30:00+09:00
PIC: Engineer / ChatGPT

# NWF Entity ID System v2.0.0

---

## 1. 概要

本ドキュメントは  
Novel Writing Framework（NWF）における  
Entity ID システムを定義する。

NWFではすべてのストーリー要素は  
一意の ID によって識別される。

目的

- Entity識別の一意性確保
- Entity間参照の安定化
- データベース構造の明確化
- Engine処理の効率化

このIDシステムは  
NWF Data Model の基盤仕様である。

---

## 2. ID System Overview

NWFでは以下のEntityが  
IDによって識別される。

WorldRule  
Character  
Thread  
Scene  
Beat

すべてのEntityは  
一意のIDを持つ。

---

## 3. ID Naming Structure

NWF ID は以下の構造を持つ。

entity_prefix + "_" + number

例

char_001  
thread_001  
scene_010  
beat_003

---

## 4. Entity Prefix

各Entityは  
専用のPrefixを持つ。

WorldRule

world_rule_

Character

char_

Thread

thread_

Scene

scene_

Beat

beat_

---

## 5. ID Uniqueness

IDは  
Story Data Store 内で  
**一意である必要がある。**

例

正しい例

char_001  
char_002  
char_003

誤った例

char_001  
char_001

---

## 6. ID Reference

Entityは  
IDによって相互参照される。

例

Character → Thread

character_id

char_001

Thread

related_characters

char_001

---

## 7. Scene References

Sceneは  
複数Entityを参照する。

例

scene_id

scene_010

participants

char_001  
char_002

related_thread

thread_001

---

## 8. Beat References

Beatは  
Scene内部で管理される。

例

beat_id

beat_001

scene_id

scene_010

---

## 9. ID Generation Rules

IDは以下のルールで生成される。

1  
Prefix を付ける

2  
連番を使用する

3  
3桁以上の数字を使用する

例

char_001  
char_002  
char_010

---

## 10. Stable ID Principle

IDは  
**一度作成されたら変更しない。**

理由

- Git履歴安定
- Engine参照保持
- データ整合性維持

---

## 11. Human Readable Design

NWF IDは  
人間が読める形式で設計されている。

例

char_001

characterの識別子

thread_003

3番目のThread

---

## 12. JSON Representation Example

例

character

character_id

char_001

name

Alice

thread

thread_id

thread_001

title

Main Mystery

scene

scene_id

scene_010

participants

char_001  
char_002

---

## 13. Extensibility

将来  
以下のEntityにもIDが追加可能である。

Location  
Item  
Faction  
Event

ID Prefix は  
同様の方式で追加する。

---

## 14. まとめ

NWF Entity ID System は  
NWFのすべてのストーリー要素を  
一意に識別する仕組みである。

本システムにより

- Entity参照の安定化
- Engine処理の効率化
- Gitによる履歴管理
- AI処理の簡略化

が可能になる。

この仕様は  
NWF Data Model と密接に連携する。

---

[EOF]