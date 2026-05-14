Source: docs/spec/System_Architecture/NWF_Layered_Architecture_v2.0.1.md
Updated: 2026-04-05T05:32:00+09:00
PIC: Engineer / ChatGPT

# NWF Layered Architecture v2.0.1

---

## 1. 概要

本ドキュメントは、NWF (Narrative Workflow Framework) のシステム構造をレイヤモデルとして定義するものである。
NWF は物語生成システムであると同時に、仕様駆動型データ管理システムであり、OS に類似した多層構造を持つ。

レイヤ構造を明確に定義する目的は以下の通り。

- システムの責務分離
- 依存関係の明確化
- 将来的な拡張性の確保
- 実装順序の整理
- ドキュメント構造との対応付け

NWF は以下の 8 レイヤ構造で定義される。

---

## 2. NWF レイヤ一覧

NWF のレイヤ構造は下位レイヤから上位レイヤへと積み上がる構造を持つ。

1. Spec Layer
2. Schema Layer
3. Data Control Layer (Kernel)
4. Audit / Snapshot Layer
5. Validation Layer
6. Engine Layer
7. AI Workflow Layer
8. Interface / UI Layer

上位レイヤは下位レイヤに依存するが、下位レイヤは上位レイヤを認識してはならない。

これは OS における Kernel → Application の依存方向と同じ設計思想である。

---

## 3. 各レイヤの定義

### 3.1 Spec Layer

システムの最上位概念定義レイヤ。
Markdown で記述された仕様書群が存在する。

役割:
- システムルールの定義
- データ構造の概念定義
- 制約条件の定義
- ワークフロー定義
- 命名規則
- バージョン管理方針

重要概念:
Spec が Single Source of Truth である。
実装・スキーマ・データは Spec に従う。

---

### 3.2 Schema Layer

JSON Schema によるデータ構造のバリデーションレイヤ。

役割:
- Entity 構造定義
- Metadata 構造定義
- JSON データ検証
- 型チェック
- 必須項目チェック
- enum 制約
- format 制約

Spec Layer の内容を機械可読な形に落とし込むレイヤである。

---

### 3.3 Data Control Layer (Kernel)

NWF のカーネルレイヤ。
すべてのデータ操作はこのレイヤを通過しなければならない。

主なモジュール:
- id_generator
- entity_manager
- state_manager
- metadata_manager
- version_manager

役割:
- Entity 作成
- Entity 更新
- Entity 削除
- ID 発行
- Metadata 更新
- Version 管理
- State 管理

このレイヤは Immutable Data 原則に従う。

---

### 3.4 Audit / Snapshot Layer

データの履歴管理と状態復元を行うレイヤ。

主な機能:
- Audit Log (Append Only)
- Transaction Log
- Snapshot 保存
- Rollback
- Time Travel
- Branch 管理（将来）

重要概念:
Transaction + Audit Log = Causality

ログに存在しない変更は、NWF 世界では発生しなかったものとみなす。

---

### 3.5 Validation Layer

複数 Entity 間の論理整合性を検証するレイヤ。

Schema Layer は「構造」を検証するが、
Validation Layer は「論理」を検証する。

例:
- 存在しない Character を Scene が参照していないか
- Timeline が逆転していないか
- 状態遷移が許可されたものか
- World Rule に違反していないか

このレイヤは Phase 3 で実装される。

---

### 3.6 Engine Layer

物語生成・シミュレーションエンジンレイヤ。

主な機能:
- Story Engine
- Simulation Engine
- Event Generator
- Character Behavior Engine
- World Simulation
- Plot Generator

NWF の「物語を動かす」部分に相当する。

---

### 3.7 AI Workflow Layer

AI と人間の協調作業プロトコルレイヤ。

主な機能:
- Prompt Template
- Workflow 定義
- AI Task Pipeline
- Spec → Data → Story 変換フロー
- 自動生成パイプライン
- ドキュメント生成
- テストデータ生成

このレイヤは NWF を「AI 協働開発環境」として機能させる。

---

### 3.8 Interface / UI Layer

ユーザーが操作するインターフェースレイヤ。

将来機能:
- Entity Editor
- Timeline Editor
- Relationship Graph
- Story Visualizer
- World Map Viewer
- Diff Viewer
- Audit Log Viewer
- Scenario Editor
- GUI Authoring Tool

最上位レイヤであり、すべての下位レイヤを利用する。

---

## 4. レイヤ依存関係

依存関係は以下の方向のみ許可される。

Interface/UI
→ AI Workflow
→ Engine
→ Validation
→ Audit/Snapshot
→ Data Control (Kernel)
→ Schema
→ Spec

逆方向依存は禁止する。

特に Kernel は Engine や UI を絶対に参照してはならない。
Kernel は純粋なデータ操作のみを担当する。

---

## 5. 開発フェーズとレイヤ対応

NWF の開発フェーズはレイヤ構造と対応している。

Phase 1:
Spec Layer

Phase 2:
Schema Layer
Data Control Layer
Audit Layer

Phase 3:
Validation Layer

Phase 4:
Engine Layer

Phase 5:
AI Workflow Layer

Phase 6:
Snapshot / Temporal Management

Phase 7:
Interface / UI Layer

この順序で開発することで、依存関係を崩さずにシステムを拡張できる。

---

## 6. まとめ

NWF は以下の特徴を持つ多層システムである。

- Spec Driven Architecture
- Immutable Data Kernel
- Audit Based Causality
- Validation Logic Layer
- Narrative Engine
- AI Collaboration Workflow
- GUI Authoring Environment

この Layered Architecture は NWF のシステム設計における最上位構造定義であり、
今後のすべての実装・仕様・ドキュメントは本レイヤ構造に従うものとする。

---

[EOF]