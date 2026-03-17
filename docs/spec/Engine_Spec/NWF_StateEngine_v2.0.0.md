Source: docs/spec/Engine_Spec/NWF_StateEngine_v2.0.0.md
Updated: 2026-03-17T20:00:00+09:00
PIC: Engineer / ChatGPT

# NWF StateEngine v2.0.0

---

## 1. 概要

State Engine は NWF（Novel Writing Framework）において、物語内の状態（State）を管理するエンジンである。

State とは、キャラクター・関係性・世界・情報などの「物語の現在の状況」を表すデータであり、物語は State の変化によって進行する。

State Engine は Thread Engine によって定義された構造を基盤として、状態の生成・更新・整合性管理を行う。

---

## 2. State の定義

State は物語内の任意の対象の状態を表す。

対象の例

- キャラクター（感情・目的・認識）
- 関係性（信頼・対立・依存）
- 世界（環境・ルール・社会構造）
- 情報（秘密・事実・誤解）

State は以下の特徴を持つ。

- 時間とともに変化する
- Scene によって更新される
- Thread の進行に影響を与える

---

## 3. State Engine の役割

State Engine は以下の役割を持つ。

- State の定義と初期化
- State の更新管理
- State 間の依存関係管理
- 状態遷移の整合性検証
- 物語全体の状態の一貫性維持

State Engine は「物語の動的変化」を管理するエンジンである。

---

## 4. State モデル

### 4.1 State の構造

State は以下の要素を持つ。

- state_id
- 対象（entity）
- 属性（attributes）
- 現在値（value）
- 更新履歴（history）

---

### 4.2 State の種類

State は以下のカテゴリに分類される。

- Character State
- Relationship State
- World State
- Information State

---

## 5. State 遷移

State は Scene によって変化する。

### 5.1 遷移の定義

State 遷移は以下で定義される。

- 前状態（pre-state）
- イベント（Scene）
- 後状態（post-state）

---

### 5.2 遷移の特性

- 因果関係を持つ
- 可逆でない場合がある
- 複数の State に影響することがある

---

## 6. Thread との関係

- Thread は State 変化の流れとして定義される
- Thread Engine が構造を提供する
- State Engine はその構造上で状態を管理する

Thread は「構造」、State は「内容」である。

---

## 7. Scene との関係

- Scene は State を変化させる単位である
- 1つの Scene は複数の State を更新する
- Scene Engine は State 更新イベントを生成する

---

## 8. 入出力仕様

### 8.1 入力

- Thread Graph
- 初期 State 定義
- Scene 定義（またはイベント定義）

---

### 8.2 出力

- 更新された State
- State 遷移ログ
- 状態依存関係データ

---

## 9. 処理フロー

State Engine は以下の処理を行う。

1. 初期 State の生成
2. State 依存関係の構築
3. Scene に基づく State 更新
4. 状態遷移の記録
5. 整合性チェック

---

## 10. 検証（Validation）

State Engine は以下を検証する。

- 矛盾する状態の検出
- 未定義 State の参照検出
- 不正な遷移の検出
- 状態依存関係の破綻検出

---

## 11. 他 Engine との関係

State Engine は以下の Engine と連携する。

- Thread Engine（構造の提供）
- Scene Engine（状態変化イベント）
- Character Engine（キャラクター状態）
- Relationship Engine（関係性状態）
- World Engine（世界状態）
- Information Engine（情報状態）

---

## 12. AI 連携

AI は State Engine の情報を利用して以下を行う。

- キャラクターの心理分析
- 状態変化の因果分析
- 矛盾検出
- 物語のリアリティ向上提案

---

## 13. v1.0 からの変更点

主な変更点

- State の統一モデル化
- Thread との関係の明確化
- 状態遷移の明示的定義
- Engine 分離の強化

---

## 14. 設計思想

State Engine は以下の思想に基づく。

- 物語を「状態変化」として捉える
- 因果関係の明示化
- 動的システムとしての物語設計
- Engine 間の責務分離

---

## 15. まとめ

State Engine v2.0 は、物語の状態とその変化を管理するエンジンであり、NWF における動的挙動の中心である。

Thread 構造の上で State を管理することで、物語の一貫性と因果性を高精度に維持することが可能となる。

---

[EOF]