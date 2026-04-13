Source: docs/spec/Project_Governance/NWF_Release_Management_Spec_v2.0.1.md
Updated: 2026-04-13T15:14:00+09:00
PIC: Engineer / ChatGPT

# NWF_Release_Management_Spec v2.0.1

---

## 1. 概要

本仕様書は、NWF（Narrative Workflow Framework）における Phase 2.7「Release Manager」の設計・実装仕様を定義する。

本機能は、Phase 2.6「GitHub Sync」によって蓄積されたコミット（点）を、物語的マイルストーン（面）として確定し、Spec / Code / Data の三位一体整合性を維持したまま不変のリリースとして固定することを目的とする。

---

## 2. リリースの定義

### 2.1 リリースとは

NWFにおけるリリースとは以下を満たす状態を指す：

- Spec（docs/spec）
- Code（src）
- Data（data）

がすべて一致し、

- Integrity Layer（L1〜L4）
- AnomalyDetector = SUCCESS

を満たした「完全整合スナップショット」

---

### 2.2 リリース種別

| 種別 | 対応単位 | バージョン |
|------|----------|------------|
| Patch | Beat | vX.Y.Z |
| Minor | Episode | vX.Y.0 |
| Major | Milestone | vX.0.0 |

---

## 3. システム構成

### 3.1 モジュール構成

| モジュール | パス | 役割 |
|---|---|---|
| ReleaseManager | src/release/release_manager.py | リリース統括 |
| VersionController | src/release/version_controller.py | バージョン管理 |
| DeploymentManager | src/release/deployment_manager.py | パッケージング |
| ChangelogGenerator | src/release/changelog_generator.py | 履歴生成 |

---

## 4. 基本原則

### 4.1 Integrity Gate

以下すべて SUCCESS の場合のみリリース可能：

- integrity_checker.py
- consistency_validator.py
- recursive_auditor.py
- anomaly_detector.py

---

### 4.2 Atomic Release

以下を同時に固定：

- Spec
- Code
- Data

部分リリースは禁止

---

### 4.3 Temporal Consistency

- JST固定
- ISO 8601形式
- Gitタグ時刻とEntity.updated_at一致

---

### 4.4 Immutable Snapshot

リリース後のデータは変更不可（Read Only）

---

## 5. データ構造（I/F Contract）

### 5.1 ReleaseManifest

{
  "release_id": "string",
  "version": "string",
  "release_type": "string",
  "timeline_id": "string",
  "integrity_status": "string",
  "snapshot_hash": "string",
  "created_at": "ISO8601_JST"
}

---

### 5.2 ReleaseResult

{
  "success": "bool",
  "error_code": "string",
  "message": "string"
}

---

### 5.3 ChangelogEntry

{
  "event_id": "string",
  "summary": "string",
  "entity_type": "string",
  "entity_id": "string",
  "timestamp": "ISO8601_JST"
}

---

## 6. モジュール別 I/F 定義

---

### 6.1 release_manager.py

#### Public API

execute_release(trigger: string) -> ReleaseResult

#### 処理フロー

1. Integrity Gate
2. Version決定
3. Changelog生成
4. パッケージング
5. Git Tag

---

#### 依存モジュール

- sync_scheduler.py
- anomaly_detector.py
- version_controller.py
- deployment_manager.py
- changelog_generator.py

---

### 6.2 version_controller.py

#### Public API

determine_version(release_type: string) -> string

increment_version(current_version: string, release_type: string) -> string

---

#### 依存モジュール

- version_manager.py

---

### 6.3 deployment_manager.py

#### Public API

package_release(manifest: dict) -> string

archive_release(path: string) -> bool

---

#### 出力構造

.nwf/releases/vX.Y.Z/
    ├── spec/
    ├── src/
    ├── data/
    └── manifest.json

---

### 6.4 changelog_generator.py

#### Public API

generate_changelog(events: list) -> list[ChangelogEntry]

format_changelog(entries: list) -> string

---

#### 依存モジュール

- commit_analyzer.py
- audit_log_manager.py

---

## 7. 既存モジュールとの接続

| モジュール | 接続内容 |
|---|---|
| sync_scheduler | トリガー受信 |
| workflow_executor | 実行完了通知 |
| anomaly_detector | リリース可否 |
| version_manager | バージョン取得 |
| commit_analyzer | 差分解析 |
| audit_log_manager | 履歴取得 |

---

## 8. 実行フロー

### 8.1 Release Pipeline

1. Sync 完了確認
2. Integrity Check
3. Version決定
4. Changelog生成
5. Artifact生成
6. Git Tag付与
7. ロック解除

---

## 9. エラーモデル

| error_code | 内容 |
|---|---|
| ERR_REL_001 | 整合性違反 |
| ERR_REL_002 | 同期未完了 |
| ERR_REL_003 | バージョン衝突 |
| ERR_REL_004 | パッケージ失敗 |

---

## 10. セキュリティ

- secrets/ 配下は除外
- Git Tokenは.env管理
- ReleaseはIntegrity通過時のみ

---

## 11. HITL対象

以下は人間判断必須：

- Major Version決定
- 競合解決
- リリース承認（Episode以上）

---

## 12. 拡張性

- Multi-Branch対応（Thread Graph）
- 自動リリース（Phase 2.8）
- CI/CD連携

---

## 13. まとめ

本仕様により以下を達成する：

- 完全整合リリース
- 監査可能な履歴
- 物語的マイルストーン管理
- Phase 3への拡張基盤

---

[EOF]