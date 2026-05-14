from src.core.metadata_manager import MetadataManager
from src.integrity.consistency_validator import ConsistencyValidator
from src.engine.story_engine import StoryEngine

# 最小構成のモックエンティティ
class Entity:
    def __init__(self, id, is_alive=True, scenes=None):
        self.id = id
        self.is_alive = is_alive
        self.related_scenes = scenes or []

# 1. コンポーネントの初期化
meta = MetadataManager()
validator = ConsistencyValidator()
# 世界ルールの設定：幽霊の活動を許可する
validator.world_rules["allow_ghost_activity"] = True

engine = StoryEngine(meta, validator)

# 2. サンプルデータの作成
# ルークは砂漠にいる
luke = Entity("Luke Skywalker", is_alive=True, scenes=["Desert Planet"])
# アナキンは死亡しているが、デス・スターに現れる（幽霊設定）
anakin = Entity("Anakin (Ghost)", is_alive=False, scenes=["Death Star"])

entities = [luke, anakin]

# 3. ストーリー生成
print("--- [NWF Story Engine: Generation Start] ---")
graph = engine.generate_story_graph(entities)
timeline = engine.render_timeline()

# 4. 最小ストーリー構造の出力
print(f"\n[Generated Nodes]: {graph['nodes']}")
print("\n[Chronological Timeline]:")
for unit in timeline:
    status = "Alive" if "Ghost" not in unit['actor'] else "Spirit"
    print(f"- Stardate {unit['stardate']:.2f}: {unit['actor']} ({status}) is at {unit['location']}.")

print("\n--- [Execution Complete] ---")
