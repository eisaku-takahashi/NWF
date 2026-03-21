Source: docs/spec/Core_Spec/NWF_State_Transition_Model_v2.0.1.md
Updated: 2026-03-21T20:43:00+09:00
PIC: Engineer / ChatGPT

# NWF State Transition Model v2.0.1

---

## 1. v2.0.0 の論理的限界（なぜ単純な遷移では不十分か）

v2.0.0 の State Transition Model は
source_state → trigger_event → target_state
という単純な状態遷移のみを定義するモデルであった。

しかしこの構造では以下の問題がある。

1. 遷移条件（条件分岐）が表現できない
2. 遷移確率（確率分岐）が表現できない
3. Character / Thread / World の状態を統一管理できない
4. 遷移による副作用（他状態への影響）を表現できない
5. World Rule を参照した遷移制御ができない
6. Graph 構造として管理できない
7. Story Engine のシミュレーションに対応できない

そのため v2.0.1 では
State と Transition を分離し、
State Machine / Graph Edge モデルとして再設計する。

---

## 2. State Transition Model v2.0.1 属性定義

State Transition は
「状態ノード間を接続する遷移エッジ」として定義する。

### 基本属性

transition_id  
entity_type  
source_state_id  
target_state_id  
trigger_event  
description  

### 遷移制御属性

conditions  
probability  
priority  
cooldown  

### 副作用属性

effects  

### 参照属性

required_world_rules  
required_character_states  
required_flags  

### メタデータ

tags  
metadata  

---

## 3. State Machine 動作ロジック（Story Engine との連携フロー）

State Machine は以下の流れで動作する。

1. Event Engine が Event を発生させる
2. State Machine が trigger_event を持つ Transition を検索
3. conditions を評価
4. World Rule を参照して遷移可能か判定
5. probability に基づいて遷移決定
6. target_state に状態変更
7. effects を実行（他 Entity の State 変更やフラグ更新）
8. Story Database に記録

フロー：

Event 発生  
→ Transition 検索  
→ 条件評価  
→ World Rule 検証  
→ 確率判定  
→ State 更新  
→ Effects 実行  
→ Database 記録  

この State Machine により
Character・Thread・World の状態変化を統一的に管理する。

---

## 4. 改良版 State Transition JSON スキーマ・サンプル

{
  "state_transition": {
    "transition_id": "trans_001",
    "entity_type": "character",
    "source_state_id": "state_active",
    "target_state_id": "state_injured",
    "trigger_event": "battle_lost",
    "description": "戦闘敗北による負傷状態への遷移",

    "conditions": [
      {
        "type": "character_hp",
        "operator": "<=",
        "value": 20
      },
      {
        "type": "world_rule",
        "rule_id": "rule_combat_enabled",
        "required": true
      }
    ],

    "probability": 0.8,
    "priority": 1,
    "cooldown": 0,

    "effects": [
      {
        "effect_type": "state_change",
        "target_entity_type": "thread",
        "target_id": "thread_001",
        "new_state_id": "state_crisis"
      },
      {
        "effect_type": "flag_set",
        "flag": "revenge_motivation",
        "value": true
      }
    ],

    "required_world_rules": [
      "rule_combat_enabled"
    ],

    "required_character_states": [
      "state_alive"
    ],

    "required_flags": [
      "battle_mode"
    ],

    "tags": [
      "battle",
      "injury",
      "character_state"
    ],

    "metadata": {
      "created_at": "YYYY-MM-DDTHH:MM:SS+09:00",
      "updated_at": "YYYY-MM-DDTHH:MM:SS+09:00",
      "author": "system"
    }
  }
}

---

## 5. 大規模物語シミュレーションへの適用案

State Transition Model v2.0.1 は
Graph ベースの State Machine として動作する。

Node:
State

Edge:
State Transition

Trigger:
Event

Constraint:
World Rule

Effect:
State / Flag / Event

この構造により以下が可能になる。

Character の心理変化シミュレーション  
Thread 進行管理  
World 状態変化管理  
Conflict 発生管理  
Event 連鎖生成  
物語シミュレーション  
分岐ストーリー生成  
AI によるストーリー生成  

State Transition Model は
NWF における「物語の因果律」を管理するモデルである。

Character Model が「行動主体」
World Rule Model が「世界法則」
State Model が「状態」
State Transition Model が「因果律」
Event Model が「出来事」
Conflict Model が「葛藤」

これらが組み合わさることで
Story Engine が動作する。

---

## 6. まとめ

State Transition Model v2.0.1 は
単純な状態遷移定義ではなく、
Graph ベースの State Machine として設計される。

このモデルは
Character・Thread・World の状態変化を統一的に管理し、
World Rule・Event・Conflict と連携して
物語の因果関係を制御する。

State Transition Model は
NWF Story Engine の中核となるモデルである。

---

[EOF]