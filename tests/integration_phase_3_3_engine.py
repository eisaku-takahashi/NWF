"""
Source: tests/integration_phase_3_3_engine.py
Updated: 2026-04-17T10:43:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - src/engine/story_engine.py
    - src/core/metadata_manager.py
    - src/integrity/consistency_validator.py
Docstring:
    Phase 3.3 Story Engine の統合テスト。
    World Rule による挙動分岐、Graph生成、Timeline整合性を検証する。
"""

import unittest
from datetime import datetime, timezone, timedelta

from src.core.metadata_manager import MetadataManager
from src.integrity.consistency_validator import ConsistencyValidator
from src.engine.story_engine import StoryEngine

__all__ = [
    "TestPhase33StoryEngine"
]


class MockEntity:
    """
    テスト用モックエンティティ
    """

    def __init__(self, entity_id, entity_type="character", is_alive=True, related_scenes=None):
        self.id = entity_id
        self.type = entity_type
        self.is_alive = is_alive
        self.related_scenes = related_scenes or []


class TestPhase33StoryEngine(unittest.TestCase):
    """
    Phase 3.3 Story Engine 統合テスト
    """

    def setUp(self):
        """
        テスト初期化
        """
        self.meta = MetadataManager()
        self.validator = ConsistencyValidator()

        # world_rules 初期化（存在しない場合の安全対策）
        if not hasattr(self.validator, "world_rules"):
            self.validator.world_rules = {}

        self.engine = StoryEngine(self.meta, self.validator)

    def test_01_graph_generation_normal(self):
        """
        正常系：生存キャラのエッジ生成確認
        """
        print("\n[Test 01] Graph Generation (Normal)")

        char_a = MockEntity("CHAR-A", is_alive=True, related_scenes=["SCENE-B"])
        scene_b = MockEntity("SCENE-B", entity_type="scene")

        graph = self.engine.generate_story_graph([char_a, scene_b])

        self.assertTrue(len(graph["nodes"]) == 2)
        self.assertTrue(len(graph["edges"]) == 1)

        print(" -> SUCCESS: 生存キャラのエッジ生成確認")

    def test_02_world_rule_ghost_block(self):
        """
        World Rule：幽霊行動禁止
        """
        print("\n[Test 02] World Rule (Ghost Block)")

        ghost = MockEntity("GHOST-X", is_alive=False, related_scenes=["SCENE-B"])
        scene = MockEntity("SCENE-B", entity_type="scene")

        self.validator.world_rules["allow_ghost_activity"] = False

        graph = self.engine.generate_story_graph([ghost, scene])

        self.assertEqual(len(graph["edges"]), 0)

        print(" -> SUCCESS: ゴースト行動が拒否された")

    def test_03_world_rule_ghost_allow(self):
        """
        World Rule：幽霊行動許可
        """
        print("\n[Test 03] World Rule (Ghost Allow)")

        ghost = MockEntity("GHOST-X", is_alive=False, related_scenes=["SCENE-B"])
        scene = MockEntity("SCENE-B", entity_type="scene")

        self.validator.world_rules["allow_ghost_activity"] = True

        graph = self.engine.generate_story_graph([ghost, scene])

        self.assertEqual(len(graph["edges"]), 1)

        print(" -> SUCCESS: ゴースト行動が許可された")

    def test_04_timeline_sorting(self):
        """
        Timeline の Stardate ソート確認
        """
        print("\n[Test 04] Timeline Sorting")

        self.engine.graph["edges"] = [
            {
                "source": "A",
                "target": "Mars",
                "type": "LOCATION_STAY",
                "stardate": 100.0
            },
            {
                "source": "A",
                "target": "Earth",
                "type": "LOCATION_STAY",
                "stardate": 10.0
            }
        ]

        timeline = self.engine.render_timeline()

        self.assertEqual(timeline[0]["location"], "Earth")
        self.assertEqual(timeline[1]["location"], "Mars")

        print(" -> SUCCESS: Timeline が正しくソートされた")

    def test_05_empty_graph(self):
        """
        空グラフの安全動作確認
        """
        print("\n[Test 05] Empty Graph Handling")

        self.engine.graph["edges"] = []

        timeline = self.engine.render_timeline()

        self.assertEqual(timeline, [])

        print(" -> SUCCESS: 空データ安全処理確認")


if __name__ == "__main__":
    unittest.main()

# [EOF]