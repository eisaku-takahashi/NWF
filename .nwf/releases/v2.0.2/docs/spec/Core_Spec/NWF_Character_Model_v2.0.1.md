Source: docs/spec/Core_Spec/NWF_Character_Model_v2.0.1.md
Updated: 2026-03-21T19:43:00+09:00
PIC: Engineer / ChatGPT

# NWF Character Model v2.0.1

---

## 1. 概要

Character Model は物語に登場するキャラクターを管理する
ナラティブ・データモデルである。

NWF v2.0.1 では Character は単なるプロフィール情報ではなく、
Story Database 上の Graph Node（物語グラフのノード）として扱われる。

Character は以下のエンティティと関係を持つ。

・State
・Relationship
・Scene
・Event
・Thread
・Timeline

Character 自身は状態や関係の詳細を直接保持せず、
ID参照による疎結合構造を採用する。

---

## 2. v2.0.0 の構造的問題点（静的データの限界）

v2.0.0 の Character Model には以下の問題があった。

1. Character がプロフィール情報のみの静的データだった
2. State 概念が Character 内部に含まれていた
3. Relationship 概念がモデルに存在しなかった
4. Scene / Event / Thread との関係が定義されていなかった
5. Graph データモデルに対応していなかった

その結果、Character が物語構造のノードとして機能しなかった。

v2.0.1 では Character を Graph Node として再設計する。

---

## 3. Character Model v2.0.1 属性定義

Character Entity は以下の属性を持つ。

### 3.1 Core Attributes

character_id  
name  
role  
description  

### 3.2 Story Attributes

goal  
conflict  
importance  
pov_flag  
current_state_id  

### 3.3 Metadata Attributes

tags  
metadata  

### 3.4 属性一覧表

character_id  
キャラクターID

name  
キャラクター名

role  
物語内役割（protagonist / antagonist / supporting など）

description  
キャラクター説明

goal  
キャラクターの目的

conflict  
キャラクターの対立・問題

importance  
物語重要度（1〜5）

pov_flag  
視点キャラクターかどうか

current_state_id  
現在の状態ID（State Entity を参照）

tags  
検索・分類用タグ

metadata  
拡張情報格納用オブジェクト

---

## 4. State / Relationship との連携ロジック

### 4.1 State との連携

Character は状態の詳細を持たない。
Character は current_state_id のみ保持し、
状態の詳細は State Entity に保存する。

Character → current_state_id → State

これにより Character と State は疎結合となる。

### 4.2 Relationship との連携

Character 同士の関係は Character Model 内に直接記述しない。
Relationship Entity および links データで管理する。

Character → Relationship → Character

または

Character → character_relationship_links → Character

この設計により多対多関係を柔軟に管理できる。

---

## 5. Character JSON スキーマ・サンプル

Character JSON の標準構造は以下とする。

{
  "character": {
    "character_id": "char_001",
    "name": "主人公",
    "role": "protagonist",
    "description": "物語の主人公",

    "story_attributes": {
      "goal": "真実を知る",
      "conflict": "組織に追われている",
      "importance": 1,
      "pov_flag": true,
      "current_state_id": "state_001"
    },

    "metadata": {
      "tags": ["hero", "detective"],
      "notes": "成長型キャラクター"
    }
  }
}

---

## 6. キャラクター運用（生成・更新）ガイドライン

### 6.1 Character 生成

Character 作成時に以下を設定する。

character_id  
name  
role  
description  
goal  
importance  
pov_flag  

State は別途 State Entity として作成し、
current_state_id を Character に設定する。

### 6.2 Character 更新

Character 更新では以下を変更可能とする。

goal  
conflict  
current_state_id  
metadata  
tags  

Relationship や Scene 登場情報は Character ではなく
links データを更新する。

### 6.3 設計原則

Character は以下を守る。

1. 状態の詳細は State に持たせる
2. 人間関係は Relationship / links に持たせる
3. Scene / Event との関係は links で管理
4. Character は物語グラフのノードとして扱う
5. Character JSON は軽量に保つ

---

## 7. まとめ

Character Model v2.0.1 では Character を
静的プロフィールデータから
物語グラフのノードへと再定義した。

本モデルでは以下の設計を採用した。

・Graph Node としての Character
・State の外部化
・Relationship の外部管理
・ID参照による疎結合構造
・拡張可能な metadata 構造

Character Model v2.0.1 は
Story Database と Graph Data Model の中核となる
重要なエンティティモデルである。

---

[EOF]