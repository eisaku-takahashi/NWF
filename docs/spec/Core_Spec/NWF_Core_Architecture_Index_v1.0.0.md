# NWF Core Architecture Index v1.0

## 概要

NWF（Novel Writing Framework）は、物語制作を構造化データとして管理するための Story OS 型フレームワークである。

小説・脚本・ゲームシナリオなどのナラティブを

- Thread（物語ライン）
- Scene（出来事単位）
- Beat（ドラマ最小単位）

という階層構造で管理し、物語の設計・分析・生成を可能にする。

---

# NWF Core Architecture

NWFの基本構造は以下のレイヤーで構成される。

Story Database  
↓  
Thread Engine  
↓  
Scene Engine  
↓  
Narrative Rendering  
↓  
Manuscript（最終原稿）

---

# Architecture Layers

## 1 Story Database

物語を構成するすべてのデータを保存するレイヤー。

主なデータ

- Character
- World
- Thread
- Scene
- Beat

これらはJSONなどの構造化データとして管理される。

---

## 2 Thread Engine

Threadは物語のドラマラインを表す。

例

- Main Plot Thread
- Mystery Thread
- Emotional Thread
- Character Arc Thread

Thread Engineは次の要素を管理する。

- Threadの関係性
- 進行状態
- 分岐

---

## 3 Scene Engine

SceneはThreadの状態を変化させるイベント単位である。

Sceneの役割

- 状況変化
- 情報提示
- キャラクターの意思決定
- コンフリクト発生

Scene EngineはThreadを基にSceneタイムラインを生成する。

---

## 4 Beat Layer

BeatはScene内部の最小ドラマ単位である。

例

- 情報提示
- 感情変化
- 行動
- 対立

Beatは物語テンポと感情曲線を制御する。

---

## 5 Narrative Rendering

Sceneデータを自然言語の文章へ変換するレイヤー。

出力例

- 小説原稿
- 脚本
- ナレーション

---

# NWF Core Principle

NWFは次の思想で設計されている。

Story = Data + Simulation

物語を

- データ構造
- エンジン処理

として扱うことで

- 構造分析
- AI支援執筆
- 自動整合性チェック

を可能にする。

---

# Document Position

このドキュメントは NWF Core Spec の入口ファイルであり、
以下の仕様書へのインデックスとして機能する。

- NWF_Data_Model
- NWF_Thread_Graph_Model
- NWF_Scene_Model
- NWF_Beat_Model
- NWF_Execution_Flow
- NWF_Narrative_Rendering