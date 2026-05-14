"""
Source: src/core/audit_log_manager.py
Updated: 2026-04-07T07:24:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Kernel_Spec/NWF_Kernel_Audit_System_Spec_v2.0.1.md
    - docs/spec/Data_Spec/NWF_Data_Model_v2.0.1.md
    - docs/spec/Execution_Spec/NWF_Execution_Pipeline_v2.0.1.md
    - docs/spec/Kernel_Spec/NWF_Concurrency_Control_v2.0.1.md
    - src/core/metadata_manager.py
    - src/core/version_manager.py
Docstring:
    AuditLogManager モジュール。
    NWFシステムにおける全イベントをハッシュチェーン構造で記録する
    Append-Only 監査ログ管理コンポーネント。
    因果律（Causality）を物理的に保証する。
"""

# ---------------------------------------------------------
# import
# ---------------------------------------------------------
import os
import json
import hashlib
import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, List

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
    イベントID生成（UUIDベース）
    """
    return f"EVT-{uuid.uuid4().hex}"


def _compute_hash(data: str) -> str:
    """
    SHA256ハッシュ生成
    """
    return "sha256:" + hashlib.sha256(data.encode("utf-8")).hexdigest()


def _serialize_for_hash(entry: Dict[str, Any]) -> str:
    """
    ハッシュ計算用シリアライズ
    integrity_hash を除外して順序固定でJSON化
    """
    temp = dict(entry)
    temp.pop("integrity_hash", None)
    return json.dumps(temp, sort_keys=True, ensure_ascii=False)


# ---------------------------------------------------------
# Classes
# ---------------------------------------------------------
class AuditLogManager:
    """
    AuditLogManager クラス

    Append-Only / ハッシュチェーン構造により、
    監査ログの改ざん耐性と因果律を保証する。

    Attributes:
        log_dir (str): ログディレクトリ
        last_hash (str): 直前イベントのハッシュ
    """

    def __init__(self, log_dir: str = DEFAULT_LOG_DIR):
        """
        初期化

        Args:
            log_dir (str): ログ保存ディレクトリ
        """
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)

        # 最新ハッシュのロード
        self.last_hash = self._load_last_hash()

    # -----------------------------------------------------
    # Core Logging
    # -----------------------------------------------------
    def record_event(
        self,
        event_type: str,
        actor_id: str,
        target_id: str,
        payload: Dict[str, Any],
        transaction_id: str,
    ) -> str:
        """
        イベント記録（因果律保証）

        Args:
            event_type (str): イベント種別
            actor_id (str): 操作主体
            target_id (str): 対象ID
            payload (dict): 追加情報
            transaction_id (str): トランザクションID

        Returns:
            str: event_id

        Raises:
            ValueError: 必須パラメータ不足
            RuntimeError: 書き込み失敗
        """

        if not actor_id:
            raise ValueError("actor_id is required")
        if not target_id:
            raise ValueError("target_id is required")
        if not transaction_id:
            raise ValueError("transaction_id is required")

        # -------------------------------------------------
        # 1. イベント構造生成
        # -------------------------------------------------
        event = {
            "event_id": _generate_event_id(),
            "timestamp": _now_iso(),
            "transaction_id": transaction_id,
            "actor_id": actor_id,
            "event_type": event_type,
            "target_id": target_id,
            "payload": payload or {},
            "prev_hash": self.last_hash,
            "version": "2.0.1",
        }

        # -------------------------------------------------
        # 2. ハッシュ計算（因果連鎖）
        # -------------------------------------------------
        serialized = _serialize_for_hash(event)
        current_hash = _compute_hash(serialized)
        event["integrity_hash"] = current_hash

        # -------------------------------------------------
        # 3. Append Only 書き込み
        # -------------------------------------------------
        self._append_log(event)

        # -------------------------------------------------
        # 4. 状態更新
        # -------------------------------------------------
        self.last_hash = current_hash

        return event["event_id"]

    # -----------------------------------------------------
    # Retrieval
    # -----------------------------------------------------
    def get_logs(self) -> List[Dict[str, Any]]:
        """
        全ログ取得

        Returns:
            List[Dict]: ログ一覧
        """
        logs = []

        for file in sorted(os.listdir(self.log_dir)):
            path = os.path.join(self.log_dir, file)

            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    logs.append(json.loads(line.strip()))

        return logs

    # -----------------------------------------------------
    # Integrity
    # -----------------------------------------------------
    def verify_integrity(self) -> bool:
        """
        ハッシュチェーン整合性チェック

        Returns:
            bool: Trueなら正常
        """
        previous_hash = None

        for file in sorted(os.listdir(self.log_dir)):
            path = os.path.join(self.log_dir, file)

            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    entry = json.loads(line.strip())

                    # prev_hash の一致確認
                    if entry.get("prev_hash") != previous_hash:
                        return False

                    # ハッシュ再計算
                    serialized = _serialize_for_hash(entry)
                    recalculated = _compute_hash(serialized)

                    if entry.get("integrity_hash") != recalculated:
                        return False

                    previous_hash = entry.get("integrity_hash")

        return True

    # -----------------------------------------------------
    # Internal
    # -----------------------------------------------------
    def _append_log(self, event: Dict[str, Any]) -> None:
        """
        Append Only 書き込み

        Args:
            event (dict)

        Raises:
            RuntimeError: 書き込み失敗
        """
        date_str = datetime.now(JST).strftime("%Y%m%d")
        file_path = os.path.join(self.log_dir, f"audit_{date_str}.jsonl")

        try:
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(event, ensure_ascii=False) + "\n")
        except Exception as e:
            # 因果律崩壊防止：ログ書き込み失敗は致命的エラー
            raise RuntimeError(f"Audit log write failed: {e}")

    def _load_last_hash(self) -> Optional[str]:
        """
        最新ハッシュ取得

        Returns:
            str | None
        """
        files = sorted(os.listdir(self.log_dir))
        if not files:
            return None

        last_file = os.path.join(self.log_dir, files[-1])

        try:
            with open(last_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                if not lines:
                    return None
                last_entry = json.loads(lines[-1].strip())
                return last_entry.get("integrity_hash")
        except Exception:
            return None


# ---------------------------------------------------------
# Main Guard
# ---------------------------------------------------------
if __name__ == "__main__":
    manager = AuditLogManager()

    txn_id = f"TXN-{uuid.uuid4().hex}"

    manager.record_event(
        event_type="TEST_EVENT",
        actor_id="USR-TEST",
        target_id="TEST-001",
        payload={"message": "test"},
        transaction_id=txn_id,
    )

    print(manager.verify_integrity())

# [EOF]