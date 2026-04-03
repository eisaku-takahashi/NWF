"""
Source: src/loader/spec_registry.py
Updated: 2026-04-03T09:09:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/System_Architecture/Spec_Loader_System.md
    - docs/spec/Data_Spec/Spec_Data_Model.md
    - docs/spec/Core_Spec/Audit_System.md
Docstring:
    Spec Registry モジュール。
    DependencyResolver によって解決された SpecDocument を登録し、
    ID・Category・Status などのインデックスを構築する。
    Execution Engine、AI Interface、Workflow Engine からの
    ランタイム Spec 参照を提供する知識管理レイヤー。
"""

# ============================================================
# Imports
# ============================================================

from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from threading import RLock

# ============================================================
# Constants / Settings
# ============================================================

EVENT_SPEC_REGISTERED = "SPEC_REGISTERED"
EVENT_SPEC_UNREGISTERED = "SPEC_UNREGISTERED"
EVENT_REGISTRY_CLEARED = "REGISTRY_CLEARED"
EVENT_REGISTRY_READY = "REGISTRY_READY"

# ============================================================
# Public Interface
# ============================================================

__all__ = [
    "SpecRegistry",
    "DuplicateSpecError",
    "SpecNotFoundError",
]

# ============================================================
# Exceptions
# ============================================================

class DuplicateSpecError(Exception):
    """重複 Spec ID エラー"""
    pass


class SpecNotFoundError(Exception):
    """Spec 未発見エラー"""
    pass


# ============================================================
# Data Structures
# ============================================================

@dataclass
class RegistryIndexes:
    """
    レジストリインデックス構造
    """
    category_index: Dict[str, Set[str]] = field(default_factory=dict)
    status_index: Dict[str, Set[str]] = field(default_factory=dict)
    reverse_dependency_index: Dict[str, Set[str]] = field(default_factory=dict)


# ============================================================
# Classes
# ============================================================

class SpecRegistry:
    """
    Spec Registry

    SpecDocument を登録し、ID・カテゴリ・ステータス・依存関係の
    インデックスを構築して高速検索を可能にする。
    """

    def __init__(self):
        """初期化"""
        self._specs: Dict[str, object] = {}
        self._indexes = RegistryIndexes()
        self._lock = RLock()

    # --------------------------------------------------------
    # Registry Management
    # --------------------------------------------------------

    def register(self, spec_doc: object):
        """
        SpecDocument を登録

        Args:
            spec_doc (SpecDocument): 登録対象 SpecDocument
        """
        with self._lock:
            spec_id = spec_doc.metadata.id

            if spec_id in self._specs:
                raise DuplicateSpecError(f"Spec already registered: {spec_id}")

            self._specs[spec_id] = spec_doc
            self._update_indexes(spec_doc)

    def unregister(self, spec_id: str):
        """
        Spec 登録解除

        Args:
            spec_id (str): Spec ID
        """
        with self._lock:
            if spec_id not in self._specs:
                raise SpecNotFoundError(spec_id)

            spec_doc = self._specs.pop(spec_id)
            self._remove_from_indexes(spec_doc)

    def clear(self):
        """
        レジストリ初期化
        """
        with self._lock:
            self._specs.clear()
            self._indexes = RegistryIndexes()

    # --------------------------------------------------------
    # Lookup Methods
    # --------------------------------------------------------

    def get_by_id(self, spec_id: str) -> Optional[object]:
        """
        ID で Spec 取得

        Args:
            spec_id (str): Spec ID

        Returns:
            SpecDocument or None
        """
        return self._specs.get(spec_id)

    def get_all(self) -> List[object]:
        """
        全 Spec 取得
        """
        return list(self._specs.values())

    def find_by_category(self, category: str) -> List[object]:
        """
        カテゴリ検索
        """
        ids = self._indexes.category_index.get(category, set())
        return [self._specs[i] for i in ids]

    def find_by_status(self, status: str) -> List[object]:
        """
        ステータス検索
        """
        ids = self._indexes.status_index.get(status, set())
        return [self._specs[i] for i in ids]

    def get_dependents(self, spec_id: str) -> List[object]:
        """
        逆依存 Spec 取得
        """
        ids = self._indexes.reverse_dependency_index.get(spec_id, set())
        return [self._specs[i] for i in ids]

    def is_registered(self, spec_id: str) -> bool:
        """
        登録済みか確認
        """
        return spec_id in self._specs

    # --------------------------------------------------------
    # Index Management
    # --------------------------------------------------------

    def _update_indexes(self, spec_doc: object):
        """
        インデックス更新
        """
        spec_id = spec_doc.metadata.id
        category = getattr(spec_doc.metadata, "category", None)
        status = getattr(spec_doc.metadata, "status", None)
        dependencies = getattr(spec_doc.metadata, "dependencies", [])

        # Category Index
        if category:
            self._indexes.category_index.setdefault(category, set()).add(spec_id)

        # Status Index
        if status:
            self._indexes.status_index.setdefault(status, set()).add(spec_id)

        # Reverse Dependency Index
        if dependencies:
            for dep in dependencies:
                self._indexes.reverse_dependency_index.setdefault(dep, set()).add(spec_id)

    def _remove_from_indexes(self, spec_doc: object):
        """
        インデックスから削除
        """
        spec_id = spec_doc.metadata.id
        category = getattr(spec_doc.metadata, "category", None)
        status = getattr(spec_doc.metadata, "status", None)
        dependencies = getattr(spec_doc.metadata, "dependencies", [])

        if category and category in self._indexes.category_index:
            self._indexes.category_index[category].discard(spec_id)

        if status and status in self._indexes.status_index:
            self._indexes.status_index[status].discard(spec_id)

        if dependencies:
            for dep in dependencies:
                if dep in self._indexes.reverse_dependency_index:
                    self._indexes.reverse_dependency_index[dep].discard(spec_id)


# ============================================================
# Main Guard
# ============================================================

if __name__ == "__main__":
    print("Spec Registry Module")

# [EOF]