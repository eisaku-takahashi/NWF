# NWF Thread Graph Model v1.0

## 概要

NWF（Novel Writing Framework）では、物語のドラマ構造を **Thread** という単位で管理する。

Threadは物語の中で進行するドラマライン（物語の流れ）を表す。
複数のThreadは互いに関係を持ち、物語全体としてネットワーク構造を形成する。

この構造を **Thread Graph** と呼ぶ。

本ドキュメントでは、NWFにおけるThread Graphの構造と役割を定義する。

---

# Thread Graph の基本概念

Thread Graphとは、Thread同士の関係性をグラフ構造として表現したものである。

グラフ構造の要素

- Node（ノード）  
  Thread

- Edge（エッジ）  
  Thread同士の関係

Thread Graphによって物語の構造を視覚的・論理的に管理することが可能になる。

---

# Thread

Threadは物語のドラマラインを表す。

例

- Main Plot Thread
- Sub Plot Thread
- Mystery Thread
- Character Arc Thread
- Emotional Thread

Threadは複数のSceneによって進行する。

---

# Thread Structure

Threadは通常以下の情報を持つ。

- Thread ID
- Title
- Type
- Related Characters
- Current State
- Related Scenes

ThreadはSceneの進行によって状態が変化する。

---

# Thread Relationships

Thread同士はさまざまな関係を持つ。

主な関係タイプ

## Dependency

あるThreadが別のThreadの進行に依存する関係。

例

Mystery Thread → Main Plot Thread

ミステリーの解決がメインストーリーの結末に影響する。

---

## Parallel

複数のThreadが同時に進行する関係。

例

Main Plot Thread  
Character Arc Thread

物語の本筋とキャラクターの成長が並行して進む。

---

## Trigger

あるThreadの出来事が別のThreadを開始させる関係。

例

Incident Thread → Revenge Thread

事件が復讐の物語を開始させる。

---

## Merge

複数のThreadが一つのThreadに収束する関係。

例

Sub Plot Thread → Main Plot Thread

サブストーリーが最終的にメインストーリーへ統合される。

---

# Thread Graph Representation

Thread Graphは以下のような構造で表現できる。

Thread A  
↓  
Thread B

または

Thread A → Thread B  
Thread A → Thread C

このように複数のThreadが分岐・合流することがある。

---

# Thread Graph と Scene

ThreadはSceneによって進行する。

関係

Thread  
↓  
Scene Timeline  
↓  
Scene

SceneはThreadの状態を変化させるイベントとして機能する。

---

# Thread Graph の役割

Thread Graphは次の目的で使用される。

- 物語構造の可視化
- 因果関係の整理
- サブプロット管理
- 伏線構造の分析
- 物語整合性の確認

---

# NWF Engineとの関係

Thread Graphは主に **Thread Engine** によって管理される。

Thread Engineの役割

- Thread関係の管理
- Thread進行状態の管理
- Thread依存関係の検証

Scene EngineはThread Graphを参照してSceneの順序を決定する。

---

# NWF設計における重要性

Thread GraphはNWFの中心構造であり、物語の論理構造を表す。

NWFでは

Story = Thread Graph + Scene Timeline

という構造で物語が管理される。

Thread Graphは物語の「構造」を表し、Scene Timelineは物語の「時間」を表す。