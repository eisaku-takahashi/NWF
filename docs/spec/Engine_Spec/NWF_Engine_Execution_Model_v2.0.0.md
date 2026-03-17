Source: docs/spec/Engine_Spec/NWF_Engine_Execution_Model_v2.0.0.md
Updated: 2026-03-17T19:20:00+09:00
PIC: Engineer / ChatGPT

# NWF Engine Execution Model v2.0.0

---

## 1. 概要

本ドキュメントは NWF（Novel Writing Framework）における Engine の実行モデルを定義する。

Engine Execution Model は、各 Engine の実行順序およびデータフローを規定し、物語生成プロセスの一貫性と再現性を保証する。

本仕様は Engine 層全体の基盤となる最重要仕様である。

---

## 2. 基本概念

### 2.1 Execution Model

Execution Model とは、複数の Engine をどの順序で実行し、どのようにデータを受け渡すかを定義するものである。

NWF においては、Execution Model が物語生成の「時間軸」を規定する。

---

### 2.2 Deterministic Execution

NWF の Engine 実行は決定論的である。

同一の入力（Story Database）に対しては、常に同一の出力が生成されることを保証する。

---

### 2.3 Data Flow

Engine 間のデータは以下の原則で流れる。

- 上位構造 → 下位構造
- 状態 → イベント → 構造
- 構造 → 表現

---

## 3. 実行フェーズ

Engine 実行は以下のフェーズに分割される。

### 3.1 Phase 1: Thread Resolution

- Thread の確定
- Thread Graph の解析
- 依存関係の解決

---

### 3.2 Phase 2: State Transition

- State の初期化
- 状態遷移の計算
- 状態履歴の生成

---

### 3.3 Phase 3: Scene Generation

- Scene の生成
- Scene 間の関係構築
- Thread と Scene の同期

---

### 3.4 Phase 4: Beat Generation

- Scene の分解
- Beat の生成
- ドラマ単位の構築

---

### 3.5 Phase 5: Timeline Alignment

- Scene / Beat の時系列整列
- 非線形構造の整理
- タイムラインの確定

---

### 3.6 Phase 6: Narrative Rendering

- 構造データの統合
- 自然言語への変換
- 出力生成

---

## 4. Engine 実行順序

NWF v2.0 の標準 Engine 実行順序は以下である。

1. Thread Engine
2. State Engine
3. Scene Engine
4. Beat Engine
5. Timeline Engine
6. Narrative Engine

補助 Engine

- Conflict Engine（Scene / Beat 生成時）
- Character Engine（State / Scene 更新時）
- Query Engine（全フェーズで参照可能）

---

## 5. データ依存関係

各 Engine は以下の入力と出力を持つ。

Thread Engine

- input: Story Database
- output: Thread Graph

State Engine

- input: Thread Graph
- output: State Timeline

Scene Engine

- input: State Timeline
- output: Scene List

Beat Engine

- input: Scene List
- output: Beat List

Timeline Engine

- input: Scene List, Beat List
- output: Timeline

Narrative Engine

- input: Timeline
- output: Narrative Text

---

## 6. 実行制御

### 6.1 Pipeline Execution

Engine はパイプラインとして実行される。

各 Engine は前段の出力を入力として受け取り、順次処理を行う。

---

### 6.2 Incremental Execution

一部の変更が発生した場合、影響範囲のみを再実行することが可能である。

例

- Character の変更 → State / Scene の再計算
- Thread の変更 → 全体再実行

---

### 6.3 Validation

各フェーズ終了時に検証を行う。

- データ整合性
- 依存関係の正当性
- 状態遷移の妥当性

---

## 7. 並列処理

NWF v2.0 は部分的な並列処理を許可する。

可能な並列処理

- 独立 Thread の処理
- Scene 内の Beat 生成
- Query の並列実行

ただし、最終的な出力は決定論的でなければならない。

---

## 8. エラーハンドリング

Engine 実行中のエラーは以下の分類で扱う。

- Validation Error（構造不整合）
- Dependency Error（依存関係不整合）
- State Error（状態遷移不正）

エラー発生時は処理を停止し、原因を報告する。

---

## 9. 設計思想

本 Execution Model は以下の思想に基づく。

- 決定論的処理
- 状態遷移駆動
- パイプライン処理
- 再実行可能性
- AI 連携前提設計

---

## 10. まとめ

NWF Engine Execution Model v2.0 は、物語生成の実行順序とデータフローを定義する中核仕様である。

本モデルにより、複雑な物語構造を一貫した手順で処理し、再現可能なナラティブ生成を実現する。

---

[EOF]