"""
Source: src/loader/dependency_resolver.py
Updated: 2026-04-03T08:42:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/System_Architecture/Spec_Loader_System.md
    - docs/spec/Data_Spec/Spec_Data_Model.md
    - docs/spec/Core_Spec/Audit_System.md
Docstring:
    Dependency Resolver モジュール。
    SpecParser によって生成された SpecDocument の依存関係を解析し、
    トポロジカルソートによりロード順序を決定する。
    循環依存、欠落依存、不正 ID を検出し、NWF Spec Loader System の
    論理制御レイヤーとして機能する。
"""

# ============================================================
# Imports
# ============================================================

from typing import Dict, List, Set
from dataclasses import dataclass, field

# ============================================================
# Constants / Settings
# ============================================================

# 依存解決イベント名
EVENT_RESOLVE_START = "DEPENDENCY_RESOLVE_START"
EVENT_RESOLVE_SUCCESS = "DEPENDENCY_RESOLVE_SUCCESS"
EVENT_RESOLVE_ERROR = "DEPENDENCY_RESOLVE_ERROR"

# ============================================================
# Public Interface
# ============================================================

__all__ = [
    "DependencyNode",
    "DependencyGraph",
    "DependencyResolver",
    "CircularDependencyError",
    "MissingDependencyError",
]

# ============================================================
# Utility Functions
# ============================================================

def normalize_id(spec_id: str) -> str:
    """
    Spec ID の正規化（大文字化・空白除去）

    Args:
        spec_id (str): Spec ID

    Returns:
        str: 正規化された Spec ID
    """
    return spec_id.strip().upper()


# ============================================================
# Data Structures
# ============================================================

@dataclass
class DependencyNode:
    """
    依存関係ノード

    Attributes:
        spec_id (str): Spec ID
        dependencies (Set[str]): 依存先 Spec ID
        dependents (Set[str]): 依存元 Spec ID
    """
    spec_id: str
    dependencies: Set[str] = field(default_factory=set)
    dependents: Set[str] = field(default_factory=set)


@dataclass
class DependencyGraph:
    """
    依存関係グラフ
    隣接リスト形式で Spec 間の依存関係を保持する
    """
    nodes: Dict[str, DependencyNode] = field(default_factory=dict)

    def add_node(self, spec_id: str):
        """
        ノード追加

        Args:
            spec_id (str): Spec ID
        """
        spec_id = normalize_id(spec_id)
        if spec_id not in self.nodes:
            self.nodes[spec_id] = DependencyNode(spec_id)

    def add_dependency(self, spec_id: str, dependency_id: str):
        """
        依存関係追加

        Args:
            spec_id (str): 依存元
            dependency_id (str): 依存先
        """
        spec_id = normalize_id(spec_id)
        dependency_id = normalize_id(dependency_id)

        self.add_node(spec_id)
        self.add_node(dependency_id)

        self.nodes[spec_id].dependencies.add(dependency_id)
        self.nodes[dependency_id].dependents.add(spec_id)


# ============================================================
# Exceptions
# ============================================================

class CircularDependencyError(Exception):
    """循環依存エラー"""
    pass


class MissingDependencyError(Exception):
    """欠落依存エラー"""
    pass


# ============================================================
# Classes
# ============================================================

class DependencyResolver:
    """
    Dependency Resolver

    SpecDocument の依存関係を解析し、
    トポロジカルソートによってロード順序を決定する。
    """

    def __init__(self):
        """初期化"""
        self.graph = DependencyGraph()
        self.missing_dependencies: Set[str] = set()

    # --------------------------------------------------------
    # Public Methods
    # --------------------------------------------------------

    def resolve(self, specs: List[object]) -> List[object]:
        """
        依存関係を解決し、ロード順序を決定

        Args:
            specs (List[SpecDocument]): SpecDocument リスト

        Returns:
            List[SpecDocument]: ロード順序に並んだ SpecDocument
        """
        spec_map = {normalize_id(spec.metadata.id): spec for spec in specs}

        # グラフ構築
        self._build_graph(specs)

        # 欠落依存チェック
        self._validate_missing_dependencies(spec_map)

        # 循環依存チェック
        self._detect_cycles()

        # トポロジカルソート
        sorted_ids = self._topological_sort()

        # SpecDocument の順序に変換
        return [spec_map[spec_id] for spec_id in sorted_ids]

    # --------------------------------------------------------
    # Internal Methods
    # --------------------------------------------------------

    def _build_graph(self, specs: List[object]):
        """
        依存グラフ構築
        """
        for spec in specs:
            spec_id = normalize_id(spec.metadata.id)
            self.graph.add_node(spec_id)

            if spec.metadata.dependencies:
                for dep in spec.metadata.dependencies:
                    dep_id = normalize_id(dep)
                    self.graph.add_dependency(spec_id, dep_id)

    def _validate_missing_dependencies(self, spec_map: Dict[str, object]):
        """
        欠落依存チェック
        """
        for node in self.graph.nodes.values():
            for dep in node.dependencies:
                if dep not in spec_map:
                    self.missing_dependencies.add(dep)

        if self.missing_dependencies:
            raise MissingDependencyError(
                f"Missing dependencies: {self.missing_dependencies}"
            )

    def _detect_cycles(self):
        """
        循環依存検出（DFS）
        """
        visited = set()
        recursion_stack = set()

        def dfs(node_id: str):
            visited.add(node_id)
            recursion_stack.add(node_id)

            for dep in self.graph.nodes[node_id].dependencies:
                if dep not in visited:
                    dfs(dep)
                elif dep in recursion_stack:
                    raise CircularDependencyError(
                        f"Circular dependency detected: {node_id} -> {dep}"
                    )

            recursion_stack.remove(node_id)

        for node_id in self.graph.nodes:
            if node_id not in visited:
                dfs(node_id)

    def _topological_sort(self) -> List[str]:
        """
        トポロジカルソート（Kahn Algorithm）

        Returns:
            List[str]: ソート済み Spec ID リスト
        """
        in_degree = {node_id: 0 for node_id in self.graph.nodes}

        for node in self.graph.nodes.values():
            for dep in node.dependencies:
                in_degree[node.spec_id] += 1

        queue = [node_id for node_id, deg in in_degree.items() if deg == 0]
        sorted_list = []

        while queue:
            node_id = queue.pop(0)
            sorted_list.append(node_id)

            for dependent in self.graph.nodes[node_id].dependents:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        if len(sorted_list) != len(self.graph.nodes):
            raise CircularDependencyError("Circular dependency detected during sort")

        return sorted_list


# ============================================================
# Main Guard
# ============================================================

if __name__ == "__main__":
    # テスト用簡易実行
    print("Dependency Resolver Module")

# [EOF]