Source: docs/spec/Core_Spec/NWF_Glossary_v2.0.0.md
Updated: 2026-03-17T08:25:00+09:00
PIC: Engineer / ChatGPT

# NWF Glossary v2.0.0

---

## 1. 概要

本ドキュメントは NWF（Novel Writing Framework）で使用される主要な用語を定義する。

NWF は物語を構造化データとして扱うフレームワークであり、従来の小説理論や物語論の用語が技術的な意味で使用される場合がある。

この用語集は NWF Core Spec における用語の共通理解を目的として作成されている。

---

## 2. 基本概念

### Story

物語全体を指す概念。

NWF では Story は以下の構造要素の集合として扱われる。

- World
- Character
- Thread
- Scene
- Beat

Story は物語構造と物語時間の両方を含む包括的な概念である。

---

### Story Database

物語を構成するすべてのデータを保存するデータ構造。

主に以下のデータを管理する。

- Character
- World
- Thread
- Scene
- Beat

これらのデータは JSON や Markdown などの構造化データとして保存される。

---

## 3. 構造要素

### Thread

Thread は物語のドラマラインを表す構造要素である。

代表的な Thread の例は次の通りである。

- Main Plot Thread
- Sub Plot Thread
- Mystery Thread
- Character Arc Thread
- Emotional Thread

Thread は物語の因果関係やテーマの進行を管理する。

---

### Thread Graph

Thread 同士の関係を表すグラフ構造。

Thread Graph は次のような関係を表現する。

- 依存関係
- 因果関係
- 並行進行

Thread Graph によって物語の論理構造を管理できる。

---

### Scene

Scene は物語の出来事単位であり、Thread の状態を変化させるイベントである。

Scene は通常次の要素を持つ。

- characters
- location
- conflict
- outcome

Scene は物語の時間的進行を構成する。

---

### Scene Timeline

Scene が時系列順に配置された構造。

Scene Timeline は物語の時間的流れを表す。

---

### Beat

Beat は Scene 内部の最小ドラマ単位である。

Beat は次のような要素を含む。

- 情報提示
- 感情変化
- 行動
- 対立

Beat は物語のテンポや感情曲線を形成する。

---

## 4. キャラクター関連

### Character

物語に登場する人物または主体。

Character は通常次の要素を持つ。

- 名前
- 目的
- 動機
- 性格
- 関係性

Character は Thread と Scene の両方に関与する。

---

### Character Arc

キャラクターの内面的変化の構造。

Character Arc は次のような要素を通じて表現される。

- 信念
- 成長
- 価値観の変化

Character Arc は物語のテーマ表現に重要な役割を持つ。

---

## 5. エンジン関連

### Thread Engine

Thread 構造を管理するエンジン。

主な機能は次の通りである。

- Thread 関係管理
- Thread 進行状態管理
- Thread 依存関係の検証

---

### Scene Engine

Scene Timeline を生成・管理するエンジン。

主な機能は次の通りである。

- Scene 順序管理
- Thread と Scene の同期
- Scene 構造検証

---

### Narrative Rendering

Scene や Beat などの構造データを自然言語の文章へ変換する処理。

出力例

- 小説
- 脚本
- ナレーション

Narrative Rendering は NWF における最終的な文章生成プロセスである。

---

## 6. NWF設計思想

### Story as Data

物語を構造化データとして扱う設計思想。

この思想により物語の分析、生成、再利用が可能になる。

---

### Narrative Simulation

キャラクター、Thread、Scene の相互作用によって物語が動的に進行する概念。

この概念は AI を利用した物語生成や分析の基盤となる。

---

### Story OS

物語制作を支援する統合的なシステムという考え方。

NWF は Story OS の実装を目指すフレームワークとして設計されている。

---

## 7. まとめ

本用語集は NWF Core Spec における主要概念を整理し、共通理解を提供するためのものである。

NWF は物語を構造化データとして扱うことで、物語設計、分析、生成を体系的に行うことを目的としている。

この用語集は NWF の設計、実装、運用における基礎的な参照資料として利用される。

---

[EOF]