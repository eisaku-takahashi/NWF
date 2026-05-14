Source: docs/spec/Core_Spec/NWF_Beat_Model_v2.0.1.md
Updated: 2026-03-22T16:25:00+09:00
PIC: Engineer / ChatGPT

# NWF Beat Model v2.0.1

---

## 1. 概要

NWF（Novel Writing Framework）において Beat は Scene 内部における最小ナラティブ単位であり、
State Transition を伴うミクロ・ナラティブ実行単位として定義される。

Beat は Character の行動、感情変化、情報提示、意思決定などを通じて
Thread State を微小に変化させる。

Scene が物語の実行単位であるのに対し、
Beat は物語の最小の状態変化単位である。

Beat の連続により Scene が構成され、
Scene の連続により物語が構成される。

---

## 2. Beat の定義（Beat as State Function）

Beat は以下の状態遷移関数として定義される。

input_state
↓
event
↓
output_state

Beat は状態遷移を引き起こす Event を内部に持ち、
Thread / Character / World の状態を変化させる。

Beat = State Transition Function

---

## 3. Beat の構造要素

Beat は以下の要素で構成される。

- beat_id
- related_scene_id
- beat_index
- input_state_ids[]
- event_ids[]
- output_state_ids[]
- character_ids[]
- location_id
- timeline_id
- relative_time
- intensity_delta
- emotional_delta
- visibility
- importance
- beat_role
- beat_format
- description

これにより Beat は
「誰が、どこで、何を行い、何が変化したか」
を完全に記述できる。

---

## 4. Beat Role と Beat Format

Beat には役割と表現形式の2種類の分類が存在する。

### 4.1 Beat Role（物語構造上の役割）

例：

- setup
- foreshadowing
- information
- conflict
- decision
- twist
- climax
- resolution
- aftermath

Beat Role はドラマ構造上の役割を表す。

### 4.2 Beat Format（表現形式）

例：

- action
- dialogue
- internal_monologue
- narration
- description
- reaction

Beat Format は文章表現の形式を表す。

Role と Format を分離することで、
物語構造と文章生成の両方を制御できる。

---

## 5. 時間・空間情報（Temporal / Spatial Precision）

Beat は Scene 内での相対時間と位置情報を持つ。

- timeline_id
- location_id
- relative_time（Scene 開始からの経過時間）
- beat_index（Scene 内順序）

これにより Scene 内でのイベント順序と時間経過を管理できる。

---

## 6. Beat と Event の関係

Beat は 1つ以上の Event を内包する。

構造：

Beat
 └ Event
     └ State Change

Event は状態変化のトリガーであり、
Beat は Event を包含するナラティブ単位である。

---

## 7. 感情・緊張度変化

Beat は Scene の Emotional Curve を構成する。

emotional_delta
キャラクター感情変化量

intensity_delta
Scene 緊張度変化量

これらの累積により Scene Intensity と Emotional Curve を計算できる。

---

## 8. Beat JSON Structure

Beat JSON 構造例：

{
  "beat_id": "BEAT_001",
  "related_scene_id": "SCN_001",
  "beat_index": 1,

  "timeline_id": "TL_MAIN",
  "location_id": "LOC_LIBRARY",
  "relative_time": 30,

  "character_ids": [
    "CHAR_A"
  ],

  "input_state_ids": [
    "STATE_MYSTERY_UNKNOWN"
  ],

  "event_ids": [
    "EVT_CLUE_FOUND"
  ],

  "output_state_ids": [
    "STATE_MYSTERY_CLUE_FOUND"
  ],

  "beat_role": "information",
  "beat_format": "action",

  "intensity_delta": 5,
  "emotional_delta": 3,

  "visibility": "public",
  "importance": 40,

  "description": "主人公が本棚から手がかりを発見する"
}

この構造により AI Writer は
この瞬間に何を書くべきかを判断できる。

---

## 9. Core Architecture における Beat の位置

Core Architecture 構造：

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
Thread Update

Beat は文章生成に最も近いナラティブ制御層である。

---

## 10. まとめ

NWF Beat Model v2.0.1 は以下を定義する。

- Beat = 最小ナラティブ単位
- Beat = State Transition Function
- Beat = Event Container
- Scene 内時間・空間位置
- Character 行動・感情変化
- Emotional Curve / Intensity 制御
- 物語構造 Role
- 表現形式 Format

Beat Model は NWF において
「物語の最小の拍動」を管理するコアモデルである。

---

[EOF]