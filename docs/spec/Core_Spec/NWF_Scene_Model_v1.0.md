# NWF Scene Model v1.0

## 概要

NWF（Novel Writing Framework）において **Scene** は物語の出来事単位である。

Sceneは物語の時間的進行を構成し、Threadの状態を変化させるイベントとして機能する。

Sceneはキャラクターの行動、コンフリクト、情報提示などを通じて
物語を前進させる役割を持つ。

本ドキュメントでは NWF における Scene の構造と役割を定義する。

---

# Scene の基本概念

Sceneは物語の中で発生する **一つの出来事のまとまり**である。

一般的なSceneの例

- キャラクター同士の会話
- 事件の発生
- 新しい情報の発見
- 対立や衝突
- 意思決定

Sceneは **Threadを進行させる単位**として機能する。

---

# Scene の役割

Sceneは次の役割を持つ。

- 物語を進める
- キャラクターを行動させる
- コンフリクトを発生させる
- 情報を提示する
- Threadの状態を変化させる

Sceneは物語の時間的な進行を構成する。

---

# Scene Structure

Sceneは通常以下の情報を持つ。

- Scene ID
- Title
- Location
- Characters
- Related Thread
- Conflict
- Outcome

これらの要素によってSceneの内容が定義される。

---

# Scene Timeline

Sceneは時系列順に並び **Scene Timeline** を形成する。

例

Scene 1  
↓  
Scene 2  
↓  
Scene 3

Scene Timelineは物語の時間的な流れを表す。

---

# Scene と Thread の関係

SceneはThreadの状態を変化させるイベントとして機能する。

関係

Thread  
↓  
Scene  
↓  
Thread State Change

例えば

Mystery Thread  
↓  
Scene：新しい手がかりの発見  
↓  
Mysteryの進行

このようにSceneはThreadを進行させる。

---

# Scene と Character

Sceneには通常複数のCharacterが登場する。

CharacterはSceneの中で

- 行動
- 対話
- 意思決定

を行う。

これによってSceneの結果が決定される。

---

# Scene と Beat

Sceneはさらに小さな単位である **Beat** に分解される。

構造

Scene  
↓  
Beat 1  
Beat 2  
Beat 3

BeatはScene内部のドラマ進行を表す。

---

# Scene のタイプ

Sceneは物語の役割によって分類することができる。

例

- Setup Scene（状況提示）
- Conflict Scene（対立）
- Discovery Scene（発見）
- Decision Scene（決断）
- Resolution Scene（解決）

Sceneタイプは物語構造の分析に利用できる。

---

# Scene Model の目的

NWF Scene Modelの目的は次の通りである。

- 物語の出来事を構造化する
- Threadとの関係を明確化する
- Scene Timelineを管理する
- AIによる物語分析を可能にする

Scene Modelは NWF Core Architecture における
物語時間構造の基盤となる。