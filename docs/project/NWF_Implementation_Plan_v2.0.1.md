Source: docs/project/NWF_Implementation_Plan_v2.0.1.md
Updated: 2026-03-31T07:10:00+09:00
PIC: Engineer / ChatGPT

# NWF Implementation Plan v2.0.1

---

## 1. Purpose

本ドキュメントは、NWF (Narrative Workflow Framework) に基づく Story OS の実装計画を定義するものである。  
目的は、小説制作ワークフローではなく、**物語生成 OS をソフトウェアシステムとして設計・実装・運用するためのエンジニアリング計画を確立すること**である。

本システムは以下の原則に従う。

- すべてのロジックは Spec に従う
- Spec → Code → Execution → Audit → GitHub の一方向トレーサビリティ
- Data State Machine によるデータライフサイクル管理
- HITL (Human In The Loop) による最終意思決定
- GitHub を唯一の正式履歴とする

特に重要な設計原則は以下である。

**spec_loader.py を起点として、すべての処理・検証・実行ロジックが Spec に従って動作すること。**

---

## 2. System Architecture Summary

Story OS は 3 層アーキテクチャで構成する。

### 2.1 Kernel Layer
システムの中核ロジックを提供する。

主な機能:
- Spec 読み込み
- Config 読み込み
- データ検証
- 状態遷移管理
- 整合性検査

主なモジュール:
- spec_loader.py
- config_loader.py
- validation_engine.py
- data_state_machine.py
- recursive_integrity_checker.py

### 2.2 Middleware Layer
AI・Workflow・Execution を制御する層。

主な機能:
- AI とのインターフェース
- Prompt 構築
- HITL 承認ゲート
- 実行パイプライン制御

主なモジュール:
- ai_interface.py
- prompt_builder.py
- hitl_gate.py
- pipeline_manager.py
- execution_controller.py

### 2.3 Application Layer
外部システム・GitHub・ログ・運用機能。

主な機能:
- GitHub 同期
- Audit ログ
- リリース管理
- レポート生成

主なモジュール:
- github_sync.py
- release_manager.py
- audit_logger.py

---

## 3. Module & Directory Map

src ディレクトリ構成は以下とする。

### 3.1 Directory Structure

src/
engine/
execution/
workflow/
utils/

### 3.2 Module Mapping

#### src/engine/
- validation_engine.py  
  JSON Schema / Logic Validation
- data_state_machine.py  
  Draft → Approved → Committed の状態管理
- recursive_integrity_checker.py  
  Spec / Data / Dependency の整合性検査

#### src/execution/
- pipeline_manager.py  
  実行フロー全体のオーケストレーション
- execution_controller.py  
  個別タスク実行制御

#### src/workflow/
- hitl_gate.py  
  Human Approval Gate
- ai_interface.py  
  LLM API Interface
- prompt_builder.py  
  Spec + Context → Prompt 生成

#### src/utils/
- spec_loader.py  
  Spec 読み込み（最重要）
- config_loader.py  
  設定ファイル読み込み
- audit_logger.py  
  操作・承認・実行ログ保存
- github_sync.py  
  GitHub Push / Tag / Release

---

## 4. Data & Schema Specification

### 4.1 Data Storage Structure

data/
world/
character/
episode/
schema/
logs/

### 4.2 JSON Schema

schema ディレクトリに以下を配置する。

- world.schema.json
- character.schema.json
- episode.schema.json
- timeline.schema.json

validation_engine はこれらの Schema を使用して JSON を検証する。

### 4.3 ID System

すべてのオブジェクトは UUID ベース ID を使用する。

例:
- WID: World ID
- CID: Character ID
- EID: Episode ID
- TID: Timeline ID

形式例:
CID-550e8400-e29b-41d4-a716-446655440000

### 4.4 Data State

各 JSON データは Status フィールドを持つ。

Status:
- Draft
- Validated
- Under_Review
- Approved
- Committed

data_state_machine.py が状態遷移を管理する。

---

## 5. Workflow Pipeline

Story OS の標準実行フローは以下とする。

1. Load Spec & Config
2. Context Fetch
3. AI Generation (Draft)
4. Validation (Schema & Logic)
5. HITL Gate (Human Review)
6. State Transition (Approved)
7. Commit & Tag (GitHub)
8. Audit Logging

このパイプラインは pipeline_manager.py によって制御される。

### 5.1 Pipeline Responsibilities

- spec_loader → Spec 読み込み
- prompt_builder → Prompt 作成
- ai_interface → AI 生成
- validation_engine → 検証
- hitl_gate → 人間承認
- data_state_machine → 状態更新
- github_sync → GitHub 反映
- audit_logger → ログ保存

---

## 6. HITL & Integrity Protocols

### 6.1 HITL (Human In The Loop)

AI は Draft を生成するが、最終決定は人間が行う。

hitl_gate.py の役割:
- Draft 表示
- 差分表示
- 承認 / 修正 / 却下
- 承認理由入力
- 承認ログ保存

### 6.2 Recursive Integrity Checker

recursive_integrity_checker.py は以下を検査する。

- Spec 間の整合性
- JSON データ参照関係
- ID 重複
- タイムライン矛盾
- 状態遷移不整合
- GitHub コミット状態

このチェックは Commit 前に必ず実行する。

---

## 7. Implementation Roadmap

### Phase 2: Core Engine
- spec_loader.py
- config_loader.py
- validation_engine.py
- data_state_machine.py

### Phase 3: Workflow & AI Integration
- ai_interface.py
- prompt_builder.py
- hitl_gate.py
- recursive_integrity_checker.py

### Phase 4: Execution Pipeline
- pipeline_manager.py
- execution_controller.py

### Phase 5: GitHub & Release Management
- github_sync.py
- release_manager.py
- audit_logger.py

---

## 8. Implementation Order (Critical Path)

実装はボトムアップで行う。

実装順序:

1. spec_loader.py
2. config_loader.py
3. validation_engine.py
4. data_state_machine.py
5. recursive_integrity_checker.py
6. hitl_gate.py
7. ai_interface.py
8. prompt_builder.py
9. pipeline_manager.py
10. execution_controller.py
11. github_sync.py
12. release_manager.py
13. audit_logger.py

**spec_loader.py がすべての起点となる最重要モジュールである。**

---

## 9. Environment & Deployment

### 9.1 Config Files

config/
- system_config.json
- model_config.json
- path_config.json

### 9.2 Secrets Management

.env に以下を保存する。

- OPENAI_API_KEY
- GEMINI_API_KEY
- GITHUB_TOKEN

### 9.3 GitHub Sync Operation

GitHub は以下の用途で使用する。

- Spec バージョン管理
- Data バージョン管理
- Audit Log 保存
- Release Tag
- Backup
- 変更履歴管理

Commit ルール:
- Draft → Commit 禁止
- Approved → Commit 可
- Commit → Tag
- Release Note 作成

---

## 10. Testing & QA Strategy

### 10.1 Unit Test
各モジュールごとに単体テストを作成する。

対象:
- spec_loader
- validation_engine
- data_state_machine
- recursive_integrity_checker
- github_sync

### 10.2 Integration Test
Pipeline 全体の統合テストを行う。

テスト内容:
- Spec Load
- AI Draft
- Validation
- HITL Approval
- State Transition
- GitHub Commit
- Audit Log

### 10.3 Integrity Test
整合性チェックを定期実行する。

- ID 重複
- JSON Schema 違反
- Timeline 矛盾
- Spec Version 不整合
- GitHub とローカル差分

---

## 11. Summary

Story OS は単なる小説生成ツールではなく、以下を実現するシステムである。

- Spec Driven Development
- AI Assisted Content Generation
- Human Governance
- Data State Lifecycle Management
- GitHub Based Version Control
- Full Audit Logging
- Recursive Integrity Verification

本 Implementation Plan は、Story OS を安定稼働させるためのエンジニアリング実装計画の基盤となる。

今後の開発は本ドキュメントの Implementation Order と Roadmap に従って進める。

---

[EOF]