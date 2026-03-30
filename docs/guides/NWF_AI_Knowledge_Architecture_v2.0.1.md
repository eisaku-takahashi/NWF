Source: docs/guides/NWF_AI_Knowledge_Architecture_v2.0.1.md
Updated: 2026-03-31T03:43:00+09:00
PIC: Engineer / ChatGPT

# NWF AI Knowledge Architecture v2.0.1

---

## 1. 概要

本ドキュメントは、Story OS / NWF における知識管理基盤（Knowledge Infrastructure Architecture）の構造、役割、データフロー、および整合性管理方法を定義するものである。

本アーキテクチャは単なるドキュメント管理ルールではなく、仕様（Spec）、データ（Data）、実行（Execution）、ログ（Log）、履歴（History）を含む、Story OS 全体の知識ライフサイクルを管理する基盤層として位置付けられる。

v2.0.1 においては特に以下を最重要事項とする。

- Recursive Integrity（再帰的整合性）
- HITL（Human-In-The-Loop）による承認
- Data State Machine による知識状態管理
- Audit Log による意思決定履歴の保存
- Spec を単一真実源（SSOT）とする構造

---

## 2. Knowledge Infrastructure Architecture の位置付け

Knowledge Architecture は Story OS の System Architecture における Infrastructure Layer に属し、以下の役割を持つ。

1. 仕様（Spec）の単一真実源管理
2. GitHub によるバージョン履歴管理
3. Runtime データの状態遷移管理
4. ログおよび監査履歴の保存
5. AI が参照するコンテキスト知識の管理
6. Google Drive へのバックアップによる冗長化

この層は Engine や AI Workflow より下位ではなく、それらすべてを支える基盤層として扱う。

---

## 3. Knowledge Hexagon（知識6層構造）

v2.0.1 では Knowledge 管理構造を以下の 6 層で定義する。

### 3.1 Spec Layer
docs/spec/ に保存される仕様書群。
Story OS における単一真実源（SSOT）であり、すべての判断基準は Spec に従う。

### 3.2 Repository Layer
Git / GitHub によるバージョン管理層。
変更履歴、差分、ブランチ、リリース管理を担当する。

### 3.3 Runtime Layer
workspace/ における実行時データ層。
Draft、Review、Approved などの状態遷移を行う。

### 3.4 Log & Audit Layer
logs/ に保存されるログおよび監査履歴。
AI の生成結果、失敗ログ、意思決定ログ、整合性チェック結果を保存する。

### 3.5 Context Layer
NotebookLM 等の知識検索・セマンティック検索層。
Spec やログを AI が理解・参照するためのコンテキスト管理層。

### 3.6 Backup Layer
Google Drive 等の外部ストレージによるバックアップ層。
GitHub 障害やデータ消失に備えた冗長化を行う。

---

## 4. Data State Machine と Knowledge Lifecycle

知識およびドキュメントは以下の状態遷移を行う。

1. Draft
2. Review
3. Approved
4. Archived

### 4.1 Draft
AI または人間が作成した初期状態。

### 4.2 Review
HITL Gate によるレビュー中の状態。

### 4.3 Approved
Spec または正式ドキュメントとして採用された状態。

### 4.4 Archived
旧バージョンまたは廃止された知識。

すべての Spec および Guide はこの状態遷移に従う。

---

## 5. HITL Governance（Human-In-The-Loop）

すべての Spec 更新、重要な Guide 更新、System Architecture 変更は HITL Gate を通過しなければならない。

HITL Gate の役割：

- Spec 更新承認
- Version 更新承認
- Architecture 変更承認
- Data State 遷移承認
- Recursive Integrity チェック承認

AI は Spec を直接確定してはならず、必ず HITL による承認を必要とする。

---

## 6. Recursive Integrity（再帰的整合性）

Recursive Integrity とは、ある Spec または Guide を変更した際に、関連する他の Spec、Guide、Index、Architecture との整合性を再帰的に確認するプロセスである。

変更時には以下を確認する。

1. 関連 Spec との整合性
2. System Architecture との整合性
3. Index / Master Index の更新
4. Version 整合性
5. 用語定義の整合性
6. Data Flow / Execution Flow への影響
7. AI Workflow への影響

Recursive Integrity は Knowledge Architecture における最重要機能の一つである。

---

## 7. Logging / Audit Knowledge System

Log & Audit Layer は単なるログ保存ではなく、知識生成の履歴として扱う。

保存対象：

- AI 生成ログ
- 修正履歴
- Spec 更新理由
- 設計判断ログ
- エラー / 失敗ログ
- Integrity Check 結果
- HITL 承認ログ

失敗した生成結果や誤った設計も重要な知識として保存し、将来の設計改善に利用する。

これを Audit Knowledge と呼ぶ。

---

## 8. Version Management と Knowledge Versioning

Knowledge Architecture では以下の Version を管理する。

- Spec Version
- Guide Version
- Architecture Version
- Engine Version
- Workflow Version
- Repository Version

Version 更新ルール：

1. Spec 変更 → Minor または Major 更新
2. Guide 修正 → Patch 更新
3. Architecture 変更 → Minor 以上
4. Data Format 変更 → Major

Version は GitHub Tag と連動する。

---

## 9. Security and Integrity

Knowledge System において最も重要なのは「正しさ」ではなく「追跡可能性」と「整合性」である。

Security / Integrity の目的：

- 誰が変更したか追跡できる
- いつ変更されたか追跡できる
- なぜ変更されたか説明できる
- 以前の状態に戻せる
- Spec 間の矛盾を防ぐ
- 誤った知識の確定を防ぐ

Integrity を守る仕組み：

- Spec SSOT
- Git Version Control
- HITL Approval
- Recursive Integrity Check
- Audit Log
- Backup
- Read Only Spec Release

---

## 10. まとめ

NWF AI Knowledge Architecture v2.0.1 は、単なるドキュメント管理システムではなく、Story OS 全体の知識、仕様、履歴、意思決定、ログを統合管理する Knowledge Infrastructure である。

本アーキテクチャの最重要概念は以下の 5 つである。

1. Spec = Single Source of Truth
2. Knowledge Hexagon（6 Layer Architecture）
3. Data State Machine
4. HITL Governance
5. Recursive Integrity

Story OS の安定性と長期運用性は Knowledge Architecture に依存するため、本ドキュメントは System Architecture と同等の重要度を持つ基盤仕様とする。

---

[EOF]