Source: docs/spec/Architecture_Spec/NWF_Narrative_Consistency_Model_v2.0.1.md
Updated: 2026-03-24T07:33:00+09:00
PIC: Engineer / ChatGPT

# NWF Narrative Consistency Model v2.0.1

---

## 1. 概要

NWF（Novel Writing Framework）における Narrative Consistency Model は、物語全体の整合性を検証・分析するための統合検証エンジンである。  
v2.0.1 では、従来の「整合性管理モデル」から発展し、Story OS におけるシミュレーションおよび物語生成の結果を検証する **Validation & Analysis Engine** として再定義された。

本モデルは Five-Layer Architecture において、Narrative Logic Layer および Dynamic Force Layer の出力を受け取り、Engine Layer にフィードバックを返す横断的監査モジュールとして機能する。

このモデルの目的は以下である。

- 物語の論理的破綻の検出
- キャラクター行動と設定の矛盾検出
- 世界設定違反の検出
- 因果関係の破綻検出
- 時間軸矛盾の検出
- 伏線未回収・不自然な解決の検出
- 感情変化の不整合の検出
- AI 執筆時のリアルタイム整合性チェック

Narrative Consistency Model は、Story OS における「論理的守護システム」として機能する。

---

## 2. Layer & Flow Integration

### 2.1 Five-Layer Architecture 上の位置

Narrative Consistency Model は以下のレイヤーを横断する。

- Narrative Logic Layer（Thread / Scene / Causality）
- Dynamic Force Layer（Emotion / Motivation / Conflict）
- World & Actor Layer（Character / World / Rule）
- Engine Layer（Validation / Analysis / Reporting）

本モデルはこれらのレイヤーから生成される状態・イベント・感情・時間情報を統合し、整合性検証を行う。

### 2.2 Execution Flow との統合

Story Execution Flow における位置は以下である。

World State Update
↓
Character Action
↓
Event Generation
↓
Thread Progress
↓
Scene Update
↓
Timeline Update
↓
Emotional State Update
↓
Structure Validation
↓
Narrative Consistency Validation ← 本モデル
↓
Warning / Error / Report Output

矛盾が検出された場合：

- Warning：軽微な矛盾
- Error：重大な論理破綻
- Suggestion：改善提案
- Simulation Halt：重大な破綻時にシミュレーション停止

---

## 3. Multi-Graph Consistency Matrix

Narrative Consistency Model は Multi-Graph Data Architecture の各グラフ間の整合性を検証する。

対応関係は以下の通り。

Character Graph → Character Consistency  
World / Constraint Graph → World / Constraint Consistency  
Causal / Event Graph → Causality Consistency  
Timeline Graph → Timeline Consistency  
Emotion Graph → Emotional Consistency  
Foreshadowing Graph → Foreshadowing Consistency  
State Graph → State Consistency  

これにより、単一モデルではなく **Cross-Graph Consistency Validation Engine** として機能する。

---

## 4. Consistency Types

### 4.1 Character Consistency

キャラクターの設定・性格・能力・過去と行動の整合性を検証する。

検証項目：
- 性格と行動の一致
- 能力と行動の整合性
- 背景設定との矛盾
- Emotional Curve との整合性
- Character Arc の連続性

### 4.2 World Consistency

世界設定および世界法則との整合性を検証する。

検証項目：
- 物理法則
- 魔法法則
- 社会制度
- 文化・宗教
- 地理・環境
- 技術レベル

### 4.3 Causality Consistency

因果関係の論理整合性を検証する。

検証項目：
- 原因のない結果の検出
- 結果のない原因の検出
- Thread 間因果関係
- Scene 間因果関係
- Character Action → Event → Result の論理

### 4.4 Timeline Consistency

時間軸の整合性を検証する。

検証項目：
- 出来事の順序
- キャラクター年齢
- 移動時間
- 歴史設定
- 同時刻イベントの整合性
- Story Time / Narrative Time の整合性

### 4.5 Foreshadowing Consistency

伏線と回収の整合性を検証する。

検証項目：
- 伏線設置
- 伏線回収
- 未回収伏線の検出
- 原因なし解決（Deus Ex Machina）の検出
- Thread / Character / Item 伏線管理

### 4.6 Emotional Consistency

感情変化の論理整合性を検証する。

検証項目：
- 感情変化の原因
- Emotional Curve の連続性
- 性格と感情反応の一致
- 感情強度変化の妥当性

### 4.7 State Consistency

キャラクターおよび世界状態の整合性を検証する。

検証項目：
- キャラクター位置
- 所属
- 健康状態
- 所持品
- 社会的地位
- 世界状態変化

### 4.8 Constraint Consistency

World Rule に対する違反を検証する。

検証項目：
- 物理法則違反
- 魔法制約違反
- 技術制約違反
- 社会制度違反
- 能力上限違反

---

## 5. Validation Logic & Rules

整合性検証は以下のロジックによって実行される。

### 5.1 Graph Traversal Validation

- Character Graph
- Event Graph
- Timeline Graph
- Emotion Graph
- Foreshadowing Graph

を横断探索し、矛盾を検出する。

### 5.2 Rule-Based Validation

World Rule、Character Trait、Story Rule に基づくルール検証。

例：
- 能力値 > 上限 → Error
- 移動時間 < 最短移動時間 → Error
- 感情変化量 > 許容変化量 → Warning

### 5.3 Causality Chain Validation

Event Chain を追跡し、

Cause → Action → Event → Result

のチェーンが成立しているかを検証する。

### 5.4 Foreshadowing Tracking Validation

伏線ノードと回収イベントの対応を検証する。

Foreshadow Node → Reference → Payoff Event

未接続ノードを未回収伏線として検出する。

---

## 6. Reporting System

検証結果は Consistency Report として出力される。

### 6.1 Report Types

- Info：情報
- Warning：軽微な矛盾
- Error：重大な矛盾
- Critical：物語破綻レベル
- Suggestion：改善提案

### 6.2 Report Structure

Report は以下の情報を含む。

- report_id
- consistency_type
- severity
- related_character_id
- related_thread_id
- related_scene_id
- description
- suggested_fix
- timestamp_story_time

### 6.3 Output Timing

- Scene 終了時
- Thread 進行時
- Timeline 更新時
- Emotional Update 時
- Simulation Step 終了時

---

## 7. AI & Co-Creation Workflow

AI 執筆・物語生成時、本モデルはリアルタイム整合性チェックを実行する。

AI Workflow：

1. AI が Scene / Event を生成
2. State / Timeline / Emotion 更新
3. Narrative Consistency Validation 実行
4. Consistency Score 計算
5. Warning / Error / Suggestion 出力
6. AI または人間が修正
7. Story Generation 継続

### 7.1 Consistency Score

物語の整合性を数値化する。

Consistency Score は以下の要素で構成される。

- Character Consistency Score
- World Consistency Score
- Causality Score
- Timeline Score
- Emotional Score
- Foreshadowing Score
- Constraint Score

総合 Consistency Score により、物語の論理的安定性を評価する。

---

## 8. まとめ

Narrative Consistency Model v2.0.1 は、NWF Story OS における統合整合性検証エンジンである。

本モデルは以下を実現する。

- Cross-Graph 整合性検証
- Story Execution Flow における Validation Engine
- Character / World / Timeline / Emotion / Foreshadowing の統合整合性管理
- AI 執筆時のリアルタイム整合性チェック
- Consistency Report / Warning / Error の自動生成
- 物語論理破綻の早期検出

このモデルにより NWF は単なる物語管理フレームワークではなく、  
**論理的に破綻しない物語を生成・検証できる Story Operating System** として機能する。

---

[EOF]