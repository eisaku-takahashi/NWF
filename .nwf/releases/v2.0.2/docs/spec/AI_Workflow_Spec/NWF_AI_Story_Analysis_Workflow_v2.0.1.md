Source: docs/spec/AI_Workflow_Spec/NWF_AI_Story_Analysis_Workflow_v2.0.1.md
Updated: 2026-03-28T19:59:00+09:00
PIC: Engineer / ChatGPT

# NWF AI Story Analysis Workflow v2.0.1

---

## 1. 概要

本ドキュメントは、NWF v2.0.1 (Story OS) における物語の分析・評価・品質管理プロセスを定義する。
本 Workflow は単なる事後評価ではなく、Rewrite Loop を駆動し、物語の整合性・構造健全性・芸術性を維持・向上させるための
「知能的品質管理システム」として機能する。

Analysis Workflow は以下の役割を持つ。

・物語構造の整合性検証  
・設定・時系列・因果関係の矛盾検知  
・物語品質（感情曲線・テーマ性・テンポ）の評価  
・Integrity Score の算出  
・修正指示（Rewrite Directive）の生成  
・Rewrite Loop の起動判定  

本 Workflow は Story Generation Workflow と Execution Pipeline の間に位置し、
Story OS 全体の品質ゲートとして機能する。

---

## 2. Analysis-Driven Writing 概念

NWF v2.0.1 では執筆プロセスは以下の循環構造を持つ。

Generate → Analyze → Score → Rewrite → Re-Analyze → Finalize

このプロセスを Analysis-Driven Writing と呼ぶ。

従来の執筆プロセス
Generate → Human Edit → Finish

NWF の執筆プロセス
Generate → AI Analysis → Integrity Score → Rewrite Loop → Quality Stabilization

つまり Analysis Engine は「編集者」「批評家」「校正者」「構造エンジニア」を統合した
自動品質管理システムとして機能する。

---

## 3. Analysis Layer Mapping

物語は複数の階層構造を持つため、分析も階層ごとに実行される。

### 3.1 Thread Layer Analysis
・Thread 目的の達成度  
・Thread 間の因果関係  
・伏線と回収の対応  
・Timeline 整合性  
・World Rule 違反チェック  

### 3.2 Scene Layer Analysis
・Scene Goal の存在  
・Scene Conflict の明確性  
・Scene Outcome の妥当性  
・前後 Scene との因果関係  
・情報量とテンポ  

### 3.3 Beat Layer Analysis
・感情変化  
・キャラクター行動の動機  
・セリフの自然さ  
・視点の一貫性  
・描写密度  

### 3.4 Narrative Layer Analysis
・テーマ表現  
・感情曲線  
・物語テンポ  
・ジャンル適合性  
・読者理解度  

---

## 4. End-to-End Analysis Workflow

Analysis Workflow は以下の 7 ステップで構成される。

### Step 1 Structure Parsing
生成された Thread / Scene / Beat 構造を解析し、
構造的欠損や未定義要素を検出する。

チェック項目
・Scene に Goal が存在するか
・Thread に Ending が存在するか
・Beat が Scene に紐付いているか
・Timeline に未定義時間がないか

### Step 2 Logic & Rule Validation
World Rule Engine / Timeline Engine による整合性検証。

検証対象
・物理法則
・魔法ルール
・キャラクター能力制限
・時系列矛盾
・地理的移動時間
・死亡キャラの再登場
・未回収伏線

### Step 3 Narrative Critique
AI Critic による定性的評価。

評価項目
・面白さ
・緊張感
・感情曲線
・テーマ表現
・キャラクター魅力
・テンポ
・読者没入感

### Step 4 Integrity Scoring
各評価結果を統合し Integrity Score を算出する。

### Step 5 Issue Extraction
問題箇所を Issue として抽出する。

Issue 例
・Scene 12 に目的が存在しない
・Thread B の伏線が未回収
・キャラクター動機が不明
・感情曲線が平坦
・World Rule 違反

### Step 6 Directive Generation
Issue を元に Rewrite Directive（修正指示）を生成する。

### Step 7 Loop Control
Integrity Score が閾値未満の場合 Rewrite Loop を起動する。

---

## 5. Integrity Score Specification

Integrity Score は物語品質を数値化した総合指標である。

Integrity Score は以下の要素で構成される。

### 5.1 Consistency Score
整合性スコア
・設定矛盾
・Timeline 矛盾
・キャラクター設定違反
・World Rule 違反

### 5.2 Narrative Quality Score
物語品質スコア
・感情曲線
・伏線回収
・テンポ
・対立構造
・テーマ表現

### 5.3 Structural Integrity Score
構造健全性
・Scene Goal 達成率
・因果関係強度
・Thread 完結率
・無意味 Scene の割合

### 5.4 Readability / Style Score
表現品質
・文章の読みやすさ
・文体の統一
・語彙の適切性
・冗長性

### 5.5 Overall Integrity Score
総合スコア

Overall Integrity Score =
0.30 Consistency +
0.30 Narrative Quality +
0.25 Structural Integrity +
0.15 Readability

---

## 6. Rewrite Loop Control

Rewrite Loop は Analysis Workflow によって制御される。

### 6.1 Rewrite 発動条件
Integrity Score < Threshold

Threshold 例
・90以上 → 完成
・80以上 → 軽微修正
・70以上 → Rewrite 推奨
・70未満 → Rewrite 必須
・60未満 → 構造再設計

### 6.2 Rewrite Loop フロー
1 Analysis 実行
2 Integrity Score 算出
3 Issue 抽出
4 Directive 生成
5 Writer Rewrite
6 再 Analysis
7 Score 改善確認
8 Threshold 到達まで Loop

---

## 7. Rewrite Directive Protocol

Rewrite Directive は AI Writer に対する修正指示フォーマットである。

Directive 構造

directive_id  
target_layer (Thread / Scene / Beat / Narrative)  
target_id  
problem_description  
rewrite_instruction  
priority  
expected_effect  

Directive 例

Scene 18 に主人公の行動動機が存在しない  
→ Scene 17 に動機となる情報を追加する  
→ Scene 18 の行動理由を明確化する  

---

## 8. Multi-Agent Critique Model

Analysis は複数 AI エージェントによって実行される。

### 8.1 Analyst Agent
論理・構造・整合性を分析する。
・因果関係
・Timeline
・World Rule
・Thread 構造
・Scene Goal

### 8.2 Critic Agent
芸術性・感情・面白さを評価する。
・キャラクター魅力
・感情曲線
・テーマ
・演出
・テンポ
・読後感

### 8.3 Editor Agent
文章品質を評価する。
・読みやすさ
・文体
・語彙
・冗長性
・誤字

これらの結果を Integrity Engine が統合する。

---

## 9. Human Decision Support (HITL)

最終判断は Human が行う。

Human は以下を判断する。
・Rewrite を実行するか
・Issue を無視するか
・テーマや構造を変更するか
・作品完成とするか

Analysis は Human の意思決定支援システムとして機能する。

---

## 10. Validation System Integration

Analysis Workflow は以下の Engine と連携する。

・World Rule Engine
・Timeline Engine
・ Character Engine
・ Foreshadow Engine
・ Emotional Curve Engine
・ Integrity Engine
・ Execution Pipeline

これにより Story OS 全体の整合性が維持される。

---

## 11. Metrics & Versioning

Analysis Metrics はバージョン管理される。

管理対象
・Integrity Score 計算式
・Score Weight
・Threshold
・Critique Criteria
・Validation Rules

これにより Story OS は継続的に進化可能となる。

---

## 12. まとめ

NWF AI Story Analysis Workflow は
物語を分析・評価するためのシステムではなく、

物語の完成度を自動的に向上させるための
「知能的品質管理ループ」である。

Story OS において Analysis Engine は
Writer と同等、もしくはそれ以上に重要な役割を持つ。

Generate Engine が物語を生み出し、
Analysis Engine が物語を完成させる。

この 2 つのエンジンの循環こそが
NWF Story OS の中核構造である。

---

[EOF]