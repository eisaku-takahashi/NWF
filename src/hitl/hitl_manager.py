"""
Source: src/hitl/hitl_manager.py
Updated: 2026-04-10T13:14:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Project_Governance/NWF_HITL_Control_Protocol_v2.0.1.md
Docstring:
    HITL Manager モジュール。
    ReviewQueue・ApprovalFlow・Core System を統合し、
    HITL におけるトランザクション管理・状態制御・外部連携を担う。
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional

JST = timezone(timedelta(hours=9))

__all__ = [
    "HITLManager"
]


class HITLManager:
    """
    HITL Manager クラス。

    Queue管理・状態遷移・Core連携を統括する。
    """

    def __init__(self, review_queue, approval_flow, audit_logger, event_manager, spec_registry):
        """
        初期化。

        Args:
            review_queue: ReviewQueue インスタンス
            approval_flow: ApprovalFlow インスタンス
            audit_logger: AuditLogger インスタンス
            event_manager: EventManager インスタンス
            spec_registry: SpecRegistry インスタンス
        """
        self.review_queue = review_queue
        self.approval_flow = approval_flow
        self.audit_logger = audit_logger
        self.event_manager = event_manager
        self.spec_registry = spec_registry

    def submit_for_review(self, transaction_id: str, spec_data: Dict[str, Any]) -> None:
        """
        SpecLoader から呼び出され、レビューキューへ登録する。

        Args:
            transaction_id: トランザクションID
            spec_data: スペックデータ
        """
        self.review_queue.enqueue(transaction_id, spec_data)

        self.event_manager.emit({
            "event_type": "HITL_SUBMITTED",
            "transaction_id": transaction_id,
            "timestamp": datetime.now(JST).isoformat()
        })

    def process_decision(self, transaction_id: str, decision_data: Dict[str, Any]) -> None:
        """
        レビュー結果を処理する。

        Args:
            transaction_id: トランザクションID
            decision_data: 判定データ
        """
        decision = decision_data.get("decision")

        if decision == "APPROVED":
            self.approval_flow.approve(
                transaction_id,
                decision_data["reviewer_id"],
                decision_data.get("comment", "")
            )
            self.finalize_transaction(transaction_id)

        elif decision == "REJECTED":
            self.approval_flow.reject(
                transaction_id,
                decision_data["reviewer_id"],
                decision_data.get("reason", "")
            )

        elif decision == "REVISE":
            self.approval_flow.revise(
                transaction_id,
                decision_data["reviewer_id"],
                decision_data.get("feedback", "")
            )

        else:
            raise ValueError("Invalid decision")

        # Audit 記録
        self.audit_logger.log({
            "event_type": "HITL_DECISION_MADE",
            "transaction_id": transaction_id,
            "actor": {
                "id": decision_data["reviewer_id"]
            },
            "payload": decision_data,
            "timestamp": datetime.now(JST).isoformat()
        })

    def finalize_transaction(self, transaction_id: str) -> None:
        """
        承認されたトランザクションを確定する。

        Args:
            transaction_id: トランザクションID
        """
        # SpecRegistry にロック命令
        self.spec_registry.unlock_and_lock_new_version(transaction_id)

        self.event_manager.emit({
            "event_type": "HITL_APPROVED",
            "transaction_id": transaction_id,
            "timestamp": datetime.now(JST).isoformat()
        })

    def handle_dependency_invalidated(self, transaction_id: str) -> None:
        """
        依存関係が破壊された場合の処理。

        Args:
            transaction_id: トランザクションID
        """
        item = self.review_queue.get(transaction_id)
        item["status"] = "PENDING"
        item["reviewer_id"] = None

        self.review_queue.requeue(item)

    def handle_reviewer_timeout(self, transaction_id: str) -> None:
        """
        Reviewer タイムアウト処理。

        Args:
            transaction_id: トランザクションID
        """
        item = self.review_queue.get(transaction_id)
        item["reviewer_id"] = None
        item["status"] = "PENDING"

        self.review_queue.requeue(item)

    def recover_transaction(self, transaction_id: str) -> None:
        """
        異常時のロールバック処理。

        Args:
            transaction_id: トランザクションID
        """
        item = self.review_queue.get(transaction_id)
        item["status"] = "UNDER_REVIEW"

        self.review_queue.update(item)


if __name__ == "__main__":
    # 開発用エントリポイント（本番では使用しない）
    pass

# [EOF]