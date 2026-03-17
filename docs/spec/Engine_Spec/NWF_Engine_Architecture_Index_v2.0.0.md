Source: docs/spec/Engine_Spec/NWF_Engine_Architecture_Index_v2.0.0.md
Updated: 2026-03-17T18:45:00+09:00
PIC: Engineer / ChatGPT

# NWF Engine Architecture Index v2.0.0

---

## 1. 概要

本ドキュメントは NWF（Novel Writing Framework）における Engine 層の全体構造を定義する。

Engine 層は Core Spec によって定義された構造化データを処理し、物語の進行・生成・分析を行う実行レイヤーである。

本 Index は以下を目的とする。

- Engine の全体構造の明確化
- Engine 間の依存関係の定義
- 処理レイヤーの整理
- 実装順序の標準化

---

## 2. Engine の役割

Engine は Story Database を入力とし、物語構造の変化と生成を担う。

主な役割

- 構造データの処理
- 状態遷移の管理
- 物語進行の制御
- 出力データの生成

Engine は「Story as Data」を「Story as Process」に変換する層である。

---

## 3. Engine レイヤー構造

NWF v2.0 では Engine を以下のレイヤーに分類する。

### 3.1 Execution Layer（実行制御）

- Engine Execution Model

役割

- Engine 全体の実行順序を定義
- データフローの制御

---

### 3.2 Structural Layer（構造制御）

- Thread Engine
- State Engine
- Scene Engine

役割

- 物語構造の骨格生成
- 状態遷移の管理
- Scene の生成

---

### 3.3 Detail Layer（詳細構造）

- Beat Engine
- Conflict Engine
- Character Engine

役割

- Scene 内構造の生成
- 対立・感情・関係性の制御

---

### 3.4 Temporal Layer（時間制御）

- Timeline Engine

役割

- 時系列整列
- 非線形構造の制御

---

### 3.5 Output Layer（出力）

- Narrative Engine

役割

- 構造データから自然言語への変換

---

### 3.6 Interface Layer（外部連携）

- Query Engine

役割

- Story Database の検索
- AI とのインターフェース

---

### 3.7 Extension Layer（拡張）

- Emotional Curve Engine
- Foreshadowing Engine

役割

- 感情曲線分析
- 伏線管理

※ 本レイヤーは任意実装とする

---

## 4. Engine 一覧

NWF v2.0 における標準 Engine は以下で構成される。

- NWF_Engine_Execution_Model_v2.0.0.md
- NWF_ThreadEngine_v2.0.0.md
- NWF_StateEngine_v2.0.0.md
- NWF_SceneEngine_v2.0.0.md
- NWF_BeatEngine_v2.0.0.md
- NWF_TimelineEngine_v2.0.0.md
- NWF_ConflictEngine_v2.0.0.md
- NWF_CharacterEngine_v2.0.0.md
- NWF_NarrativeEngine_v2.0.0.md
- NWF_QueryEngine_v2.0.0.md

拡張 Engine

- NWF_EmotionalCurveEngine_v2.0.0.md
- NWF_ForeshadowingEngine_v2.0.0.md

---

## 5. Engine 依存関係

Engine は以下の依存構造を持つ。

Thread Engine
↓
State Engine
↓
Scene Engine
↓
Beat Engine
↓
Timeline Engine
↓
Narrative Engine

補助関係

- Conflict Engine は Scene / Beat に依存
- Character Engine は Thread / Scene / State に依存
- Query Engine は全 Engine に横断的に接続

---

## 6. 処理フロー概要

NWF Engine の基本処理フローは以下である。

1. Thread 構造の確定
2. 状態遷移の計算
3. Scene の生成
4. Beat の生成
5. 時系列の整列
6. Narrative の生成

この処理は Engine Execution Model によって厳密に定義される。

---

## 7. 設計思想

NWF Engine Architecture v2.0 は以下の思想に基づく。

- 階層型処理構造
- 完全モジュール化
- 状態遷移駆動設計
- データ駆動型ナラティブ生成
- AI 連携前提設計

---

## 8. v1.0 からの変更点

主な変更点

- State Engine の新設
- Execution Model の分離
- Engine レイヤーの明確化
- Query Engine の追加
- 拡張 Engine の分離

---

## 9. まとめ

NWF Engine Architecture v2.0 は、Core Spec によって定義された物語構造を処理するための実行基盤である。

明確なレイヤー構造と依存関係により、複雑な物語生成プロセスを体系的かつ拡張可能な形で実現する。

---

[EOF]