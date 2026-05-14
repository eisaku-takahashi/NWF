Source: docs/spec/Engine_Spec/NWF_AnalysisEngine_v2.0.1.md
Updated: 2026-03-27T13:44:00+09:00
PIC: Engineer / ChatGPT

# NWF Analysis Engine v2.0.1
(Intelligence & Verification Layer Specification)

---

## 1. 概要

Analysis Engine は NWF v2.0.1（Story OS）において、物語全体の整合性検証・構造分析・品質評価を担当する Intelligence Layer の中核エンジンである。

本エンジンは単なるデータ解析ツールではなく、Story OS における「物語の論理的守護者（Logical Guardian of Narrative）」として機能する。

Story Engine、Event Engine、Timeline Engine、Thread Engine、Scene Engine など、すべてのエンジンが生成したデータを横断的に解析し、以下を実行する。

- 矛盾の検知
- 因果関係の整合性検証
- 物語構造の分析
- テンポ・密度の評価
- 未回収要素の検出
- 改善提案の生成
- Story Engine への再計算要求（Rollback Trigger）

Analysis Engine は Story OS における品質管理・構造監査・論理検証の最上位システムである。

---

## 2. System Architecture 上の位置づけ

NWF v2.0.1 の System Architecture において、Analysis Engine は Intelligence Layer に配置される。

Layer 構造：

- Data Layer
- Engine Layer
- Simulation Layer
- Intelligence Layer
- Interface Layer

Intelligence Layer には以下のエンジンが存在する。

- Simulation Engine（未来予測・シミュレーション）
- Analysis Engine（整合性検証・構造解析）

役割の違い：

Simulation Engine:
未来の展開・分岐・状態変化をシミュレーションする

Analysis Engine:
現在および過去の物語データを解析し、整合性・構造・品質を検証する

Analysis Engine は全 Engine の出力データを入力として使用する「全体監査エンジン」である。

---

## 3. Core Architecture

Analysis Engine は以下のデータを入力として使用する。

### 3.1 Input Data

- Thread Data
- Scene Data
- Event Data
- Timeline Data
- Character Data
- Character State
- WorldRule Data
- EmotionalCurve Data
- Foreshadowing / Payoff Data
- Story Structure Data

すべてのエンジンの出力スナップショットを入力として解析を行う。

### 3.2 Output Data

Analysis Engine は以下のデータを出力する。

1. AnalysisReport
   物語構造評価レポート

2. ConflictAlert
   矛盾・整合性エラー通知

3. OptimizationQuery
   改善提案・再生成要求

4. VisualizationData
   可視化用構造データ

---

## 4. Analysis Modules

Analysis Engine は以下のモジュールで構成される。

### 4.1 Consistency Checker（整合性検証）

以下の整合性を検証する。

- Timeline と Event の時系列整合性
- Character State の連続性
- WorldRule 違反の検出
- 因果関係の断絶
- 因果関係ループ
- 存在しない Character / Scene / Event 参照
- 伏線回収前の終了
- 回収対象の存在しない伏線

主な検証項目：

- Event Time Order Check
- Character State Continuity Check
- World Rule Validation
- Causal Chain Validation
- Reference Integrity Check

---

### 4.2 Structural Analyzer（構造・テンポ分析）

物語構造とテンポを分析する。

分析対象：

- Scene 長さ
- Event 密度
- Thread 分布
- Emotional Curve
- 三幕構成適合度
- ヒーローズジャーニー適合度
- 起承転結構造適合度

分析メトリクス：

- Pacing Density
- Scene Density
- Event Density
- Emotional Variance
- Structure Alignment Score

---

### 4.3 Thread Tracker（スレッド・伏線追跡）

Thread、伏線、テーマ、対立構造を追跡する。

検出項目：

- 未回収 Thread
- 長期間放置された Thread
- 回収のみ存在する Thread
- 伏線未回収
- Thread Coverage 不足
- Thread 偏重
- Thread 消失

Thread Coverage は以下の概念で測定する。

Thread Coverage = Thread が登場する Scene 数 / 全 Scene 数

---

## 5. Metrics & Reporting

Analysis Engine は以下の主要メトリクスを算出する。

### 5.1 Thread Coverage

各 Thread の登場頻度・分布を分析する。

目的：
未回収 Thread、存在感の薄い Thread を検出する。

### 5.2 Causal Integrity

因果関係の整合性を評価する。

検出対象：

- 原因のない結果
- 結果のない原因
- 因果ループ
- 時系列逆転因果

### 5.3 Pacing Density

Event 密度・Scene 密度からテンポを評価する。

検出対象：

- 中だるみ
- 情報過多
- クライマックス密度不足
- 導入過密

### 5.4 Engagement Score

物語の構造的面白さを数値化するための総合指標。

構成要素：

- Emotional Variance
- Conflict Density
- Thread Interaction
- Event Frequency
- Climax Intensity
- Structure Alignment

Engagement Score は物語品質評価の総合指標として使用される。

---

## 6. Feedback & Optimization Logic

Analysis Engine は解析結果に基づき、Story Engine に対して改善要求を送信する。

### 6.1 ConflictAlert

以下の場合に発行される。

- Timeline 矛盾
- Character State 矛盾
- WorldRule 違反
- 因果関係断絶
- 伏線未回収
- Thread 消失
- 不正参照

### 6.2 OptimizationQuery

以下の改善提案を生成する。

- Scene 追加提案
- Event 追加提案
- Thread 再配置
- Emotional Curve 修正
- Climax 強化提案
- 中盤 Event 追加提案
- Character Interaction 追加提案

### 6.3 Rollback Trigger

重大な矛盾が検出された場合、Analysis Engine は Story Engine に対して Rollback / Recalculate 要求を送信する。

Rollback 対象：

- Timeline 再計算
- Event 再配置
- Character State 再計算
- Thread 再構築
- Scene 再生成

Analysis Engine は Story OS の品質制御フィードバックループの中心となる。

---

## 7. Visualization Interface

Analysis Engine は可視化用の構造データを出力する。

Visualization Data 例：

- Thread × Scene マトリクス
- Event Density ヒートマップ
- Emotional Curve グラフ
- Character Interaction Network
- Causal Network Graph
- Timeline Event Distribution
- Structure Position Map（三幕構成マッピング）

これらは Interface Layer / Visualization Tool によって描画される。

---

## 8. Execution Lifecycle

Story OS の演算サイクルにおいて Analysis Engine は以下のタイミングで実行される。

1. Story Engine 実行
2. Event Engine 実行
3. Timeline Engine 実行
4. Character State 更新
5. Emotional Curve 更新
6. Analysis Engine 実行
7. ConflictAlert / OptimizationQuery 出力
8. 必要に応じて Story Engine 再実行
9. Simulation Engine 実行
10. Visualization 更新

Analysis Engine は各サイクル終了時に必ず実行される監査エンジンである。

---

## 9. Maintenance & Versioning

Analysis Engine は以下の仕様に強く依存する。

- Data_Spec v2.0.1
- Thread_Spec v2.0.1
- Scene_Spec v2.0.1
- Event_Spec v2.0.1
- Timeline_Spec v2.0.1
- Character_Spec v2.0.1
- EmotionalCurve_Spec v2.0.1
- System_Architecture v2.0.1

データ構造変更時は Analysis Engine の検証ロジックを必ず更新する必要がある。

Analysis Engine は NWF v2.0.1 において Story OS の論理整合性と構造品質を保証する最重要エンジンの一つである。

---

## 10. まとめ

Analysis Engine は以下の役割を持つ。

- 物語全体の整合性検証
- 因果関係の検証
- 時系列の検証
- Thread / 伏線追跡
- 構造分析
- テンポ分析
- 面白さ指標の算出
- 矛盾検知
- 改善提案生成
- Story Engine への再計算要求
- 可視化データ生成

Analysis Engine は Story OS における
「物語の品質管理システム」
「構造監査システム」
「論理検証エンジン」
として機能する。

NWF v2.0.1 において Analysis Engine は
Story Engine、Simulation Engine と並ぶ
Story OS の中核 Intelligence Engine である。

---

[EOF]