Source: docs/spec/AI_Workflow_Spec/NWF_AI_Story_Generation_Workflow_v2.0.1.md
Updated: 2026-03-28T19:39:00+09:00
PIC: Engineer / ChatGPT

# NWF AI Story Generation Workflow v2.0.1

---

## 1. 概要

本ドキュメントは、NWF v2.0.1（Story OS）における物語生成の標準ワークフローを定義する。

本Workflowは、従来の単純な段階生成モデルではなく、
Thread / Scene / Beat の構造階層に基づき、
System Engine の論理制約の下で、
複数のAI Agentが協調し、
Rewrite Loop による自己修復を行いながら物語品質を向上させる
**構造化物語生成プロセス（Structured Narrative Generation Process）**
を定義することを目的とする。

---

## 2. Generation Layer Hierarchy

NWFにおける物語生成は以下の階層構造に基づいて行われる。

生成階層：

1. Thread（ストーリーライン）
2. Scene（場面）
3. Beat（最小イベント）
4. Narrative（文章）

生成は上位構造から下位構造へと進行する。

Thread → Scene → Beat → Narrative

この階層構造により、
物語は構造駆動型（Structure Driven）で生成される。

---

## 3. End-to-End Workflow（v2.0.1 Standard Process）

NWF v2.0.1 における正式な物語生成ステップを定義する。

### Step 1: Inception
Human がアイデア、テーマ、コンセプトを入力する。

出力：
- Idea
- Theme
- Genre
- World Concept

---

### Step 2: Strategic Planning
Planner Agent が Thread（ストーリーライン）と Plot 構造を設計する。

出力：
- Thread Structure
- Plot Outline
- Major Events
- Character Arcs

Human は Outline を承認する。

---

### Step 3: Engine-Driven Simulation
Simulation Engine / Timeline Engine / World Rule Engine により
物語世界の状態計算を行う。

処理：
- Timeline 整合性
- World Rule 制約
- Character State 更新
- Event 因果関係計算

ここで Engine が論理的事実（State / Fact）を確定する。

---

### Step 4: Structural Construction
Event Generator / Scene Builder が
Scene および Beat 単位のイベント構造を生成する。

生成物：
- Scene List
- Beat Structure
- Event Chain
- Scene Objectives

ここで物語の構造が確定する。

---

### Step 5: Narrative Design
Narrative Strategist が語りの設計を行う。

設計内容：
- POV（視点）
- Narrative Voice
- 情報開示順序
- 緊張と緩和の配置
- Emotional Curve

---

### Step 6: Creative Authoring
Writer Agent が Narrative Text（本文）を生成する。

生成内容：
- 地の文
- セリフ
- 心理描写
- シーン描写
- アクション描写

Writer は Engine が確定した State / Fact を変更してはならない。

---

### Step 7: Critique & Analysis
Critic Agent と Analysis Engine が物語を分析する。

分析内容：
- プロット整合性
- キャラクター動機
- 感情曲線
- テーマ整合性
- 伏線構造
- pacing
- narrative quality

問題が検出された場合 Rewrite Loop に入る。

---

### Step 8: Self-Correction (Rewrite Loop)
Critic / Validator が問題を検出した場合、
Writer に Rewrite Directive を送る。

Rewrite Loop：

Draft
→ Analysis
→ Problem Detection
→ Rewrite Instruction
→ Rewrite
→ Re-Validation
→ OK なら次へ
→ NG ならループ継続

このループにより物語品質を向上させる。

---

### Step 9: Final Validation
最終整合性チェックを行う。

Validation 内容：
- Timeline 整合性
- World Rule 整合性
- Character State 整合性
- Plot 整合性
- Thread 整合性
- Integrity Score

Human が Final Approval を行う。

---

## 4. Engine & Agent Collaboration

物語生成における Engine と AI Agent の役割分担を定義する。

基本原則：

- Engine は論理を担当する
- AI Agent は表現を担当する
- Human は意思決定を担当する

役割分担：

Engine：
- Timeline
- Simulation
- World Rule
- Character State
- Analysis
- Integrity

AI Agents：
- Planning
- Narrative Design
- Writing
- Critique
- Editing
- Validation

Human：
- Approval
- Direction
- Final Decision

Engine Output（State / Fact）
→ AI Interface
→ AI Agents
→ Narrative / Text / Analysis
→ Human Approval

---

## 5. Multi-Agent Authoring Process

物語生成に関与する主なAI Agent：

- Planner
- Narrative Strategist
- Writer
- Critic
- Editor
- Validator
- Director

基本シーケンス：

Planner → Strategist → Writer → Critic → Editor → Validator → Director → Human

この分業構造により、
物語制作は AI チームによって行われる。

---

## 6. Rewrite & Improvement Loop

Rewrite Loop のトリガー条件：

- Timeline 矛盾
- Character 行動矛盾
- World Rule 違反
- Plot Hole
- Emotional Curve 不備
- Narrative Quality 低評価
- Theme 乖離

Rewrite Loop の終了条件：

- Integrity Score が閾値以上
- Critic 評価 OK
- Validator OK
- Human Approval

---

## 7. Human Approval Gates

Human-in-the-Loop における承認ポイントを定義する。

承認ゲート：

1. Idea Approval
2. Plot / Thread Approval
3. Character Approval
4. Scene Structure Approval
5. Draft Approval
6. Rewrite Approval
7. Final Approval

重要な意思決定は必ず Human が行う。

---

## 8. Parallel Execution Model

NWF v2.0.1 では以下の並列生成が可能である。

### Scene-Level Parallelism
複数の Scene を同時に生成可能。

### Variant Generation
同一プロットに対して複数の文体・展開案を生成可能。

### Analysis Parallelism
論理検証、感情曲線分析、テーマ分析を並列実行可能。

### Rewrite Parallelism
複数の Rewrite 案を同時生成し比較可能。

並列処理により Story Generation はスケーラブルになる。

---

## 9. Maintenance & Versioning

Story Generation Workflow の更新ルール：

- Engine 仕様変更時は Workflow を更新する
- Data Structure 変更時は生成順序を見直す
- AI Agent Role 追加時は Pipeline を更新する
- Version は SemVer に従う
- Workflow 変更は AI_Workflow_Index に記録する

---

## 10. まとめ

NWF AI Story Generation Workflow v2.0.1 は

- Thread → Scene → Beat → Narrative の構造生成
- Engine 制約下での生成
- Multi-Agent 協調執筆
- Rewrite Loop による自己修復
- Human-in-the-Loop 承認
- Parallel Generation 対応

を統合した
**構造化物語生成システム**である。

本Workflowは NWF Story OS における
物語生成プロセスの中核仕様となる。

---

[EOF]