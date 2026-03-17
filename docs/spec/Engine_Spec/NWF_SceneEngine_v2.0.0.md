Source: docs/spec/Engine_Spec/NWF_SceneEngine_v2.0.0.md
Updated: 2026-03-17T20:20:00+09:00
PIC: Engineer / ChatGPT

# NWF SceneEngine v2.0.0

---

## 1. 概要

Scene Engine は NWF（Novel Writing Framework）において、物語を Scene（シーン）単位で管理するエンジンである。

Scene は物語における具体的な出来事を表す最小の実行単位であり、キャラクターの行動・対話・意思決定が発生する。

Scene Engine は Thread Engine による構造および State Engine による状態を基盤として、Scene の生成・配置・進行制御を行う。

---

## 2. Scene の定義

Scene は物語における「状態変化を伴う出来事の単位」である。

### 2.1 基本要素

Scene は以下の要素を持つ。

- 登場人物（Characters）
- 場所（Location）
- 時間（Time）
- 出来事（Event）

---

### 2.2 特徴

- State を変化させる
- Thread の進行を具体化する
- 時系列上の位置を持つ
- 他の Scene と関係を持つ

---

## 3. Scene Engine の役割

Scene Engine は以下の役割を持つ。

- Scene の生成
- Scene の順序制御
- Scene 間関係の管理
- Scene と Thread / State の整合性維持
- Scene 配置の最適化

Scene Engine は「物語の実行層」を担うエンジンである。

---

## 4. Scene 構造

### 4.1 内部構造

Scene は以下の構造を持つ。

- 開始（Setup）
- 展開（Development）
- 転換（Turning Point）
- 終了（Resolution）

---

### 4.2 構造特性

- 各 Scene は最小のドラマ単位である
- 必ず何らかの State 変化を伴う
- 次の Scene への因果的接続を持つ

---

## 5. Scene と Thread

- Scene は Thread の一部として存在する
- 1つの Thread は複数の Scene によって構成される
- 1つの Scene は複数の Thread に関与することがある

Scene Engine は Thread Engine から以下を受け取る。

- Thread の進行順序
- Thread 関係情報
- 構造制約

---

## 6. Scene と State

- Scene は State を変化させるイベントである
- Scene の実行により State が更新される
- Scene は State 遷移のトリガーとなる

Scene Engine は State Engine と連携して以下を行う。

- State 更新イベントの発行
- 状態変化の記録

---

## 7. Scene 間関係

Scene は以下の関係を持つ。

- 時系列関係（前後関係）
- 因果関係（Cause-Effect）
- 並行関係（Parallel）

---

## 8. 入出力仕様

### 8.1 入力

- Thread Graph
- State 定義および現在状態
- Scene 定義（テンプレートまたはルール）

---

### 8.2 出力

- Scene リスト
- Scene 実行順序
- State 更新イベント
- Scene 関係データ

---

## 9. 処理フロー

Scene Engine は以下の処理を行う。

1. Scene 定義の読み込み
2. Thread に基づく Scene 配置
3. Scene 間関係の構築
4. Scene 実行順序の決定
5. State 更新イベントの生成
6. 整合性チェック

---

## 10. 検証（Validation）

Scene Engine は以下の検証を行う。

- State 変化を伴わない Scene の検出
- 因果関係の欠如の検出
- 時系列矛盾の検出
- Thread 制約違反の検出

---

## 11. 他 Engine との関係

Scene Engine は以下の Engine と連携する。

- Thread Engine（構造の提供）
- State Engine（状態管理）
- Character Engine（登場人物情報）
- Dialogue Engine（対話生成）
- Conflict Engine（対立構造）
- Foreshadowing Engine（伏線管理）

---

## 12. AI 連携

AI は Scene Engine の情報を利用して以下を行う。

- Scene 展開の提案
- 演出・構成の最適化
- テンポ調整
- ドラマ性の強化

---

## 13. v1.0 からの変更点

主な変更点

- State Engine との統合強化
- Scene を「状態変化イベント」として再定義
- Thread との関係の明確化
- Scene 間関係の拡張

---

## 14. 設計思想

Scene Engine は以下の思想に基づく。

- 物語を「実行されるイベント」として捉える
- 状態変化を中心とした構造設計
- 因果関係の明確化
- モジュール化された演出管理

---

## 15. まとめ

Scene Engine v2.0 は、物語の出来事を Scene 単位で管理し、Thread 構造と State 変化を統合する実行エンジンである。

Scene を中心に据えることで、物語の具体性・因果性・可読性を高水準で維持することが可能となる。

---

[EOF]