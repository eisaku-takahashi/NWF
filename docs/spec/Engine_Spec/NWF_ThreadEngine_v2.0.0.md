Source: docs/spec/Engine_Spec/NWF_ThreadEngine_v2.0.0.md
Updated: 2026-03-17T19:45:00+09:00
PIC: Engineer / ChatGPT

# NWF ThreadEngine v2.0.0

---

## 1. 概要

Thread Engine は NWF（Novel Writing Framework）において、物語のストーリーライン（Thread）を管理する中核エンジンである。

Thread は物語の因果関係およびテーマの進行を表す構造であり、Thread Engine はその生成・関係管理・進行制御を担う。

本エンジンは Engine Execution Model における最初の処理フェーズを担当し、以降のすべての Engine の基盤となる構造を提供する。

---

## 2. Thread の定義

Thread は物語の一つのドラマラインを表す構造である。

例

- 主人公の成長
- ミステリーの謎解き
- 人間関係の変化
- 感情の推移

Thread は以下の特徴を持つ。

- 複数の Scene によって具体化される
- 時系列に沿って進行する
- 他の Thread と関係を持つ

---

## 3. Thread Engine の役割

Thread Engine は以下の役割を持つ。

- Thread の生成
- Thread Graph の構築
- Thread 間の依存関係管理
- Thread 進行状態の初期化
- ストーリーラインの整合性検証

Thread Engine は「物語の骨格」を定義するエンジンである。

---

## 4. Thread Graph

Thread Graph は Thread 間の関係を表すグラフ構造である。

### 4.1 関係タイプ

Thread は以下の関係を持つ。

- 並行関係（parallel）
- 依存関係（dependency）
- 収束関係（convergence）

---

### 4.2 グラフ特性

Thread Graph は以下の特性を持つ。

- 有向グラフ
- 非循環構造（DAG を推奨）
- 部分的な独立性を許容

---

## 5. Thread と State

Thread は State と密接に関連する。

- Thread は状態遷移の単位である
- 各 Thread は独立した State を持つ
- State Engine により状態が更新される

Thread Engine は State Engine の入力構造を生成する。

---

## 6. Thread と Scene

Thread は複数の Scene によって表現される。

- Scene は Thread の状態変化を具体化するイベントである
- 1つの Scene は複数の Thread に関与することがある

Thread Engine は Scene Engine に対して以下を提供する。

- Thread の進行順序
- Scene の配置制約
- Thread 関係情報

---

## 7. 入出力仕様

### 7.1 入力

- Story Database
- Thread 定義データ

---

### 7.2 出力

- Thread Graph
- Thread 初期状態
- Thread 関係データ

---

## 8. 処理フロー

Thread Engine は以下の処理を行う。

1. Thread 定義の読み込み
2. Thread ノードの生成
3. Thread 関係の構築
4. Thread Graph の生成
5. 整合性チェック

---

## 9. 検証（Validation）

Thread Engine は以下の検証を行う。

- 孤立 Thread の検出
- 循環依存の検出
- 未定義参照の検出
- 不整合な関係の検出

---

## 10. 他 Engine との関係

Thread Engine は以下の Engine に依存関係を提供する。

- State Engine（状態遷移の基盤）
- Scene Engine（Scene 生成の制約）
- Character Engine（関係性の基盤）
- Conflict Engine（対立構造の基盤）

---

## 11. AI 連携

AI は Thread Engine の情報を利用して以下を行う。

- ストーリー構造の分析
- プロット提案
- 物語の分解・再構築
- ストーリーラインの最適化

---

## 12. v1.0 からの変更点

主な変更点

- State Engine との明確な分離
- Thread と State の関係定義の追加
- Execution Model への統合
- Graph 構造の厳密化

---

## 13. 設計思想

Thread Engine は以下の思想に基づく。

- ストーリーラインの明確な分離
- 因果関係の構造化
- 状態遷移駆動設計との統合
- モジュール化された物語設計

---

## 14. まとめ

Thread Engine v2.0 は、物語のストーリーラインを構造化し、全 Engine の基盤となる中核エンジンである。

Thread Graph を中心とした設計により、複雑な物語を一貫した構造として管理することが可能となる。

---

[EOF]