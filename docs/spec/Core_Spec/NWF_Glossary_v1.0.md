# NWF Glossary v1.0

## 概要

このドキュメントは NWF（Novel Writing Framework）で使用される主要な用語を定義する。

NWFは物語を構造化データとして扱うため、従来の小説用語とは少し異なる
技術的な意味で用語が使用される場合がある。

本用語集は NWF Core Spec における用語の共通理解を目的とする。

---

# 基本概念

## Story

物語全体を指す概念。

NWFでは Story は以下の要素の集合として扱われる。

- World
- Character
- Thread
- Scene
- Beat

---

## Story Database

物語を構成するすべてのデータを保存するデータ構造。

主なデータ

- Character
- World
- Thread
- Scene
- Beat

これらのデータはJSONなどの構造化データとして管理される。

---

# 構造要素

## Thread

Threadは物語のドラマラインを表す構造。

例

- Main Plot Thread
- Sub Plot Thread
- Mystery Thread
- Character Arc Thread
- Emotional Thread

Threadは物語の因果関係やテーマの進行を管理する。

---

## Thread Graph

Thread同士の関係を表すグラフ構造。

Thread Graphは

- 依存関係
- 因果関係
- 並行進行

などを表現する。

---

## Scene

Sceneは物語の出来事単位であり、Threadの状態を変化させるイベントである。

Sceneは以下の要素を持つ。

- Characters
- Location
- Conflict
- Outcome

Sceneは物語の時間的な進行を構成する。

---

## Scene Timeline

Sceneが時系列順に並んだ構造。

Scene Timelineは物語の時間的流れを表す。

---

## Beat

BeatはScene内部の最小ドラマ単位である。

Beatは以下のような要素を含む。

- 情報提示
- 感情変化
- 行動
- 対立

Beatは物語のテンポや感情曲線を調整する。

---

# キャラクター関連

## Character

物語に登場する人物または主体。

Characterは以下の要素を持つ。

- 名前
- 目的
- 動機
- 性格
- 関係性

CharacterはThreadとSceneの両方に関与する。

---

## Character Arc

キャラクターの内面的変化の構造。

Character Arcは

- 信念
- 成長
- 価値観の変化

などを通じて表現される。

---

# エンジン関連

## Thread Engine

Thread構造を管理するエンジン。

主な機能

- Thread関係管理
- Thread進行状態管理
- Thread依存関係処理

---

## Scene Engine

Sceneタイムラインを生成・管理するエンジン。

主な機能

- Scene順序管理
- ThreadとSceneの同期
- Scene構造検証

---

## Narrative Rendering

Sceneデータを自然言語の文章へ変換する処理。

出力例

- 小説
- 脚本
- ナレーション

---

# NWF設計思想

## Story as Data

物語を構造化データとして扱う思想。

---

## Narrative Simulation

キャラクターやThreadの相互作用によって
物語が動的に生成される概念。

---

## Story OS

物語制作を支援するための統合システムという考え方。

NWFはこの Story OS の実装を目指している。