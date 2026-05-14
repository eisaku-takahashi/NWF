Source: docs/spec/Kernel_Spec/NWF_Kernel_Core_Concept_v2.0.1.md
Updated: 2026-04-05T06:32:00+09:00
PIC: Engineer / ChatGPT

# NWF Kernel Core Concept v2.0.1

---

## 1. 概要

本ドキュメントは、NWF (Narrative World Framework) における Kernel の中核概念を定義するものである。  
NWF Kernel は、物語データの整合性、因果律、バージョン履歴、状態遷移を保証する **Narrative Operating System (NOS)** の中核実行基盤であり、すべてのデータ操作は Kernel を通じてのみ実行される。

Kernel は創作や推論を行う Engine 層とは明確に分離され、**データの正しさと履歴の不変性のみを責務とする最小特権システム**として設計される。

---

## 2. Kernel Definition (Kernel の定義)

NWF Kernel とは、以下の性質を持つシステムである。

- 物語データの整合性を強制する
- すべての変更を Transaction として記録する
- データの不変性 (Immutability) を保証する
- 状態遷移を State Machine により管理する
- Spec (Markdown 仕様) を実行時制約として読み込む
- Version / Snapshot / Audit Log を統合管理する

定義：

NWF Kernel = Data Control Engine + Spec Loader + Audit / Version / State Manager

Kernel は NWF Layered Architecture において **Data Control Layer の中核** に位置する。

---

## 3. Kernel Responsibilities (Kernel の責務)

Kernel は以下の責務のみを持つ。

### 3.1 Identity Management
- Entity ID
- Transaction ID
- Version ID
- Snapshot ID
- UUID v7 による時系列順序保証

### 3.2 Integrity Enforcement
- entity_schema 検証
- metadata_schema 検証
- spec_schema 検証
- データ構造の強制

### 3.3 Causality Recording
- すべての操作を Transaction として記録
- Audit Log へ Append Only で保存
- 誰が、いつ、何を変更したかを記録

### 3.4 State Governance
- DataStateMachine による状態遷移管理
- 不正な状態遷移の拒否
- 状態の不可逆性保証

### 3.5 Version Control
- Semantic Versioning
- Entity Version 履歴管理
- Snapshot 保存
- 過去状態の再現 (Replay)

### 3.6 Spec Loading
- Markdown Spec の読み込み
- Spec Registry 管理
- Spec を実行時制約として注入

---

## 4. Kernel Modules (Kernel モジュール構成)

Kernel は以下のモジュールで構成される。

### 4.1 EntityManager
- Entity 作成
- Entity 取得
- Entity 論理削除
- Entity Snapshot 取得

### 4.2 DataStateManager
- DataStateMachine 実行
- 状態遷移検証
- 状態変更ログ記録

### 4.3 MetadataManager
- Metadata 注入
- Actor 記録
- Spec 参照記録
- Timestamp 記録

### 4.4 VersionManager
- Version 更新
- Version 履歴管理
- Semantic Versioning 適用

### 4.5 AuditLogManager
- Transaction 開始
- Transaction 終了
- Audit Log 書き込み
- JSONL / Markdown Log 同期

### 4.6 IDGenerator
- UUID v7 発行
- Entity / Transaction / Version ID 発行

### 4.7 SpecRegistry
- Spec 読み込み
- Spec キャッシュ
- Spec 参照提供

---

## 5. Data Lifecycle (データライフサイクル)

Entity は Kernel により以下のライフサイクルを辿る。

### Phase 1 Creation
Transaction Start  
ID 発行  
Metadata 注入  
State = DRAFT  
Entity 作成  

### Phase 2 Evolution
Version 更新  
Metadata 更新  
Audit Log 記録  

### Phase 3 Transition
Validation  
State Machine  
REVIEW → APPROVED → LOCKED  

### Phase 4 Persistence
Snapshot 保存  
Audit Log Append  
Version Fix  

### Phase 5 End-of-Life
State → ARCHIVED  
論理削除  
参照のみ可能  

---

## 6. Immutable / Append Only Model

NWF の最重要設計思想は **Immutability** である。

### 6.1 Object Immutability
- 特定 Version の Entity は変更不可
- 変更は必ず新 Version を生成
- 過去 Version は永久保存

### 6.2 Append Only Log
- Audit Log は追記のみ
- ログ削除禁止
- ログ書き換え禁止

### 6.3 State Reconstruction
現在の Entity 状態は以下で定義される。

Current State = Initial State + Sum of Transactions

Entity の現在状態は Audit Log を Replay することで再構築可能である。

---

## 7. Transaction / Audit / Version / State Relationship

NWF Kernel における因果律の関係。

Transaction = 変更イベント  
Audit Log = Transaction の時系列記録  
Version = 特定時点の Entity Snapshot  
State = Entity の論理状態  

関係式：

Current State = f(Initial State + Σ Transactions)

つまり、**Audit Log がシステムの唯一の真実 (Single Source of Truth)** となる。

---

## 8. Kernel Boundary Definition (Kernel 境界)

### Kernel 内部
- ID Generator
- Metadata Manager
- Audit Log Manager
- Version Manager
- State Machine
- Schema Validator
- Spec Loader
- Entity Manager

### Kernel 外部
- Story Engine
- Simulation Engine
- Workflow Engine
- UI
- LLM Prompt System
- Export / Import Tools

### Boundary Rule
外部システムは Kernel API (Transaction API) を通じてのみデータ変更可能。  
直接 Entity を変更することは禁止。

---

## 9. Layered Architecture との関係

Layered Architecture における位置。

Spec Layer  
↓  
Kernel (Data Control Layer Core)  
↓  
Engine Layer  
↓  
Workflow Layer  
↓  
Application Layer  

Kernel は **Layered Architecture の重力中心** であり、  
すべてのデータは Kernel を中心に管理される。

---

## 10. Kernel Architecture Summary

NWF Kernel v2.0.1 の本質は以下である。

- Spec を実行時制約として読み込む
- すべての変更を Transaction として記録する
- Audit Log を唯一の真実とする
- Entity Version は不変
- 状態遷移は State Machine によってのみ変更可能
- すべてのデータ変更は Kernel API 経由のみ
- Append Only / Immutable を絶対原則とする

NWF Kernel は、物語データを OS のファイルシステムやプロセス管理のように扱う  
**Narrative Operating System の中核** である。

---

[EOF]