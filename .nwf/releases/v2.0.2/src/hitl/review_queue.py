"""
Source: src/hitl/review_queue.py
Updated: 2026-04-10T12:26:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Project_Governance/NWF_HITL_Control_Protocol_v2.0.1.md
    - docs/spec/Core_Spec/NWF_Event_Model_v2.0.1.md
    - docs/spec/Kernel_Spec/NWF_Concurrency_Control_v2.0.1.md
Docstring:
    HITL Review Queue モジュール。
    transaction 単位でレビュー対象を管理し、依存関係と優先度に基づいて
    人間レビューの順序制御と状態管理を行う。
"""

from datetime import datetime, timezone, timedelta
from queue import PriorityQueue
from threading import Lock
from typing import Dict, List, Optional, Any

JST = timezone(timedelta(hours=9))

__all__ = [
    "ReviewQueue",
    "ReviewItem"
]

# 定数定義
STATUS_PENDING = "PENDING"
STATUS_UNDER_REVIEW = "UNDER_REVIEW"
STATUS_APPROVED = "APPROVED"
STATUS_REJECTED = "REJECTED"
STATUS_REVISE = "REVISE"

VALID_STATUSES = {
    STATUS_PENDING,
    STATUS_UNDER_REVIEW,
    STATUS_APPROVED,
    STATUS_REJECTED,
    STATUS_REVISE
}


class ReviewItem:
    """
    レビュー対象となる Transaction 単位のデータ構造。

    Attributes:
        transaction_id (str): トランザクションID
        parent_transaction_id (Optional[str]): 親トランザクション
        status (str): 現在の状態
        priority (int): 優先度（0〜5）
        spec_ids (List[str]): 含まれるSpec ID群
        diff_data (Dict[str, Any]): 差分情報
        submitted_at (str): ISO8601形式の提出時刻
        reviewer_id (Optional[str]): 担当レビューア
        dependencies (List[str]): 依存トランザクション
    """

    def __init__(
        self,
        transaction_id: str,
        spec_ids: List[str],
        diff_data: Dict[str, Any],
        priority: int = 0,
        parent_transaction_id: Optional[str] = None,
        dependencies: Optional[List[str]] = None
    ):
        self.transaction_id = transaction_id
        self.parent_transaction_id = parent_transaction_id
        self.status = STATUS_PENDING
        self.priority = priority
        self.spec_ids = spec_ids
        self.diff_data = diff_data
        self.submitted_at = datetime.now(JST).isoformat()
        self.reviewer_id = None
        self.dependencies = dependencies or []

    def is_ready(self, completed_transactions: List[str]) -> bool:
        """
        依存関係がすべて解決されているかを判定する。

        Args:
            completed_transactions (List[str]): 完了済み transaction_id リスト

        Returns:
            bool: レビュー可能かどうか
        """
        return all(dep in completed_transactions for dep in self.dependencies)

    def assign_reviewer(self, reviewer_id: str) -> None:
        """
        レビュワーを割り当て、状態を UNDER_REVIEW に変更する。

        Args:
            reviewer_id (str): レビュワーID
        """
        if self.status != STATUS_PENDING:
            raise ValueError("PENDING 状態でのみ reviewer を割り当て可能")

        self.reviewer_id = reviewer_id
        self.status = STATUS_UNDER_REVIEW

    def update_status(self, new_status: str) -> None:
        """
        状態遷移を実行する。

        Args:
            new_status (str): 遷移先状態

        Raises:
            ValueError: 不正な状態遷移
        """
        if new_status not in VALID_STATUSES:
            raise ValueError(f"無効な状態: {new_status}")

        if self.status == STATUS_PENDING and new_status != STATUS_UNDER_REVIEW:
            raise ValueError("PENDING → UNDER_REVIEW のみ許可")

        if self.status == STATUS_UNDER_REVIEW and new_status not in {
            STATUS_APPROVED,
            STATUS_REJECTED,
            STATUS_REVISE
        }:
            raise ValueError("UNDER_REVIEW からの遷移が不正")

        if self.status in {STATUS_APPROVED, STATUS_REJECTED}:
            raise ValueError("終端状態からの遷移は禁止")

        self.status = new_status


class ReviewQueue:
    """
    HITL レビューキュー管理クラス。

    PriorityQueue を使用し、優先度と依存関係を考慮した
    レビュー順序制御を行う。
    """

    def __init__(self):
        self._queue = PriorityQueue()
        self._items: Dict[str, ReviewItem] = {}
        self._lock = Lock()
        self._completed_transactions: List[str] = []

    def add_item(self, item: ReviewItem) -> None:
        """
        キューに ReviewItem を追加する。

        Args:
            item (ReviewItem): 追加対象
        """
        with self._lock:
            if item.transaction_id in self._items:
                raise ValueError("既に存在する transaction_id")

            self._items[item.transaction_id] = item
            self._queue.put((item.priority, item.transaction_id))

    def get_next_item(self) -> Optional[ReviewItem]:
        """
        次にレビュー可能なアイテムを取得する。

        Returns:
            Optional[ReviewItem]: レビュー可能なアイテム
        """
        with self._lock:
            temp_items = []

            while not self._queue.empty():
                priority, txn_id = self._queue.get()
                item = self._items[txn_id]

                if item.is_ready(self._completed_transactions):
                    return item
                else:
                    temp_items.append((priority, txn_id))

            # 未処理アイテムを戻す
            for entry in temp_items:
                self._queue.put(entry)

            return None

    def mark_completed(self, transaction_id: str) -> None:
        """
        トランザクションを完了として記録する。

        Args:
            transaction_id (str): 完了対象
        """
        with self._lock:
            if transaction_id not in self._completed_transactions:
                self._completed_transactions.append(transaction_id)

    def get_item(self, transaction_id: str) -> Optional[ReviewItem]:
        """
        指定IDの ReviewItem を取得する。

        Args:
            transaction_id (str): ID

        Returns:
            Optional[ReviewItem]
        """
        return self._items.get(transaction_id)

    def reset_to_pending(self, transaction_id: str) -> None:
        """
        Dependency 変更などにより PENDING に戻す。

        Args:
            transaction_id (str): 対象ID
        """
        with self._lock:
            item = self._items.get(transaction_id)
            if not item:
                raise ValueError("transaction_id が存在しない")

            item.status = STATUS_PENDING
            item.reviewer_id = None
            self._queue.put((item.priority, transaction_id))

    def release_reviewer(self, transaction_id: str) -> None:
        """
        reviewer を解除し、再度キューに戻す（Timeout対応）。

        Args:
            transaction_id (str): 対象ID
        """
        with self._lock:
            item = self._items.get(transaction_id)
            if not item:
                raise ValueError("transaction_id が存在しない")

            item.reviewer_id = None
            item.status = STATUS_PENDING
            self._queue.put((item.priority, transaction_id))


if __name__ == "__main__":
    pass

# [EOF]