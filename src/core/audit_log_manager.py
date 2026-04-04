"""
Source: src/core/audit_log_manager.py
Updated: 2026-04-04T22:40:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Kernel_Spec/NWF_Kernel_Audit_System_Spec_v2.0.1.md
    - docs/spec/Data_Spec/NWF_Data_Model_v2.0.1.md
    - docs/spec/Execution_Spec/NWF_Execution_Pipeline_v2.0.1.md
    - src/core/audit_logger.py
    - src/core/metadata_manager.py
    - src/core/version_manager.py
Docstring:
    AuditLogManager モジュール。
    NWF システムにおける全イベントを構造化ログとして記録し、
    因果関係（Provenance）を保証する高レベル監査管理コンポーネント。
"""

# ---------------------------------------------------------
# import
# ---------------------------------------------------------
import os
import json
import hashlib
import uuid
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Dict, Any

# ---------------------------------------------------------
# 定数 / 設定
# ---------------------------------------------------------
JST = timezone(timedelta(hours=9))

DEFAULT_LOG_DIR = "logs/audit"

# ---------------------------------------------------------
# 公開インターフェース
# ---------------------------------------------------------
__all__ = [
    "AuditLogManager",
]

# ---------------------------------------------------------
# Utility Functions
# ---------------------------------------------------------
def _now_iso() -> str:
    """
    現在時刻を ISO8601 (JST) で取得
    """
    return datetime.now(JST).isoformat()


def _generate_event_id() -> str:
    """
    イベントIDを生成（UUIDベース）
    """
    return f"LOG-{uuid.uuid4().hex}"


def _generate_transaction_id() -> str:
    """
    トランザクションIDを生成
    """
    return f"TXN-{uuid.uuid4().hex}"


def _compute_hash(data: str) -> str:
    """
    データのSHA256ハッシュを生成
    """
    return "sha256:" + hashlib.sha256(data.encode("utf-8")).hexdigest()


# ---------------------------------------------------------
# Classes
# ---------------------------------------------------------
class AuditLogManager:
    """
    AuditLogManager クラス

    NWFシステムの全イベントをJSONL形式で記録し、
    トランザクション単位で因果関係を保証する。

    Attributes:
        log_dir (str): ログ保存ディレクトリ
        current_transaction (Optional[str]): 現在のトランザクションID
    """

    def __init__(self, log_dir: str = DEFAULT_LOG_DIR):
        """
        初期化

        Args:
            log_dir (str): ログ保存ディレクトリ
        """
        self.log_dir = log_dir
        self.current_transaction: Optional[str] = None

        # ディレクトリが存在しない場合は作成
        os.makedirs(self.log_dir, exist_ok=True)

    # -----------------------------------------------------
    # Transaction Management
    # -----------------------------------------------------
    def begin_transaction(self, actor_id: str) -> str:
        """
        新規トランザクション開始

        Args:
            actor_id (str): 操作主体ID

        Returns:
            str: transaction_id

        Raises:
            ValueError: actor_id未指定
        """
        if not actor_id:
            raise ValueError("actor_id is required")

        txn_id = _generate_transaction_id()
        self.current_transaction = txn_id

        # トランザクション開始ログ
        self.record_event(
            event_type="TRANSACTION_BEGIN",
            subject_id=None,
            actor_id=actor_id,
            payload={"message": "Transaction started"},
        )

        return txn_id

    # -----------------------------------------------------
    # Core Logging
    # -----------------------------------------------------
    def record_event(
        self,
        event_type: str,
        subject_id: Optional[str],
        actor_id: str,
        payload: Optional[Dict[str, Any]] = None,
        status: str = "SUCCESS",
        spec_id: Optional[str] = None,
    ) -> None:
        """
        イベントログ記録

        Args:
            event_type (str): イベント種別
            subject_id (str): 対象Entity ID
            actor_id (str): 操作主体
            payload (dict): 追加情報
            status (str): SUCCESS / FAILED
            spec_id (str): 関連Spec ID
        """

        if not actor_id:
            raise ValueError("actor_id is required")

        if not self.current_transaction:
            raise RuntimeError("Transaction not started")

        event = {
            "event_id": _generate_event_id(),
            "timestamp": _now_iso(),
            "transaction_id": self.current_transaction,
            "actor_id": actor_id,
            "event_type": event_type,
            "subject_id": subject_id,
            "spec_id": spec_id,
            "status": status,
            "payload": payload or {},
        }

        # integrity hash 計算
        event_str = json.dumps(event, sort_keys=True)
        event["integrity_hash"] = _compute_hash(event_str)

        self._append_log(event)

    def record_error(
        self,
        actor_id: str,
        error_code: str,
        message: str,
        stack_trace: Optional[str] = None,
    ) -> None:
        """
        エラーログ記録

        Args:
            actor_id (str): 操作主体
            error_code (str): エラーコード
            message (str): エラーメッセージ
            stack_trace (str): スタックトレース
        """
        payload = {
            "error_code": error_code,
            "message": message,
            "stack_trace": stack_trace,
        }

        self.record_event(
            event_type="ERROR",
            subject_id=None,
            actor_id=actor_id,
            payload=payload,
            status="FAILED",
        )

    # -----------------------------------------------------
    # Retrieval
    # -----------------------------------------------------
    def get_logs(
        self,
        transaction_id: Optional[str] = None,
        subject_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        ログ取得

        Args:
            transaction_id (str): トランザクションID
            subject_id (str): Entity ID

        Returns:
            list: ログ一覧
        """
        logs = []

        for file in os.listdir(self.log_dir):
            path = os.path.join(self.log_dir, file)
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    entry = json.loads(line.strip())

                    if transaction_id and entry["transaction_id"] != transaction_id:
                        continue
                    if subject_id and entry["subject_id"] != subject_id:
                        continue

                    logs.append(entry)

        return logs

    def get_transaction_trace(self, transaction_id: str) -> List[Dict[str, Any]]:
        """
        トランザクション単位のログ取得

        Args:
            transaction_id (str)

        Returns:
            list
        """
        return self.get_logs(transaction_id=transaction_id)

    # -----------------------------------------------------
    # Integrity
    # -----------------------------------------------------
    def verify_integrity(self) -> bool:
        """
        ログの整合性チェック

        Returns:
            bool: Trueなら正常
        """
        for file in os.listdir(self.log_dir):
            path = os.path.join(self.log_dir, file)
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    entry = json.loads(line.strip())

                    original_hash = entry.get("integrity_hash")
                    temp = dict(entry)
                    temp.pop("integrity_hash", None)

                    recalculated = _compute_hash(
                        json.dumps(temp, sort_keys=True)
                    )

                    if original_hash != recalculated:
                        return False

        return True

    # -----------------------------------------------------
    # Export
    # -----------------------------------------------------
    def export_logs(self, format: str = "json") -> str:
        """
        ログエクスポート

        Args:
            format (str): json / md

        Returns:
            str: 出力文字列
        """
        logs = self.get_logs()

        if format == "json":
            return json.dumps(logs, indent=2, ensure_ascii=False)

        elif format == "md":
            lines = ["# Audit Log Export\n"]
            for log in logs:
                lines.append(f"- {log['timestamp']} | {log['event_type']} | {log['status']}")
            return "\n".join(lines)

        else:
            raise ValueError("Unsupported format")

    # -----------------------------------------------------
    # Internal
    # -----------------------------------------------------
    def _append_log(self, event: Dict[str, Any]) -> None:
        """
        ログ追記（Append Only）

        Args:
            event (dict)
        """
        date_str = datetime.now(JST).strftime("%Y-%m-%d")
        file_path = os.path.join(self.log_dir, f"{date_str}.jsonl")

        # Append Only で書き込み
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")


# ---------------------------------------------------------
# Main Guard
# ---------------------------------------------------------
if __name__ == "__main__":
    manager = AuditLogManager()

    txn = manager.begin_transaction(actor_id="USR-TEST")

    manager.record_event(
        event_type="TEST_EVENT",
        subject_id="TEST-001",
        actor_id="USR-TEST",
        payload={"message": "test"},
    )

    print(manager.get_transaction_trace(txn))

# [EOF]