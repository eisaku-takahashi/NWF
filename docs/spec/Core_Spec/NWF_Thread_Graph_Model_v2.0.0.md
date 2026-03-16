Source: docs/spec/Core_Spec/NWF_Thread_Graph_Model_v2.0.0.md
Updated: 2026-03-17T08:15:00+09:00
PIC: Engineer / ChatGPT

# NWF Thread Graph Model v2.0.0

---

## 1. 概要

NWF（Novel Writing Framework）では、物語のドラマ構造を Thread という単位で管理する。

Thread は物語の中で進行するドラマライン（物語の流れ）を表す。複数の Thread は互いに関係を持ち、物語全体としてネットワーク構造を形成する。

このネットワーク構造を Thread Graph と呼ぶ。

NWF Thread Graph Model は、Thread 同士の関係構造を定義し、物語全体の論理構造を管理するためのコアモデルである。

---

## 2. Thread Graph の基本概念

Thread Graph とは、Thread 同士の関係性をグラフ構造として表現したものである。

グラフ構造は以下の要素で構成される。

Node  
Thread を表す。

Edge  
Thread 同士の関係を表す。

このグラフ構造によって物語のドラマ構造を論理的に管理することができる。

---

## 3. Thread

Thread は物語のドラマラインを表す構造要素である。

代表的な Thread の例は次の通りである。

- Main Plot Thread
- Sub Plot Thread
- Mystery Thread
- Character Arc Thread
- Emotional Thread

Thread は複数の Scene によって進行する。

---

## 4. Thread Structure

Thread は通常以下の情報を持つ。

- thread_id
- title
- type
- related_characters
- current_state
- related_scenes

Thread の状態は Scene の進行によって変化する。

---

## 5. Thread Relationships

Thread 同士はさまざまな関係を持つ。

主な関係タイプは次の通りである。

### Dependency

ある Thread が別の Thread の進行に依存する関係。

例

Mystery Thread → Main Plot Thread

ミステリーの解決がメインストーリーの結末に影響する。

---

### Parallel

複数の Thread が同時に進行する関係。

例

Main Plot Thread  
Character Arc Thread

物語の本筋とキャラクターの成長が並行して進行する。

---

### Trigger

ある Thread の出来事が別の Thread を開始させる関係。

例

Incident Thread → Revenge Thread

事件が復讐の物語を開始させる。

---

### Merge

複数の Thread が一つの Thread に収束する関係。

例

Sub Plot Thread → Main Plot Thread

サブストーリーが最終的にメインストーリーへ統合される。

---

## 6. Thread Graph Representation

Thread Graph は以下のような関係構造で表現できる。

例

Thread A  
↓  
Thread B

または

Thread A → Thread B  
Thread A → Thread C

このように Thread は分岐や合流を伴うネットワーク構造を形成する。

---

## 7. Thread Graph と Scene

Thread は Scene によって進行する。

関係構造は次の通りである。

Thread  
↓  
Scene Timeline  
↓  
Scene

Scene は Thread の状態を変化させるイベントとして機能する。

---

## 8. Thread Graph の役割

Thread Graph は次の目的で使用される。

- 物語構造の可視化
- 因果関係の整理
- サブプロットの管理
- 伏線構造の分析
- 物語整合性の確認

Thread Graph によって物語全体の論理構造を体系的に把握することができる。

---

## 9. NWF Engine との関係

Thread Graph は主に Thread Engine によって管理される。

Thread Engine の主な役割は次の通りである。

- Thread 関係の管理
- Thread 進行状態の管理
- Thread 依存関係の検証

Scene Engine は Thread Graph を参照して Scene の順序や関係を処理する。

---

## 10. NWF設計における重要性

Thread Graph は NWF の中心構造であり、物語の論理構造を表す。

NWF では物語は次の構造として定義される。

Story = Thread Graph + Scene Timeline

Thread Graph は物語の構造を表し、Scene Timeline は物語の時間進行を表す。

この二つの構造によって、物語の論理構造と時間構造を分離して管理することができる。

---

## 11. まとめ

NWF Thread Graph Model は、物語のドラマラインである Thread をグラフ構造として管理するためのモデルである。

Thread 同士の関係を明確化することで、物語の因果構造やサブプロットの関係を体系的に整理できる。

このモデルは NWF における物語構造管理の中核として機能する。

---

[EOF]