Source: docs/spec/Architecture_Spec/NWF_Foreshadowing_Model_v2.0.1.md
Updated: 2026-03-24T09:32:00+09:00
PIC: Engineer / ChatGPT

# NWF Foreshadowing Model v2.0.1

---

## 1. Overview

Foreshadowing Model は、物語における伏線の設置（Setup）と回収（Payoff）を体系的に管理するモデルである。

v2.0.1 では、本モデルを単なる「伏線管理表」から発展させ、
物語の意味的因果と読者の期待・カタルシスを制御する

**Setup-Payoff Engine（セットアップ・回収エンジン）**

として再定義する。

本モデルは Story OS において以下のレイヤにまたがる。

- Narrative Logic Layer（因果・意味・回収）
- Dynamic Force Layer（期待・緊張・カタルシス）

Foreshadowing は、物語の論理的満足度と感情的満足度の両方を支配する重要なシステムである。

---

## 2. Layer & Flow Integration

### 2.1 Layer Placement

Foreshadowing Model の主な責務は以下である。

Narrative Logic Layer
- Setup と Payoff の因果関係管理
- 伏線の意味・象徴・テーマとの関係
- 未回収伏線チェック
- 矛盾回収の検出

Dynamic Force Layer
- Setup による期待・謎・緊張の生成
- Payoff によるカタルシス・驚き・納得の生成
- Emotional Curve への Tension / Release 信号送信

つまり Foreshadowing Model は

**Logic（因果）と Force（感情）を接続するモデル**

である。

---

### 2.2 Execution Flow Integration

Execution Flow v2.0.1 において、
Foreshadowing Model は以下のタイミングで更新される。

1. Event 実行
2. Foreshadowing State Update
3. Emotional State Update
4. Consistency Check
5. Next Action Selection
6. Scene Generation

Foreshadowing State Update では以下を行う。

- 新規 Setup 登録
- Reinforcement 登録
- Payoff 判定
- 未回収伏線チェック
- Chekhov's Gun 警告
- Emotional Curve への信号送信

---

## 3. Foreshadowing Graph Architecture

Foreshadowing Model は Foreshadowing Graph として表現される。

### 3.1 Foreshadowing Node

foreshadowing_node は伏線本体を表す。

主な属性

- foreshadowing_id
- foreshadowing_type
- importance_level
- payoff_impact
- related_thread_id
- related_character_id
- status
- reader_awareness_level

---

### 3.2 Setup Edge

setup_edge は伏線の設置を表す。

- Scene
- Beat
- Dialogue
- Object
- Event
- Description

Setup は読者に情報を与え、
期待・謎・緊張を生む。

---

### 3.3 Reinforcement Edge

reinforcement_edge は伏線の強調を表す。

伏線は通常、複数回提示されることで
読者の記憶に残る。

例

- 同じ小道具の再登場
- 同じ台詞の繰り返し
- 同じテーマの象徴
- 同じ謎の再提示

---

### 3.4 Payoff Edge

payoff_edge は伏線の回収を表す。

Payoff により以下が発生する。

- 謎の解決
- 伏線の意味の判明
- キャラクターの成長の証明
- テーマの表現
- 読者の驚き
- カタルシス

---

## 4. Foreshadowing Types & Impact

伏線は複数のタイプに分類される。

### 4.1 Foreshadowing Types

主なタイプ

- Object（小道具）
- Dialogue（台詞）
- Event（出来事）
- Symbol（象徴）
- Theme（テーマ）
- Mystery（謎）
- Red Herring（ミスリード）
- Chekhov's Gun（必ず回収される要素）

---

### 4.2 Importance Level

伏線の重要度を表す。

例

- Low
- Medium
- High
- Critical

重要度が高いほど、
Payoff Impact も大きくなる。

---

### 4.3 Payoff Impact

回収時の影響度。

例

- 情報提示
- キャラクター成長
- ストーリー転換
- 真相判明
- クライマックス
- テーマ表現

---

## 5. Dynamics & Timing

### 5.1 Setup-Payoff Distance

伏線設置から回収までの距離を管理する。

距離の種類

- Scene Distance
- Beat Distance
- Time Distance
- Thread Distance

距離が短すぎると驚きが弱く、
長すぎると読者が忘れる。

最適な距離を管理することで
伏線効果を最大化する。

---

### 5.2 Reader Awareness Level

読者が伏線をどれだけ意識しているかの推定値。

例

- Unnoticed
- Slightly Noticed
- Remembered
- Expected
- Forgotten

これにより以下を調整する。

- Reinforcement の必要性
- Payoff のタイミング
- Surprise の強さ
- Mystery の維持

---

### 5.3 Setup-Payoff Score

伏線構造の品質を評価するスコア。

評価要素

- Importance
- Distance
- Reinforcement Count
- Payoff Impact
- Emotional Impact
- Logical Consistency

---

## 6. Narrative Consistency Integration

Foreshadowing Model は Narrative Consistency Model と連携する。

検出対象

- 未回収伏線
- 回収のみ存在する伏線
- 伏線と回収の因果が弱い
- 回収が唐突
- 伏線の意味矛盾
- 同一伏線の複数回収矛盾
- Chekhov's Gun 未回収
- Red Herring 未処理

Foreshadowing は
物語整合性チェックの重要対象である。

---

## 7. Emotional Curve Integration

Foreshadowing は Emotional Curve と強く連携する。

関係は以下の通り。

Setup
- Mystery
- Expectation
- Anxiety
- Curiosity
- Tension 増加

Reinforcement
- Tension 維持
- Expectation 強化

Payoff
- Surprise
- Understanding
- Catharsis
- Release

つまり

Setup → Tension
Payoff → Release

という感情曲線を生成する。

Foreshadowing Model は Emotional Curve に
Tension / Release イベントを送信する。

---

## 8. AI & Co-Creation Workflow

AI は Foreshadowing Model を使用して以下を支援する。

- 伏線不足の検出
- 未回収伏線の検出
- 伏線回収タイミングの提案
- Setup-Payoff Distance の最適化
- Chekhov's Gun 提案
- Red Herring 提案
- Mystery Thread 設計支援
- クライマックス Payoff 強化提案
- Emotional Curve との連動最適化
- テーマ伏線の配置提案

Foreshadowing Model は
AI と人間の共同創作において
物語構造設計の重要な基盤となる。

---

## 9. Summary

Foreshadowing Model v2.0.1 は以下を管理する。

- Foreshadowing Node
- Setup / Reinforcement / Payoff
- Setup-Payoff Distance
- Importance Level
- Payoff Impact
- Reader Awareness
- Chekhov's Gun
- Red Herring
- Narrative Consistency Integration
- Emotional Curve Integration
- Setup-Payoff Score

本モデルは Story OS において

**物語の因果的満足と感情的カタルシスを設計するエンジン**

であり、

Character Model が「人物」、
Thread Model が「物語の筋」、
Emotional Curve Model が「感情の波」だとすれば、

Foreshadowing Model は

**物語の意味と回収を司る構造エンジン**

である。

---

[EOF]