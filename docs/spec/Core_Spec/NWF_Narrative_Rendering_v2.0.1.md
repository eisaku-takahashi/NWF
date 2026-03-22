Source: docs/spec/Core_Spec/NWF_Narrative_Rendering_v2.0.1.md
Updated: 2026-03-22T19:01:00+09:00
PIC: Engineer / ChatGPT

# NWF Narrative Rendering v2.0.1

---

## 1. 概要

Narrative Rendering は、NWF において構造化された物語データ（Thread / Scene / Beat / Timeline / Relationship / Conflict など）を、人間が読める文章へと変換する最終レンダリング層である。

本モデルは単なる文章生成ではなく、以下を統合的に制御する「ナラティブ演出エンジン」である。

- 視点（POV）
- 語り口（Voice）
- 文体（Style）
- 情報開示制御（Information Control）
- 時間表現（Tense / Narrative Time）
- 描写密度（Description Density）
- 会話比率（Dialogue Ratio）
- シーン遷移
- 伏線・回想の叙述順

Narrative Rendering は NWF アーキテクチャにおける Rendering Layer の Core Spec である。

---

## 2. Rendering Layer の位置

NWF 全体アーキテクチャにおける位置は以下の通り。

Data Layer  
Entity Layer  
Logic Layer  
Timeline Layer  
Graph / Analysis Layer  
Execution Flow Layer  
Rendering Layer ← 本仕様  
Output Layer  

Execution Flow においては Generation Phase の内部で動作する。

Logic-Validated Data  
↓  
Narrative Rendering  
↓  
Output Text / Novel / Script  

---

## 3. Rendering Pipeline v2.0.1

Narrative Rendering Pipeline は以下のステップで構成される。

### 3.1 Rendering Pipeline

1. Structure Retrieval  
2. Order Resolution  
3. POV Filtering  
4. Information Control  
5. Temporal Rendering  
6. Narrative Construction  
7. Style & Voice Application  
8. AI Prompt Template Generation  
9. Text Generation  
10. Output Formatting  

---

### 3.2 各ステップ詳細

#### 1. Structure Retrieval
Thread / Scene / Beat / Event / Character / Location / Timeline を取得する。

#### 2. Order Resolution
Timeline Model の NT（Narrative Time）に基づいて叙述順を決定する。

ST（Story Time）順ではなく、以下を考慮する。

- 回想
- 伏線
- 並列スレッド
- 情報遅延開示
- 視点変更

#### 3. POV Filtering
POV_Character_ID を基に、描写可能な情報を制限する。

POV キャラクターが：
- 見たもの
- 聞いたもの
- 推測したもの
- 知らない情報

を区別し、神の視点にならないように制御する。

#### 4. Information Control
Information Control Model に基づき、読者へ提示する情報量を制御する。

- Hidden Information
- Reader Known
- Character Known
- Dramatic Irony
- Foreshadow
- Mystery Delay

#### 5. Temporal Rendering
Timeline の NT / ST / ET を基に時制を決定する。

例：
- 現在進行
- 過去回想
- 未来予測
- 同時進行
- 時間ジャンプ

#### 6. Narrative Construction
Beat → Paragraph  
Scene → Section  
Thread → Chapter  

の階層で文章構造を構築する。

#### 7. Style & Voice Application
Narrative Voice Profile を適用し、文体・語り口・描写密度を決定する。

#### 8. AI Prompt Template Generation
NWF データをタグ形式に変換し、AI 文章生成用プロンプトを生成する。

#### 9. Text Generation
AI または Human により文章生成。

#### 10. Output Formatting
章構造・改行・会話形式・段落などを整形。

---

## 4. Perspective & POV Control

### 4.1 POV_Character_ID

各 Scene には POV_Character_ID を設定する。

POV により描写可能情報を制御する。

描写可能情報：

- 視覚情報
- 聴覚情報
- 感情
- 思考
- 推測
- 記憶

描写禁止情報：

- 他キャラクターの内心（POV が知らない場合）
- 未観測イベント
- 未来情報
- 隠された真実

### 4.2 POV フィルタリングルール

情報タイプごとに以下を判定する。

Observed  
Heard  
Inferred  
Remembered  
Unknown  

Unknown 情報は Narrative Rendering で除外または伏線化する。

---

## 5. Narrative Voice Profile

Narrative Voice Profile は文体・語り口・描写密度を制御するパラメータセットである。

### 5.1 Voice Parameters

voice_person  
voice_tense  
description_density  
dialogue_ratio  
sentence_length  
vocabulary_level  
emotion_expression_level  
metaphor_usage_level  
narrator_distance  
internal_monologue_ratio  

### 5.2 Voice Profile 例

Literary  
Light Novel  
Hardboiled  
Detective  
Sci-Fi Documentary  
Fairy Tale  
Horror Psychological  

Voice Profile により同じ Scene でも文章が変化する。

---

## 6. Temporal Rendering

Timeline Model v2.0.1 の NT（Narrative Time）を基に時制を制御する。

### 6.1 Time Types

Story Time (ST)  
Narrative Time (NT)  
Event Time (ET)  

### 6.2 Temporal Rendering Rules

NT が ST より過去 → 回想（Past Perfect）  
NT が ST と同時 → 現在進行  
NT が ST より未来 → 予告 / 伏線  

Temporal Rendering は以下を制御する。

- 時制
- 回想開始
- 回想終了
- 未来予告
- 同時進行描写
- 時間ジャンプ

---

## 7. Information Control Rendering

Information Control は Narrative Rendering において最重要要素の一つである。

制御対象：

- 読者が知っている情報
- キャラクターが知っている情報
- 読者が知らない情報
- キャラクターが知らない情報
- 伏線
- ミスリード
- サプライズ
- ドラマティックアイロニー

Rendering Engine は Information State を参照し、文章に含める情報を決定する。

---

## 8. AI Prompt Template Engine

Narrative Rendering v2.0.1 では AI 文章生成のためのタグベーステンプレートを使用する。

### 8.1 Template Tag 例

SCENE_ID  
POV_CHARACTER  
LOCATION  
TIME  
CHARACTERS_PRESENT  
EMOTION_STATE  
CONFLICT_STATE  
GOAL  
OBSTACLE  
OUTCOME  
INFORMATION_REVEAL  
FORESHADOW  
TONE  
STYLE  

### 8.2 AI Prompt Template 例

[SCENE]
Scene_ID:
POV:
Location:
Time:
Characters:
Goal:
Conflict:
Emotion:
Information_Reveal:
Foreshadow:
Tone:
Style:

[WRITE_SCENE_TEXT]

このテンプレートにより AI は構造データを理解した文章を生成できる。

---

## 9. Execution Flow v2.0.1 との統合

Execution Flow の Generation Phase において Narrative Rendering は以下の位置に存在する。

Execution Flow：

Initialization  
Ingestion  
Synthesis  
Validation  
Generation  
Feedback  

Generation Phase 内部：

Logic Validated Data  
↓  
Graph Generation  
↓  
Analysis  
↓  
AI Planning  
↓  
Narrative Rendering ← 本仕様  
↓  
Text Generation  
↓  
Output Generation  

つまり Narrative Rendering は  
「構造 → 文章」変換の中核エンジンである。

---

## 10. Rendering Architecture

Narrative Rendering Engine は以下のサブシステムで構成される。

Structure Loader  
Timeline Resolver  
POV Filter  
Information Controller  
Temporal Renderer  
Narrative Constructor  
Voice & Style Engine  
AI Prompt Template Engine  
Text Generator Interface  
Output Formatter  

これは NWF の中でも最も複雑なエンジンの一つである。

---

## 11. 総合評価

Narrative Rendering v2.0.1 は以下を統合する。

- Timeline Model
- POV Control
- Information Control
- Narrative Voice
- Style System
- AI Prompt Template
- Execution Flow Generation Phase
- Thread / Scene / Beat 構造
- Temporal Rendering
- Foreshadow / Flashback 制御

このエンジンは単なる文章生成ではなく、

「物語構造を文学作品へ変換するナラティブ演出エンジン」

である。

NWF v2.0 において Narrative Rendering は
Core Engine の一つとして位置付けられる。

---

## 12. まとめ

Narrative Rendering v2.0.1 の役割：

構造化物語データ  
↓  
Timeline / POV / Information Control 統合  
↓  
Narrative Rendering Pipeline  
↓  
Voice / Style / Tense / POV 制御  
↓  
AI Prompt Template  
↓  
Text Generation  
↓  
Novel / Script / Narrative Text  

これは NWF における最終出力エンジンであり、
物語を「読める形」に変換する中核仕様である。

---

[EOF]