Source: docs/spec/Project_Governance/NWF_Workflow_Engine_Spec_v2.0.1.md
Updated: 2026-04-11T04:20:00+09:00
PIC: Engineer / ChatGPT

# NWF Workflow Engine Specification v2.0.1

---

## 1. 概要

本ドキュメントは、NWF v2.0.1 における Workflow Engine の標準仕様を定義する。

Workflow Engine は以下の責務を担う：

- Spec / Engine / AI / HITL の統合制御
- 実行順序・依存関係の管理
- 状態遷移の厳密制御
- 実行時データの一貫性保証
- 異常時の安全停止およびHITL連携

本仕様は Phase 2.4 の実装対象である以下モジュールに適用される：

- src/workflow/workflow_engine.py
- src/workflow/workflow_executor.py
- src/workflow/workflow_state_machine.py
- src/workflow/workflow_context.py

---

## 2. 核心哲学

### 2.1 因果律（Causality）

すべての処理は transaction_id を単位とする因果律に従う。

- 出力は必ず次の入力に連鎖する
- 非決定的な分岐は禁止

---

### 2.2 非矛盾性（Consistency）

- Validation System による検証を必須とする
- 矛盾検知時は即時 SUSPEND

---

### 2.3 疎結合（Loose Coupling）

- Engine 間の直接呼び出しは禁止
- EventManager を介した通信を強制

---

## 3. 用語定義

| 用語 | 定義 |
|------|------|
| Workflow | 一連の Task 実行フロー |
| Task | 最小実行単位（Engine メソッド） |
| Step | 複数 Task の論理単位 |
| Transaction | 因果律の最小単位 |
| Context | 実行時共有データ |
| ExecutionResult | 実行結果オブジェクト |

---

## 4. データモデル

### 4.1 基本型

- workflow_id: str（UUID）
- transaction_id: str（Entity ID 準拠）
- state_payload: Dict[str, Any]

---

### 4.2 WorkflowContext 構造

context_data:

- transaction_id: str
- global_vars: Dict[str, NWFObject]
- local_vars: Dict[str, Any]
- metadata: Dict[str, Any]
- created_at: datetime (JST)
- updated_at: datetime (JST)

---

### 4.3 ExecutionResult

- status: SUCCESS | FAILURE | SUSPEND
- data: Optional[NWFObject]
- error_code: Optional[str]
- message: Optional[str]
- transaction_id: str
- timestamp: datetime (JST)

---

## 5. 状態遷移モデル

### 5.1 状態一覧

- IDLE
- READY
- RUNNING
- SUSPEND
- COMPLETED
- FAILED
- ABORTED

---

### 5.2 許可遷移

- IDLE → READY
- READY → RUNNING
- RUNNING → COMPLETED
- RUNNING → FAILED
- RUNNING → SUSPEND
- SUSPEND → RUNNING
- SUSPEND → ABORTED
- COMPLETED → IDLE
- FAILED → IDLE
- ABORTED → IDLE

---

### 5.3 禁止遷移

- READY → COMPLETED
- COMPLETED → 他状態
- FAILED → 他状態

---

### 5.4 SUSPEND 条件

- Validation エラー
- AI 信頼度低下
- Recoverable Error
- HITL 要求

---

## 6. モジュール責務

### 6.1 WorkflowEngine

責務：

- 全体オーケストレーション
- Task スケジューリング
- 状態遷移制御
- HITL 連携
- Event 発火
- Audit 記録

依存：

- WorkflowExecutor
- WorkflowStateMachine
- WorkflowContext
- HITLManager
- EventManager
- AuditLogManager

---

### 6.2 WorkflowExecutor

責務：

- Engine 呼び出し
- 型変換（dict ↔ NWFObject）
- ExecutionResult 生成
- エラーハンドリング

禁止：

- 状態遷移の直接操作

---

### 6.3 WorkflowStateMachine

責務：

- 状態管理
- 遷移バリデーション
- atomic 状態更新

仕様：

- 不正遷移時は例外発生
- 全遷移は単一API経由

---

### 6.4 WorkflowContext

責務：

- transaction単位のデータ保持
- スコープ管理（global/local）
- immutable データ保護
- timestamp 更新

制約：

- Engine 間直接共有禁止
- Context 経由のみ許可

---

## 7. 実行フロー

1. WorkflowEngine 初期化
2. transaction_id 発行
3. Context 初期化
4. 状態 → READY
5. 状態 → RUNNING
6. Task 実行ループ

   - Executor 実行
   - Validation
   - Event 発火
   - Context 更新

7. 分岐：

   - SUCCESS → 次 Task
   - FAILURE → FAILED
   - SUSPEND → HITL

8. HITL：

   - submit_for_review()
   - APPROVED → RUNNING
   - REJECTED → FAILED

9. 全 Task 完了：

   - COMPLETED
   - finalize

---

## 8. HITL 連携

### 8.1 呼び出し条件

- SUSPEND 時のみ

---

### 8.2 フロー

1. Context snapshot
2. ReviewItem 作成
3. HITLManager.submit_for_review()
4. 状態待機
5. 結果反映

---

## 9. Event / Audit

### 9.1 Event

- WORKFLOW_STARTED
- WORKFLOW_COMPLETED
- WORKFLOW_FAILED
- WORKFLOW_SUSPENDED
- TASK_EXECUTED

---

### 9.2 Audit

必須記録：

- transaction_id
- state
- task
- timestamp
- result

---

## 10. エラーモデル

### 10.1 Level 1

- Retryable
- Executor 内処理

---

### 10.2 Level 2

- Logic Error
- SUSPEND → HITL

---

### 10.3 Level 3

- Fatal
- FAILED

---

## 11. 並列実行（拡張仕様）

### 11.1 基本方針

- デフォルトは逐次実行
- 並列は依存関係がない場合のみ許可

---

### 11.2 Dependency

- dependency_resolver に委譲
- DAG 構造を前提

---

## 12. Context 管理

### 12.1 更新

- 各 Task 実行後更新

---

### 12.2 GC（補完仕様）

- COMPLETED / FAILED 時に解放
- 長期保持は禁止

---

## 13. 制約

- 未承認 Spec 実行禁止
- Engine 直接呼び出し禁止
- transaction_id 必須
- Audit 必須
- Event 必須

---

## 14. 実装補完（不足仕様の補填）

本仕様では以下を補完する：

- ExecutionResult の標準化
- Context GC ルール
- 並列実行の条件定義
- HITL 復帰フローの明確化
- 状態遷移の完全定義

---

## 15. まとめ

Workflow Engine は以下を保証する：

- 因果律の維持
- 非矛盾性の担保
- 実行フローの統合
- HITL による最終判断
- 長期運用可能な設計

本仕様は Phase 2.4 実装の唯一の基準とする。

---

[EOF]