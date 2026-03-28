Source: docs/spec/AI_Workflow_Spec/NWF_AI_Workflow_Index_v2.0.1.md
Updated: 2026-03-28T18:31:00+09:00
PIC: Engineer / ChatGPT

# NWF AI Workflow Index v2.0.1

---

## 1. 概要

本ドキュメントは Novel Writing Framework（NWF）v2.0.1（Story OS）における  
AI Workflow Specification の全体構造および設計思想を定義する最上位インデックスである。

これまでの Spec（Core / Architecture / Data / Engine / Execution / AI Interface）は、
Story OS の静的構造およびシステム仕様を定義してきた。

AI Workflow Spec は、それらの仕様を基盤として、
AI エージェントがどのように協調し、物語を生成・分析・改稿・検証し、
最終作品へと完成させるかという **動的運用プロセス** を定義する。

本 Spec は Story OS における **AI Orchestration（AI 協調制御）層** を構成する。

---

## 2. Story OS 全体レイヤー構造における位置付け

Story OS は以下のレイヤー構造で設計される。

### Story OS Layer Structure

1. Core Concept Layer  
2. System Architecture Layer  
3. Architecture Spec Layer  
4. Data Spec Layer  
5. Engine Spec Layer  
6. Execution Spec Layer  
7. AI Interface Layer  
8. AI Workflow Layer  
9. Tools / UI / External Interface Layer（将来）  
10. Runtime / Deployment Layer（将来）

AI Workflow Spec は **Layer 8: AI Workflow Layer** に位置する。

このレイヤーは以下の役割を持つ。

- Execution Pipeline 上で AI がどの順序で動作するか定義する
- AI Agent の役割分担と協調方法を定義する
- 物語生成・分析・改稿・検証の業務フローを定義する
- Human-in-the-Loop（作者介入）を定義する
- Rewrite / Improvement Loop を定義する
- 並列生成・並列分析などの Workflow モデルを定義する

つまり AI Workflow Layer は

**「Story OS を実際に動かす運用ロジック層」**

である。

---

## 3. Execution Pipeline と AI Workflow の関係

Story OS では以下の2種類の処理フローが存在する。

### 3.1 Execution Pipeline

Execution Pipeline は以下を定義する。

- Engine の実行順序
- Data の更新順序
- Simulation / Narrative / Validation の処理順序
- システム内部の時系列制御

つまり Execution は  
**「システム内部の処理パイプライン」** である。

### 3.2 AI Workflow

AI Workflow は以下を定義する。

- AI Agent の役割分担
- AI 間の情報受け渡し
- 生成 → 分析 → 改稿 → 検証 の業務フロー
- 人間の承認ポイント
- Rewrite Loop
- Parallel Workflow

つまり Workflow は  
**「AI エージェントと人間の作業フロー」** である。

### 3.3 両者の関係

Execution Pipeline と AI Workflow の関係は以下である。

Execution Pipeline の各フェーズの内部で  
AI Workflow が実行される。

関係性：

System Execution
    └ Execution Pipeline
        └ Engine Processing
            └ AI Workflow (Agent Collaboration)

つまり

Execution = システム処理の流れ  
Workflow = AI と人間の作業の流れ  

である。

---

## 4. AI Workflow v2.0.1 の中心概念

v2.0.1 における AI Workflow の中心構造は
単発生成ではなく、自己改善ループである。

### Rewrite & Improvement Loop

基本ループ：

Generate  
→ Analyze  
→ Critic  
→ Rewrite  
→ Validate  
→ Approval  
→ Finalize  

または以下のループ構造になる。

Generate  
→ Analyze  
→ Criticize  
→ Rewrite  
→ Validate  
→ OK?  
    No → Rewrite Loop  
    Yes → Finalize  

この構造を **Story Improvement Loop** と呼ぶ。

AI Workflow Spec はこのループを中心構造として設計される。

---

## 5. Human-in-the-Loop（作者承認ゲート）

Story OS は完全自動生成システムではない。  
必ず人間の作者が最終決定権を持つ。

Workflow 内には以下の承認ゲートを設置する。

### Approval Gates

- Idea Approval  
- Outline Approval  
- Character Approval  
- Scene Approval  
- Draft Approval  
- Rewrite Approval  
- Final Approval  

AI は生成・分析・提案・修正を行うが、  
**最終決定は常に Human Author が行う。**

---

## 6. AI Agent Collaboration（Multi-Agent Model）

Story OS では AI は単一の AI ではなく、
複数の役割を持つ Agent として動作する。

### AI Agent Roles

- Story Planner  
- Event Generator  
- Narrative Strategist  
- Writer  
- Critic  
- Editor  
- Validator  
- Director  
- User（Human Author）

これらの Agent がリレー形式で物語制作を行う。

基本パイプライン：

Planner  
→ Strategist  
→ Writer  
→ Critic  
→ Editor  
→ Validator  
→ User  

この Multi-Agent Collaboration が
AI Workflow Spec の中心思想である。

---

## 7. AI Workflow Spec ドキュメント構成（v2.0.1）

AI Workflow Spec は以下のドキュメントで構成される。

### Document Structure

1. NWF_AI_Workflow_Index_v2.0.1.md  
   AI Workflow Spec 全体インデックス・設計思想

2. NWF_AI_Collaboration_Model_v2.0.1.md  
   Multi-Agent 協調モデル

3. NWF_AI_Story_Generation_Workflow_v2.0.1.md  
   物語生成ワークフロー

4. NWF_AI_Analysis_Critique_Workflow_v2.0.1.md  
   分析・批評ワークフロー

5. NWF_AI_Rewrite_Improvement_Loop_v2.0.1.md  
   Rewrite / 改稿ループ

6. NWF_AI_Human_In_The_Loop_v2.0.1.md  
   人間介入・承認プロセス

7. NWF_AI_Agent_Role_Definition_v2.0.1.md  
   AI Agent の役割定義

8. NWF_AI_Parallel_Workflow_Model_v2.0.1.md  
   並列生成・並列分析ワークフロー

これらのドキュメント群により
AI Workflow Layer 全体を構成する。

---

## 8. 設計方針（v2.0.1 Workflow Design Principles）

AI Workflow Spec は以下の設計方針に基づく。

### Design Principles

- Multi-Agent Collaboration
- Human-in-the-Loop
- Rewrite & Improvement Loop
- Structural Story Generation
- Analysis Driven Editing
- Parallel Processing Support
- Deterministic Workflow Structure
- Reproducible Creative Process
- Scalable Workflow Architecture

本 Workflow は単なる文章生成手順ではなく、
**AI 協調による物語制作オペレーティングシステム**
として設計される。

---

## 9. まとめ

AI Workflow Spec は Story OS において
以下の役割を担う。

- AI エージェント協調制御
- 物語生成プロセス管理
- 分析・批評・改稿ループ管理
- 人間承認プロセス管理
- 並列生成・並列分析管理
- Story Improvement Loop 管理

Core / Architecture / Data / Engine / Execution / AI Interface
が Story OS の構造を定義するのに対し、

AI Workflow Spec は  
**Story OS を実際に動かす運用プロセスを定義する層**
である。

これにより Story OS は

Static Spec（構造）  
+  
Dynamic Workflow（運用）  

の2層構造として完成する。

---

[EOF]