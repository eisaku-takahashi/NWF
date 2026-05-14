Source: docs/spec/Kernel_Spec/NWF_Kernel_Audit_System_Spec_v2.0.1.md
Updated: 2026-04-06T12:01:00+09:00
PIC: Engineer / ChatGPT

# NWF Kernel Audit System Spec v2.0.1

---

## 1. 概要

本仕様は、NWF v2.0.1 における Kernel Layer 最下層基盤である Audit System（Immutable Memory）の仕様を定義する。

Audit System は単なるログ出力機構ではなく、NWF システムにおいて発生したすべての事象・状態遷移・実行履歴・意思決定・データ変更を記録する「不変の記憶（Immutable Memory / Immutable Ledger）」として機能する。

Audit Log は NWF における Single Source of Truth であり、理論上すべての Entity / State / Timeline / Workflow の状態は Audit Log の Replay によって復元可能でなければならない。

---

## 2. 目的

Audit System の目的は以下である。

- 完全なトレーサビリティの確保
- 状態遷移の監査可能性
- AI / Workflow の意思決定履歴の保存
- フォレンジック対応（事後検証）
- Spec Driven System の証拠基盤
- Execution Pipeline の再現性確保
- システム状態の Replay / Rollback / Time Travel の基盤
- データ真正性の保証

---

## 3. 適用範囲

Audit System は以下のすべてのレイヤ・モジュールに適用される。

### 3.1 Kernel Layer
- Event Manager
- Entity Manager
- Data State Manager
- Version Manager
- Metadata Manager
- Concurrency Control
- Temporal Management
- Audit Logger

### 3.2 Core / Engine
- Execution Pipeline
- Timeline Engine
- Event Engine
- Story Engine
- Query Engine
- Simulation Engine
- Analysis Engine
- Validation System

### 3.3 AI / Workflow
- AI Authoring Interface
- AI Analysis Interface
- AI Collaboration Workflow
- Human in the Loop Workflow
- Parallel Workflow
- Story Generation Workflow
- Story Analysis Workflow

### 3.4 Loader / Spec / File System
- Spec Loader
- Spec Registry
- Dependency Resolver
- File System
- GitHub Sync
- Spec Migration

---

## 4. 基本原則（Kernel Constraints）

### 4.1 Append-Only

Audit Log は追記専用とする。

- 更新禁止
- 削除禁止
- 上書き禁止

すべての変更は新しいイベントとして記録する。

---

### 4.2 Immutable

Audit Log は不変である。

- 改ざん不可
- 履歴削除不可
- 永続保存
- 将来：ハッシュチェーンによる完全性保証

---

### 4.3 JST 固定

すべてのタイムスタンプは JST とする。

形式：
YYYY-MM-DDTHH:MM:SS+09:00

---

### 4.4 JSONL 形式

ログは JSON Lines 形式で保存する。

- 1行 = 1イベント
- UTF-8
- Append Only
- Stream Write

---

### 4.5 全イベント記録

以下は必ず Audit に記録される。

- Entity 作成・更新
- State Transition
- Engine 実行
- Workflow 実行
- AI 実行
- Validation
- Error / Exception
- File Operation
- Spec Load / Migration
- Transaction Begin / Commit / Rollback
- Lock / Unlock
- Timeline 操作

---

## 5. Audit Event 分類

Audit Event は以下のカテゴリに分類される。

### 5.1 System / Kernel Event
- SYSTEM_START
- SYSTEM_STOP
- SPEC_LOAD
- SPEC_MIGRATION
- GITHUB_SYNC
- TRANSACTION_BEGIN
- TRANSACTION_COMMIT
- TRANSACTION_ROLLBACK
- LOCK_ACQUIRE
- LOCK_RELEASE

### 5.2 Data / State Event
- ENTITY_CREATED
- ENTITY_UPDATED
- ENTITY_DELETED
- STATE_TRANSITION
- VERSION_CREATED
- METADATA_UPDATED

### 5.3 Engine / Execution Event
- PIPELINE_START
- PIPELINE_END
- ENGINE_START
- ENGINE_END
- VALIDATION_RESULT

### 5.4 Narrative / Timeline Event
- SCENE_START
- THREAD_BRANCH
- THREAD_MERGE
- TIMELINE_MOVE
- TIMELINE_ROLLBACK

### 5.5 Workflow / AI Event
- AI_EXECUTION
- WORKFLOW_START
- WORKFLOW_END
- HUMAN_APPROVAL
- HUMAN_REJECT
- PARALLEL_WORKFLOW_MERGE

### 5.6 File Event
- FILE_CREATE
- FILE_UPDATE
- FILE_DELETE
- FILE_READ

### 5.7 Error / Exception
- ERROR
- EXCEPTION
- VALIDATION_ERROR

---

## 6. Audit Log データ構造

### 6.1 必須フィールド

| フィールド | 型 | 説明 |
|------------|----|------|
| event_id | string | UUID |
| timestamp | string | JST ISO8601 |
| transaction_id | string | トランザクションID |
| category | string | Event分類 |
| event_type | string | イベント種別 |
| actor | string | 実行主体 |
| object_id | string | 対象Object |
| entity_id | string | Entity ID |
| spec_id | string | Spec ID |
| action | string | 実行内容 |
| status_before | string | 変更前 |
| status_after | string | 変更後 |

---

### 6.2 コンテキスト情報

| フィールド | 型 | 説明 |
|------------|----|------|
| timeline_id | string | Timeline |
| thread_id | string | Thread |
| scene_id | string | Scene |
| workflow_id | string | Workflow |
| engine_id | string | Engine |

---

### 6.3 任意フィールド

| フィールド | 型 | 説明 |
|------------|----|------|
| payload | dict | 入出力 |
| metadata | dict | 拡張 |
| validation_result | dict | 検証結果 |
| error | string | エラー |
| hash | string | ハッシュチェーン |

---

## 7. Transaction / Context モデル

Audit System は以下の 3 レベルでコンテキストを管理する。

### 7.1 Atomic Level
単一 Entity 更新

### 7.2 Transaction Level
Engine 実行 / Execution Pipeline 実行

### 7.3 Workflow Level
AI + Human + Workflow の一連の処理

transaction_id は contextvars によりスレッド・非同期処理間で共有される。

Audit Logger は Context Manager を提供する。

例：

with transaction("ENGINE_EXECUTION"):
    処理

---

## 8. Audit Event Lifecycle

Audit Event は以下のライフサイクルを持つ。

1. Event Generation
2. Transaction Buffering
3. Validation
4. Persistent Write (JSONL Append)
5. Broadcast / Notification

---

## 9. ファイル管理

### 9.1 保存形式
JSONL

### 9.2 命名規則
audit_YYYYMMDD.jsonl

### 9.3 ログローテーション
- 日付変更時に切替
- 起動時チェック
- ファイルハンドル再生成

---

## 10. 初期化順序

Audit System は最優先で初期化される。

初期化順序：

1. Audit System
2. Spec Loader
3. Entity Manager
4. Event Manager
5. State Manager
6. Engines
7. Workflow
8. AI Interface

理由：
すべてのエラー・イベントを記録するため。

---

## 11. Kernel Architecture における位置付け

Audit System は NWF Layered Architecture において最下層に位置する。

役割：

- すべてのイベントの記録
- 状態復元の基盤
- Temporal Management の現在位置管理
- Concurrency Control の履歴管理
- Spec Governance の証跡
- AI 判断履歴の保存

Audit Log は NWF 世界の「因果律の記録」である。

---

## 12. セキュリティ / 完全性

将来拡張：

- ハッシュチェーン
- 改ざん検知
- 分散監査ログ
- 監査API
- リアルタイム監視
- Event Streaming
- Audit Replay Engine

---

## 13. 実装対応

対応ファイル：

- src/core/audit_logger.py
- src/core/audit_log_manager.py

関連モジュール：

- entity_manager
- data_state_manager
- event_manager
- execution_pipeline
- spec_loader
- concurrency_control
- temporal_management
- validation_system

---

## 14. まとめ

Audit System は NWF Kernel の最下層に位置する Immutable Memory であり、

「すべてを記録し、決して忘れない」

という原則に基づいて設計される。

Audit Log は以下を保証する。

- 完全な透明性
- 再現可能な Execution
- AI 判断の説明可能性
- データの真正性
- Timeline / State の完全復元
- Spec Driven System の証拠基盤

Audit System は NWF OS における「時間と因果律の記録装置」である。

---

[EOF]