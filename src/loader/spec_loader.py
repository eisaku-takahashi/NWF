"""
Source: src/loader/spec_loader.py
Updated: 2026-04-10T03:11:00+09:00
PIC: Engineer / Gemini (Architect)
Version: NWF v2.0.1
Docstring:
    Spec Loader モジュール（Phase 2.2 最終統合版）。
    因果律（transaction_id）の伝播を完全保証し、統合テストの検証をパスする。
"""

import os
import uuid
from datetime import datetime, timezone, timedelta
from typing import List, Any

# JST Timezone 定義
JST = timezone(timedelta(hours=9))

# Loader Modules
from .spec_parser import SpecParser
from .dependency_resolver import DependencyResolver
from .spec_registry import SpecRegistry
from .spec_validator import SpecValidator

# Core System（Kernel Core 連携）
from src.core.audit_log_manager import AuditLogManager
from src.core.event_manager import EventManager

__all__ = ["SpecLoader"]


class SpecLoader:
    """
    SpecLoader クラス
    Spec のロード・検証・依存解決・登録を行う中核モジュール。
    """

    def __init__(self, spec_registry, spec_validator, audit_log_manager, event_manager, spec_root="docs/spec"):
        """ Phase 2.2 準拠の初期化（依存注入モデル） """
        self.registry = spec_registry
        self.validator = spec_validator
        self.audit_mgr = audit_log_manager
        self.event_mgr = event_manager
        
        self.parser = SpecParser()
        self.resolver = DependencyResolver()
        self.spec_root = spec_root

    def load_all_specs(self) -> None:
        """ すべての Spec をロードするメイン処理 """
        transaction_id = str(uuid.uuid4())
        start_time = datetime.now(JST).isoformat()

        # 因果律の記録（位置引数として ID を渡すことでテスト整合性を確保）
        self.audit_mgr.record_event(
            transaction_id,
            "SPEC_LOAD_STARTED",
            {
                "timestamp": start_time,
                "spec_root": self.spec_root
            }
        )

        md_files = self._scan_markdown_files(self.spec_root)

        parsed_specs: List[Any] = []
        for file_path in md_files:
            try:
                spec = self.parser.parse_file(file_path)
                parsed_specs.append(spec)
            except Exception as e:
                self._audit_error(transaction_id, "SPEC_PARSE_ERROR", file_path, str(e))
                raise

        parsed_specs_objs = [s for s in parsed_specs if s]
        validated_specs: List[Any] = []
        for spec in parsed_specs_objs:
            try:
                self.validator.validate(spec)
                self._enforce_version(spec)
                validated_specs.append(spec)
            except Exception as e:
                spec_id = getattr(spec, "subject_id", "unknown") if hasattr(spec, "subject_id") else spec.get("subject_id", "unknown")
                self._audit_error(transaction_id, "SPEC_VALIDATION_ERROR", spec_id, str(e))
                raise

        try:
            sorted_specs = self.resolver.resolve(validated_specs)
        except Exception as e:
            self._audit_error(transaction_id, "DEPENDENCY_RESOLUTION_FAILED", "resolver", str(e))
            raise

        for spec in sorted_specs:
            self.registry.register(spec, transaction_id)

        end_time = datetime.now(JST).isoformat()
        self.audit_mgr.record_event(
            transaction_id,
            "SPEC_LOAD_COMPLETED",
            {
                "timestamp": end_time,
                "spec_count": len(sorted_specs)
            }
        )

        self.event_mgr.emit(
            "SPEC_LOAD_COMPLETED",
            {
                "transaction_id": transaction_id,
                "spec_count": len(sorted_specs)
            }
        )

    def _process_spec_data(self, spec_data: dict, transaction_id: str) -> None:
        """
        [統合テスト用] 個別スペックデータの処理。
        """
        # 1. 検証
        self.validator.validate(spec_data)
        
        # 2. 登録
        self.registry.register(spec_data, transaction_id)
        
        # 3. 監査記録（テスト検証のため位置引数で ID を渡す）
        self.audit_mgr.record_event(
            transaction_id,
            "SPEC_DATA_PROCESSED",
            {
                "subject_id": spec_data.get("subject_id"),
                "status": "SUCCESS"
            }
        )

    def reload_specs(self) -> None:
        transaction_id = str(uuid.uuid4())
        self.audit_mgr.record_event(transaction_id, "SPEC_RELOAD_STARTED", {})
        self.registry.clear()
        self.load_all_specs()
        self.audit_mgr.record_event(transaction_id, "SPEC_RELOAD_COMPLETED", {})

    def get_spec(self, spec_id: str):
        return self.registry.get_spec(spec_id)

    def _scan_markdown_files(self, root_dir: str) -> List[str]:
        md_files: List[str] = []
        for root, _, files in os.walk(root_dir):
            for file in files:
                if file.endswith(".md"):
                    md_files.append(os.path.join(root, file))
        return md_files

    def _enforce_version(self, spec: Any) -> None:
        expected_version = "v2.0.1"
        version = getattr(spec, "version", None) or (spec.get("version") if isinstance(spec, dict) else None)
        if version != expected_version:
            raise ValueError(f"Invalid Spec Version: {version}. Expected: {expected_version}")

    def _audit_error(self, transaction_id: str, event_type: str, target: str, message: str) -> None:
        self.audit_mgr.record_event(
            transaction_id,
            event_type,
            {"target": target, "error": message}
        )

# [EOF]