Source: docs/spec/Execution_Spec/NWF_Concurrency_Control_v2.0.1.md
Updated: 2026-04-06T09:03:00+09:00
PIC: Engineer / ChatGPT

# NWF Concurrency Control v2.0.1

---

## 1. 概要

本ドキュメントは、NWF (Narrative World Framework) における同時実行制御（Concurrency Control）の設計仕様を定義する。

NWF は Event Sourcing および Audit Log を中心とした「Story OS」であり、Concurrency Control の目的は単なるデータ競合の回避ではなく、**物語の因果律と世界線の整合性を維持すること**である。

そのため、本仕様では従来のデータベースロックモデルに加え、Timeline、Scene、Entity など物語構造に基づく階層型制御モデルを採用する。

---

## 2. 設計原則 (Design Principles)

### 2.1 Causality First

NWF において最も重要な原則は **因果関係の保護** である。
後に発生したイベントが過去の前提条件を破壊することは禁止される。

すべての Transaction は以下を満たさなければならない。

- 過去の Audit Log を改変しない
- 因果関係リンク (causal_link) を破壊しない
- Timeline の順序を逆転させない

---

### 2.2 Audit Log First Architecture

NWF ではデータベースの状態は以下の式で表現される。

State = Projection(Audit Log)

つまり、Concurrency Control の本質は  
**Audit Log に書き込まれるイベントの順序制御** である。

---

### 2.3 Snapshot Isolation

Transaction は開始時点の Snapshot を参照して処理を行う。
これにより読み取りと書き込みの並列性を確保する。

---

## 3. NWF Transaction Model (NWF-ACID)

NWF では ACID を以下のように再定義する。

### 3.1 Atomicity (原子性)
1つの Transaction ID に紐づく変更はすべて成功するか、すべて失敗する。

対象:
- Entity 更新
- Scene 更新
- Timeline 更新
- Audit Log 追記

---

### 3.2 Consistency (整合性)
Transaction 実行前後で以下を満たす必要がある。

- Schema Validation
- State Machine Validation
- Causal Dependency Check
- Timeline Order Check

---

### 3.3 Isolation (隔離性)
Isolation Level は以下を採用する。

Snapshot Isolation

Transaction は開始時点の世界状態を参照する。
他 Transaction の未コミット変更は見えない。

---

### 3.4 Durability (永続性)
以下の条件を満たした時点で Transaction は確定する。

- Audit Log に append 完了
- integrity_hash 更新完了
- HEAD version 更新完了

確定後は変更不可（Immutable History）。

---

## 4. Lock Hierarchy (階層型ロックモデル)

NWF ではリソースの粒度に応じた階層型ロックを採用する。

ロック階層は以下の通り。

### 4.1 Global Lock
システムアーキテクチャやスキーマ変更時に使用。

例:
- Schema Migration
- Timeline Structure Change

---

### 4.2 Timeline Lock
特定 Timeline の構造変更時に使用。

例:
- 正史 Timeline 編集
- IF ルート作成
- Timeline Merge

---

### 4.3 Scene / Thread Lock
Scene または Thread 編集時に使用。

例:
- 会話シーン編集
- 戦闘シーン編集
- 複数キャラクター相互作用

---

### 4.4 Entity Lock (最小粒度)
Character、Item、Location など単一 Entity 更新時に使用。

例:
- Character 状態変更
- Item 所持変更
- Location 状態変更

---

## 5. MVCC + Merge Model

NWF の同時実行制御は以下のハイブリッドモデルを採用する。

MVCC (Multi-Version Concurrency Control)
+
Git-like Merge Model

### 5.1 MVCC
各 Transaction は Snapshot Version を持つ。

読み取り:
- Snapshot Version を参照

書き込み:
- 新しい Version を生成
- Audit Log にイベントとして記録

---

### 5.2 Branch Model

AI や人間の編集は Branch 上で行う。

Branch 種類:

- main (正史)
- draft/*
- ai/*
- if/*
- hotfix/*

Branch → Merge → main Timeline

---

### 5.3 Merge Flow

1. Draft Branch 作成
2. 編集・Transaction 実行
3. Conflict Detection
4. Merge Request
5. Review (AI / Human)
6. Main Timeline へ Merge
7. Audit Log Commit

---

## 6. Transaction Flow

Transaction の標準フローを定義する。

### 6.1 Begin
- HEAD Version を取得
- Snapshot Version を生成
- Lock 取得

### 6.2 Execute
- Entity 更新
- Scene 更新
- State Machine Validation

### 6.3 Validate
- Conflict Detection
- Schema Validation
- Causal Dependency Check
- Timeline Order Check

### 6.4 Commit
- Audit Log Append
- integrity_hash 更新
- HEAD 更新
- Lock 解放

---

## 7. Conflict Detection

競合は以下の場合に発生する。

- 同一 Entity の同時更新
- 同一 Scene の同時編集
- Timeline Order Conflict
- Causal Dependency Conflict

Conflict 種類:

1. Write-Write Conflict
2. Timeline Conflict
3. Causal Conflict
4. Merge Conflict

---

## 8. Conflict Resolution

### 8.1 Automatic Resolve
以下は自動解決可能。

- 異なる属性更新
- 所持品追加
- フラグ追加
- メタデータ更新

---

### 8.2 Manual Review (HITL)

以下は人間または監督 AI による解決が必要。

- プロット矛盾
- キャラクター死亡/生存の衝突
- Timeline 分岐衝突
- 会話内容衝突

---

## 9. Audit Ordering Model

Audit Log は **Strict Ordering** を採用する。

### 9.1 Single Writer Principle
Audit Log への書き込みは単一プロセスが行う。
これにより順序保証を行う。

---

### 9.2 Transaction Block
関連するイベントは Transaction Block としてまとめる。

例:
- 戦闘イベント
- 会話イベント
- アイテム取得イベント

Transaction Block = 因果の最小単位

---

## 10. AI Collaboration Concurrency

AI 協働作業の並列編集モデルを定義する。

### 10.1 AI Draft Branch
AI は main Timeline を直接編集しない。
必ず Draft Branch で作業する。

---

### 10.2 Merge Governance
Merge は以下の順序で承認される。

AI Draft
→ Validation System
→ Supervisor AI
→ Human Review (必要な場合)
→ Main Timeline Merge

---

## 11. 用語定義

### Subject Lock
subject_id 単位での排他制御。

### Causal Linkage
イベント間の因果依存関係。

### Ghost State
Transaction 実行中のみ存在する未確定状態。

### Snapshot Version
Transaction 開始時点の世界状態。

### HEAD Version
現在の確定世界状態。

---

## 12. まとめ

NWF の Concurrency Control は以下を目的とする。

- 因果律の保護
- Timeline 整合性維持
- Audit Log 順序保証
- AI と Human の並列編集
- Branch / Merge ベースの世界線管理
- Event Sourcing との整合性維持

本仕様により、NWF は単なるデータベースではなく、
**複数のエージェントが安全に世界線を構築するための Story OS 同時実行制御基盤**
として機能する。

---

[EOF]