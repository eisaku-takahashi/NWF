Source: docs/spec/Core_Spec/NWF_Scene_Model_v2.0.1.md
Updated: 2026-03-22T15:34:00+09:00
PIC: Engineer / ChatGPT

# NWF Scene Model v2.0.1

---

## 1. 概要

NWF（Novel Writing Framework）において Scene は物語の「実行単位（Narrative Execution Unit）」である。

Scene は Beat の集合を内包し、Event をトリガーとして Thread State を変化させる。
Scene は物語の時間・空間・登場人物・ルール・感情強度を統合的に管理するコンテナ構造であり、
AI Writer が「何を、どこで、誰が、どの状態で行うか」を決定するための基盤データとなる。

Scene は Thread Graph / Thread State / Story Database と直接連携し、
物語進行を実行レベルで制御する。

---

## 2. Scene の定義（Scene as Execution Container）

Scene は以下を包含するコンテナである。

- Beat の配列
- Event トリガー
- 登場キャラクター
- 適用世界ルール
- Thread State の入力
- Thread State の出力
- 時間・場所情報
- Scene のタイプ
- Scene の緊張度（Intensity）

構造概念：

Initial Thread State
↓
Scene（Beat / Event）
↓
Resultant Thread State

Scene は「状態遷移を引き起こす物語実行ユニット」である。

---

## 3. Scene の時空間アンカー（Spatio-Temporal Anchor）

Scene は必ず物理的な時空間座標を持つ。

必須フィールド：

- timeline_id
- timestamp
- location_id

これにより Scene は Story Timeline 上の正確な位置に配置される。

Scene = Timeline + Time + Location + Event

この構造により物語の時間構造と空間構造を統合管理できる。

---

## 4. Entity Participation（登場要素）

Scene に参加するエンティティを明示的に管理する。

### 4.1 Character Participation
- cast_ids[]
Scene に登場するキャラクター ID 配列

### 4.2 Active World Rules
- active_rule_ids[]
Scene 内で適用される世界ルール ID 配列

これにより Scene 内で
「誰が」「どのルール下で」行動しているかを定義できる。

---

## 5. Scene Type と Intensity

Scene は物語リズム制御のため、タイプと緊張度を持つ。

### 5.1 Scene Type
例：

- static（静）
- dynamic（動）
- transition（転）
- climax（頂点）
- resolution（解決）
- exposition（説明）
- conflict（対立）
- discovery（発見）
- decision（決断）

### 5.2 Intensity
Scene の緊張度・感情強度を数値で表す。

例：

- 0 = Calm
- 25 = Low tension
- 50 = Medium
- 75 = High tension
- 100 = Extreme / Climax

Intensity により Emotional Curve を計算可能。

---

## 6. Scene と Thread State

Scene は Thread State を変化させる。

Scene は次の状態参照を持つ：

- input_state_ids[]
- output_state_ids[]

構造：

Thread State (Before Scene)
↓
Scene Execution
↓
Thread State (After Scene)

Scene は Thread State Machine の実行ノードとして機能する。

---

## 7. Scene 内部構造（Beat / Event）

Scene は Beat と Event によって構成される。

### 7.1 Beat
Beat は Scene 内の最小ドラマ単位。

例：

Beat 1：会話開始  
Beat 2：情報提示  
Beat 3：対立  
Beat 4：決断  

### 7.2 Event
Event は状態変化を引き起こすトリガー。

例：

- clue_found
- character_death
- relationship_change
- decision_made
- secret_revealed

Event が Thread State Change を発生させる。

---

## 8. Scene JSON Structure

Scene の JSON スキーマ例：

{
  "scene_id": "SCN_001",
  "title": "Mysterious Letter",
  "scene_type": "discovery",
  "intensity": 40,

  "timeline_id": "TL_MAIN",
  "timestamp": "2026-01-01T10:00:00",
  "location_id": "LOC_LIBRARY",

  "cast_ids": [
    "CHAR_A",
    "CHAR_B"
  ],

  "active_rule_ids": [
    "RULE_MAGIC_LIMIT",
    "RULE_POLICE_AUTHORITY"
  ],

  "related_thread_ids": [
    "THR_MYSTERY"
  ],

  "input_state_ids": [
    "STATE_MYSTERY_UNKNOWN"
  ],

  "output_state_ids": [
    "STATE_MYSTERY_CLUE_FOUND"
  ],

  "event_ids": [
    "EVT_CLUE_FOUND"
  ],

  "beat_ids": [
    "BEAT_001",
    "BEAT_002",
    "BEAT_003"
  ]
}

この構造により AI Writer は以下を即座に理解できる。

- どの Thread に関係する Scene か
- 登場人物
- 場所と時間
- Scene の目的
- 状態変化
- 書くべき Beat

---

## 9. Scene Model の役割（Core Architecture 内）

NWF Core Architecture における Scene の位置：

Story Database
↓
Thread Graph
↓
Thread State Machine
↓
Scene（Execution Unit）
↓
Beat
↓
Text Output

Scene は「物語構造」と「文章生成」の橋渡しを行う実行層である。

---

## 10. まとめ

NWF Scene Model v2.0.1 において Scene は以下の役割を持つ。

- 物語の実行単位
- Thread State を変化させるイベントコンテナ
- Beat のコンテナ
- 時間・場所のアンカー
- 登場キャラクター管理
- 世界ルール適用管理
- Emotional Intensity 管理
- AI Writer の執筆指示データ

Scene は NWF において
「物語の現場」を定義する最重要実行モデルである。

---

[EOF]