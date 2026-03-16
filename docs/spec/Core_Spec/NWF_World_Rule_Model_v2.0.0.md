Source: docs/spec/Core_Spec/NWF_World_Rule_Model_v2.0.0.md
Updated: 2026-03-17T05:10:00+09:00
PIC: Engineer / ChatGPT

# NWF World Rule Model v2.0.0

---

## 1. 概要

World Rule Model は
物語世界のルールを管理するデータモデルである。

物理法則、社会構造、特殊ルールなど
物語世界の制約条件を定義する。

---

## 2. World Rule の役割

World Rule は以下を管理する。

世界設定  
物理法則  
社会ルール  
特殊能力  

---

## 3. World Rule 属性

world_rule_id

ルールID

rule_name

ルール名称

rule_type

ルール種別

description

ルール説明

scope

適用範囲

---

## 4. World Rule JSON Example

{
  "world_rule": {
    "world_rule_id": "rule_001",
    "rule_name": "記憶共有システム",
    "rule_type": "technology",
    "scope": "global",
    "description": "人間の記憶を共有できる技術が存在する"
  }
}

---

## 5. 関連 Spec

NWF_Story_Database  
NWF_Event_Model  
NWF_Conflict_Model

---

## 6. まとめ

World Rule Model は
物語世界の基本ルールを定義する。

このルールは
Event・Conflict・Character の行動制約となる。

---

[EOF]