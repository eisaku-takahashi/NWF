"""
Source: src/engine/story_engine.py
Updated: 2026-04-16T14:23:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Engine_Spec/NWF_Story_Engine_Implementation_v2.0.1.md
    - docs/spec/Core_Spec/NWF_World_Rule_Execution_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
Docstring:
    Story Engine モジュール。
    Entity から Story Graph を生成し、World Rule に基づいた整合性検証を行い、
    Stardate ベースのナラティブタイムラインを構築する。
"""

from typing import List, Dict, Any, Optional

from src.core.metadata_manager import MetadataManager
from src.integrity.consistency_validator import ConsistencyValidator

__all__ = [
    "StoryEngine"
]


class StoryEngine:
    """
    Story Engine クラス

    Entity を Story Graph に変換し、
    World Rule に基づく整合性検証を行いながら
    Timeline を生成する。
    """

    def __init__(
        self,
        metadata_manager: MetadataManager,
        validator: ConsistencyValidator
    ) -> None:
        """
        初期化

        Args:
            metadata_manager: MetadataManager インスタンス
            validator: ConsistencyValidator インスタンス
        """
        self.meta_manager = metadata_manager
        self.validator = validator

        # グラフ初期化
        self.graph: Dict[str, List[Dict[str, Any]]] = {
            "nodes": [],
            "edges": []
        }

    def generate_story_graph(
        self,
        context: Any,
        entities: List[Any]
    ) -> Dict[str, Any]:
        """
        エンティティ群からストーリーグラフを生成する

        Args:
            context: WorkflowContext
            entities: エンティティ一覧

        Returns:
            StoryGraph
        """

        # World Rule 取得
        world_rules: Dict[str, Any] = context._metadata.get("world_rules", {})

        nodes = []
        edges = []

        # Node生成
        for entity in entities:
            node = {
                "id": getattr(entity, "id", None),
                "type": getattr(entity, "type", None),
                "state": getattr(entity, "state", None)
            }
            nodes.append(node)

        # Edge生成
        for entity in entities:
            relationships = getattr(entity, "relationships", [])

            for rel in relationships:
                edge = {
                    "source": entity.id,
                    "target": rel.get("target"),
                    "type": rel.get("type"),
                    "weight": rel.get("weight", 1.0),
                    "stardate": None
                }

                # Stardate付与
                timestamp = rel.get("timestamp")
                if timestamp:
                    edge["stardate"] = self.meta_manager.convert_to_stardate(timestamp)

                # World Rule チェック
                if not self._apply_world_rules_to_edge(entity, edge, world_rules):
                    continue

                # Consistency Validator 実行
                validation_result = self.validator.validate(context, None)

                if not validation_result.is_consistent:
                    # 不整合エッジは破棄
                    continue

                edges.append(edge)

        self.graph = {
            "nodes": nodes,
            "edges": edges
        }

        return self.graph

    def render_timeline(self) -> List[Dict[str, Any]]:
        """
        グラフからタイムラインを生成

        Returns:
            NarrativeUnit のリスト
        """

        edges = self.graph.get("edges", [])

        # Stardate順ソート
        sorted_edges = sorted(
            edges,
            key=lambda x: x.get("stardate", 0.0)
        )

        timeline: List[Dict[str, Any]] = []

        for edge in sorted_edges:
            unit = {
                "timestamp": edge.get("stardate"),
                "actor": edge.get("source"),
                "location": edge.get("target"),
                "action": edge.get("type"),
                "integrity_status": "valid"
            }
            timeline.append(unit)

        # 時間整合性チェック
        self.meta_manager.check_timeline_linearity(sorted_edges)

        return timeline

    def _apply_world_rules_to_edge(
        self,
        entity: Any,
        edge: Dict[str, Any],
        world_rules: Dict[str, Any]
    ) -> bool:
        """
        World Rule に基づきエッジ生成可否を判定

        Args:
            entity: 対象エンティティ
            edge: エッジ情報
            world_rules: World Rule 設定

        Returns:
            bool: 許可可否
        """

        # 死亡状態チェック
        is_alive = getattr(entity, "is_alive", True)

        if is_alive is False:
            allow_ghost = world_rules.get("allow_ghost_activity", False)

            if not allow_ghost:
                return False

        # 時間逆行チェック
        allow_time_reversal = world_rules.get("allow_time_reversal", False)

        if not allow_time_reversal:
            # Stardate逆転チェック（簡易）
            stardate = edge.get("stardate")
            if stardate is not None and stardate < 0:
                return False

        return True


if __name__ == "__main__":
    # 簡易テスト（デバッグ用）
    print("StoryEngine module loaded.")

# [EOF]