Source: docs/spec/Project_Governance/NWF_GitHub_Sync_Spec_v2.0.1.md
Updated: 2026-04-13T06:06:00+09:00
PIC: Engineer / ChatGPT

# NWF_GitHub_Sync_Spec v2.0.1

---

## 1. 概要

本仕様書は、NWF（Narrative Workflow Framework）における Phase 2.6「GitHub Sync」機能の実装仕様を定義する。

本機能は以下の目的を持つ：

- Spec / Code / Data の三位一体整合性を外部（GitHub）へ拡張
- Integrity Layer（L1〜L4）通過後のみ同期を許可
- 外部変更に対する逆方向整合性保証（Pull Validation）
- 監査可能な同期履歴の生成

---

## 2. システム構成

### 2.1 モジュール構成

| モジュール名 | パス | 役割 |
|---|---|---|
| GitHubSyncManager | src/integration/github_sync_manager.py | 同期処理の統括 |
| RepositoryWatcher | src/integration/repository_watcher.py | 変更検知 |
| CommitAnalyzer | src/integration/commit_analyzer.py | コミット解析 |
| SyncScheduler | src/integration/sync_scheduler.py | 実行制御 |

---

## 3. 基本原則

### 3.1 Integrity First

- integrity_checker.py
- consistency_validator.py
- recursive_auditor.py
- anomaly_detector.py

全て SUCCESS の場合のみ同期可能

---

### 3.2 Atomic Sync

以下を同時に同期する：

- Spec（docs/spec）
- Code（src）
- Data（data）

部分同期は禁止

---

### 3.3 Temporal Consistency

- JST固定
- ISO 8601形式
- GitHub commit timestamp と Entity.updated_at の整合性保証

---

## 4. 同期フロー

### 4.1 Push（Local → GitHub）

1. RepositoryWatcher が変更検知
2. Integrity Layer 実行
3. CommitAnalyzer によるメッセージ生成
4. GitHubSyncManager が push 実行

---

### 4.2 Pull（GitHub → Local）

1. Temporary Fetch（.nwf/temp_sync）
2. Shadow Validation 実行
3. 判定
   - 成功 → マージ
   - 失敗 → HITL

---

## 5. インターフェース定義（I/F Contract）

本章は Phase 2.6 実装における最重要仕様である。

---

### 5.1 共通データ構造

#### SyncEvent

{
  "event_id": "string",
  "entity_id": "string",
  "event_type": "string",
  "timestamp": "ISO8601_JST",
  "status": "string"
}

---

#### SyncResult

{
  "success": "bool",
  "error_code": "string",
  "message": "string"
}

---

### 5.2 github_sync_manager.py

#### Public API

sync_push(changes: list[SyncEvent]) -> SyncResult

sync_pull() -> SyncResult

resolve_conflict(conflict_data: dict) -> SyncResult

---

#### 依存モジュール

- version_manager.py
- audit_log_manager.py
- anomaly_detector.py

---

### 5.3 repository_watcher.py

#### Public API

detect_changes() -> list[SyncEvent]

filter_scope(paths: list[str]) -> list[str]

---

#### 依存モジュール

- data_state_manager.py
- file_system spec

---

### 5.4 commit_analyzer.py

#### Public API

generate_commit_message(events: list[SyncEvent]) -> string

analyze_impact(events: list[SyncEvent]) -> dict

---

#### フォーマット

[NWF-SYNC] ACTION: ENTITY_TYPE (ENTITY_ID) at TIMELINE_POINT

---

#### 依存モジュール

- audit_log_manager.py
- entity_manager.py
- timeline_model

---

### 5.5 sync_scheduler.py

#### Public API

schedule_sync(trigger: string) -> None

execute_sync_cycle() -> SyncResult

---

#### トリガー

- workflow_executor 完了
- Beat終了
- Episode終了

---

#### 依存モジュール

- workflow_executor.py
- execution_pipeline

---

## 6. 既存モジュールとの整合性

| モジュール | 接続内容 |
|---|---|
| data_state_manager | 状態差分取得 |
| version_manager | バージョン比較 |
| audit_log_manager | 監査ログ取得 |
| workflow_executor | 実行完了トリガー |
| anomaly_detector | 最終同期許可判定 |

---

## 7. セキュリティ仕様

### 7.1 Token管理

- 保存先: secrets/.env
- Git管理禁止
- 環境変数経由で取得

---

### 7.2 アクセス制御

- all スコープのみ許可
- 書き込みは Integrity 通過時のみ

---

## 8. エラーモデル

| error_code | 内容 |
|---|---|
| ERR_SYNC_001 | 認証失敗 |
| ERR_SYNC_002 | 整合性違反 |
| ERR_SYNC_003 | 競合 |
| ERR_SYNC_004 | Pull検証失敗 |

---

## 9. 拡張性

### 9.1 Multi-Branch対応

- Git branch = Thread Graph 分岐

---

### 9.2 Automation連携

- Phase 2.8 にて自動修復へ接続

---

## 10. 未定義事項（要HITL決定）

1. Token暗号化方式
2. Pull優先度ルール
3. 自動マージ範囲

---

## 11. まとめ

本仕様により以下を達成する：

- 外部同期における完全整合性
- 双方向検証（Push / Pull）
- 監査可能な変更履歴
- Phase 3以降への拡張基盤

---

[EOF]