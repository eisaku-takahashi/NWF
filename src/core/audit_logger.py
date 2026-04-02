"""
Source: src/core/audit_logger.py
Updated: 2026-04-02T19:35:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Engine_Spec/NWF_State_Machine_Spec_v2.0.1.md
    - docs/spec/Data_Spec/NWF_Data_Model_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
    - src/core/event_manager.py
    - src/models/nwf_object.py
Docstring:
    Audit Logger モジュール。
    EventManager から発行されるイベントを監査ログとして JSON Lines 形式で永続化する。
    NWF システムにおけるすべての状態遷移・データ更新・AI実行・エラーなどを
    改ざん不可の監査証跡として logs/audit/ ディレクトリに記録する。
"""

# --------------------------------------------------
# import
# --------------------------------------------------
import os
import json
import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List

# --------------------------------------------------
# 定数 / 設定
# --------------------------------------------------
JST = timezone(timedelta(hours=9))
AUDIT_LOG_DIR = "logs/audit"

# --------------------------------------------------
# __all__
# --------------------------------------------------
__all__ = [
    "AuditLogger"
]

# --------------------------------------------------
# Utility Functions
# --------------------------------------------------
def get_jst_timestamp() -> str:
    """
    JSTの現在時刻をISO 8601形式で取得する。

    Returns:
        str: JST ISO 8601 タイムスタンプ
    """
    return datetime.now(JST).isoformat()


def generate_audit_id() -> str:
    """
    Audit Log ID を生成する。

    Returns:
        str: UUID形式のAudit ID
    """
    return str(uuid.uuid4())


# --------------------------------------------------
# Classes
# --------------------------------------------------
class AuditLogger:
    """
    Audit Logger クラス。
    EventManager から送信されるイベントを監査ログとして保存する。
    """

    def __init__(self, log_dir: str = AUDIT_LOG_DIR):
        """
        AuditLogger を初期化する。

        Args:
            log_dir (str): 監査ログ保存ディレクトリ
        """
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)

    # --------------------------------------------------
    # Log File Path
    # --------------------------------------------------
    def _get_log_file_path(self) -> str:
        """
        当日の監査ログファイルパスを取得する。

        Returns:
            str: ログファイルパス
        """
        date_str = datetime.now(JST).strftime("%Y%m%d")
        filename = f"audit_{date_str}.jsonl"
        return os.path.join(self.log_dir, filename)

    # --------------------------------------------------
    # Event Handler
    # --------------------------------------------------
    def handle_event(self, event) -> None:
        """
        EventManager から呼び出されるイベントハンドラ。
        Event を Audit Log エントリに変換して保存する。

        Args:
            event: EventManager から渡される Event オブジェクト
        """
        entry = self._create_audit_entry(event)
        self._write_jsonl(entry)

    # --------------------------------------------------
    # Create Audit Entry
    # --------------------------------------------------
    def _create_audit_entry(self, event) -> Dict[str, Any]:
        """
        Event オブジェクトから Audit Log エントリを生成する。

        Args:
            event: Event オブジェクト

        Returns:
            Dict[str, Any]: Audit Log エントリ
        """
        entry = {
            "audit_id": generate_audit_id(),
            "event_id": getattr(event, "event_id", None),
            "timestamp": get_jst_timestamp(),
            "event_type": getattr(event, "event_type", None),
            "actor": getattr(event, "actor", None),
            "object_id": getattr(event, "object_id", None),
            "old_state": getattr(event, "old_state", None),
            "new_state": getattr(event, "new_state", None),
            "payload": getattr(event, "payload", {}),
            "result": "SUCCESS",
            "version": getattr(event, "version", None)
        }

        return entry

    # --------------------------------------------------
    # Write JSONL
    # --------------------------------------------------
    def _write_jsonl(self, entry: Dict[str, Any]) -> None:
        """
        Audit Log を JSON Lines 形式でファイルに追記する。

        Args:
            entry (Dict[str, Any]): Audit Log エントリ
        """
        file_path = self._get_log_file_path()

        # Append-Only でログを書き込む
        with open(file_path, "a", encoding="utf-8") as f:
            json.dump(entry, f, ensure_ascii=False)
            f.write("\n")

    # --------------------------------------------------
    # Fetch Logs by Object
    # --------------------------------------------------
    def fetch_by_object(self, object_id: str) -> List[Dict[str, Any]]:
        """
        指定オブジェクトIDに関連する監査ログを取得する。

        Args:
            object_id (str): オブジェクトID

        Returns:
            List[Dict[str, Any]]: 該当ログ一覧
        """
        logs = []

        if not os.path.exists(self.log_dir):
            return logs

        for file_name in os.listdir(self.log_dir):
            if file_name.endswith(".jsonl"):
                file_path = os.path.join(self.log_dir, file_name)

                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        try:
                            entry = json.loads(line.strip())
                            if entry.get("object_id") == object_id:
                                logs.append(entry)
                        except json.JSONDecodeError:
                            continue

        return logs


# --------------------------------------------------
# Main Guard
# --------------------------------------------------
if __name__ == "__main__":
    """
    簡易テスト用。
    """
    class DummyEvent:
        def __init__(self):
            self.event_id = "event-001"
            self.event_type = "OBJECT_CREATED"
            self.actor = "System"
            self.object_id = "obj-001"
            self.old_state = None
            self.new_state = "Draft"
            self.payload = {"name": "Test Object"}
            self.version = "1.0.0"

    logger = AuditLogger()
    event = DummyEvent()
    logger.handle_event(event)

# [EOF]