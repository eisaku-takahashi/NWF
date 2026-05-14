"""
Source: src/workflow/workflow_engine.py
Updated: 2026-04-11T05:40:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Project_Governance/NWF_Workflow_Engine_Spec_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
Docstring:
    Workflow Engine モジュール。
    NWF におけるワークフロー全体のオーケストレーションを担う。
    状態遷移、タスク実行、HITL連携、Event/Audit記録を統合管理する。
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional

from src.workflow.workflow_executor import WorkflowExecutor
from src.workflow.workflow_state_machine import WorkflowStateMachine
from src.workflow.workflow_context import WorkflowContext

# 外部依存（既存モジュール）
from src.hitl.hitl_manager import HITLManager
from src.core.event_manager import EventManager
from src.core.audit_log_manager import AuditLogManager

# JST 定義
JST = timezone(timedelta(hours=9))

__all__ = [
    "WorkflowEngine"
]


class WorkflowEngine:
    """
    WorkflowEngine クラス。

    概要:
        ワークフロー全体の制御を行う中核クラス。
        Task 実行、状態遷移、HITL連携を統合する。

    Args:
        hitl_manager (HITLManager): HITL 管理
        event_manager (EventManager): イベント管理
        audit_manager (AuditLogManager): 監査ログ管理

    Returns:
        None
    """

    def __init__(
        self,
        hitl_manager: HITLManager,
        event_manager: EventManager,
        audit_manager: AuditLogManager
    ) -> None:
        """
        初期化処理
        """
        self.hitl_manager = hitl_manager
        self.event_manager = event_manager
        self.audit_manager = audit_manager

        self.executor = WorkflowExecutor()
        self.state_machine = WorkflowStateMachine()

    def run(
        self,
        transaction_id: str,
        tasks: List[Dict[str, Any]]
    ) -> None:
        """
        ワークフロー実行エントリポイント

        Args:
            transaction_id (str): トランザクションID
            tasks (List[Dict]): タスク定義リスト

        Returns:
            None

        Raises:
            RuntimeError: 状態遷移エラー
        """

        # Context 初期化
        context = WorkflowContext(transaction_id=transaction_id)

        # 状態遷移: IDLE → READY → RUNNING
        self.state_machine.transition_to("READY")
        self.state_machine.transition_to("RUNNING")

        # イベント発火
        self.event_manager.emit("WORKFLOW_STARTED", {
            "transaction_id": transaction_id,
            "timestamp": datetime.now(JST).isoformat()
        })

        for task in tasks:
            try:
                # Task 実行
                result = self.executor.execute(task, context)

                # Audit 記録
                self.audit_manager.record({
                    "transaction_id": transaction_id,
                    "task": task,
                    "result": result["status"],
                    "timestamp": datetime.now(JST).isoformat()
                })

                # 状態分岐
                if result["status"] == "SUCCESS":
                    context.update(result.get("data"))

                    self.event_manager.emit("TASK_EXECUTED", {
                        "transaction_id": transaction_id,
                        "status": "SUCCESS"
                    })

                elif result["status"] == "SUSPEND":
                    # 状態遷移
                    self.state_machine.transition_to("SUSPEND")

                    self.event_manager.emit("WORKFLOW_SUSPENDED", {
                        "transaction_id": transaction_id
                    })

                    # HITL 連携
                    review_item = {
                        "transaction_id": transaction_id,
                        "context": context.snapshot()
                    }

                    self.hitl_manager.submit_for_review(
                        transaction_id,
                        review_item
                    )

                    # 承認待機（簡易実装）
                    decision = self.hitl_manager.wait_for_decision(transaction_id)

                    if decision == "APPROVED":
                        self.state_machine.transition_to("RUNNING")
                        continue
                    else:
                        self.state_machine.transition_to("FAILED")
                        break

                elif result["status"] == "FAILURE":
                    self.state_machine.transition_to("FAILED")
                    break

            except Exception as e:
                # 例外は致命的エラーとして扱う
                self.state_machine.transition_to("FAILED")

                self.audit_manager.record({
                    "transaction_id": transaction_id,
                    "error": str(e),
                    "level": "CRITICAL",
                    "timestamp": datetime.now(JST).isoformat()
                })

                break

        # 最終状態処理
        current_state = self.state_machine.get_state()

        if current_state == "RUNNING":
            self.state_machine.transition_to("COMPLETED")

            self.event_manager.emit("WORKFLOW_COMPLETED", {
                "transaction_id": transaction_id
            })

        elif current_state == "FAILED":
            self.event_manager.emit("WORKFLOW_FAILED", {
                "transaction_id": transaction_id
            })

        # Context GC
        context.clear()

        # IDLEへ戻す
        self.state_machine.transition_to("IDLE")


# [EOF]