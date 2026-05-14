"""
Source: src/integrity/integrity_checker.py
Updated: 2026-04-12T01:25:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Project_Governance/NWF_Recursive_Integrity_Spec_v2.0.1.md
    - docs/spec/Core_Spec/NWF_Entity_ID_System_v2.0.1.md
    - docs/spec/Core_Spec/NWF_Data_Model_v2.0.1.md
    - data/schema/entity_schema.json
    - src/models/nwf_object.py
Docstring:
    Integrity Checker モジュール。
    WorkflowExecutor の ExecutionResult を受け取り、
    構造的整合性（Structural Integrity）を検証する。
    Schema検証・Entity ID検証・Timestamp検証を行い、
    ValidationResult を返却する。
"""

# ------------------------------
# import
# ------------------------------
import json
import logging
import re
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Any

try:
    import jsonschema
    from jsonschema import validate
except ImportError:
    jsonschema = None

from src.models.nwf_object import NWFObject

# ------------------------------
# 定数 / 設定
# ------------------------------
JST = timezone(timedelta(hours=9))

ENTITY_ID_PATTERN = r"^[A-Z0-9\-\_]+$"

DEFAULT_SCHEMA_PATH = "data/schema/entity_schema.json"

# ------------------------------
# __all__
# ------------------------------
__all__ = [
    "ValidationResult",
    "IntegrityChecker"
]

# ------------------------------
# Utility Functions
# ------------------------------
def _now_jst() -> datetime:
    """現在時刻をJSTで取得する"""
    return datetime.now(JST)


def _is_jst_isoformat(ts: str) -> bool:
    """ISO8601 +09:00 形式か検証する"""
    try:
        dt = datetime.fromisoformat(ts)
        return dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) == timedelta(hours=9)
    except Exception:
        return False


# ------------------------------
# Classes
# ------------------------------
class ValidationResult:
    """
    構造的整合性の検証結果コンテナ

    Args:
        transaction_id (str): トランザクションID

    Attributes:
        is_valid (bool): 全体の妥当性
        errors (List[str]): エラー一覧
        warnings (List[str]): 警告一覧
        transaction_id (str): トランザクションID
        timestamp (datetime): 検証時刻（JST）
    """

    def __init__(self, transaction_id: str):
        self.is_valid: bool = True
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.transaction_id: str = transaction_id
        self.timestamp: datetime = _now_jst()

    def add_error(self, message: str) -> None:
        """エラー追加"""
        self.is_valid = False
        self.errors.append(message)

    def add_warning(self, message: str) -> None:
        """警告追加"""
        self.warnings.append(message)


class IntegrityChecker:
    """
    Structural Integrity Checker

    ExecutionResult を入力とし、
    以下を検証する：

    - Schema 準拠
    - Entity ID 整合性
    - Timestamp 整合性
    """

    def __init__(self, schema_path: str = DEFAULT_SCHEMA_PATH):
        """
        Args:
            schema_path (str): JSON Schema のパス
        """
        self.schema_path = schema_path
        self.schema = None
        self._load_schema()

        # ログ設定
        self.logger = logging.getLogger(self.__class__.__name__)

    def _load_schema(self) -> None:
        """Schema をロードする"""
        try:
            with open(self.schema_path, "r", encoding="utf-8") as f:
                self.schema = json.load(f)
        except Exception:
            # Schemaがロードできない場合は警告扱い（システム停止はしない）
            self.schema = None

    def check(self, execution_result: Any) -> ValidationResult:
        """
        ExecutionResult を検証する

        Args:
            execution_result: WorkflowExecutor の出力

        Returns:
            ValidationResult
        """
        transaction_id = getattr(execution_result, "transaction_id", "UNKNOWN")
        result = ValidationResult(transaction_id)

        # ------------------------------
        # 1. 基本構造チェック
        # ------------------------------
        if execution_result is None:
            result.add_error("ERR_INTEGRITY_000: ExecutionResult is None.")
            return result

        if not hasattr(execution_result, "data"):
            result.add_error("ERR_INTEGRITY_001: ExecutionResult missing data field.")
            return result

        if execution_result.data is None:
            result.add_error("ERR_INTEGRITY_002: Data body is missing.")
            return result

        # ------------------------------
        # 2. NWFObject 検証
        # ------------------------------
        if not isinstance(execution_result.data, NWFObject):
            result.add_error("ERR_INTEGRITY_003: Data is not NWFObject.")

        # ------------------------------
        # 3. Schema Validation
        # ------------------------------
        self._validate_schema(execution_result.data, result)

        # ------------------------------
        # 4. Entity ID Validation
        # ------------------------------
        self._validate_entity_id(execution_result.data, result)

        # ------------------------------
        # 5. Timestamp Validation
        # ------------------------------
        self._validate_timestamp(execution_result, result)

        # ------------------------------
        # ログ出力（監査）
        # ------------------------------
        self._log_result(result)

        return result

    def _validate_schema(self, data: NWFObject, result: ValidationResult) -> None:
        """
        JSON Schema 検証

        Args:
            data (NWFObject)
            result (ValidationResult)
        """
        if self.schema is None:
            result.add_warning("WARN_INTEGRITY_001: Schema not loaded.")
            return

        if jsonschema is None:
            result.add_warning("WARN_INTEGRITY_002: jsonschema library not installed.")
            return

        try:
            # NWFObject → dict 変換を前提
            data_dict = data.to_dict() if hasattr(data, "to_dict") else data.__dict__
            validate(instance=data_dict, schema=self.schema)
        except Exception as e:
            result.add_error(f"ERR_INTEGRITY_010: Schema validation failed: {str(e)}")

    def _validate_entity_id(self, data: NWFObject, result: ValidationResult) -> None:
        """
        Entity ID 検証

        Args:
            data (NWFObject)
            result (ValidationResult)
        """
        entity_id = getattr(data, "entity_id", None)

        if not entity_id:
            result.add_error("ERR_INTEGRITY_020: entity_id is missing.")
            return

        if not isinstance(entity_id, str):
            result.add_error("ERR_INTEGRITY_021: entity_id must be string.")
            return

        if not re.match(ENTITY_ID_PATTERN, entity_id):
            result.add_error("ERR_INTEGRITY_022: entity_id format invalid.")

    def _validate_timestamp(self, execution_result: Any, result: ValidationResult) -> None:
        """
        Timestamp 検証

        Args:
            execution_result
            result (ValidationResult)
        """
        timestamp = getattr(execution_result, "timestamp", None)

        if timestamp is None:
            result.add_error("ERR_INTEGRITY_030: timestamp missing.")
            return

        # datetime 型チェック
        if not isinstance(timestamp, datetime):
            result.add_error("ERR_INTEGRITY_031: timestamp must be datetime.")
            return

        # JSTチェック
        if timestamp.tzinfo is None or timestamp.tzinfo.utcoffset(timestamp) != timedelta(hours=9):
            result.add_error("ERR_INTEGRITY_032: timestamp must be JST.")

    def _log_result(self, result: ValidationResult) -> None:
        """
        検証結果をログ出力する

        Args:
            result (ValidationResult)
        """
        if result.is_valid:
            self.logger.info(
                f"[INTEGRITY_CHECK_PASS] transaction_id={result.transaction_id}"
            )
        else:
            self.logger.error(
                f"[INTEGRITY_CHECK_FAIL] transaction_id={result.transaction_id} errors={result.errors}"
            )


# ------------------------------
# Main Guard
# ------------------------------
if __name__ == "__main__":
    # 簡易テスト用
    pass


# [EOF]