"""
Source: src/loader/spec_loader.py
Updated: 2026-04-03T06:32:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Architecture_Spec/Spec_Loader_Architecture.md
    - docs/spec/Data_Spec/Spec_Data_Model.md
    - docs/spec/Core_Spec/Event_System.md
    - docs/spec/Core_Spec/Audit_System.md
Docstring:
    Spec Loader モジュール。
    docs/spec 配下の Markdown Spec を読み込み、
    Parser・DependencyResolver・SpecRegistry を統合して
    Spec Index を構築するオーケストレーター。
"""

import os
from datetime import datetime, timezone, timedelta
from typing import List

# JST Timezone 定義
JST = timezone(timedelta(hours=9))

# 外部モジュール（後続実装）
from .spec_parser import SpecParser
from .dependency_resolver import DependencyResolver
from .spec_registry import SpecRegistry

# Core System
from src.core.audit_logger import AuditLogger
from src.core.event_manager import EventManager

__all__ = [
    "SpecLoader"
]


class SpecLoader:
    """
    SpecLoader クラス

    docs/spec ディレクトリから Spec Markdown を読み込み、
    Parser → Dependency Resolver → Registry の順で処理し、
    Spec Index を構築する。

    システム起動時の Spec 初期化を担当する。
    """

    def __init__(self, spec_root: str):
        """
        初期化

        Args:
            spec_root (str): docs/spec のルートディレクトリ
        """
        self.spec_root = spec_root
        self.parser = SpecParser()
        self.resolver = DependencyResolver()
        self.registry = SpecRegistry()

        self.audit_logger = AuditLogger()
        self.event_manager = EventManager()

    def load_all_specs(self) -> None:
        """
        すべての Spec をロードするメイン処理

        処理フロー:
        1. Markdown ファイルスキャン
        2. SpecParser でパース
        3. DependencyResolver で順序決定
        4. SpecRegistry に登録
        5. イベント発行

        Raises:
            Exception: 循環依存や読み込みエラー
        """

        start_time = datetime.now(JST).isoformat()
        self.audit_logger.info(f"Spec loading started at {start_time}")

        # Step 1: ファイルスキャン
        md_files = self._scan_markdown_files(self.spec_root)

        # Step 2: パース
        spec_documents = []
        for file_path in md_files:
            try:
                spec_doc = self.parser.parse_file(file_path)
                spec_documents.append(spec_doc)
            except Exception as e:
                self.audit_logger.error(f"Spec parse error: {file_path} : {e}")
                raise

        # Step 3: 依存関係解決
        try:
            sorted_specs = self.resolver.resolve(spec_documents)
        except Exception as e:
            self.audit_logger.critical(f"Dependency resolution failed: {e}")
            raise

        # Step 4: Registry 登録
        for spec in sorted_specs:
            self.registry.register(spec)

        end_time = datetime.now(JST).isoformat()
        self.audit_logger.info(f"Spec loading completed at {end_time}")

        # Step 5: イベント通知
        self.event_manager.emit("SPEC_LOAD_COMPLETED")

    def reload_specs(self) -> None:
        """
        Spec の再読み込み（ホットリロード用）
        """
        self.audit_logger.info("Spec reload started")
        self.registry.clear()
        self.load_all_specs()
        self.audit_logger.info("Spec reload completed")

    def get_spec(self, spec_id: str):
        """
        Spec ID から Spec を取得

        Args:
            spec_id (str): Spec ID

        Returns:
            SpecDocument
        """
        return self.registry.get(spec_id)

    def get_specs_by_category(self, category: str):
        """
        カテゴリ別 Spec 取得

        Args:
            category (str): Spec Category

        Returns:
            List[SpecDocument]
        """
        return self.registry.filter(category)

    def get_dependency_graph(self):
        """
        Dependency Graph 取得

        Returns:
            dict: Dependency Graph
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
        md_files = []

        for root, _, files in os.walk(root_dir):
            for file in files:
                if file.endswith(".md"):
                    md_files.append(os.path.join(root, file))

        return md_files


if __name__ == "__main__":
    """
    テスト用実行
    """
    loader = SpecLoader("docs/spec")
    loader.load_all_specs()

# [EOF]