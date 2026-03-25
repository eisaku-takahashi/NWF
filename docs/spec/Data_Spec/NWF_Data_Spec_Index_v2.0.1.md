Source: docs/spec/Data_Spec/NWF_Data_Spec_Index_v2.0.1.md
Updated: 2026-03-26T05:24:00+09:00
PIC: Engineer / ChatGPT

# NWF_Data_Spec_Index v2.0.1
Data Architecture Overview (Story OS)

---

## 1. 概要

本ドキュメントは NWF (Novel Writing Framework) v2.0.1 における Data Layer の全体構造を定義する **Data Architecture Overview** である。

NWF v2.0.1 では、物語を「文章」ではなく **状態・因果・時間・認識によって構成される動的システム（Story OS）」** として扱う。
そのため Data Spec は単なるデータ定義ではなく、Engine・Simulation・Narrative・Analysis などの各システム層と連動する **システム基盤** として設計される。

本ドキュメントの目的は以下である。

- Data Layer の分類と責任範囲の定義
- Data Spec 間の関係性の整理
- Engine Layer と Data Layer の対応関係の明示
- 将来拡張 Data Spec の整理
- データ整合性と保守方針の定義

本 Index は Data_Spec ディレクトリの **最上位アーキテクチャ文書** として機能する。

---

## 2. Data Layer Classification

NWF v2.0.1 では Data Layer を以下の 6 カテゴリに分類する。

### 2.1 Structure Data（物語構造データ）

物語の骨格構造を定義するデータ。

対象データ：
- Story
- Thread
- Scene
- Beat

役割：
物語の構造階層を定義し、Narrative Engine や Story Engine の基盤となる。

---

### 2.2 Entity Data（構成要素データ）

物語世界を構成する存在を定義するデータ。

対象データ：
- Character
- World
- Location
- Item
- Organization
- Relationship（将来拡張）

役割：
Simulation Engine および State System の主体・客体を定義する。

---

### 2.3 State & Dynamics Data（状態・動的変化データ）

物語内で変化する状態や対立、感情曲線などを扱うデータ。

対象データ：
- State
- Conflict
- EmotionalCurve
- Goal
- Knowledge
- RelationshipState

役割：
Simulation Engine が物語の状態変化を計算・更新するための基盤となる。

---

### 2.4 Event & Time Data（イベント・時間データ）

出来事と時間軸、因果関係を扱うデータ。

対象データ：
- Timeline
- Event
- Causality
- History

役割：
物語の時間進行と因果関係の整合性を管理する。
Causality Check や Timeline Simulation の基盤となる。

---

### 2.5 Narrative & Information Data（提示・情報データ）

読者・視点・情報開示・伏線など、Narrative 制御を扱うデータ。

対象データ：
- Narrative
- Foreshadowing
- Information
- Reveal
- Perspective

役割：
Narrative Engine が「読者に何がいつ見えるか」を制御するためのデータ。

---

### 2.6 Query & Analysis Data（クエリ・分析データ）

システムへの問い合わせや分析結果を扱うデータ。

対象データ：
- Query
- AnalysisResult
- Report
- Metrics

役割：
Story Analysis、Plot Analysis、Consistency Check などの結果を保存する。

---

## 3. Core Data Specifications (Structure & Entity)

### 3.1 Structure Core

Structure Data は物語の階層構造を形成する。

階層構造：

Story  
 └ Thread  
     └ Scene  
         └ Beat  

説明：

- Story: 作品全体
- Thread: ストーリーライン（主線・副線）
- Scene: 時間・場所・状況の単位
- Beat: 感情・行動・情報提示の最小単位

Structure Data は Story Engine と Narrative Engine の基盤となる。

---

### 3.2 Entity Core

Entity Data は物語世界の構成要素を定義する。

主な Entity：

- Character
- World
- Location
- Item
- Organization

Entity は State・Event・Conflict の主体となる。

---

## 4. Dynamics & Intelligence Specifications (State & Knowledge)

このカテゴリでは物語の「変化」を扱う。

主なデータ：

- State（状態）
- Conflict（対立）
- EmotionalCurve（感情曲線）
- Goal（目的）
- Knowledge（知識）
- RelationshipState（関係性状態）

関係例：

- Conflict は Character と Goal に依存する
- EmotionalCurve は Scene / Beat に依存する
- State は Character / World / Relationship に依存する
- Knowledge は Information / Event に依存する

これらは Simulation Engine と AI Analysis の中核データとなる。

---

## 5. Operational Specifications (Causality & Query)

### 5.1 Event & Timeline

Event は物語内で発生する出来事を定義する。
Timeline は Event を時間順に管理する。

Causality（因果関係）は以下を管理する：

- Event A が Event B の原因
- Event の前提条件
- Event の結果 State
- Timeline 整合性

これにより **Causality Check** が可能になる。

---

### 5.2 Query & Analysis

Query Data はシステムへの問い合わせを定義する。

例：

- このキャラクターの感情曲線を取得
- この Thread の Conflict を取得
- Timeline の因果矛盾を検出
- Foreshadowing 未回収一覧を取得

AnalysisResult は分析結果を保存する。

---

## 6. Engine-Data Mapping Table

Engine と Data Spec の対応関係を以下に示す。

StoryEngine
- Story
- Thread
- Scene
- Beat

SimulationEngine
- State
- Conflict
- Goal
- Relationship
- Event
- Timeline

NarrativeEngine
- Narrative
- Foreshadowing
- Information
- Perspective
- Scene
- Beat

AnalysisEngine
- Query
- AnalysisResult
- Metrics
- Timeline
- Conflict
- EmotionalCurve

WorldEngine
- World
- Location
- Organization
- Item

CharacterEngine
- Character
- Relationship
- State
- Goal
- Knowledge

---

## 7. Inter-Data Dependency Graph

主要な依存関係を以下に示す。

- Thread → Story
- Scene → Thread
- Beat → Scene
- Conflict → Character / Goal / State
- EmotionalCurve → Character / Scene / Beat
- Event → Character / Location / Timeline
- Timeline → Event
- Narrative → Scene / Information
- Foreshadowing → Event / Information
- Knowledge → Information / Event
- Relationship → Character
- State → Character / World / Relationship

原則：
下位構造は上位構造に依存しない。
時間データは Structure と Entity に依存する。
Narrative は Event と Information に依存する。

---

## 8. Future Expansion Specs

将来追加予定の Data Spec：

- RelationshipData
- InformationData
- ItemData
- OrganizationData
- MagicSystemData
- TechnologyData
- EconomyData
- CultureData
- LanguageData
- ThemeData
- SymbolData
- MotifData

これらは World Simulation および Narrative Analysis 強化のために追加される予定。

---

## 9. Maintenance & Integrity

Data Layer の整合性を維持するため、以下のチェックを行う。

### 9.1 Causality Check
- 原因のない Event が存在しないか
- 結果のない Event が存在しないか
- Timeline の順序矛盾
- Character の生存状態矛盾

### 9.2 Structure Check
- Scene が Thread に属しているか
- Beat が Scene に属しているか
- 孤立 Thread が存在しないか

### 9.3 Narrative Check
- 未回収 Foreshadowing
- 情報開示順序の矛盾
- 視点矛盾

### 9.4 State Consistency Check
- Character State の時間逆行
- Relationship の不整合
- Goal の未解決

---

## 10. まとめ

NWF v2.0.1 において Data Layer は単なるデータ定義ではなく、

Structure  
Entity  
State  
Event  
Narrative  
Query  

によって構成される **Story OS の基盤アーキテクチャ** である。

本 Data Spec Index は Data_Spec 全体の設計地図として機能し、
すべての Data Spec は本アーキテクチャに従って設計・拡張される。

---

[EOF]