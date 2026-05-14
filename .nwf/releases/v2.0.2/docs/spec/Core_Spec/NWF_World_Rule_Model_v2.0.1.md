Source: docs/spec/Core_Spec/NWF_World_Rule_Model_v2.0.1.md
Updated: 2026-03-21T20:15:00+09:00
PIC: Engineer / ChatGPT

# NWF World Rule Model v2.0.1

---

## 1. v2.0.0 の限界分析（なぜエンジン化が必要か）

v2.0.0 の World Rule Model は
物語世界の設定情報を保存する「静的設定データモデル」であり、
物語の進行やイベント生成に対して直接的な制御能力を持たない。

しかし NWF v2.0 では Story Engine / Event Engine / Conflict Engine が
物語を半自動生成・管理する構造を持つため、
World Rule は単なる設定資料ではなく、
物語の整合性を監視し、イベント発生条件を制御する
「World Rule Engine」として機能する必要がある。

v2.0.0 の問題点：

1. ルール違反の概念が存在しない
2. Event 発生条件として利用できない
3. Conflict 生成との関連がない
4. scope が単一で階層構造がない
5. Character / Scene とのリンク構造がない
6. 物語シミュレーションに使用できない
7. 静的データであり動的制約になっていない

そのため v2.0.1 では
World Rule を「世界制約エンジン」として再設計する。

---

## 2. World Rule Model v2.0.1 属性定義

World Rule は以下の2種類の情報を持つ。

1. Static Settings（静的世界設定）
2. Dynamic Constraints（動的制約・ルールエンジン）

### 基本属性

world_rule_id  
rule_name  
rule_type  
description  

### スコープ属性

scope_level  
priority  
override_allowed  

### 静的設定属性

settings  
tags  

### 動的制約属性

trigger_logic  
constraint_conditions  
violation_consequence  
conflict_patterns  
effect  

### リンク属性

linked_entities  
metadata  

---

## 3. スコープ階層とオーバーライド・ルール

World Rule は以下のスコープ階層を持つ。

scope_level:

global  
regional  
character  
scene  

優先順位は以下の通り。

scene > character > regional > global

上位スコープは下位スコープのルールを上書きできる。
override_allowed が true の場合のみ上書き可能。

例：

global: 魔法は存在しない  
regional: 王国では魔法研究が許可  
character: 主人公だけ魔法が使える  

このような階層ルールを許可する。

---

## 4. 改良版 World Rule JSON スキーマ・サンプル

{
  "world_rule": {
    "world_rule_id": "rule_001",
    "rule_name": "記憶共有システム",
    "rule_type": "technology",
    "description": "人間の記憶を共有できる技術",
    
    "scope": {
      "scope_level": "global",
      "priority": 1,
      "override_allowed": false
    },

    "settings": {
      "memory_share_possible": true,
      "device_required": true
    },

    "constraints": {
      "trigger_logic": "memory_access_without_permission",
      "constraint_conditions": [
        "consent_required",
        "device_connected"
      ],
      "violation_consequence": [
        "legal_penalty",
        "memory_lock",
        "conflict_event"
      ]
    },

    "conflict_patterns": [
      "privacy_violation",
      "memory_theft",
      "identity_confusion"
    ],

    "effect": {
      "event_modifiers": [
        "memory_event_enabled",
        "investigation_event_enabled"
      ]
    },

    "linked_entities": {
      "characters": [],
      "scenes": [],
      "regions": []
    },

    "tags": [
      "technology",
      "memory",
      "society"
    ],

    "metadata": {
      "created_at": "YYYY-MM-DDTHH:MM:SS+09:00",
      "updated_at": "YYYY-MM-DDTHH:MM:SS+09:00",
      "author": "system"
    }
  }
}

---

## 5. Story Engine との連携フロー

World Rule Engine は Story Engine と以下の流れで連携する。

1. Event Engine がイベント候補を生成
2. World Rule Engine がイベントを検証
3. ルール違反があるか trigger_logic で判定
4. 違反する場合 violation_consequence を適用
5. Conflict Engine が conflict_patterns を参照し葛藤生成
6. Event を修正または新規 Conflict Event を生成
7. Story Database に記録

フロー：

Event Candidate  
→ Rule Check  
→ Constraint Validation  
→ Violation Detection  
→ Consequence  
→ Conflict Generation  
→ Event Finalization  

World Rule は以下を制御する。

Event 発生可能条件  
Character 行動制約  
Conflict 発生パターン  
世界設定の整合性  
ストーリーシミュレーション  

World Rule Model v2.0.1 は
NWF における「世界の物理法則・社会法則・物語制約」を管理する
最上位制約エンジンである。

---

## 6. まとめ

World Rule Model v2.0.1 は
単なる世界設定データではなく、
Story Engine・Event Engine・Conflict Engine を制御する
世界制約エンジンとして機能する。

このモデルは
Character・Event・Scene・Conflict の行動可能性を制限し、
物語世界の整合性を維持する。

World Rule は
NWF における「世界の神の視点」をデータ化したモデルである。

---

[EOF]