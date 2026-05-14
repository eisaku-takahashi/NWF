Source: docs/spec/Engine_Spec/NWF_Engine_Architecture_v2.0.1.md
Updated: 2026-04-06T10:50:00+09:00
PIC: Engineer / ChatGPT

# NWF Engine Architecture v2.0.1

---

## 1. 概要

本ドキュメントは、NWF (Narrative World Framework) における Engine 層のアーキテクチャを定義する。

NWF における Engine とは、Kernel が保証する因果律および Audit Log を基盤として、
物語世界の構造・状態・時間・感情・イベント・ストーリー構造を演算・生成・解析・検証する
論理実行体（Logical Execution Units）である。

Engine 層は Story OS において、Kernel と AI Workflow / Application Layer の中間に位置する
ミドルウェア兼ランタイム層として機能する。

---

## 2. Story OS における Engine の位置付け

NWF の全体アーキテクチャは以下の層構造で構成される。

1. Storage Layer（ファイル・Audit Log）
2. Kernel Layer（Version / Audit / Concurrency / Transaction）
3. Engine Layer（論理演算・物語構造演算）
4. Execution Layer（Pipeline / Engine Order / Validation）
5. AI Workflow / Interface Layer（AI / Human Authoring）
6. Application Layer（Story Generation / Analysis / Editing）

この中で Engine Layer は以下の役割を持つ。

- データ構造を物語構造へ変換
- Event / Timeline / Story / Emotion の演算
- Simulation / Analysis / Rendering の実行
- AI が編集可能な範囲を論理的に制約
- Execution Pipeline 上で順序実行される計算ユニット

Engine は Story OS における「論理演算装置（Story Logic Processor）」として定義される。

---

## 3. Engine Layer の構造

Engine 層は責務に応じて複数のサブレイヤーに分割される。

### 3.1 Base Logic Engine Layer

基盤的なデータ処理・検索・解析を行う Engine。

主な Engine:
- Query Engine
- Analysis Engine

役割:
- Query Language の解釈
- Entity / Event / Scene / Thread の検索
- Audit Log の解析
- 統計・傾向分析
- 他 Engine へのデータ供給

---

### 3.2 Core Narrative Engine Layer

物語の時間・因果・構造を扱う中核 Engine。

主な Engine:
- Timeline Engine
- Event Engine
- Story Engine

役割:
- Timeline の順序制御
- Event の発生条件計算
- Thread Graph 管理
- Beat / Conflict / Story Structure 管理
- 因果関係の整合性維持

---

### 3.3 Contextual / Simulation Engine Layer

世界状態・感情・叙述など文脈的演算を行う Engine。

主な Engine:
- Simulation Engine
- Emotional Curve Engine
- Narrative Engine

役割:
- World Rule に基づく状態遷移
- Character 感情推移計算
- Narrative Rendering
- Story の起伏生成
- シミュレーション実行

---

## 4. Engine Execution Pipeline

Engine は Execution Pipeline 上で順序制御される。
基本的な Engine 実行パイプラインは以下の通り。

### 4.1 Step 1: Snapshot Fetch
- Version Manager から Snapshot を取得
- Transaction Context を生成

### 4.2 Step 2: Context Loading
- Engine Context を生成
- 対象 Timeline / Thread / Scene / Entity をロード
- 制約条件・World Rule をロード

### 4.3 Step 3: Cross Engine Computation
- Engine Order に従って Engine を順次実行
- Engine 間で Context を共有
- 中間状態（Engine State）を更新

### 4.4 Step 4: Validation
- Validation System により整合性チェック
- State Machine Validation
- Timeline Order Validation
- Narrative Consistency Validation

### 4.5 Step 5: Transaction Commit
- EntityManager 経由で変更を登録
- Audit Log Append
- Version Update
- Transaction Complete

---

## 5. Engine Dependency Graph

Engine 間には依存関係が存在し、実行順序が定義される。

一般的な依存レベルは以下の通り。

Level 0:
- Query Engine

Level 1:
- Timeline Engine
- Event Engine

Level 2:
- Story Engine
- Emotional Curve Engine

Level 3:
- Narrative Engine
- Analysis Engine

依存関係の基本原則:
- Timeline → Event → Story → Emotion → Narrative
- Analysis は全ての結果を参照可能
- Query Engine は全 Engine の基盤

---

## 6. Engine Data Flow

Engine のデータフローは以下の構造を持つ。

Input:
- Spec Files (Markdown)
- Audit Log (JSONL)
- Snapshot Data
- User Prompt / AI Prompt
- World Rules
- Timeline Data
- Entity Data

Processing:
- Engine Context
- Engine State
- Intermediate Results

Output:
- Entity Updates
- Event Creation
- Timeline Updates
- Emotional Curve Updates
- Narrative Output
- Validation Report
- Transaction Log

すべての書き込みは Audit Log を経由する。

---

## 7. Engine と Kernel の関係

Engine は直接ファイルやデータベースを更新しない。
すべての変更は Kernel API を通じて行う。

主な Kernel コンポーネント:
- AuditLogManager
- VersionManager
- ConcurrencyControl
- EntityManager
- EventManager
- MetadataManager

Engine → Kernel → Audit Log → Version Update → Snapshot Update

この流れにより因果律が物理的に保証される。

---

## 8. Engine Context / State / Snapshot

### 8.1 Engine Context
Engine 実行時のスコープ情報。

含まれる情報:
- timeline_id
- thread_id
- scene_id
- entity_ids
- world_rule_set
- execution_parameters
- transaction_id
- snapshot_version

Engine は Context を共有しながら協調動作する。

---

### 8.2 Engine State
Transaction 確定前の仮状態。

特徴:
- メモリ上のみ存在
- Commit 前は Audit Log に書き込まれない
- Validation 対象となる
- Ghost State とも呼ばれる

---

### 8.3 Snapshot
Engine 計算の基準となる不変データ。

- Transaction 開始時に取得
- Execution 中は変更されない
- MVCC により複数 Snapshot が共存可能

---

## 9. Engine Runtime Architecture

Engine Runtime は以下の特徴を持つ。

### 9.1 Stateless Engine
Engine 本体は状態を持たない。
状態はすべて Execution Context に保存される。

### 9.2 Parallel Execution
Engine は並列実行可能だが、
Commit は Concurrency Control により順序制御される。

### 9.3 Transaction Based Execution
Engine のすべての処理は Transaction 内で実行される。

### 9.4 Deterministic Execution
同一 Snapshot + 同一 Context → 同一結果
になることが保証される必要がある。

---

## 10. Engine Plugin Architecture

NWF は Engine の追加・拡張を可能とする。

### 10.1 Base Engine Interface

すべての Engine は共通インターフェースを実装する。

主なメソッド概念:
- initialize(context)
- execute(context)
- validate(context)
- commit(context)

### 10.2 Hook System
特定のイベント時に Engine をフック可能。

例:
- On Event Created
- On Scene Updated
- On Timeline Branch Created
- On Character State Changed

### 10.3 Plugin Engine
外部 Engine を追加可能。

例:
- Game Mechanics Engine
- Dialogue Engine
- AI Planning Engine
- Probability Engine

---

## 11. Engine と AI Workflow の関係

AI は直接世界状態を変更できない。
必ず Engine を経由する。

AI Workflow:
AI Prompt → Authoring Interface → Engine Execution → Validation → Commit

Engine は AI に対する「論理制約装置」として機能する。

AI は Engine の計算結果と Validation を無視して
世界を書き換えることはできない。

---

## 12. まとめ

NWF Engine Architecture の本質は以下である。

- Engine は Story OS の論理演算ユニット
- Engine は Kernel の Transaction 制御下で動作する
- Engine は Execution Pipeline 上で順序実行される
- Engine は Context を共有しながら協調動作する
- Engine は Stateless で Snapshot ベースで動作する
- Engine の出力は必ず Audit Log に記録される
- Engine は Plugin により拡張可能
- Engine は AI と Human の編集を論理的に制御する

Engine Layer は Story OS における
「思考・演算・物語展開」を司る中核層である。

---

[EOF]