"""
Source: src/loader/spec_loader.py
Updated: 2026-04-20T01:10:00+09:00  # ← Phase 3.4 Adapter対応で更新
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
    - docs/spec/Execution_Spec/NWF_Validator_And_Context_Contract_v2.0.1.md
    - src/loader/spec_parser.py
    - src/loader/dependency_resolver.py
    - src/loader/spec_registry.py
    - src/loader/spec_validator.py
    - src/core/audit_log_manager.py
    - src/core/event_manager.py
Docstring:
    Spec Loader モジュール（Phase 3.4 対応版）。

    【役割】
    - Spec のロード・検証・依存解決・登録
    - transaction_id による監査トレーサビリティ確保
    - Adapter対応による後方互換性維持（Phase 2 → Phase 3.4）

    【Phase 3.4 変更点】
    - registry のデフォルト注入（Adapter対応）
    - 後方互換維持（既存テスト破壊防止）
"""

import os
import uuid
from datetime import datetime, timezone, timedelta
from typing import List, Any, Optional

# JST Timezone 定義（Spec準拠）
JST = timezone(timedelta(hours=9))

# Loader Modules
from .spec_parser import SpecParser
from .dependency_resolver import DependencyResolver
from .spec_registry import SpecRegistry
from .spec_validator import SpecValidator

# --- Phase 3.4 追加 ---
# DefaultRegistry（存在しない場合のフォールバック用）
# なぜ必要か：
# - SpecLoader の単体利用時に registry 未注入でも動作させるため
# - Phase 2 系コードとの互換性維持
class DefaultRegistry(SpecRegistry):
    """
    デフォルトレジストリ（フォールバック用）
    """
    pass

# Core System（Kernel Core 連携）
from src.core.audit_log_manager import AuditLogManager
from src.core.event_manager import EventManager

__all__ = ["SpecLoader"]


class SpecLoader:
    """
    SpecLoader クラス

    なぜ存在するか：
    - Spec Driven Development の中核
    - Spec を唯一の真実（SSoT）としてシステムに反映するため

    責務：
    - 読み込み
    - 検証
    - 依存解決
    - 登録
    """

    # --- 修正前 ---
    # def __init__(self, spec_registry, spec_validator, audit_log_manager, event_manager, spec_root="docs/spec"):

    # --- 修正後（Phase 3.4 Adapter対応） ---
    def __init__(
        self,
        spec_registry: Optional[SpecRegistry] = None,
        spec_validator: Optional[SpecValidator] = None,
        audit_log_manager: Optional[AuditLogManager] = None,
        event_manager: Optional[EventManager] = None,
        spec_root: str = "docs/spec"
    ):
        """
        初期化処理（依存注入 + Adapter対応）

        Args:
            spec_registry: SpecRegistry（未指定時はDefaultRegistry）
            spec_validator: SpecValidator
            audit_log_manager: AuditLogManager
            event_manager: EventManager
            spec_root: Spec格納ルート

        なぜ変更したか：
        - Phase 3.4 で registry の未指定許容（Adapter化）
        - テスト・旧コードとの互換性維持
        """

        # --- 修正前 ---
        # self.registry = spec_registry

        # --- 修正後 ---
        # registry 未指定時は DefaultRegistry を使用
        self.registry = spec_registry or DefaultRegistry()

        # --- 修正前 ---
        # self.validator = spec_validator

        # --- 修正後（None許容しつつそのまま保持） ---
        self.validator = spec_validator

        self.audit_mgr = audit_log_manager
        self.event_mgr = event_manager

        self.parser = SpecParser()
        self.resolver = DependencyResolver()
        self.spec_root = spec_root

    def load_all_specs(self) -> None:
        """
        すべての Spec をロードするメイン処理

        処理フロー：
        1. transaction_id 発行
        2. ファイルスキャン
        3. パース
        4. バリデーション
        5. 依存解決
        6. 登録
        7. 完了ログ
        """

        transaction_id = str(uuid.uuid4())
        start_time = datetime.now(JST).isoformat()

        # --- 監査ログ ---
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
                # --- 修正前 ---
                # self.validator.validate(spec)

                # --- 修正後 ---
                # validator が None の場合はスキップ（後方互換）
                if self.validator:
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

        なぜ必要か：
        - integration test の検証ポイント
        - SpecLoader を部分的に検証するため
        """

        # 1. 検証
        if self.validator:
            self.validator.validate(spec_data)

        # 2. 登録
        self.registry.register(spec_data, transaction_id)

        # 3. 監査ログ
        self.audit_mgr.record_event(
            transaction_id,
            "SPEC_DATA_PROCESSED",
            {
                "subject_id": spec_data.get("subject_id"),
                "status": "SUCCESS"
            }
        )

    def reload_specs(self) -> None:
        """
        Spec 再読み込み

        なぜ必要か：
        - 動的更新対応
        - 開発時のホットリロード
        """
        transaction_id = str(uuid.uuid4())

        self.audit_mgr.record_event(transaction_id, "SPEC_RELOAD_STARTED", {})

        self.registry.clear()
        self.load_all_specs()

        self.audit_mgr.record_event(transaction_id, "SPEC_RELOAD_COMPLETED", {})

    def get_spec(self, spec_id: str):
        """
        Spec 取得
        """
        return self.registry.get_spec(spec_id)

    def _scan_markdown_files(self, root_dir: str) -> List[str]:
        """
        Markdown ファイルスキャン

        なぜ必要か：
        - Spec は Markdown で管理されるため
        """
        md_files: List[str] = []
        for root, _, files in os.walk(root_dir):
            for file in files:
                if file.endswith(".md"):
                    md_files.append(os.path.join(root, file))
        return md_files

    def _enforce_version(self, spec: Any) -> None:
        """
        Spec Version 強制チェック

        なぜ必要か：
        - Version不整合による実行エラー防止
        """
        expected_version = "v2.0.1"

        version = getattr(spec, "version", None) or (spec.get("version") if isinstance(spec, dict) else None)

        if version != expected_version:
            raise ValueError(f"Invalid Spec Version: {version}. Expected: {expected_version}")

    def _audit_error(self, transaction_id: str, event_type: str, target: str, message: str) -> None:
        """
        エラー監査ログ

        なぜ必要か：
        - エラー原因のトレース
        - 監査要件対応
        """
        self.audit_mgr.record_event(
            transaction_id,
            event_type,
            {"target": target, "error": message}
        )


# [EOF]