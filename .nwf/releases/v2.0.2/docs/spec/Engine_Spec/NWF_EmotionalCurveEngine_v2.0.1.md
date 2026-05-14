Source: docs/spec/Engine_Spec/NWF_EmotionalCurveEngine_v2.0.1.md
Updated: 2026-03-27T09:27:00+09:00
PIC: Engineer / ChatGPT

# NWF Emotional Curve Engine v2.0.1

---

## 1. 概要

Emotional Curve Engine は、NWF v2.0.1 (Story OS) において読者体験の「熱量」「緊張」「感情強度」「テンポ」を数値化し制御する Dynamics / Presentation 制御エンジンである。

本エンジンは単なる感情値の記録ではなく、Story OS における Dramatic Tension Modulator（ドラマ演出制御装置）として機能する。Structure Layer および Simulation Layer によって生成された出来事、対立、情報開示、キャラクター関係の変化などを入力として、物語のテンション波形を生成し、Narrative Engine と Story Engine にフィードバックすることで、物語全体のテンポとドラマ性を自律的に制御することを目的とする。

Emotional Curve Engine は「何が起きたか」ではなく、「それがどれだけドラマチックか」を管理するエンジンである。

---

## 2. Core Architecture

### 2.1 Emotional Curve Engine の役割

Story OS における Emotional Curve Engine の役割は以下である。

- Scene / Beat / Event のドラマ強度計算
- 物語テンション波形の生成
- 感情強度の数値化
- クライマックス検出
- 中だるみ検出
- Scene 重要度推定
- Narrative Engine への演出パラメータ出力
- Story Engine へのテンション分析フィードバック

---

### 2.2 Multilayer Curve Model

Emotional Curve は単一のテンション値ではなく、複数の感情・緊張曲線の合成として計算される。

Emotional Curve は以下の 5 層構造で管理される。

1. Global Story Curve  
   物語全体のテンション推移

2. Character Emotional Curve  
   キャラクター個人の感情変化

3. Relationship Curve  
   キャラクター間の関係性緊張・親密度

4. Mystery / Information Curve  
   情報格差、謎、伏線、開示によるテンション

5. Danger / Conflict Curve  
   危険、対立、戦闘、問題、リスクによるテンション

Scene Tension はこれらの合成値として計算される。

---

### 2.3 Input Data

Emotional Curve Engine の入力データ。

- scene_data
- beat_data
- event_data
- character_state
- relationship_state
- conflict_state
- story_phase
- foreshadowing_flags
- reveal_flags
- information_gap
- danger_level
- conflict_level
- emotional_state
- relationship_tension

---

### 2.4 Output Data

Emotional Curve Engine の出力データ。

- scene_tension
- beat_tension
- story_tension
- emotion_intensity
- climax_flag
- peak_flag
- tension_trend
- scene_importance
- pacing_parameters
- narrative_style_parameters

---

## 3. Operational Algorithms

### 3.1 Tension Calculation Algorithm

Scene Tension は以下の要素を合成して計算される。

scene_tension =
conflict_level +
danger_level +
information_gap +
relationship_tension +
emotion_intensity

各要素の例。

- conflict_level：対立・問題・争い
- danger_level：生命・社会・心理的危険
- information_gap：読者とキャラクターの情報差
- relationship_tension：人間関係の緊張
- emotion_intensity：喜怒哀楽の強度

重み係数を設定することでジャンルごとの調整が可能。

例。

scene_tension =
w1 * conflict_level +
w2 * danger_level +
w3 * information_gap +
w4 * relationship_tension +
w5 * emotion_intensity

---

### 3.2 State Categories

Emotional Curve Engine で管理する主な状態変数。

- tension_value
- emotion_intensity
- conflict_level
- danger_level
- hope_level
- despair_level
- relationship_tension
- information_gap
- mystery_level
- foreshadowing_tension
- climax_flag
- resolution_flag
- scene_importance
- tension_trend
- emotional_peak_flag

これらは Story / Scene / Beat の 3 階層で管理される。

---

### 3.3 Event-Driven Dynamic Update

Emotional Curve は静的な曲線ではなく、イベント駆動型で更新される。

更新トリガー。

- Scene 開始
- Beat 実行
- Event 実行
- Character Decision
- Conflict 発生
- Relationship 変化
- Foreshadowing 提示
- Reveal 発生
- Scene 終了

各イベント後に Emotional State を再計算し、テンション波形を更新する。

---

### 3.4 Climax & Peak Detection

クライマックスおよび感情ピークは以下の条件で検出する。

Climax 判定条件。

- story_tension が閾値以上
- conflict_level が最大付近
- information_gap が解消方向
- emotional_intensity が高い
- story_phase が終盤

Peak Detection。

- tension_value が局所最大
- emotion_intensity が局所最大
- relationship_tension が急変
- reveal_event 発生

これにより以下のフラグを設定する。

- climax_flag
- emotional_peak_flag
- tension_peak_flag

---

## 4. Narrative / Story Integration

### 4.1 Narrative Engine への演出パラメータ出力

テンション値に応じて Narrative Engine へ演出パラメータを出力する。

低テンション時。

- sentence_length = long
- description_density = high
- inner_monologue_ratio = high
- dialogue_ratio = low
- pacing = slow

中テンション時。

- sentence_length = medium
- description_density = medium
- inner_monologue_ratio = medium
- dialogue_ratio = medium
- pacing = medium

高テンション時。

- sentence_length = short
- description_density = low
- inner_monologue_ratio = low
- dialogue_ratio = high
- pacing = fast

これにより文章テンポと演出がテンションと同期する。

---

### 4.2 Story Engine へのフィードバック

Story Engine へ提供する分析データ。

- story_tension_curve
- tension_trend
- climax_prediction
- scene_importance
- tension_sag_detection
- emotional_peak_points
- pacing_recommendation
- story_phase_estimation

Story Engine はこれらを用いて以下を調整する。

- クライマックス配置
- シーン順序
- 中だるみ防止
- テンションバランス
- 物語フェーズ管理

---

## 5. Execution Lifecycle

Emotional Curve Engine の実行ライフサイクル。

1. Initialize Emotional Curve Engine
2. Load Emotional Parameters
3. Scene Start
4. Initialize Scene Emotional State
5. Beat Execution
6. Event Trigger
7. Emotional State Update
8. Tension Calculation
9. Peak / Climax Detection
10. Output Narrative Parameters
11. Output Story Analysis Data
12. Scene End
13. Story Curve Update

Beat または Event 実行ごとに Emotional Update を行う。

---

## 6. Maintenance & Versioning

Emotional Curve Engine は以下の Data Spec に依存する。

- EmotionalCurveData v2.0.1
- SceneData v2.0.1
- BeatData v2.0.1
- EventData v2.0.1
- CharacterStateData v2.0.1
- RelationshipData v2.0.1
- ConflictData v2.0.1
- ForeshadowingData v2.0.1

データ仕様変更時には Emotional Curve Engine の更新が必要。

Version 更新ルール。

- テンション計算式変更 → Minor Version
- Emotional Model 変更 → Minor Version
- Engine Architecture 変更 → Major Version
- Data Spec 依存変更 → Minor Version

---

## 7. まとめ

Emotional Curve Engine は Story OS において、出来事、対立、関係性、情報格差、感情強度を数値化し、物語のテンション波形を生成するエンジンである。

Structure Engine が出来事を作り、
Simulation Engine が因果関係を決め、
Emotional Curve Engine がドラマ強度を計算し、
Narrative Engine がそれを物語表現へ変換する。

つまり Emotional Curve Engine は
「物語の面白さの波」
「読者体験のテンポ」
「クライマックス構造」
を制御する Story OS の演出中枢エンジンである。

---

[EOF]