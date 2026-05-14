Source: docs/spec/Project_Governance/NWF_HITL_Control_Protocol_v2.0.1.md
Updated: 2026-04-10T11:49:00+09:00
PIC: Engineer / ChatGPT

# NWF HITL Control Protocol v2.0.1

---

## 1. 概要

本仕様は、NWF v2.0.1 における Phase 2.3（Human-In-The-Loop: HITL）の制御プロトコルおよび実装契約を定義する。

HITL は SpecLoader による構文的正当性（Mechanical Truth）を前提とし、人間による意味論的正当性（Semantic Truth）を付与する「信頼のゲートキーパー」として機能する。

本仕様は以下を統合する：

- 責務境界（Authority Boundary）
- データ構造（Queue / Transaction）
- 状態遷移（State Machine）
- 実装インターフェース（I/F Contract）
- Audit / Event 連携
- 例外処理

---

## 2. HITL の責務境界（Authority Boundary）

### 2.1 権限レベル

- Level 2: Gatekeeper（採用）

### 2.2 定義

- SpecValidator 通過後のみ HITL 対象とする
- 承認前 Spec は以下を禁止する
  - SpecRegistry Lock
  - Engine 実行
- Validator 違反の Override は禁止

### 2.3 Truth Hierarchy

1. Mechanical Truth（SpecValidator）
2. Semantic Truth（HITL）
3. Execution Truth（Engine）

---

## 3. レビュー対象の粒度

### 3.1 単位

- transaction_id 単位
- diff ベース

### 3.2 原則

- Transaction は因果律の最小単位
- atomic レビューを必須とする

### 3.3 REVISE フロー

- 差分 + コメントを返却
- 新規 transaction_id を発行
- parent_transaction_id に旧 ID を記録

---

## 4. Queue データ構造（review_queue）

### 4.1 Queue Item

- transaction_id: string
- parent_transaction_id: string または null
- status: string（PENDING / UNDER_REVIEW / APPROVED / REJECTED / REVISE）
- priority: integer（0〜5）
- spec_ids: list[string]
- diff_data: object
- submitted_at: datetime（JST）
- reviewer_id: string または null
- dependencies: list[string]

### 4.2 Queue 仕様

- PriorityQueue を採用
- dependency を優先
- 同一 transaction_id は排他制御

### 4.3 並行制御

- 1 transaction = 1 reviewer
- 状態変更は atomic

---

## 5. 状態モデル（State Machine）

### 5.1 状態

- PENDING
- UNDER_REVIEW
- APPROVED
- REJECTED
- REVISE

### 5.2 遷移

- PENDING → UNDER_REVIEW
- UNDER_REVIEW → APPROVED
- UNDER_REVIEW → REJECTED
- UNDER_REVIEW → REVISE

### 5.3 禁止遷移

- PENDING → APPROVED
- APPROVED → 他状態
- REJECTED → 他状態

---

## 6. Approval Flow（approval_flow）

### 6.1 API

- approve(transaction_id, reviewer_id, comment)
- reject(transaction_id, reviewer_id, reason)
- revise(transaction_id, reviewer_id, feedback)

### 6.2 バリデーション

- reviewer_id は HumanActor であること
- reviewer_id != author_id（Admin除く）
- authority_level チェック
- 状態が UNDER_REVIEW であること

### 6.3 出力

- 状態更新
- Event 発火
- Audit 記録

---

## 7. HITL Manager（hitl_manager）

### 7.1 責務

- Queue 管理
- 状態制御
- Core 連携

### 7.2 インターフェース

- submit_for_review(transaction_id, spec_data)
- process_decision(transaction_id, decision_data)
- finalize_transaction(transaction_id)

### 7.3 Core 連携

- SpecLoader → submit_for_review
- EventManager → イベント送信
- AuditLogManager → ログ記録
- SpecRegistry → finalize 時に Lock

### 7.4 トランザクション

- HITL 判定を Kernel Transaction として扱う
- 異常時は UNDER_REVIEW にロールバック

---

## 8. Versioning / Branching

### 8.1 状態対応

| 状態 | metadata.status | version |
|------|----------------|---------|
| PENDING | unverified | draft |
| APPROVED | verified | released |
| REVISE | rejected | branch |

### 8.2 Branch

- REVISE 時に分岐
- main へ影響禁止
- APPROVED で merge

---

## 9. Audit / Event 連携

### 9.1 Event

- HITL_SUBMITTED
- HITL_UNDER_REVIEW
- HITL_APPROVED
- HITL_REJECTED
- HITL_REVISE_REQUESTED

### 9.2 Payload

- transaction_id: string
- reviewer_id: string
- decision: string
- comment: string
- timestamp: datetime

---

## 10. Execution Pipeline 統合

### 10.1 位置

- Validation_System 後
- Engine 実行前

### 10.2 制御

- APPROVED のみ実行可能

---

## 11. Staging モデル

### 11.1 定義

- 承認前 Spec の仮実行環境

### 11.2 制約

- 書き込み禁止
- Chronicle 不干渉

---

## 12. 意味論的正当性

### 12.1 定義

- 実行結果を人間が予見し承認した Spec

### 12.2 レイヤー

- 物語的妥当性
- シミュレーション妥当性
- メタデータ整合性

---

## 13. レビュー観点

### 13.1 技術

- ID競合
- Pipeline整合

### 13.2 物語

- Narrative
- Beat

### 13.3 整合性

- Thread
- Foreshadowing

---

## 14. 例外処理

### 14.1 Dependency Invalidated

- 状態を PENDING に戻す
- 再レビュー要求

### 14.2 Reviewer Timeout

- reviewer_id を解除
- Queue に戻す

---

## 15. Metadata 更新

### 15.1 タイミング

- APPROVED 時

### 15.2 内容

- status を trusted に更新

### 15.3 単位

- transaction 単位で一括更新

---

## 16. Human Actor

### 16.1 属性

- reviewer_id: string
- role: AUTHOR / EDITOR / ADMIN
- authority_level: integer

---

## 17. 制約

- Validator 未通過は対象外
- Override 禁止
- 未承認実行禁止

---

## 18. まとめ

本仕様により：

- 構文的正当性（Validator）
- 意味論的正当性（HITL）
- 実行結果（Engine）

を厳密に分離・統合し、

NWF における因果律と物語的整合性を保証する。

---

[EOF]