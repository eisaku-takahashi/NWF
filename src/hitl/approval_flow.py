"""
Source: src/hitl/approval_flow.py
Updated: 2026-04-10T12:53:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Project_Governance/NWF_HITL_Control_Protocol_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
Docstring:
    Approval Flow モジュール。
    HITL における承認・却下・修正要求の状態遷移制御を担当する。
    状態遷移の厳密制御・バリデーション・Audit/Event 発火を行う。
"""

from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any

# JST 定義
JST = timezone(timedelta(hours=9))

__all__ = [
    "ApprovalFlow"
]


class ApprovalFlow:
    """
    HITL 承認フロー管理クラス。

    概要:
        transaction_id 単位での承認・却下・修正要求を制御する。
        状態遷移の正当性を保証し、Audit/Event 連携を行う。

    Args:
        event_manager: EventManager インスタンス
        audit_log_manager: AuditLogManager インスタンス

    Raises:
        ValueError: 不正な状態遷移・バリデーション違反
    """

    def __init__(self, event_manager, audit_log_manager):
        self.event_manager = event_manager
        self.audit_log_manager = audit_log_manager

    def approve(self, item: Dict[str, Any], reviewer_id: str, comment: str) -> Dict[str, Any]:
        """
        承認処理。

        Args:
            item: Queue Item
            reviewer_id: 承認者ID
            comment: コメント

        Returns:
            更新済み item

        Raises:
            ValueError: 状態遷移違反
        """
        self._validate_transition(item, reviewer_id)

        item["status"] = "APPROVED"
        item["reviewer_id"] = reviewer_id

        self._emit_event("HITL_APPROVED", item, reviewer_id, comment)
        self._write_audit(item, reviewer_id, "APPROVED", comment)

        return item

    def reject(self, item: Dict[str, Any], reviewer_id: str, reason: str) -> Dict[str, Any]:
        """
        却下処理。

        Args:
            item: Queue Item
            reviewer_id: 担当者
            reason: 却下理由

        Returns:
            更新済み item
        """
        self._validate_transition(item, reviewer_id)

        item["status"] = "REJECTED"
        item["reviewer_id"] = reviewer_id

        self._emit_event("HITL_REJECTED", item, reviewer_id, reason)
        self._write_audit(item, reviewer_id, "REJECTED", reason)

        return item

    def revise(self, item: Dict[str, Any], reviewer_id: str, feedback: str) -> Dict[str, Any]:
        """
        修正要求処理。

        Args:
            item: Queue Item
            reviewer_id: 担当者
            feedback: 修正指示

        Returns:
            更新済み item
        """
        self._validate_transition(item, reviewer_id)

        item["status"] = "REVISE"
        item["reviewer_id"] = reviewer_id

        self._emit_event("HITL_REVISE_REQUESTED", item, reviewer_id, feedback)
        self._write_audit(item, reviewer_id, "REVISE", feedback)

        return item

    def _validate_transition(self, item: Dict[str, Any], reviewer_id: str) -> None:
        """
        状態遷移バリデーション。

        Args:
            item: Queue Item
            reviewer_id: 担当者

        Raises:
            ValueError: 不正な状態遷移
        """
        status = item.get("status")

        # UNDER_REVIEW 状態のみ許可
        if status != "UNDER_REVIEW":
            raise ValueError(f"Invalid transition from {status}")

        # reviewer 未設定チェック
        if not reviewer_id:
            raise ValueError("reviewer_id is required")

    def _emit_event(self, event_type: str, item: Dict[str, Any], reviewer_id: str, comment: str) -> None:
        """
        Event 発火。

        Args:
            event_type: イベント種別
            item: Queue Item
            reviewer_id: 担当者
            comment: コメント
        """
        payload = {
            "transaction_id": item["transaction_id"],
            "reviewer_id": reviewer_id,
            "decision": event_type,
            "comment": comment,
            "timestamp": datetime.now(JST).isoformat()
        }

        self.event_manager.emit(event_type, payload)

    def _write_audit(self, item: Dict[str, Any], reviewer_id: str, decision: str, comment: str) -> None:
        """
        Audit ログ記録。

        Args:
            item: Queue Item
            reviewer_id: 担当者
            decision: 判定
            comment: コメント
        """
        audit_payload = {
            "event_type": "HITL_DECISION_MADE",
            "transaction_id": item["transaction_id"],
            "actor": {
                "id": reviewer_id,
                "role": "EDITOR"
            },
            "payload": {
                "decision": decision,
                "comment": comment
            },
            "timestamp": datetime.now(JST).isoformat()
        }

        self.audit_log_manager.record(audit_payload)


if __name__ == "__main__":
    pass

# [EOF]