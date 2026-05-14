Source: docs/spec/Core_Spec/NWF_Conflict_Model_v2.0.1.md
Updated: 2026-03-22T16:52:00+09:00
PIC: Engineer / ChatGPT

# NWF Conflict Model v2.0.1

---

## 1. 概要

Conflict Model は、NWF における物語の「推進力」を管理するコアモデルである。

Thread が物語の目的構造を表し、
Event が世界の状態変化を表すのに対し、
Conflict は「対立によって発生する緊張と進行」を管理する。

v2.0.1 では Conflict を単なる設定情報ではなく、
**Progress Machine（進行状態機械）**として定義する。

Conflict は以下を管理する：

- 対立参加者（Entities）
- 目的（Goals）
- 利害（Stakes）
- 進行状態（Status）
- 進行度（Progress）
- 緊張度（Intensity）
- 解決条件（Resolution Conditions）
- 関連 Thread / Event / Scene / Beat への影響

Conflict は物語の緊張曲線を生成する中心モデルである。

---

## 2. Conflict as Progress Machine

Conflict は状態遷移を持つステートマシンとして動作する。

### 2.1 Conflict Status

Conflict は以下の status を持つ。

| status | 説明 |
|-------|------|
| latent | 潜在的対立 |
| discovered | 対立の発見 |
| escalating | 激化 |
| crisis | 危機 |
| climax | クライマックス |
| resolving | 解決過程 |
| resolved | 解決済 |
| aftermath | 余波 |

### 2.2 Conflict Progress

progress は 0.0〜1.0 の値で表される。

| progress | 状態 |
|---------|------|
| 0.0 | 未開始 |
| 0.2 | 対立発見 |
| 0.4 | 対立激化 |
| 0.6 | 危機 |
| 0.8 | クライマックス |
| 1.0 | 解決 |

Conflict Progress は Event によって変化する。

---

## 3. Conflict Participants（Multi-Layered Opposition）

Conflict の参加者は Entity ID によって管理される。

Entity は以下を含む：

- Character
- Organization
- Society
- AI
- World Rule
- Environment
- System

これにより以下の対立が表現可能：

| 対立タイプ |
|-------------|
| Character vs Character |
| Character vs Society |
| Character vs Self |
| Character vs Nature |
| Character vs System |
| Organization vs Organization |
| Human vs AI |
| Human vs World Rule |
| Ideology vs Ideology |

---

## 4. Stakes & Goals Definition

Conflict は Goals と Stakes を持つ。

### 4.1 conflict_goals
各参加者が達成したい目的。

### 4.2 conflict_stakes
失敗した場合に失うもの（リスク）。

例：

- 命
- 名誉
- 財産
- 人間関係
- 世界の存続
- 記憶
- 自我
- 自由

Stakes が大きいほど Conflict Intensity が上昇する。

---

## 5. Resolution Conditions

Conflict は論理的な解決条件を持つ。

resolution_conditions は以下を参照する：

- state_id
- event_id
- thread_goal_id
- world_rule_condition
- character_status
- location_condition
- item_condition

例：

- ボスが死亡
- 証拠が公開される
- 真実が判明
- 世界ルールが破壊
- 主人公が自我を受け入れる

---

## 6. Conflict Intensity Sync

Conflict の激化は Scene と Beat に影響を与える。

### 6.1 Intensity Parameters

| parameter | 説明 |
|-----------|------|
| intensity_base | 基本緊張度 |
| stakes_weight | Stakes の重み |
| opposition_power | 敵対勢力の強さ |
| time_pressure | 時間制限 |
| uncertainty | 不確実性 |
| emotional_weight | 感情影響 |
| world_impact | 世界への影響 |

### 6.2 Scene / Beat への影響

Conflict Intensity は以下へ影響：

- Scene Intensity
- Beat Emotional Delta
- Thread Tension Curve
- Story Climax Timing

---

## 7. Conflict JSON Structure

Conflict は以下の JSON 構造で管理される。

{
  "conflict_id": "conflict_001",
  "related_thread_id": "thread_001",
  "status": "escalating",
  "progress": 0.45,
  "intensity": 0.72,
  "participants": [
    {
      "entity_id": "character_001",
      "goal_id": "goal_001",
      "stakes_id": "stakes_001"
    },
    {
      "entity_id": "organization_001",
      "goal_id": "goal_002",
      "stakes_id": "stakes_002"
    }
  ],
  "resolution_conditions": [
    "event_045",
    "state_010"
  ],
  "related_event_ids": [
    "event_010",
    "event_020",
    "event_030"
  ],
  "intensity_parameters": {
    "stakes_weight": 0.8,
    "opposition_power": 0.7,
    "time_pressure": 0.4,
    "uncertainty": 0.6,
    "emotional_weight": 0.9,
    "world_impact": 0.5
  },
  "scene_intensity_weight": 0.75,
  "beat_emotion_weight": 0.65
}

---

## 8. Conflict と Core Models の関係

### 8.1 Thread Model
Thread は Conflict を解決するプロセスである。

Thread Progress ≒ Conflict Progress

### 8.2 Event Model
Event は Conflict Progress を変化させる。

Event → State Change → Conflict Progress Change

### 8.3 State Model
Conflict は State の変化によって進行する。

### 8.4 Beat Model
Beat Emotional Delta は Conflict Intensity の影響を受ける。

### 8.5 World Rule Model
World Rule は Conflict の制約条件や解決条件になる。

---

## 9. Conflict Engine Logic

執筆エンジンは以下を計算する：

1. 現在アクティブな Conflict
2. 各 Conflict の intensity
3. 各 Conflict の progress
4. Stakes の大きさ
5. Climax に最も近い Conflict
6. 次に Conflict を進める Event
7. Scene Intensity
8. Emotional Curve への影響

### Conflict Priority Score

Conflict Priority は以下で計算できる：

priority =
intensity × stakes_weight × progress_weight × thread_importance

この値が最も高い Conflict が
「現在最も熱い葛藤」となる。

---

## 10. まとめ

Conflict Model v2.0.1 では、

Conflict を

**設定情報ではなく、進行・緊張・解決を管理する状態機械**

として定義した。

Conflict は以下を支配する：

- Thread Progress
- Scene Intensity
- Beat Emotion
- Story Tension Curve
- Climax Timing
- Resolution Logic

つまり Conflict Model は

**Story Engine の中心モデル**

である。

---

[EOF]