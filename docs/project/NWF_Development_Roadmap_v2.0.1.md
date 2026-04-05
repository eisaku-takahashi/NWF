Source: docs/project/NWF_Development_Roadmap_v2.0.1.md
Updated: 2026-04-06T03:08:00+09:00
PIC: Engineer / ChatGPT

# NWF Development Roadmap v2.0.1

---

## 1. 概要

NWF（Narrative Workflow Framework）は、
**物語を生成・管理・進化させるための Narrative Operating System（Story OS）**である。

本ドキュメントは、NWF を単なるツールではなく
**因果律を強制する OS として完成させるための開発ロードマップ**を定義する。

NWF の根本定義：

- Story = Data + Logic + Pipeline
- Current State = f(Initial State + Σ Transactions)

本ロードマップは、Spec-Driven Architecture と Kernel-Centric 設計に基づき、
**仕様・実装・運用を統合した開発戦略**を提示する。

---

## 2. Architecture Stack（8層構造）

NWF は以下の 8 層で構成される。

### 2.1 Layer Definition

| Layer        | 役割 |
|--------------|------|
| Philosophy   | 設計思想（因果律・不変性・正典性） |
| Spec         | 世界の定義（Schema / Data Model） |
| Kernel       | 因果律の強制（Audit / State / Transaction） |
| Engine       | 物語演算（Story / Timeline / Emotion） |
| Workflow     | 実行制御（AI Collaboration / HITL） |
| Production   | 出力生成（Scene / Draft / Narrative） |
| Governance   | 整合性管理（Spec / Audit / Version） |
| Optimization | 改善ループ（Analysis / Feedback） |

### 2.2 構造原則

- 下位層は上位層に依存されるが、逆は不可
- Kernel は全レイヤの整合性を強制する「重力中心」
- Spec はすべての実装の正典

---

## 3. Kernel / Core System 責務

Kernel は「物語の物理法則」を実装する。

### 3.1 Core Responsibilities

- Identity Management（UUID v7）
- Audit Log（全トランザクション記録）
- State Machine（状態遷移制御）
- Transaction（原子操作）
- Validation（Schema + 因果律）
- Version Control（Snapshot 管理）

### 3.2 Kernel Principle

- No Log, No Change
- Append-Only
- Immutability

---

## 4. Implementation Dependency Graph

### 4.1 実装順序

Foundation → Kernel → Core → Loader → Engine → Workflow → Governance

### 4.2 Dependency Detail

1. Entity Schema / Metadata Schema
2. ID Generator（UUID v7）
3. AuditLogManager
4. DataStateManager
5. EntityManager / VersionManager
6. SpecParser / SpecRegistry
7. QueryEngine
8. Story / Timeline Engine
9. Workflow（AI Collaboration）
10. Governance（Audit / Spec Control）

---

## 5. Development Phases

### Phase 1: Spec Foundation（完了）

内容：
- Core Spec / Data Spec 定義

DoD：
- 全 Schema 定義完了
- JSON Validation 成功

---

### Phase 2.1: Core Data Control（完了）

内容：
- Kernel 基本実装
- Audit Log / State 管理

DoD：
- Entity 作成 → Audit Log 記録成功
- State 遷移が正常動作

---

### Phase 2.2: Integrity & Validation（次）

内容：
- Validation System 強化
- 状態遷移の厳密化

DoD：
- 不正データの完全拒否
- Schema + 因果律の統合検証

---

### Phase 3: Engine Integration

内容：
- Story Engine / Timeline Engine 実装

DoD：
- Entity → Plot 構造生成可能

---

### Phase 4: AI Workflow & HITL

内容：
- AI Collaboration Model 実装
- Antigravity 連携

DoD：
- AI + Human による共同制作
- Audit Log ベースの操作統合

---

### Phase 5: Production Pipeline

内容：
- Scene → Draft → Release Pipeline

DoD：
- 物語生成フロー完全稼働

---

### Phase 6: Governance System

内容：
- Audit / Version / Spec Governance

DoD：
- 全変更が追跡可能
- Spec と実装の整合性維持

---

### Phase 7: Optimization Loop

内容：
- Analysis / Feedback / Spec Update

DoD：
- Recursive Improvement Loop 稼働

---

## 6. MVP Definition

### 6.1 Kernel MVP

- UUID v7 ID
- Audit Log（JSONL）
- 基本 State 管理

### 6.2 Engine MVP

- Query Engine
- Timeline ソート

### 6.3 Workflow MVP

- GitHub Sync
- AI ブリーフィング

---

## 7. Development Lifecycle

### 7.1 OS Development Loop

Spec → Kernel → Engine → Workflow → Production → Governance → Optimization → Spec

### 7.2 Story Production Loop

Idea → World → Character → Thread → Scene → Draft → Review → Release → Feedback → Improve

---

## 8. Directory / Module 対応

### 8.1 Directory Structure

NWF/
 ├── docs/
 ├── src/
 ├── data/
 ├── logs/

### 8.2 Module Mapping

| Module | 役割 |
|--------|------|
| core   | Kernel 実装 |
| models | Entity 定義 |
| loader | Spec 読み込み |
| engine | 物語演算 |
| workflow | 制御 |
| governance | 監査 |

---

## 9. Logging / Audit / Governance

### 9.1 Log Types

- Audit Log（不可変）
- Engine Log
- Validation Log
- Error Log

### 9.2 Policy

- Audit Log は削除不可
- すべての変更は Transaction 経由

---

## 10. Critical Path

最優先課題：

- UUID v7 への統一
- subject_id 命名統一
- Validation System 完成
- Audit Log 完全強制

---

## 11. Next Action

Phase 2.2 移行条件：

- Kernel 動作安定
- Schema 完全適用
- Audit Log 整合性確認

次ステップ：

- Validation System 実装
- Concurrency Control Spec 作成
- Temporal Management Spec 作成

---

## 12. まとめ

NWF は以下の原則に基づく：

- Spec First
- Kernel-Centric
- Causality Driven
- Immutability
- Human-in-the-loop
- Recursive Optimization

NWF はツールではなく、

**「物語の因果律を管理する OS」**

である。

---

[EOF]