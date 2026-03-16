Source: docs/spec/Core_Spec/NWF_Data_Model_v2.0.0.md
Updated: 2026-03-17T04:20:00+09:00
PIC: Engineer / ChatGPT

# NWF Data Model v2.0.0

---

## 1. 概要

本ドキュメントは  
Novel Writing Framework（NWF）における  
物語データ構造（Data Model）を定義する。

NWFでは物語を単なる文章ではなく  
**構造化されたストーリーデータ**として管理する。

このデータモデルは

- 物語構造の明確化
- エンジン処理との統合
- AIによる分析と生成
- Gitによるバージョン管理

を可能にする。

本仕様は  
NWF Core Architecture の基盤となる。

---

## 2. NWF Story Data Model

NWFでは物語は以下の主要要素で構成される。

WorldRule  
Character  
Thread  
Scene  
Beat

これらの要素は  
**Story Data Store** 内で管理される。

---

## 3. Story Data Store

Story Data Store は  
物語のすべてのデータを管理する集合である。

主な役割

- ストーリーデータ保存
- Entity間参照管理
- データ整合性維持
- Engine処理用データ供給

Story Data Store は通常以下の形式で保存される。

JSON  
YAML  
Markdown

---

## 4. Core Entities

### 4.1 WorldRule

WorldRule は  
物語世界の基本ルールを定義する。

例

世界観  
社会構造  
技術レベル  
物理法則  
魔法体系  
歴史

WorldRule は  
物語全体の環境制約を決定する。

---

### 4.2 Character

Character は  
物語に登場する主体である。

Characterは以下の情報を持つ。

character_id  
name  
role  
goal  
motivation  
personality  
relationships

Character は

Scene  
Thread

に参加する。

---

### 4.3 Thread

Thread は  
物語のドラマラインを表す。

Threadはストーリーの  
**問題 → 変化 → 解決**  
の流れを表現する。

Thread の主な要素

thread_id  
title  
thread_type  
status  
related_characters

例

Main Plot Thread  
Sub Plot Thread  
Mystery Thread  
Character Arc Thread

Thread は Scene を通じて進行する。

---

### 4.4 Scene

Scene は  
物語の出来事単位である。

Sceneは  
Threadの状態を変化させるイベントである。

Sceneの主な要素

scene_id  
location  
participants  
conflict  
outcome

Scene は  
Scene Timeline を形成する。

---

### 4.5 Beat

Beat は  
Scene内部の最小ドラマ単位である。

Beatは物語の微細な変化を表す。

例

情報提示  
感情変化  
行動  
対立  
決断

BeatはSceneの内部構造を形成する。

---

## 5. Entity Relationships

NWFのデータ要素は以下の関係を持つ。

WorldRule  
↓  
Character  
↓  
Thread  
↓  
Scene  
↓  
Beat

また各Entityは  
ID参照によって関連付けられる。

例

character_id → thread_id  
thread_id → scene_id  
scene_id → beat_id

---

## 6. Timeline Structure

Scene は  
時系列構造を形成する。

Scene Timeline は

story_start  
story_end

の間で順序付けられる。

Thread は  
Scene Timeline 内で進行する。

---

## 7. Data Representation

NWFではストーリーデータは  
以下の形式で表現できる。

JSON  
YAML  
Markdown

この設計により

人間による編集  
Gitによる履歴管理  
AIによる解析  

を容易にする。

---

## 8. Data Model Design Principles

NWF Data Model は  
以下の設計原則に基づく。

構造化ストーリー管理  
AI処理適合性  
拡張可能設計  
Gitフレンドリー構造  

---

## 9. まとめ

NWF Data Model は  
物語を構造化データとして管理するための  
基盤仕様である。

本データモデルにより

- 物語構造の明確化
- Engine処理との統合
- AI支援創作
- Git管理

が可能になる。

この仕様は  
NWF Core Architecture の中心となる。

---

[EOF]