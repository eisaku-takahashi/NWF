Source: docs/spec/Engine_Spec/NWF_NarrativeEngine_v2.0.1.md
Updated: 2026-03-27T05:36:00+09:00
PIC: Engineer / ChatGPT

# NWF Narrative Engine v2.0.1

---

## 1. 概要

Narrative Engine は、NWF v2.0.1 (Story OS) における Execution & Presentation Layer を担当するエンジンであり、Structure Layer および Dynamics Layer によって計算・生成された出来事構造、キャラクター行動、感情曲線、伏線情報などを統合し、最終的な「物語の文章（Narrative Text）」として出力する役割を持つ。

本エンジンは単なる文章生成機構ではなく、Story OS における最終レンダリングユニットとして機能する。Simulation 層および Analysis 層で確定した「事実（What Happened）」を、視点、時制、テンポ、感情曲線、情報制御などの演出パラメータに基づき、「読者が体験する物語（How It Is Told）」へ変換することが目的である。

Narrative Engine は Story Engine の最終段に位置し、物語構造を読者体験へ変換する最終出力エンジンである。

---

## 2. Core Architecture

### 2.1 Engine Role in Story OS

Story OS における Narrative Engine の役割は以下である。

- Scene / Beat / Event の構造データを文章へ変換
- Dialogue Engine の会話文と Narrative Text の統合
- Emotional Curve に基づく文章テンポ・描写密度の制御
- Foreshadowing 情報の文章上での暗示・強調表現
- POV（視点）に基づく情報開示制御
- Narrative Block の生成と Story Engine への返却

Narrative Engine は以下の Engine と連携する。

- Story Engine
- Scene Engine
- Dialogue Engine
- Emotional Curve Engine
- Foreshadowing Engine
- Simulation Engine
- Analysis Engine

---

### 2.2 Input Data

Narrative Engine が受け取る主な入力データは以下である。

- scene_data
- beat_data
- event_data
- dialogue_data
- character_state
- emotional_curve
- foreshadowing_flags
- pov_settings
- tense_settings
- style_parameters

これらのデータを統合し、Narrative Block を生成する。

---

### 2.3 Output Data

Narrative Engine の出力は以下である。

- narrative_blocks
- scene_text
- transition_text
- narration_metadata

最終的に Story Engine が物語全体のテキストとして統合する。

---

## 3. Narrative Generation Algorithms

### 3.1 POV Control

POV Control は、物語の視点および語りの距離を制御するアルゴリズムである。

管理項目は以下。

- pov_type
    - first_person
    - third_person_limited
    - third_person_omniscient
- pov_character_id
- narrative_distance
- knowledge_scope
- information_visibility

POV Control の主な役割。

1. 視点キャラクターが知っている情報のみ描写
2. 他キャラクターの内面情報の表示制御
3. 語りの距離（心理描写の深さ）の制御
4. 視点変更時の遷移処理

---

### 3.2 Tense Management

Tense Management は物語全体の時制を管理する。

管理項目。

- base_tense
    - past
    - present
- flashback_tense
- memory_sequence_flag
- timeline_offset
- narration_time_reference

機能。

- 回想シーンの時制切替
- 現在進行描写の制御
- 時間ジャンプ時の文章遷移生成
- 時系列整合性の維持

---

### 3.3 Pacing Control

Pacing Control は文章テンポと描写密度を制御するアルゴリズムである。

主な入力。

- emotional_curve_value
- scene_importance
- action_intensity
- dialogue_ratio
- exposition_ratio

制御項目。

- description_density
- sentence_length
- paragraph_length
- narration_speed
- transition_speed

一般ルール。

- 緊張が高い → 文を短く → 描写密度低 → 行動中心
- 緊張が低い → 文を長く → 描写密度高 → 情景描写中心
- 重要シーン → 内面描写増加
- 移動シーン → 要約描写（Tell）

---

### 3.4 Description Density Algorithm

Description Density は以下の要素から計算される。

- environment_importance
- object_importance
- emotional_state
- scene_role
- pacing_level

出力。

- environment_description_level
- character_description_level
- object_description_level
- inner_monologue_level

これにより Show と Tell の比率が決定される。

---

## 4. Structural Integration

### 4.1 Narrative + Dialogue Integration

Narrative Engine は以下の要素を統合する。

- Narrative Text
- Dialogue
- Action Description
- Inner Monologue
- Scene Transition
- Foreshadowing Text

統合アルゴリズムの基本構造。

1. Beat を読み込む
2. Beat 内の Event を処理
3. Dialogue を挿入
4. Action 描写を生成
5. 必要に応じて Inner Monologue を挿入
6. Emotional Curve に基づき文章テンポ調整
7. Narrative Block を生成

---

### 4.2 Inner Monologue Insertion Logic

内面描写挿入の条件。

- emotional_intensity が閾値以上
- decision_event が発生
- conflict_event が発生
- pov_character が関与
- scene_importance が高い

挿入頻度は pacing_level により変化する。

---

### 4.3 Scene Transition Generation

Scene Transition は以下の状況で生成される。

- location_change
- time_skip
- pov_change
- emotional_phase_change
- chapter_boundary

Transition Text は以下の情報を含む。

- 時間変化
- 場所変化
- 状況変化
- 心理状態変化

---

## 5. Narrative Style Definition

### 5.1 Style Parameters

Narrative Style は以下のパラメータで定義される。

- sentence_length_average
- vocabulary_level
- metaphor_density
- dialogue_ratio
- inner_monologue_ratio
- description_ratio
- narration_distance
- tone
- writing_style
- genre_style

Genre Style の例。

- mystery
- sci_fi
- fantasy
- literary
- thriller
- horror
- romance

Style Parameters により文体が決定される。

---

### 5.2 Information Asymmetry Representation

Narrative Engine は情報の非対称性を文章構造に反映する。

管理される情報。

- character_known_information
- reader_known_information
- hidden_information
- foreshadowing_information
- reveal_timing

これにより以下を実現する。

- 叙述トリック
- ミスリード
- 伏線提示
- 伏線回収
- サスペンス演出

---

## 6. Narrative Output Pipeline

Narrative Engine の処理パイプライン。

1. Story Engine から Scene 実行要求を受信
2. Scene Data / Beat Data / Event Data を読み込み
3. Emotional Curve を取得
4. Foreshadowing 情報を取得
5. POV / Tense / Style Parameters を読み込み
6. Beat 単位で Narrative Block を生成
7. Dialogue / Action / Inner Monologue を統合
8. Scene Narrative Text を生成
9. Transition Text を生成
10. Narrative Blocks を Story Engine へ返却

出力構造。

- chapter_text
- scene_text
- narrative_blocks
- dialogue_blocks
- transition_blocks

---

## 7. Execution Lifecycle

Narrative Engine の実行ライフサイクル。

1. Initialize Narrative Engine
2. Load Style Parameters
3. Receive Scene Execution Request
4. Load Scene / Beat / Event Data
5. Apply POV Control
6. Apply Tense Management
7. Apply Pacing Control
8. Generate Narrative Blocks
9. Integrate Dialogue and Action
10. Generate Scene Text
11. Generate Transition Text
12. Return Narrative Output to Story Engine
13. End Scene Execution

---

## 8. Maintenance & Versioning

Narrative Engine は以下のデータ仕様に依存する。

- NarrativeData v2.0.1
- SceneData v2.0.1
- BeatData v2.0.1
- DialogueData v2.0.1
- EmotionalCurveData v2.0.1
- ForeshadowingData v2.0.1
- CharacterStateData v2.0.1

データ仕様が変更された場合、Narrative Engine のアルゴリズムおよび入出力仕様も更新する必要がある。

Version 更新ルール。

- 文体パラメータ変更 → Minor Version
- Narrative Algorithm 変更 → Minor Version
- Engine Architecture 変更 → Major Version
- Data Spec 依存変更 → Minor Version

---

## 9. まとめ

Narrative Engine は Story OS において、構造化された出来事、キャラクター行動、感情曲線、伏線、情報制御などを統合し、「出来事の記録」を「読者が体験する物語」へ変換する最終レンダリングエンジンである。

Structure Layer が「何が起きたか」を定義し、
Simulation Layer が「なぜ起きたか」を計算し、
Narrative Engine が「それをどう語るか」を決定する。

つまり Narrative Engine は Story OS における最終出力知能であり、物語体験そのものを生成するエンジンである。

---

[EOF]