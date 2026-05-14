Source: docs/spec/Core_Spec/NWF_Core_Spec_Map_v2.0.1.md
Updated: 2026-03-22T21:16:00+09:00
PIC: Engineer / ChatGPT

# NWF Core Spec Map v2.0.1

---

## 1. 概要

NWF Core Spec Map は、NWF Core Specification v2.0.1 を構成する全 19 要素の仕様を統合し、相互依存関係、データフロー、実行サイクル、アーキテクチャ階層を整理するためのマスターマップである。

本ドキュメントは NWF の全体構造を俯瞰する最上位ナビゲーション仕様であり、すべての Core Spec は本マップを基準として設計・更新される。

NWF は最終的に以下の変換を目的とする。

Story World  
↓  
Narrative Structure  
↓  
Logical Structure  
↓  
Story Data  
↓  
Execution Flow  
↓  
Narrative Rendering  
↓  
Text / Novel / Script

---

## 2. Five-Layer Architecture

NWF Core Spec v2.0.1 は以下の 5 レイヤー構造で構成される。

### 2.1 Foundation Layer
データ構造・ID・データベースなど、すべての基盤。

- Data Model
- Entity ID System
- Story Database
- Core Architecture Index

### 2.2 World & Actor Layer
キャラクター・世界設定・関係性など、物語世界の構成要素。

- Character Model
- World Rule Model
- Relationship Model

### 2.3 Narrative Logic Layer
物語構造・時間・イベント・状態など、物語の論理構造。

- Thread Graph Model
- Scene Model
- Beat Model
- Event Model
- Timeline Model
- Thread State Model
- State Transition Model

### 2.4 Dynamic Force Layer
物語を動かす力（対立・感情・因果など）。

- Conflict Model
- Emotion / Intensity System
- Causality / Event Chain

### 2.5 Engine & Interface Layer
物語データを処理・分析・文章生成するエンジン。

- Execution Flow
- Narrative Rendering
- Query Language (NQL)

---

## 3. Dynamic Spec Integration

NWF の心臓部は以下の 3 エンジンである。

Execution Flow  
Narrative Rendering  
Query Language (NQL)

### 3.1 Execution Flow
物語データ処理の実行順序を定義する。

Data Ingestion  
Logic Validation  
Timeline Resolution  
Graph Generation  
Analysis  
AI Planning  
Narrative Rendering  
Output Generation  

### 3.2 Narrative Rendering
物語構造データを文章へ変換する。

Thread → Scene → Beat  
POV Control  
Information Control  
Temporal Rendering  
Voice / Style  
AI Prompt Template  
Text Generation  

### 3.3 Query Language (NQL)
物語データを検索・分析・検証する。

Temporal Query  
Graph Traversal  
Causality Tracking  
Aggregation Analytics  
AI Validation  
Unresolved Foreshadow Detection  

---

## 4. Entity & Relation Flow

NWF におけるデータの流れは以下の通り。

Character / World / Relationship 定義  
↓  
Thread 定義  
↓  
Scene 定義  
↓  
Beat 定義  
↓  
Event 定義  
↓  
Timeline 設定（ST / NT）  
↓  
State / Conflict 更新  
↓  
Story Database 保存  
↓  
Execution Flow 実行  
↓  
Graph / Analysis / Query  
↓  
Narrative Rendering  
↓  
Text Output  

### 4.1 ID Flow

Entity ID System によりすべての要素が ID で接続される。

Character_ID  
Thread_ID  
Scene_ID  
Beat_ID  
Event_ID  
Timeline_ID  
Conflict_ID  
Relationship_ID  

これにより NWF は完全なリレーショナル物語データ構造となる。

---

## 5. Story → Data → Text 変換フロー

NWF の最も重要な概念は以下の変換である。

Story Idea  
↓  
World / Character  
↓  
Thread Structure  
↓  
Scene Structure  
↓  
Beat Structure  
↓  
Event / Timeline / Conflict  
↓  
Story Data (Database)  
↓  
Execution Flow  
↓  
Narrative Rendering  
↓  
Novel Text

つまり NWF は

物語 = データ構造 + 実行フロー + レンダリング

という構造を持つ。

---

## 6. Core Spec 19 要素マスターリスト

NWF Core Spec v2.0.1 を構成する 19 要素とその役割を一言で定義する。

1. Core Architecture Index  
NWF 全体構造定義

2. Data Model  
物語データ基本構造

3. Entity ID System  
全要素識別子管理

4. Relationship Model  
キャラクター・要素関係グラフ

5. Character Model  
キャラクター情報管理

6. World Rule Model  
世界設定・ルール管理

7. Thread Graph Model  
物語メイン構造

8. Scene Model  
シーン構造

9. Beat Model  
最小物語単位

10. Event Model  
出来事・因果イベント

11. Timeline Model  
時間管理（ST / NT）

12. Thread State Model  
物語状態管理

13. State Transition Model  
状態変化ルール

14. Conflict Model  
対立・葛藤構造

15. Emotion / Intensity System  
感情強度・物語ピーク管理

16. Story Database  
物語データ保存層

17. Execution Flow  
データ処理・生成フロー

18. Narrative Rendering  
物語 → 文章変換エンジン

19. Query Language (NQL)  
物語データ検索・分析言語

---

## 7. NWF Core Structure Summary

NWF Core Structure を一行で表すと次のようになる。

World + Character  
→ Relationship  
→ Thread  
→ Scene  
→ Beat  
→ Event  
→ Timeline  
→ State / Conflict  
→ Database  
→ Execution Flow  
→ Query / Analysis  
→ Narrative Rendering  
→ Text

これは NWF の物語生成パイプラインである。

---

## 8. まとめ

NWF Core Spec Map v2.0.1 は以下を定義する。

- Five-Layer Architecture
- 19 Core Specifications
- Entity ID Flow
- Story Data Flow
- Execution Flow Integration
- Narrative Rendering Integration
- Query Language Integration
- Story → Data → Text 変換構造

本マップは NWF v2.0.1 の全体設計図であり、
NWF のすべての仕様はこの構造に基づいて統合される。

---

[EOF]