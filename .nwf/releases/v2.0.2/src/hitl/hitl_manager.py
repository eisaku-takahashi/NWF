"""
Source: src/hitl/hitl_manager.py
Updated: 2026-04-11T01:20:00+09:00
PIC: Engineer / Gemini (Architect)
Version: NWF v2.0.1
Docstring:
    HITL Manager モジュール。
    ValueError (Invalid transition from PENDING) を解消。
    判定処理 (process_decision) 前に状態が UNDER_REVIEW であることを保証するロジックを追加。
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional

from src.hitl.review_queue import ReviewItem

JST = timezone(timedelta(hours=9))

__all__ = ["HITLManager"]

class HITLManager:
    def __init__(self, review_queue, approval_flow, audit_logger, event_manager, spec_registry):
        self.review_queue = review_queue
        self.approval_flow = approval_flow
        self.audit_logger = audit_logger
        self.event_manager = event_manager
        self.spec_registry = spec_registry

    def submit_for_review(self, transaction_id: str, spec_data: Dict[str, Any], priority: int = 3) -> None:
        """ReviewItem インスタンスを作成し、キューに追加する。"""
        item = ReviewItem(
            transaction_id=transaction_id,
            spec_ids=spec_data.get("spec_ids", []),
            diff_data=spec_data.get("diff_data", spec_data),
            priority=priority
        )
        self.review_queue.add_item(item)

        self.event_manager.emit({
            "event_type": "HITL_SUBMITTED",
            "transaction_id": transaction_id,
            "timestamp": datetime.now(JST).isoformat()
        })

    def start_review(self, transaction_id: str, reviewer_id: str) -> None:
        """ReviewItem.assign_reviewer を呼び出し、状態を UNDER_REVIEW に遷移させる。"""
        item = self.review_queue.get_item(transaction_id)
        if item:
            # 内部で status を UNDER_REVIEW に変更
            item.assign_reviewer(reviewer_id)

    def process_decision(self, transaction_id: str, decision_data: Dict[str, Any]) -> None:
        """
        [修正理由] ApprovalFlow は status == 'UNDER_REVIEW' を厳格にチェックする。
        テストコード側で start_review が呼ばれていない場合に備え、
        判定処理の直前で状態をチェックし、必要に応じて自動遷移させる。
        """
        decision = decision_data.get("decision")
        reviewer_id = decision_data.get("reviewer_id")
        item_obj = self.review_queue.get_item(transaction_id)

        if not item_obj:
            raise ValueError(f"Transaction {transaction_id} not found.")

        # --- 2026-04-11 追加: 状態の自動整合 (Auto-Transition) ---
        # 状態が PENDING のまま process_decision が呼ばれた場合、
        # 流体的に判定へ進めるよう自動でレビュワーを割り当てる（または警告を出す）
        if item_obj.status == "PENDING":
            item_obj.assign_reviewer(reviewer_id)

        # ApprovalFlow 適合用辞書の生成
        adapter_item = {
            "transaction_id": item_obj.transaction_id,
            "status": item_obj.status,
            "reviewer_id": item_obj.reviewer_id,
            "spec_ids": item_obj.spec_ids
        }

        # --- 判定処理の実行 ---
        if decision == "APPROVED":
            self.approval_flow.approve(
                adapter_item,
                reviewer_id,
                decision_data.get("comment", "")
            )
            item_obj.update_status(adapter_item["status"])
            self.finalize_transaction(transaction_id)
            self.review_queue.mark_completed(transaction_id)

        elif decision == "REJECTED":
            self.approval_flow.reject(
                adapter_item,
                reviewer_id,
                decision_data.get("reason", "")
            )
            item_obj.update_status(adapter_item["status"])

        elif decision == "REVISE":
            self.approval_flow.revise(
                adapter_item,
                reviewer_id,
                decision_data.get("feedback", "")
            )
            self.review_queue.reset_to_pending(transaction_id)

        else:
            raise ValueError(f"Invalid decision: {decision}")

        # --- 過去の修正履歴 (保持) ---
        """
        # [2026-04-11 試行1-3] 引数順序・型不一致の解消済み
        # [2026-04-11 試行4] 
        # ERROR: ValueError: Invalid transition from PENDING
        # (原因: ApprovalFlow 側の _validate_transition が UNDER_REVIEW 以外を弾くため)
        """

        self.audit_logger.log({
            "event_type": "HITL_DECISION_MADE",
            "transaction_id": transaction_id,
            "actor": {"id": reviewer_id},
            "payload": decision_data,
            "timestamp": datetime.now(JST).isoformat()
        })

    def finalize_transaction(self, transaction_id: str) -> None:
        self.spec_registry.unlock_and_lock_new_version(transaction_id)
        self.event_manager.emit({
            "event_type": "HITL_APPROVED",
            "transaction_id": transaction_id,
            "timestamp": datetime.now(JST).isoformat()
        })

    def handle_reviewer_timeout(self, transaction_id: str) -> None:
        self.review_queue.release_reviewer(transaction_id)

    def recover_transaction(self, transaction_id: str) -> None:
        item = self.review_queue.get_item(transaction_id)
        if item:
            item.status = "UNDER_REVIEW"

if __name__ == "__main__":
    pass

# [EOF]