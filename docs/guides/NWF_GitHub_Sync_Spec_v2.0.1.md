Source: docs/guides/NWF_GitHub_Sync_Spec_v2.0.1.md
Updated: 2026-04-04T16:21:00+09:00
PIC: Engineer / ChatGPT

# NWF GitHub Sync Spec v2.0.1

---

## 1. 概要

本ドキュメントは、Story OS / NWF における GitHub Repository の役割、同期（Sync）手順、ブランチ戦略、バージョン管理、バックアップ連携、および Governance との関係を定義する。

GitHub は単なるバックアップやファイル共有ではなく、Story OS における **Truth Persistence Layer（真実の保存層）** として位置付けられる。

GitHub は以下を保証する。

- Spec の Single Source of Truth
- Version History（who / when / why）
- Release 固定
- Audit Trail
- Disaster Recovery
- Team Collaboration
- Knowledge Persistence

---

## 2. Architecture Role（GitHub の位置付け）

Story OS Knowledge Architecture における GitHub の位置付けは以下の通り。

### 2.1 Repository Layer（Primary SSOT）
GitHub Repository は以下のデータを管理する。

- spec
- guides
- project_documents
- engine_code
- approved_data
- schema
- audit_logs（重要なもの）

GitHub は **primary single source of truth** とする。

### 2.2 Google Drive との役割分担

| layer | system | role |
|------|--------|------|
| repository_layer | github | primary ssot / version control |
| backup_layer | google_drive | redundancy / sync |
| runtime_layer | workspace | draft / review data |
| log_layer | logs/ | execution / audit logs |

Google Drive は backup / sync、GitHub は truth repository とする。

---

## 3. Repository Structure（管理対象ディレクトリ）

GitHub で管理するディレクトリは以下。

### 3.1 管理対象
- docs/spec/
- docs/guides/
- docs/project/
- src/
- data/schema/
- logs/audit/
- output/

### 3.2 条件付き管理
- logs/
- data/
- workspace/review/

### 3.3 Git 管理対象外（.gitignore）
以下は GitHub にコミットしない。

- workspace/temp/
- workspace/draft/
- logs/temp/
- logs/runtime/
- .env
- cache/
- node_modules/
- __pycache__/
- large_media/
- backup/

---

## 4. Branch Strategy（ブランチ戦略）

v2.0.1 標準ブランチ戦略を以下とする。

### 4.1 main
production / stable / approved_data

以下のみコミット可能。
- approved spec
- approved guides
- release version
- stable engine
- completed output

### 4.2 dev
review / integration branch

- review 中 spec
- architecture 更新
- integration test
- pre-release 状態

### 4.3 feature/*
draft / experiment branch

例：
- feature/spec_update
- feature/engine_refactor
- feature/story_plot
- feature/data_schema

Data State と Branch の対応は以下。

| data_state | branch |
|------------|--------|
| draft | feature/* |
| review | dev |
| approved | main |
| archived | tag / release |

---

## 5. Sync Workflow（GitHub 同期手順）

### 5.1 基本 Sync 手順
1. git pull
2. ファイル更新
3. git add
4. git commit
5. git push

### 5.2 Sync 実行タイミング
以下のタイミングで Sync を実行する。

1. spec 更新後
2. guide 作成後
3. architecture 変更後
4. version 更新後
5. hitl 承認後
6. release 作成前
7. 作業終了時
8. disaster recovery 前
9. audit log 確定時

---

## 6. HITL Governance と Commit Rule

v2.0.1 の最重要ルール：

approved = commit

### 6.1 Data State と Commit の関係

| state | commit |
|------|--------|
| draft | no |
| review | dev branch |
| approved | main branch |
| archived | tag |

### 6.2 Commit 可能な条件
以下を満たす場合のみ main に commit 可能。

- hitl 承認済み
- version 更新済み
- recursive integrity check 完了
- index 更新済み
- metadata 更新済み
- audit log 記録済み

---

## 7. Version / Tag / Release Rule

### 7.1 Version Format
v[major].[minor].[patch]

例：
- v2.0.0
- v2.0.1
- v2.1.0
- v3.0.0

### 7.2 Version 更新ルール

| change | version |
|-------|---------|
| architecture_change | major |
| spec_structure_change | minor |
| guide_update | patch |
| typo_fix | patch |
| data_format_change | major |
| engine_change | minor |

### 7.3 Tag と Release
Version 更新時は以下を実行する。

1. spec version 更新
2. master index 更新
3. commit
4. git tag 作成
5. github release 作成

Release は Story OS version freeze を意味する。

---

## 8. Audit & Transparency（監査と透明性）

GitHub Commit History は Story OS の意思決定履歴となる。

さらに、NWF_Kernel_Audit_System と統合し、Git 操作はすべて Audit Event として記録される。

### 8.1 Audit Event 定義

各 Sync 操作は以下のイベントを発行する。

- event_type: system_start / commit / push / release
- actor: user:id または system
- transaction_id: uuid_v4
- timestamp: iso_8601_jst
- metadata:
  - commit_hash
  - branch
  - files_changed
  - approval_id
  - related_spec

### 8.2 SYSTEM_START イベント

システム起動時に以下を必ず記録する。

- event_type: system_start
- metadata:
  - github_commit_hash
  - active_branch
  - version
  - environment

これにより「実行ログ」と「ソースコード状態」を完全に紐付ける。

### 8.3 Commit Message Rule（拡張）

commit message には以下を必ず含める。

- what
- why
- version
- impact_scope
- related_spec
- hitl_approval_id

---

## 9. Disaster Recovery（災害復旧）

障害発生時の復旧順序は以下。

1. github repository を clone
2. 最新 release tag を checkout
3. google drive backup から workspace 復元
4. logs を復元
5. engine / environment 再構築
6. integrity check 実行
7. system resume

GitHub を最優先復旧ソースとする。

---

## 10. まとめ

NWF GitHub Sync Spec v2.0.1 において GitHub は単なる同期ツールではなく、Story OS の truth persistence layer として機能する。

さらに Audit System により、

「いつ・誰が・どのコードで・なぜ変更したか」

を完全に追跡可能とする。

本仕様の最重要ルールは以下。

1. github = primary ssot
2. google drive = backup / sync
3. approved = commit
4. draft = feature branch
5. review = dev branch
6. release = tag / version freeze
7. git history = decision history
8. repository = knowledge persistence
9. commit = audit event
10. system_start = code state anchor

GitHub 運用は Story OS の整合性、透明性、再現性、説明責任を保証する中核システムである。

---

[EOF]