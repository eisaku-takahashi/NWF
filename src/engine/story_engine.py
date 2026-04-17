"""
Source: src/engine/story_engine.py
Updated: 2026-04-17T09:39:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Engine_Spec/NWF_Story_Engine_Implementation_v2.0.1.md
    - docs/spec/Core_Spec/NWF_World_Rule_Execution_v2.0.1.md
    - src/core/metadata_manager.py
    - src/integrity/consistency_validator.py
Docstring:
    Story Engine モジュール。
    Entity から StoryGraph を生成し、World Rule に基づく整合性を維持しながら
    タイムライン（NarrativeUnit）を構築する。
"""

from typing import List, Dict, Any
from datetime import datetime, timezone, timedelta
import logging

from src.core.metadata_manager import MetadataManager
from src.integrity.consistency_validator import ConsistencyValidator

__all__ = [
    "StoryEngine"
]

# JST 定義
JST = timezone(timedelta(hours=9))

# ロガー設定
logger = logging.getLogger(__name__)


class StoryEngine:
    """
    物語生成の中核エンジン。
    Entity → Graph → Timeline 変換を担う。
    """

    def __init__(self, metadata_manager: MetadataManager, validator: ConsistencyValidator):
        """
        Args:
            metadata_manager: 時間管理モジュール
            validator: 整合性検証モジュール（World Rule 含む）
        """
        self.meta_manager = metadata_manager
        self.validator = validator

        # グラフ初期化
        self.graph: Dict[str, Any] = {
            "nodes": [],
            "edges": []
        }

    def generate_story_graph(self, entities: List[Any]) -> Dict[str, Any]:
        """
        Entity 群から StoryGraph を生成する。

        Args:
            entities: Entity オブジェクトのリスト

        Returns:
            StoryGraph
        """

        # 初期化
        self.graph["nodes"] = []
        self.graph["edges"] = []

        # 現在時刻（JST）
        current_time = datetime.now(JST)

        # ノード生成
        for entity in entities:
            node = {
                "id": getattr(entity, "id", "unknown"),
                "type": getattr(entity, "type", "unknown"),
                "state": "alive" if getattr(entity, "is_alive", True) else "dead"
            }
            self.graph["nodes"].append(node)

        # エッジ生成
        for entity in entities:
            related_scenes = getattr(entity, "related_scenes", [])

            for scene_id in related_scenes:
                edge = {
                    "source": entity.id,
                    "target": scene_id,
                    "type": "LOCATION_STAY",
                    "weight": 1.0,
                    "stardate": self.meta_manager.convert_to_stardate(current_time),
                    "metadata": {
                        "is_alive": getattr(entity, "is_alive", True)
                    }
                }

                # --- World Rule 判定 ---
                if not self._apply_world_rules(entity, edge):
                    logger.warning(
                        f"World Rule によりエッジ生成拒否: entity={entity.id}, scene={scene_id}"
                    )
                    continue

                # --- ConsistencyValidator 呼び出し（将来拡張） ---
                # 現段階では最小実装としてスキップ可能
                # TODO: context + validation_result を接続

                self.graph["edges"].append(edge)

        return self.graph

    def render_timeline(self) -> List[Dict[str, Any]]:
        """
        グラフからタイムラインを生成する。

        Returns:
            NarrativeUnit のリスト
        """

        edges = self.graph.get("edges", [])

        if not edges:
            return []

        # Stardate 昇順ソート
        sorted_edges = sorted(edges, key=lambda e: e.get("stardate", 0.0))

        timeline = []

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
        try:
            self.meta_manager.check_timeline_linearity(timeline)
        except Exception as e:
            logger.error(f"Timeline 整合性エラー: {e}")

        return timeline

    def _apply_world_rules(self, entity: Any, edge: Dict[str, Any]) -> bool:
        """
        World Rule に基づく行動可否判定

        なぜ必要か：
        - 因果律は固定ではなく世界設定に依存するため
        - Narrative Relativity 原則の実装

        Args:
            entity: 対象エンティティ
            edge: 生成予定エッジ

        Returns:
            bool: 許可可否
        """

        # validator から world_rules を取得（存在しない場合は空）
        world_rules = getattr(self.validator, "world_rules", {})

        is_alive = getattr(entity, "is_alive", True)

        # --- ゴースト行動 ---
        allow_ghost = world_rules.get("allow_ghost_activity", False)

        if not is_alive and not allow_ghost:
            return False

        # --- 将来拡張 ---
        # allow_resurrection
        # allow_time_reversal
        # など

        return True


# メインガード（テスト用）
if __name__ == "__main__":
    logger.info("StoryEngine standalone test start")

# [EOF]