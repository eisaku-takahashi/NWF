Source: docs/spec/Core_Spec/NWF_Scene_Model_v2.0.0.md
Updated: 2026-03-17T08:10:00+09:00
PIC: Engineer / ChatGPT

# NWF Scene Model v2.0.0

---

## 1. 概要

NWF（Novel Writing Framework）において Scene は物語の出来事単位を表すコア構造要素である。

Scene は物語の時間的進行を構成し、Thread の状態を変化させるイベントとして機能する。キャラクターの行動、対立、情報提示などを通じて物語を前進させる役割を持つ。

NWF Scene Model は、物語の出来事構造を明確に定義し、Thread、Character、Beat などの他の物語要素との関係を体系化することを目的とする。

---

## 2. Scene の基本概念

Scene は物語の中で発生する一つの出来事のまとまりを表す。

典型的な Scene の例は次の通りである。

- キャラクター同士の会話
- 事件の発生
- 新しい情報の発見
- 対立や衝突
- 意思決定

Scene は Thread を進行させる単位として機能し、物語の進展を担う。

---

## 3. Scene の役割

Scene は物語において次の役割を持つ。

- 物語の進行
- キャラクター行動の表現
- コンフリクトの発生
- 情報提示
- Thread 状態の変化

Scene の連続によって物語の時間構造が形成される。

---

## 4. Scene Structure

Scene は通常以下の情報を持つ。

- scene_id
- title
- location
- characters
- related_thread
- conflict
- outcome

これらの要素によって Scene の内容と物語上の役割が定義される。

---

## 5. Scene Timeline

Scene は時系列順に配置され、Scene Timeline を形成する。

例

Scene 1  
↓  
Scene 2  
↓  
Scene 3

Scene Timeline は物語の時間的な流れを表す構造であり、物語進行の基盤となる。

---

## 6. Scene と Thread の関係

Scene は Thread の状態を変化させるイベントとして機能する。

基本関係

Thread  
↓  
Scene  
↓  
Thread State Change

例

Mystery Thread  
↓  
Scene：新しい手がかりの発見  
↓  
Mystery の進行

このように Scene は Thread の進行を具体的な出来事として実現する。

---

## 7. Scene と Character

Scene には通常複数の Character が登場する。

Character は Scene 内で次の行動を行う。

- 行動
- 対話
- 意思決定
- 感情変化

これらの要素によって Scene の結果が決定される。

---

## 8. Scene と Beat

Scene はさらに小さなドラマ単位である Beat によって構成される。

構造

Scene  
↓  
Beat 1  
Beat 2  
Beat 3

Beat は Scene 内部のドラマ進行を表し、物語のテンポと感情変化を形成する。

---

## 9. Scene のタイプ

Scene は物語における役割によって分類することができる。

代表的な Scene タイプは次の通りである。

- Setup Scene（状況提示）
- Conflict Scene（対立）
- Discovery Scene（発見）
- Decision Scene（決断）
- Resolution Scene（解決）

Scene タイプは物語構造分析や AI によるストーリー理解に利用される。

---

## 10. Scene Model の目的

NWF Scene Model の目的は次の通りである。

- 物語の出来事を構造化する
- Thread との関係を明確化する
- Scene Timeline を管理する
- AI による物語分析を可能にする

Scene Model は NWF Core Architecture における物語時間構造の基盤となる。

---

## 11. まとめ

NWF Scene Model は物語の出来事構造を定義するコアモデルである。

Scene は Thread を進行させるイベント単位として機能し、Character の行動や Beat の連続によって具体的な物語展開を形成する。

このモデルにより、NWF は物語の時間進行と出来事構造を体系的に管理できる。

---

[EOF]