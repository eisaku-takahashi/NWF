Source: docs/guides/NWF_GitHub_Sync_Spec_v2.0.1.md
Updated: 2026-03-31T04:12:00+09:00
PIC: Engineer / ChatGPT

# NWF GitHub Sync Spec v2.0.1

---

## 1. 概要

本ドキュメントは、Story OS / NWF における GitHub Repository の役割、同期（Sync）手順、ブランチ戦略、バージョン管理、バックアップ連携、および Governance との関係を定義する。

GitHub は単なるバックアップやファイル共有ではなく、Story OS における **Truth Persistence Layer（真実の保存層）** として位置付けられる。

GitHub は以下を保証する。

- Spec の Single Source of Truth
- Version History（Who / When / Why）
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

- Spec
- Guides
- Project Documents
- Engine / Workflow Code
- Approved Data
- Schema
- Audit Logs（重要なもの）

GitHub は **Primary Single Source of Truth** とする。

### 2.2 Google Drive との役割分担

| Layer | System | Role |
|------|--------|------|
| Repository Layer | GitHub | Primary SSOT / Version Control |
| Backup Layer | Google Drive | Redundancy / Sync |
| Runtime Layer | Workspace | Draft / Review Data |
| Log Layer | logs/ | Execution / Audit Logs |

Google Drive は Backup / Sync、GitHub は Truth Repository とする。

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
- output/（完成成果物）

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
Production / Stable / Approved Data

以下のみコミット可能。
- Approved Spec
- Approved Guides
- Release Version
- Stable Engine
- Completed Output

### 4.2 dev
Review / Integration Branch

- Review 中 Spec
- Architecture 更新
- Integration Test
- Pre-Release 状態

### 4.3 feature/*
Draft / Experiment Branch

例：
- feature/spec_update
- feature/engine_refactor
- feature/story_plot
- feature/data_schema

Data State と Branch の対応は以下。

| Data State | Branch |
|------------|--------|
| Draft | feature/* |
| Review | dev |
| Approved | main |
| Archived | tag / release |

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

1. Spec 更新後
2. Guide 作成後
3. Architecture 変更後
4. Version 更新後
5. HITL 承認後
6. Release 作成前
7. 作業終了時
8. Disaster Recovery 前
9. Audit Log 確定時

---

## 6. HITL Governance と Commit Rule

v2.0.1 の最重要ルール：

**Approved = Commit**

### 6.1 Data State と Commit の関係

| State | Commit |
|------|--------|
| Draft | No |
| Review | dev branch |
| Approved | main branch |
| Archived | tag |

### 6.2 Commit 可能な条件
以下を満たす場合のみ main に commit 可能。

- HITL 承認済み
- Version 更新済み
- Recursive Integrity Check 完了
- Index 更新済み
- Metadata 更新済み
- Audit Log 記録済み

---

## 7. Version / Tag / Release Rule

### 7.1 Version Format
v[Major].[Minor].[Patch]

例：
- v2.0.0
- v2.0.1
- v2.1.0
- v3.0.0

### 7.2 Version 更新ルール

| Change | Version |
|-------|---------|
| Architecture Change | Major |
| Spec Structure Change | Minor |
| Guide Update | Patch |
| Typo Fix | Patch |
| Data Format Change | Major |
| Engine Change | Minor |

### 7.3 Tag と Release
Version 更新時は以下を実行する。

1. Spec Version 更新
2. Master Index 更新
3. Commit
4. Git Tag 作成
5. GitHub Release 作成

Release は Story OS Version Freeze を意味する。

---

## 8. Audit & Transparency（監査と透明性）

GitHub Commit History は Story OS の意思決定履歴となる。

Commit Message には以下を含める。

- What（何を変更したか）
- Why（なぜ変更したか）
- Spec Version
- Impact
- Related Spec
- HITL Approval

例：

Update System Architecture v2.0.1
Reason: Knowledge Architecture Integration
Impact: AI Workflow / Data Flow Updated
Approved by HITL

Git History = Decision History とする。

---

## 9. Disaster Recovery（災害復旧）

障害発生時の復旧順序は以下。

1. GitHub Repository を Clone
2. 最新 Release Tag を Checkout
3. Google Drive Backup から Workspace 復元
4. Logs を復元
5. Engine / Environment 再構築
6. Integrity Check 実行
7. System Resume

GitHub を最優先復旧ソースとする。

---

## 10. まとめ

NWF GitHub Sync Spec v2.0.1 において GitHub は単なる同期ツールではなく、Story OS の Truth Persistence Layer として機能する。

本仕様の最重要ルールは以下。

1. GitHub = Primary SSOT
2. Google Drive = Backup / Sync
3. Approved = Commit
4. Draft = feature branch
5. Review = dev branch
6. Release = Tag / Version Freeze
7. Git History = Decision History
8. Repository = Knowledge Persistence

GitHub 運用は Story OS の整合性、透明性、再現性、長期運用性を保証するための中核システムである。

---

[EOF]