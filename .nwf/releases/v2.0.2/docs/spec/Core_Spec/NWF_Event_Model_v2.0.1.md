Source: docs/spec/Core_Spec/NWF_Event_Model_v2.0.1.md
Updated: 2026-03-22T16:05:00+09:00
PIC: Engineer / ChatGPT

# NWF Event Model v2.0.1

---

## 1. 概要

NWF（Novel Writing Framework）において Event は物語における因果関係を構成する基本単位であり、
State Transition を引き起こす「因果トリガー（Causal Trigger）」として定義される。

Event は Scene 内で発生し、Thread、Character、World の状態を変化させる。
Event を因果連鎖として記録することで、物語の論理構造と時間構造を同時に管理することができる。

Event Model は Story Database における因果ログモデルとして機能する。

---

## 2. Event の定義（Event as Causal Trigger）

Event は以下の構造を持つ。

Cause
↓
Event
↓
Effect（State Change）

Event は状態遷移を引き起こす入力として機能する。

Event は以下を定義する。

- 何が起きたか
- なぜ起きたか
- 何を変化させたか
- 誰に影響したか
- いつどこで起きたか

Event は Thread State Machine における遷移トリガーとして機能する。

---

## 3. 因果関係フィールド（Cause / Effect）

Event は因果連鎖を表現するため、以下のフィールドを持つ。

cause_ids[]
この Event を引き起こした原因 Event または State ID

effect_ids[]
この Event によって発生した結果 Event または State ID

構造例：

Event A → Event B → Event C

これにより物語の因果グラフを構築できる。

---

## 4. Entity Impact Matrix（影響対象）

Event は影響を受けるエンティティを明示する。

target_entity_ids[]

対象となるエンティティ：

- Character
- Thread
- World
- Location
- Relationship

これにより
「このイベントが何に影響したのか」
を明確に記録できる。

---

## 5. Scene / Beat との階層関係

Event は Scene 内の Beat に紐づく。

フィールド：

- related_scene_id
- beat_index

構造：

Scene
 └ Beat 1
     └ Event
 └ Beat 2
     └ Event

これにより Scene Model v2.0.1 との親子関係が確定する。

---

## 6. 拡張 Event 属性

Event はナラティブ制御のため、追加属性を持つ。

importance
イベントの重要度（0〜100）

is_public
イベント情報がキャラクターに公開されているか
true = 公開情報
false = 秘密情報

timestamp
イベント発生時刻

location_id
イベント発生場所

description
イベント内容説明

---

## 7. Event JSON Structure

Event JSON 構造例：

{
  "event_id": "EVT_001",
  "event_type": "clue_found",
  "importance": 60,
  "is_public": true,

  "timestamp": "2026-01-01T10:30:00",
  "location_id": "LOC_LIBRARY",

  "related_scene_id": "SCN_001",
  "beat_index": 2,

  "cause_ids": [
    "EVT_000"
  ],

  "effect_ids": [
    "STATE_MYSTERY_CLUE_FOUND"
  ],

  "target_entity_ids": [
    "CHAR_A",
    "THR_MYSTERY"
  ],

  "description": "主人公が図書館で手がかりを発見した"
}

この JSON により以下を完全に記述できる。

- いつ
- どこで
- 何が
- なぜ起き
- 何を変えたか
- 誰に影響したか

---

## 8. Event と Thread State Transition

State Transition 構造：

State A
↓
Event
↓
State B

Event は State Machine のトリガーとして動作する。

Thread State Model と Event Model は
状態遷移関数を共有する。

---

## 9. Event Model の役割（Core Architecture）

Core Architecture における位置：

Story Database
↓
Timeline
↓
Scene
↓
Beat
↓
Event
↓
State Transition
↓
Thread Graph Update

Event は物語の因果律を管理するロジック層である。

---

## 10. まとめ

NWF Event Model v2.0.1 は以下を管理する。

- 出来事
- 因果関係
- 状態遷移トリガー
- 影響対象エンティティ
- Scene / Beat 階層
- 時間・場所
- 公開情報 / 秘密情報
- イベント重要度

Event Model により NWF は
物語の因果構造を論理的・データベース的に管理できる。

Event は NWF において
「物語の因果の力」を制御するコアモデルである。

---

[EOF]