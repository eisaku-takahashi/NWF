"""
Source: src/integrity/integrity_checker.py
Updated: 2026-04-15T08:05:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Execution_Spec/NWF_Validation_System_v2.0.1.md
    - docs/spec/Core_Spec/NWF_World_Rule_Model_v2.0.1.md
    - docs/spec/Project_Governance/NWF_Recursive_Integrity_Spec_v2.0.1.md
    - docs/spec/Core_Spec/NWF_Entity_ID_System_v2.0.1.md
    - docs/spec/Core_Spec/NWF_Data_Model_v2.0.1.md
    - data/schema/entity_schema.json
    - src/models/nwf_object.py
Docstring:
    Phase 3.1 対応 Integrity Checker。
    構造的整合性 + 因果律 + 不変性を検証し、
    NWFEvent に違反情報を付与する。
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

# [PHASE3_ADD] consistency validator
try:
    from src.integrity.consistency_validator import ConsistencyValidator
except ImportError:
    ConsistencyValidator = None

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
    """現在時刻をJSTで取得"""
    return datetime.now(JST)


# [PHASE2_LEGACY] ★削除せず保持（重要）
def _is_jst_isoformat(ts: str) -> bool:
    """
    ISO8601 +09:00 形式チェック
    Phase3でも外部入力防御として必要
    """
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
    Phase 3 拡張 ValidationResult
    """

    def __init__(self, transaction_id: str):
        self.is_valid: bool = True
        self.errors: List[str] = []
        self.warnings: List[str] = []

        # [PHASE3_ADD]
        self.violations: List[dict] = []

        self.transaction_id: str = transaction_id
        self.timestamp: datetime = _now_jst()

    def add_error(self, message: str) -> None:
        self.is_valid = False
        self.errors.append(message)

    def add_warning(self, message: str) -> None:
        self.warnings.append(message)

    # [PHASE3_ADD]
    def add_violation(self, violation_type: str, reference_spec: str, message: str):
        self.is_valid = False
        self.violations.append({
            "violation_type": violation_type,
            "reference_spec": reference_spec,
            "message": message
        })


class IntegrityChecker:
    """
    Phase 3: Canonical Integrity Gatekeeper
    """

    def __init__(self, schema_path: str = DEFAULT_SCHEMA_PATH):
        self.schema_path = schema_path
        self.schema = None
        self._load_schema()

        self.logger = logging.getLogger(self.__class__.__name__)

        # [PHASE3_ADD]
        self.consistency_validator = ConsistencyValidator() if ConsistencyValidator else None

    def _load_schema(self) -> None:
        try:
            with open(self.schema_path, "r", encoding="utf-8") as f:
                self.schema = json.load(f)
        except Exception:
            self.schema = None

    # --------------------------------------------------
    # [PHASE3_MOD] パイプライン統合
    # --------------------------------------------------
    def check(self, execution_result: Any) -> ValidationResult:

        transaction_id = getattr(execution_result, "transaction_id", "UNKNOWN")
        result = ValidationResult(transaction_id)

        # ------------------------------
        # 基本チェック
        # ------------------------------
        if execution_result is None:
            result.add_error("ERR_INTEGRITY_000: ExecutionResult is None.")
            return result

        if not hasattr(execution_result, "data"):
            result.add_error("ERR_INTEGRITY_001: missing data")
            return result

        # ------------------------------
        # L1 Schema
        # ------------------------------
        self._validate_schema(execution_result.data, result)

        # ------------------------------
        # L2 Constraint
        # ------------------------------
        self._validate_constraints(execution_result.data, result)

        # ------------------------------
        # L3 Logic
        # ------------------------------
        self._validate_logic(execution_result.data, result)

        # ------------------------------
        # 既存チェック
        # ------------------------------
        self._validate_entity_id(execution_result.data, result)
        self._validate_timestamp(execution_result, result)

        # ------------------------------
        # Event付与
        # ------------------------------
        self._attach_event_metadata(execution_result, result)

        # ------------------------------
        # Fail Safe
        # ------------------------------
        if not result.is_valid:
            self._trigger_auto_repair(execution_result, result)

        # ------------------------------
        # Audit Log
        # ------------------------------
        self._log_result(result)

        return result

    # ------------------------------
    # [PHASE2_LEGACY] Schema
    # ------------------------------
    def _validate_schema(self, data: NWFObject, result: ValidationResult):
        if self.schema is None:
            result.add_warning("Schema not loaded")
            return

        if jsonschema is None:
            result.add_warning("jsonschema missing")
            return

        try:
            data_dict = data.to_dict() if hasattr(data, "to_dict") else data.__dict__
            validate(instance=data_dict, schema=self.schema)
        except Exception as e:
            result.add_violation("SCHEMA_MISMATCH", "NWF_Validation_System", str(e))

    # ------------------------------
    # [PHASE3_ADD]
    # ------------------------------
    def _validate_constraints(self, data, result):
        if not self.consistency_validator:
            return
        for v in self.consistency_validator.validate_constraints(data):
            result.add_violation("IMMUTABLE_VIOLATION", "NWF_Core", v)

    def _validate_logic(self, data, result):
        if not self.consistency_validator:
            return
        for v in self.consistency_validator.validate_logic(data):
            result.add_violation("CAUSALITY_VIOLATION", "NWF_World_Rule_Model", v)

    def _validate_entity_id(self, data, result):
        entity_id = getattr(data, "entity_id", None)

        if not entity_id:
            result.add_error("entity_id missing")
            return

        if not re.match(ENTITY_ID_PATTERN, entity_id):
            result.add_violation("ENTITY_ID_INVALID", "NWF_Entity_ID_System", entity_id)

    # ------------------------------
    # [PHASE3_MOD] Timestamp 強化
    # ------------------------------
    def _validate_timestamp(self, execution_result, result):

        timestamp = getattr(execution_result, "timestamp", None)

        # [PHASE3_ADD] string対応
        if isinstance(timestamp, str):
            if not _is_jst_isoformat(timestamp):
                result.add_violation(
                    "TIMESTAMP_FORMAT_INVALID",
                    "NWF_Temporal_Management",
                    timestamp
                )
            return

        # [PHASE2_LEGACY] datetimeチェック
        if isinstance(timestamp, datetime):
            if timestamp.tzinfo is None or timestamp.tzinfo.utcoffset(timestamp) != timedelta(hours=9):
                result.add_violation(
                    "TIMESTAMP_INVALID",
                    "NWF_Temporal_Management",
                    "Must be JST"
                )
            return

        result.add_error("timestamp invalid")

    # ------------------------------
    # [PHASE3_ADD]
    # ------------------------------
    def _attach_event_metadata(self, execution_result, result):
        if hasattr(execution_result, "event"):
            execution_result.event.validation = {
                "is_valid": result.is_valid,
                "violations": result.violations,
                "timestamp": result.timestamp.isoformat()
            }

    def _trigger_auto_repair(self, execution_result, result):
        try:
            # [PHASE3_ADD] 将来実装
            # from src.repair.auto_repair_engine import AutoRepairEngine
            # AutoRepairEngine().repair(...)
            pass
        except Exception as e:
            self.logger.error(f"[AUTO_REPAIR_FAILED] {e}")

    def _log_result(self, result):
        if result.is_valid:
            self.logger.info(f"[PASS] {result.transaction_id}")
        else:
            self.logger.error(f"[FAIL] {result.transaction_id} {result.violations}")


# ------------------------------
# Main Guard
# ------------------------------
if __name__ == "__main__":
    pass


# [EOF]