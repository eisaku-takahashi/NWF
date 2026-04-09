"""
Source: src/loader/spec_loader.py
Updated: 2026-04-10T00:11:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Core_Spec/NWF_File_System_v2.0.1.md
    - docs/spec/Core_Spec/NWF_Event_Model_v2.0.1.md
    - docs/spec/Kernel_Spec/NWF_Kernel_Audit_System_Spec_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
    - docs/spec/Index/NWF_Spec_Master_Index_v2.0.1.md
Docstring:
    Spec Loader モジュール（再構築版）。

    docs/spec 配下の Markdown Spec を読み込み、
    Parser → Validator → Dependency Resolver → Registry の順で処理し、
    Spec Index（不変）を構築する。

    また、Kernel Core と統合され、
    transaction_id による因果律管理・AuditLog 記録・Event 発火を行う。
"""

import os
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

# 修正前（削除対象）2026-04-10T00:11:00+09:00
# from src.core.id_generator import IDGenerator

__all__ = [
    "SpecLoader"
]


class SpecLoader:
    """
    SpecLoader クラス

    Spec のロード・検証・依存解決・登録を行う中核モジュール。

    特徴:
        - transaction_id による因果律管理
        - Spec Version 強制整合（v2.0.1）
        - 循環依存検出
        - Registry の不変構築
        - Audit / Event 完全統合
    """

    # 修正前 2026-04-10T01:29:00+09:00
    '''
    def __init__(self, spec_root: str):
        """
        初期化

        Args:
            spec_root (str): docs/spec のルートディレクトリ
        """
        self.spec_root = spec_root

        # Loader Components
        self.parser = SpecParser()
        self.validator = SpecValidator()
        self.resolver = DependencyResolver()
        self.registry = SpecRegistry()

        # Core Components
        self.audit_log_manager = AuditLogManager()
        self.event_manager = EventManager()
        self.id_generator = IDGenerator()
    '''
    # 修正後
    def __init__(self, spec_registry, spec_validator, audit_log_manager, event_manager, spec_root="docs/spec"):
        """
        Phase 2.2 準拠の初期化（依存注入モデル）
        """
        # 1. 外部から注入される中核コンポーネント
        self.registry = spec_registry
        self.validator = spec_validator
        self.audit_mgr = audit_log_manager
        self.event_mgr = event_manager
        
        # 2. 内部で使用するユーティリティ（これらは内部生成でOK）
        self.parser = SpecParser()
        self.resolver = DependencyResolver()
        
        # 3. 設定値
        self.spec_root = spec_root

        # [重要] self.id_generator = IDGenerator() は削除
        # 理由：既に物理削除済みであり、uuid または EntityManager を使用するため

    def load_all_specs(self) -> None:
        """
        すべての Spec をロードするメイン処理

        フロー:
            1. transaction_id 発行
            2. Markdown ファイルスキャン
            3. SpecParser によるパース
            4. SpecValidator による検証
            5. DependencyResolver による順序決定
            6. SpecRegistry に登録（不変）
            7. Audit 記録
            8. Event 発火

        Raises:
            Exception: 検証エラー / 循環依存 / IOエラー
        """

        # --- transaction_id 発行（因果律の起点） ---
        transaction_id = self.id_generator.generate_id()

        start_time = datetime.now(JST).isoformat()

        self.audit_log_manager.record_event(
            transaction_id=transaction_id,
            event_type="SPEC_LOAD_STARTED",
            payload={
                "timestamp": start_time,
                "spec_root": self.spec_root
            }
        )

        # --- Step 1: ファイルスキャン ---
        md_files = self._scan_markdown_files(self.spec_root)

        # --- Step 2: パース ---
        parsed_specs: List[Any] = []
        for file_path in md_files:
            try:
                spec = self.parser.parse_file(file_path)
                parsed_specs.append(spec)
            except Exception as e:
                self._audit_error(transaction_id, "SPEC_PARSE_ERROR", file_path, str(e))
                raise

        # --- Step 3: バリデーション ---
        validated_specs: List[Any] = []
        for spec in parsed_specs:
            try:
                self.validator.validate(spec)
                self._enforce_version(spec)
                validated_specs.append(spec)
            except Exception as e:
                self._audit_error(transaction_id, "SPEC_VALIDATION_ERROR", getattr(spec, "id", "unknown"), str(e))
                raise

        # --- Step 4: 依存関係解決 ---
        try:
            sorted_specs = self.resolver.resolve(validated_specs)
        except Exception as e:
            self._audit_error(transaction_id, "DEPENDENCY_RESOLUTION_FAILED", "resolver", str(e))
            raise

        # --- Step 5: Registry 登録（不変） ---
        for spec in sorted_specs:
            self.registry.register(spec)

        end_time = datetime.now(JST).isoformat()

        # --- Step 6: Audit ---
        self.audit_log_manager.record_event(
            transaction_id=transaction_id,
            event_type="SPEC_LOAD_COMPLETED",
            payload={
                "timestamp": end_time,
                "spec_count": len(sorted_specs)
            }
        )

        # --- Step 7: Event ---
        self.event_manager.emit(
            "SPEC_LOAD_COMPLETED",
            {
                "transaction_id": transaction_id,
                "spec_count": len(sorted_specs)
            }
        )

    def reload_specs(self) -> None:
        """
        Spec の再読み込み（ホットリロード）

        注意:
            Registry をクリアし、完全再ロードする。
        """
        transaction_id = self.id_generator.generate_id()

        self.audit_log_manager.record_event(
            transaction_id=transaction_id,
            event_type="SPEC_RELOAD_STARTED",
            payload={}
        )

        self.registry.clear()
        self.load_all_specs()

        self.audit_log_manager.record_event(
            transaction_id=transaction_id,
            event_type="SPEC_RELOAD_COMPLETED",
            payload={}
        )

    def get_spec(self, spec_id: str):
        """
        Spec ID から Spec を取得

        Args:
            spec_id (str): Spec ID

        Returns:
            Any: SpecDocument
        """
        return self.registry.get(spec_id)

    def get_specs_by_category(self, category: str):
        """
        カテゴリ別 Spec 取得

        Args:
            category (str): Spec Category

        Returns:
            List[Any]
        """
        return self.registry.filter(category)

    def get_dependency_graph(self):
        """
        Dependency Graph を取得

        Returns:
            dict
        """
        return self.resolver.get_graph()

    def _scan_markdown_files(self, root_dir: str) -> List[str]:
        """
        Markdown ファイルを再帰的に探索

        Args:
            root_dir (str): ルートディレクトリ

        Returns:
            List[str]: Markdown ファイル一覧
        """
        md_files: List[str] = []

        for root, _, files in os.walk(root_dir):
            for file in files:
                if file.endswith(".md"):
                    md_files.append(os.path.join(root, file))

        return md_files

    def _enforce_version(self, spec: Any) -> None:
        """
        Spec バージョンの強制チェック

        Args:
            spec (Any): SpecDocument

        Raises:
            ValueError: バージョン不整合
        """
        expected_version = "v2.0.1"
        if getattr(spec, "version", None) != expected_version:
            raise ValueError(f"Invalid Spec Version: {getattr(spec, 'version', None)}")

    def _audit_error(self, transaction_id: str, event_type: str, target: str, message: str) -> None:
        """
        エラー監査ログ記録

        Args:
            transaction_id (str): トランザクションID
            event_type (str): イベント種別
            target (str): 対象
            message (str): エラーメッセージ
        """
        self.audit_log_manager.record_event(
            transaction_id=transaction_id,
            event_type=event_type,
            payload={
                "target": target,
                "error": message
            }
        )


if __name__ == "__main__":
    """
    テスト実行
    """
    loader = SpecLoader("docs/spec")
    loader.load_all_specs()

# [EOF]