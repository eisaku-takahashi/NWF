Source: docs/spec/System_Architecture/NWF_System_Architecture_v2.0.1.md
Updated: 2026-03-23T15:20:00+09:00
PIC: Engineer / ChatGPT

# NWF System Architecture v2.0.1

---

## 1. システム概要

NWF System Architecture は Novel Writing Framework（NWF）全体の構造を定義する最上位レベルのアーキテクチャ仕様である。

NWF v2.0.1 において、NWF は単なる小説制作ツールではなく、以下のように定義される。

NWF = Story Operating System (Story OS)

これは物語を文章として直接書くのではなく、

World
Character
Relationship
Thread
Scene
Beat
Event
Timeline
State
Conflict
Emotion

といった物語構造要素をデータとして構築し、
それらをシステム上で実行・解析・レンダリングすることで、
最終的に文章として出力するシステムである。

物語生成パイプラインは以下で表現される。

Story Structure Data
→ Story Database
→ Execution Pipeline
→ Narrative Rendering
→ Text Output

NWF は以下の要素を統合したプラットフォームである。

Story Database
Graph Structure Engine
Simulation Engine
Query / Analysis Engine
Narrative Rendering Engine
AI Co-Creation System

本仕様は NWF 全体のシステム構造、データ構造、実行構造、AI連携構造を定義する。

---

## 2. Architectural Principles

NWF System Architecture は以下の設計原則に基づく。

1. Story as Data
物語を文章ではなく構造化データとして管理する。

2. Graph-Based Narrative Structure
物語構造は Thread、Event、Relationship などの有向グラフとして管理する。

3. Deterministic Execution Pipeline
物語データは定義された Execution Pipeline によって決定論的に処理される。

4. Stateful World Model
World、Character、Relationship、Thread は状態を持ち、
Event によって State Transition が発生する。

5. Dual-Axis Timeline
Timeline は Story Time（ST）と Narrative Time（NT）の二重時間軸で管理される。

6. Modular Engine Architecture
各処理は Engine として分離され、Execution Flow によって統合される。

7. Human + AI Co-Creation
人間と AI が共同で物語構造を設計・解析・生成する制作環境を提供する。

---

## 3. Layer Architecture

NWF Core v2.0.1 は Five-Layer Architecture を採用する。

Layer 1: Foundation Layer
Layer 2: World & Actor Layer
Layer 3: Narrative Logic Layer
Layer 4: Dynamic Force Layer
Layer 5: Engine & Interface Layer

### 3.1 Foundation Layer

Foundation Layer は NWF システムの基盤構造を定義する。

主な要素

Core Architecture Index
Data Model
Entity ID System
Story Database
Graph Structure
Timeline System

このレイヤーはすべてのレイヤーの基盤となる。

### 3.2 World & Actor Layer

World と Actor（登場主体）に関するモデルを定義する。

主な要素

Character Model
World Rule Model
Relationship Model
Organization
Location
Item

このレイヤーは物語世界と登場人物の状態を管理する。

### 3.3 Narrative Logic Layer

物語構造の論理構造を定義する。

主な要素

Thread Graph Model
Scene Model
Beat Model
Event Model
Timeline Model
Thread State Model
State Transition Model

このレイヤーは物語構造と因果関係を管理する。

### 3.4 Dynamic Force Layer

物語を動かす力学要素を管理する。

主な要素

Conflict Model
Emotion / Intensity System
Motivation
Goal
Obstacle
Tension

このレイヤーは物語の動力学を管理する。

### 3.5 Engine & Interface Layer

データ処理、実行、AI連携を担当する。

主な要素

Execution Flow
Narrative Rendering
Query Language (NQL)
Analysis Engine
AI Interface
AI Workflow

このレイヤーは NWF を実行するシステム層である。

---

## 4. Component Architecture

NWF Core Spec v2.0.1 は以下の 19 Spec で構成される。

1. NWF_Core_Architecture_Index
2. NWF_Data_Model
3. NWF_Entity_ID_System
4. NWF_Story_Database
5. NWF_Character_Model
6. NWF_World_Rule_Model
7. NWF_Relationship_Model
8. NWF_Thread_Graph_Model
9. NWF_Scene_Model
10. NWF_Beat_Model
11. NWF_Event_Model
12. NWF_Timeline_Model
13. NWF_Thread_State_Model
14. NWF_State_Transition_Model
15. NWF_Conflict_Model
16. NWF_Emotion_Intensity_System
17. NWF_Execution_Flow
18. NWF_Narrative_Rendering
19. NWF_Query_Language

これらの Spec は Five-Layer Architecture に対応して配置される。

Foundation Layer
Data_Model
Entity_ID_System
Story_Database

World & Actor Layer
Character_Model
World_Rule_Model
Relationship_Model

Narrative Logic Layer
Thread_Graph_Model
Scene_Model
Beat_Model
Event_Model
Timeline_Model
Thread_State_Model
State_Transition_Model

Dynamic Force Layer
Conflict_Model
Emotion_Intensity_System

Engine & Interface Layer
Execution_Flow
Narrative_Rendering
Query_Language

---

## 5. Data & Graph Architecture

NWF のデータ構造は Multi-Graph Architecture を採用する。

主なグラフ構造

Thread Graph
Event Causal Graph
Relationship Graph
State Transition Graph
Timeline Graph

すべてのノードは Entity ID System によって一意に識別される。

例

CHR-001
THR-010
SCN-020
EVT-101

Event は cause_ids / effect_ids によって因果関係グラフを形成する。

Timeline は Story Time（ST）と Narrative Time（NT）の
二重タイムスタンプを持つ。

Story Database はこれらすべての Entity と Graph を保存する
物語データベースである。

---

## 6. Execution Architecture

NWF の Execution Pipeline は以下で構成される。

Data Ingestion
Logic Synthesis
Structure Validation
Timeline Resolution
State / Conflict Update
Database Storage
Query / Analysis
Narrative Rendering
Text Output

この Execution Pipeline により、
物語データは解析・検証・更新・出力される。

Timeline Resolution では ST / NT の整合性が検証される。
State Update では Character / World / Thread の状態遷移が更新される。

---

## 7. AI Integration Architecture

NWF は Human + AI Co-Creation Workflow を採用する。

制作ループは以下である。

Human Edit
→ Data Update
→ Execution Flow
→ AI Analysis
→ AI Suggestion
→ Human Revision
→ Narrative Rendering
→ Text Output
→ Human Edit

AI の役割

Director AI
物語構造設計、プロット設計

Engineer AI
構造検証、整合性チェック、データ構造解析

Writer AI
文章生成、シーン描写、会話生成

AI Interface は JSON ベースの構造化データを
入力・出力フォーマットとする。

---

## 8. Project Directory Structure

NWF Project Root を基準としてディレクトリ構造を定義する。

<project_root>/

docs/
spec/
engines/
schemas/
projects/
runtime/
tools/
tests/
archive/

docs/spec はすべての仕様書を格納する。
projects は Story Database を格納する。
engines は Engine 実装を格納する。

---

## 9. Data & Control Flow

NWF のデータフローは以下である。

Story Structure Data
→ Story Database
→ Execution Pipeline
→ Analysis / Query
→ Narrative Rendering
→ Text Output

制御フローは Execution Flow Engine によって管理される。

Execution Flow は各 Engine の実行順序、
Validation、Timeline Resolution、State Update を管理する。

---

## 10. まとめ & 役割定義

NWF System Architecture は
NWF 全体のシステム構造を定義する最上位設計書である。

Core Architecture Index は概念体系と設計原則を定義する「憲法」であり、
System Architecture はそれをシステム構造として実装レベルに配置する
「システム設計図」である。

Core Specification はデータ構造とモデルを定義し、
Engine Specification は処理ロジックを定義し、
Execution Specification は実行順序を定義し、
AI Specification は AI ワークフローを定義する。

System Architecture はそれらすべてを統合する
NWF の全体構造設計書として機能する。

---

[EOF]