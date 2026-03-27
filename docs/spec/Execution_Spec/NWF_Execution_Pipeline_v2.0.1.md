Source: docs/spec/Execution_Spec/NWF_Execution_Pipeline_v2.0.1.md
Updated: 2026-03-27T21:38:00+09:00
PIC: Engineer / ChatGPT

# NWF Execution Pipeline v2.0.1

---

## 1. 概要

Execution Pipeline は NWF v2.0.1 (Story OS) における全エンジンの実行順序、データフロー、状態遷移、および検証・再試算ループを統合的に管理するシステム実行仕様である。

本仕様は単なる処理手順ではなく、Story OS 全体の動作サイクルを統治する「System Orchestration（システム制御機構）」として定義される。

Execution Pipeline は物語生成の実行順序、データ更新タイミング、エラー処理、検証ループ、状態保存を統合し、Story OS が自律的に物語を生成・検証・修正・記録する循環構造を形成する。

---

## 2. Execution Pipeline の役割

Execution Pipeline の役割は以下である。

- Engine 実行順序の統制
- Engine 間データフロー管理
- Story Execution Lifecycle の管理
- Analysis による検証ループ制御
- Error / Validation の処理制御
- State / History の永続化タイミング管理
- Narrative 出力タイミング管理

Execution Pipeline は Story OS の Orchestration Layer に属し、全 Engine を統括する制御機構として機能する。

---

## 3. Story OS Execution Lifecycle

NWF v2.0.1 では Execution Pipeline は直列処理ではなく、以下の 8 フェーズからなる Execution Lifecycle Loop として定義される。

Execution Lifecycle は以下の順序で実行される。

1. Load
2. Query
3. Plan
4. Execute (Event)
5. Simulate
6. Analyze
7. Narrate
8. Save

この 8 フェーズは Event / Beat 単位で繰り返されるマイクロループとして動作する。

---

## 4. Execution Lifecycle 詳細

### 4.1 Load Phase

目的：
物語実行に必要な基礎データを Data Layer から読み込む。

主な読み込みデータ：
- Story
- Thread
- Scene
- Timeline
- Character
- WorldRule
- State
- EmotionalCurve
- Previous StateHistory

Load フェーズでは Structure Error および Reference Error の検証が実行される。

---

### 4.2 Query Phase

目的：
Query Engine を使用して必要なデータを取得・検索・関連付けする。

主な処理：
- 現在 Timeline Position の取得
- 次 Event / Beat の候補検索
- 関連 Character / State / Emotional 情報取得
- 因果関係 Event の参照
- 過去 Event / StateHistory の検索

Query Engine は全 Engine のデータアクセスゲートウェイとして機能する。

---

### 4.3 Plan Phase

目的：
Story Engine および Timeline Engine により、次に実行される Event / Beat の計画を確定する。

主な処理：
- Timeline 上の次 Event 決定
- Scene / Beat 進行決定
- Event Priority / Dependency 確定
- Simulation パラメータ準備

このフェーズで物語の「次に起きる事実候補」が確定する。

---

### 4.4 Execute Phase (Event Engine)

目的：
Event Engine により Event を実行し、物語上の「事実」を確定させる。

主な処理：
- Event 実行
- Event Result 生成
- EventLog 作成
- Timeline Position 更新

Event 実行後、EventLog が生成される。

Event 実行直後に Validation Error の初期チェックが実行される。

---

### 4.5 Simulate Phase (Simulation / EmotionalCurve Engine)

目的：
Event 実行による状態変化を Simulation Engine で計算し、EmotionalCurve Engine により感情変化を更新する。

主な処理：
- StateDelta 計算
- Character State 更新
- Relationship State 更新
- World State 更新
- Emotional State 更新
- Emotional Curve 更新

Simulation 後に StateDelta が State に適用される。

---

### 4.6 Analyze Phase (Analysis Engine)

目的：
Analysis Engine により物語構造、因果関係、状態整合性、感情曲線整合性を検証する。

主な検証：
- 因果関係矛盾
- Timeline 矛盾
- Character 動機整合性
- Emotional Curve 異常
- 未回収伏線
- State 矛盾

問題が検出された場合、Execution Pipeline は Recalculate / Retry を実行する。

Recalculate Loop：
Analyze → 問題検出 → Event / Simulation 再実行 → 再 Analyze

このループは最大再試行回数に達するまで実行される。

---

### 4.7 Narrate Phase (Narrative Engine)

目的：
Narrative Engine により Event および State 変化を文章表現へ変換する。

主な処理：
- Scene Narrative 生成
- Beat Narrative 生成
- Character Dialogue 生成
- Narrative Output 作成

Narrative Error（文章上の矛盾・不自然表現）はこの段階で検出される。

---

### 4.8 Save Phase (Persistence)

目的：
Execution 結果を Data Layer に永続化する。

保存対象：
- State
- StateHistory
- EventLog
- TimelineLog
- EmotionalState
- AnalysisResult
- NarrativeOutput

StateHistory は Narrative 完了後に最終確定される。

---

## 5. Engine Orchestration 順序

Execution Pipeline における論理的 Engine 実行順序は以下である。

1. Query Engine
2. Story Engine
3. Timeline Engine
4. Event Engine
5. Simulation Engine
6. EmotionalCurve Engine
7. Analysis Engine
8. Narrative Engine
9. Persistence (Data Layer)

Analysis Engine は Simulation 後に実行され、必要に応じて Event または Simulation へ差し戻しを行う。

---

## 6. Analysis & Feedback Loop

Execution Pipeline は以下のフィードバックループを持つ。

Event → Simulation → Analysis → 問題検出 → 再 Simulation または Event 再計算 → Analysis → OK → Narrative

再試行制御：
- max_retry_event
- max_retry_simulation
- max_retry_analysis

最大再試行回数を超えた場合、Pipeline は Error として停止する。

---

## 7. Data Update & Persistence Strategy

各データの更新タイミングは以下の通り。

- Event 実行後
  EventLog 生成
  Timeline 更新

- Simulation 後
  State 更新
  EmotionalState 更新
  StateDelta 記録

- Analysis 後
  AnalysisResult 保存

- Narrative 後
  NarrativeOutput 保存
  StateHistory 最終確定

- Save Phase
  全ログおよび履歴を Data Layer に永続化

---

## 8. Error Management

Execution Pipeline における Error 発生フェーズは以下。

- Load Phase
  structure_error
  reference_error

- Execute / Simulate Phase
  validation_error

- Analyze Phase
  validation_error
  narrative_error（論理矛盾）

- Narrate Phase
  narrative_error

Critical Error の場合 Pipeline は停止する。
Warning Error の場合 Pipeline は継続する。

---

## 9. 実行粒度（Execution Granularity）

Execution Pipeline は以下の階層ループ構造を持つ。

- Story Loop
- Scene Loop
- Event / Beat Micro Loop

基本実行単位は Event / Beat Micro Loop とする。

Scene は Event Loop の集合、
Story は Scene Loop の集合として構成される。

---

## 10. まとめ

NWF Execution Pipeline v2.0.1 は Story OS の Orchestration System であり、全 Engine を統合し、以下を実現する。

- Event Driven Story Execution
- Simulation & Analysis Feedback Loop
- Narrative Generation Pipeline
- State History Persistence
- Error Controlled Execution
- Autonomous Story Execution Cycle

本 Pipeline は Story OS における「物語生成の心拍」として機能し、論理・感情・時間・物語表現を統合した自律的物語生成サイクルを形成する。

---

[EOF]