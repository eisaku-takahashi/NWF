Source: docs/spec/Core_Spec/NWF_Timeline_Model_v2.0.1.md
Updated: 2026-03-22T17:43:00+09:00
PIC: Engineer / ChatGPT

# NWF Timeline Model v2.0.1

---

## 1. 概要

Timeline Model は NWF における
物語時間・叙述順序・因果関係・並行世界を管理する
時間構造モデルである。

v2.0.1 では Timeline を単なる時系列ではなく、
以下を統合する時間アーキテクチャとして定義する。

・Story Time（因果時間）
・Narrative Time（叙述順序）
・Timeline Layer（時間層）
・Parallel Timeline（並行時間）
・Sync Point（同期点）
・Causality Link（因果リンク）
・Abstract Time Unit（抽象時間単位）

Timeline Model は
NWF Core Architecture における
Time Layer を構成する。

---

## 2. Dual Timeline Logic

Timeline Model では
Story Time と Narrative Time を分離する。

### 2.1 Story Time（因果時間）

Story Time は物語世界内部の時間順序であり、
因果関係は Story Time に従う。

例：

事件発生 → 捜査 → 真相判明 → 解決

これは必ず Story Time 順で発生する。

主な属性：

story_time_tick  
story_timestamp  
story_duration  

### 2.2 Narrative Time（叙述順序）

Narrative Time は
読者・視聴者に提示される順序である。

例：

現在 → 回想 → 過去 → 現在 → 未来 → 真相

Narrative Time は Story Time と一致しない場合がある。

主な属性：

narrative_order  
narrative_sequence_id  
flashback_flag  
foreshadow_flag  

### 2.3 Event による結合

Story Time と Narrative Time は
Event ID によって結合される。

Event
  ├ story_time
  └ narrative_order

---

## 3. Timeline Layering & Sync

Timeline は複数の Layer を持つことができる。

### 3.1 Timeline Layer

| layer | 説明 |
|------|------|
| main | 正史 |
| flashback | 回想 |
| dream | 夢 |
| vision | 予知 |
| parallel | 並行世界 |
| if_route | IFルート |
| simulation | 仮想世界 |

timeline_layer により
非線形・並行世界・回想構造を管理する。

### 3.2 Sync Point（同期点）

Sync Point は
複数 Timeline が合流・同期するポイントである。

例：

・並行世界が合流  
・回想が現在に追いつく  
・複数 Thread が合流  
・時間ジャンプの到着点  

sync_point_id により
Timeline 同期を管理する。

---

## 4. Abstract Time Units

NWF Timeline は
現実のカレンダーに依存しない抽象時間単位を使用できる。

### 4.1 Abstract Time

| 属性 | 説明 |
|------|------|
| time_tick | 最小時間単位 |
| story_day | 物語日 |
| story_year | 物語年 |
| era | 時代 |
| cycle | 周期 |
| story_duration | 継続時間 |

これにより

・ファンタジー暦
・SF宇宙時間
・ループ時間
・夢時間
・異世界時間

などを表現できる。

---

## 5. Causal Consistency

Timeline Model は
Event Model の因果関係を時間軸上で検証する。

### 5.1 Causality Link

| 属性 | 説明 |
|------|------|
| cause_event_id | 原因イベント |
| effect_event_id | 結果イベント |
| causality_type | 因果タイプ |
| causality_weight | 因果強度 |

例：

Event A → Event B → Event C

Timeline は因果関係が
Story Time 順序と矛盾しないかを検証する。

### 5.2 因果整合性ルール

effect_event.story_time >= cause_event.story_time

このルールにより
時間矛盾を検出できる。

---

## 6. Timeline JSON Structure

Timeline は以下の JSON 構造で管理される。

{
  "timeline_id": "timeline_main",
  "time_unit": "tick",
  "events": [
    {
      "event_id": "event_001",
      "story_time_tick": 100,
      "story_duration_tick": 5,
      "narrative_order": 1,
      "timeline_layer": "main",
      "sync_point_id": null,
      "causality_links": [
        {
          "cause_event_id": null,
          "effect_event_id": "event_001"
        }
      ]
    },
    {
      "event_id": "event_010",
      "story_time_tick": 50,
      "story_duration_tick": 3,
      "narrative_order": 5,
      "timeline_layer": "flashback",
      "sync_point_id": "sync_01",
      "causality_links": [
        {
          "cause_event_id": "event_005",
          "effect_event_id": "event_010"
        }
      ]
    }
  ],
  "sync_points": [
    {
      "sync_point_id": "sync_01",
      "story_time_tick": 120
    }
  ]
}

---

## 7. Timeline Engine Logic

Timeline Engine は以下を管理する。

1. Story Time 順序
2. Narrative Order
3. Flashback / Foreshadow
4. Parallel Timeline
5. Timeline Layer
6. Sync Point
7. Event Duration
8. Causality Check
9. Timeline Consistency
10. Next Event Selection

### Next Event Selection Logic

次に提示するイベントは以下で決定できる。

priority =
narrative_order_weight +
conflict_intensity_weight +
relationship_importance +
thread_priority +
timeline_position_weight

Timeline Engine は
Story Engine の進行順序を決定する。

---

## 8. Core Models との関係

Timeline Model は以下のモデルを時間軸で統合する。

| Model | 関係 |
|------|------|
| Event Model | 時間配置 |
| Scene Model | Scene 順序 |
| Thread Model | Thread 同期 |
| Conflict Model | 対立進行時間 |
| Relationship Model | 関係変化時間 |
| State Model | 状態変化時間 |
| Character Model | キャラクター時間 |
| World Rule Model | 世界イベント時間 |

Timeline Model は
Core Spec 全体を時間軸で統合するモデルである。

---

## 9. まとめ

Timeline Model v2.0.1 では Timeline を

単なる時系列ではなく

・Story Time（因果時間）
・Narrative Time（叙述順序）
・Timeline Layer
・Parallel Timeline
・Sync Point
・Abstract Time
・Causality Link

を統合する

**Multilayered Temporal Architecture**

として定義した。

Timeline Model は
NWF Core Architecture における

**Time Layer / Story Time Engine / Narrative Order Controller**

である。

---

[EOF]