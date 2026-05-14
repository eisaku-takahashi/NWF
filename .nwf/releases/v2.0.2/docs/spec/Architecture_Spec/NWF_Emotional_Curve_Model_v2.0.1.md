Source: docs/spec/Architecture_Spec/NWF_Emotional_Curve_Model_v2.0.1.md
Updated: 2026-03-24T09:02:00+09:00
PIC: Engineer / ChatGPT

# NWF Emotional Curve Model v2.0.1

---

## 1. Overview

Emotional Curve Model は、物語における感情の変化、緊張、解放、感情エネルギーの流れを管理するモデルである。

v2.0.1 では、本モデルを単なる「感情変化の記録モデル」ではなく、
物語の進行・キャラクターの行動・イベント発生確率に影響を与える

**Emotion Dynamics Engine（感情ダイナミクス・エンジン）**

として再定義する。

本モデルは Story OS において、物語を動かすエネルギーを扱う
**Dynamic Force Layer** の中核コンポーネントとなる。

---

## 2. Layer & Flow Integration

### 2.1 Layer Placement

Emotional Curve Model は以下のレイヤに属する。

Dynamic Force Layer

これは以下のレイヤとは役割が異なる。

- Narrative Logic Layer → 因果・整合性・論理
- Data Layer → キャラクター・設定・世界情報
- Dynamic Force Layer → 感情・緊張・欲望・動機・エネルギー

物語は論理だけでは動かず、
**感情・欲望・恐怖・希望などの力によって動く**。

Emotional Curve Model はその「物語を動かす力」を管理する。

---

### 2.2 Execution Flow Integration

Execution Flow v2.0.1 における本モデルの実行位置は以下とする。

1. Timeline Update
2. Event Result Update
3. Emotional State Update   ← Emotional Curve Model
4. Consistency Check
5. Next Action Selection
6. Scene Generation

つまり、
**イベントの結果が感情を変化させ、その感情が次の行動に影響する**
という流れを形成する。

---

## 3. Emotion Graph Architecture

Emotional Curve Model は Emotion Graph として表現される。

### 3.1 Emotional State Node

emotional_state_node は以下を表す。

- キャラクターの感情状態
- シーンの感情状態
- ストーリー全体の感情状態

主なプロパティ

- emotion_type
- intensity
- polarity
- inertia
- timestamp
- related_event_id
- related_character_id

---

### 3.2 Cause Emotion Edge

cause_emotion_edge は以下を表す。

Event → Emotion

例

- 裏切り → 怒り
- 勝利 → 喜び
- 死 → 悲しみ
- 謎 → 不安
- 危険 → 恐怖

イベントが感情に与える影響の強さを edge weight として管理する。

---

### 3.3 Emotion Affects Action Edge

emotion_affects_action_edge は以下を表す。

Emotion → Action Selection

例

- 怒り → 攻撃
- 恐怖 → 逃走
- 愛 → 保護
- 希望 → 挑戦
- 絶望 → 放棄

これにより、
**感情が次の行動選択にバイアスを与えるモデル**
を構築する。

---

## 4. Emotional State Machine

各キャラクターは Emotional State Machine を持つ。

### 4.1 Emotional States

基本感情例

- Joy
- Anger
- Sadness
- Fear
- Surprise
- Trust
- Disgust
- Anticipation

これらは離散状態として扱うことも、
連続値ベクトルとして扱うこともできる。

---

### 4.2 State Transition

感情遷移は以下によって発生する。

- Event
- Character Interaction
- Memory Recall
- Goal Progress
- Failure
- Relationship Change

State Transition は以下の要素を持つ。

- transition_probability
- emotion_delta
- inertia_effect
- personality_modifier

---

## 5. Dynamics & Energy

本モデルの重要概念は
**Emotional Energy（感情エネルギー）**
である。

### 5.1 Tension

緊張状態を表す。

例

- 危険
- 対立
- 謎
- 期限
- 秘密
- 追跡
- 裏切り

Tension が高いほど読者の集中度は高まる。

---

### 5.2 Release

緊張の解放。

例

- 問題解決
- 勝利
- 告白
- 真相判明
- 和解
- 安全確保

Tension → Release のサイクルが
物語のリズムを作る。

---

### 5.3 Emotional Momentum

感情には慣性がある。

一度強い感情状態になると、
すぐには反対の感情にはならない。

これを Emotional Momentum と定義する。

---

### 5.4 Peak / Valley

感情曲線にはピークと谷が存在する。

- Peak → 最大緊張 / 最大感動
- Valley → 休息 / 静かな場面

物語は
**Peak と Valley の波**
によって構成される。

---

## 6. Multi-Level Curves

Emotional Curve は複数のレベルで存在する。

### 6.1 Character Emotional Curve

キャラクター個人の感情変化。

Character Arc と強く関連する。

---

### 6.2 Thread Emotional Curve

ストーリーの筋（Thread）ごとの感情曲線。

例

- 恋愛スレッド
- ミステリースレッド
- 成長スレッド
- 戦争スレッド

---

### 6.3 Scene Emotional Curve

各シーンの感情構造。

Scene 内でも
導入 → 上昇 → クライマックス → 余韻
という曲線が存在する。

---

### 6.4 Global Story Curve

作品全体の感情曲線。

例

- 起承転結
- 三幕構成
- ヒーローズジャーニー
- 黄金比構造

Global Curve は
作品全体の満足度や読後感に強く影響する。

---

## 7. Cross-Model Mapping

Emotional Curve Model は他のモデルと強く連携する。

### 7.1 Character Model

- Personality → 感情遷移確率
- Desire → 感情強度
- Trauma → 特定感情の増幅
- Relationship → 感情変化

---

### 7.2 Thread Model

- Thread Goal
- Conflict
- Progress
- Failure
- Resolution

Thread の進行が Emotional Curve を形成する。

---

### 7.3 Scene Model

Scene Event が Emotional State を更新する。

Scene は Emotional Curve の基本単位である。

---

### 7.4 Narrative Consistency Model

以下を検出する。

- 理由のない感情変化
- キャラクター性格と矛盾する感情
- 前のイベントと整合しない感情
- 感情の急激すぎる変化

これを
**Emotional Consistency**
と定義する。

---

### 7.5 AI Interface Model

AI は Emotional Curve を参照して以下を行う。

- 次のシーンの緊張度を調整
- 感情ピークの配置提案
- 読者感情の予測
- クライマックス位置の最適化
- キャラクター感情の一貫性チェック
- 感情的に強いイベントの提案

AI は
**読者の感情体験を最適化するための支援**
を行う。

---

## 8. AI & Co-Creation Workflow

AI と人間の共同創作において、
Emotional Curve Model は以下の役割を持つ。

AI ができること

- 感情曲線の可視化
- 感情ピーク不足の検出
- 中だるみの検出
- クライマックス弱さの検出
- キャラクター感情矛盾の検出
- 読者感情予測
- シーン感情強度の提案
- ストーリーリズムの改善提案

つまり本モデルは

**物語の感情設計支援エンジン**
として機能する。

---

## 9. Summary

Emotional Curve Model v2.0.1 は以下を管理する。

- Emotional State
- Emotion Graph
- Emotional State Machine
- Tension & Release
- Emotional Momentum
- Peak / Valley
- Character Curve
- Thread Curve
- Scene Curve
- Global Story Curve
- Emotional Consistency
- AI Emotional Optimization

本モデルは Story OS において

**物語にエネルギー・リズム・感情体験を与える心臓部**
である。

Narrative Logic Model が「頭脳」だとすれば、
Emotional Curve Model は「心臓」である。

---

[EOF]