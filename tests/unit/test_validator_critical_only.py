"""
Source: tests/unit/test_validator_critical_only.py
Updated: 2026-05-02T19:57:00+09:00  # ★Phase 3.5 MockStoryDB I/F準拠化対応
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Execution_Spec/NWF_Validator_And_Context_Contract_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
    - src/integrity/consistency_validator.py
    - src/workflow/workflow_context.py
    - src/models/nwf_enums.py
    - src/engine/story_engine.py
Docstring:
    Validator単体におけるCRITICAL生成保証テスト。

    本テストの目的：
    - Pipelineに依存せず、Validator単体でCRITICALが生成されることを保証
    - IMMUTABILITY_BREACH が CRITICAL に正しくマッピングされることを確認
    - Severity Monotonicity Rule の起点（生成点）を検証

    ★Phase 3.4:
    - Engine.evaluate_validation_results() を直接呼び出し
    - Engine単体でもCRITICAL停止が発火することを検証

    ★Phase 3.5:
    - MockStoryDB を story_db.get() I/F に準拠させる
    - ValidatorとのI/F断絶を完全排除

    注意：
    - story_db を利用して過去状態を注入し、意図的に不変性違反を発生させる
    - 副作用なし・完全決定論的
"""

# =========================================================
# import
# =========================================================
import unittest
import uuid
from datetime import timezone, timedelta

from src.integrity.consistency_validator import ConsistencyValidator
from src.workflow.workflow_context import WorkflowContext
from src.models.nwf_enums import NWFSeverity
from src.engine.story_engine import StoryEngine


# =========================================================
# 定数 / 設定
# =========================================================
JST = timezone(timedelta(hours=9))


# =========================================================
# モック定義
# =========================================================
class DummyEntity:
    """
    不変フィールドを持つエンティティ
    """

    def __init__(self, entity_id: str, uuid_val: str):
        self.id = entity_id
        self.uuid = uuid_val
        self.created_at = "2026-01-01"
        self.origin_event_id = "origin_001"
        self.is_alive = True


class MockStoryDB:
    """
    StoryDBのI/Fに準拠したモックDB

    目的：
    - Validatorが依存する story_db.get(entity_id) のみを提供
    - 内部構造を隠蔽（I/F経由アクセスの強制）
    """

    # -----------------------------
    # 修正前コード（削除せず記録）
    # -----------------------------
    # 理由：
    # - Validatorは get_previous_state を使用していない
    # - I/F不整合の原因となっていたため廃止
    #
    # def __init__(self, previous_entities):
    #     self.previous_entities = previous_entities
    #
    # def get_previous_state(self, transaction_id: str):
    #     return {
    #         "global_vars": self.previous_entities
    #     }

    # -----------------------------
    # 修正後コード（I/F準拠）
    # -----------------------------
    def __init__(self, data: dict):
        # 内部データ（外部非公開）
        self._data = data

    def get(self, entity_id: str):
        """
        entity_id に対応する過去Entityを取得する

        Args:
            entity_id (str): エンティティID

        Returns:
            Optional[Entity]: 過去状態（存在しない場合はNone）
        """
        # IDをstrに正規化（Spec準拠）
        return self._data.get(str(entity_id))


# =========================================================
# Utility
# =========================================================
def create_context(current_entities):
    """
    WorkflowContext生成

    Args:
        current_entities (dict): 現在のエンティティ群

    Returns:
        WorkflowContext
    """

    context = WorkflowContext(
        metadata={},
        world_rules={},
        transaction=[],
        current_stardate=1.000001
    )

    context.transaction_id = str(uuid.uuid4())

    # Validatorが参照する現在状態
    context.global_vars = current_entities

    return context


# =========================================================
# Test Class
# =========================================================
class TestValidatorCriticalOnly(unittest.TestCase):

    def test_immutability_breach_generates_critical(self):
        """
        IMMUTABILITY_BREACH → CRITICAL が生成されること

        検証内容：
        - uuid変更で violation が発生
        - CRITICALにマッピングされる
        - Engineで停止する
        """

        # -----------------------------
        # 旧状態（DB）
        # -----------------------------
        prev_entity = DummyEntity("entity_001", "UUID_OLD")

        previous_entities = {
            "entity_001": prev_entity
        }

        story_db = MockStoryDB(previous_entities)

        # -----------------------------
        # 現在状態（変更あり）
        # -----------------------------
        current_entity = DummyEntity("entity_001", "UUID_NEW")

        current_entities = {
            "entity_001": current_entity
        }

        context = create_context(current_entities)

        # -----------------------------
        # Validator実行
        # -----------------------------
        validator = ConsistencyValidator(story_db=story_db)

        results = validator.validate(context, current_entity)

        # -----------------------------
        # デバッグ出力
        # -----------------------------
        print("DEBUG results:", results)
        print("DEBUG severities:", [r.severity for r in results])

        # -----------------------------
        # 検証（Validator単体）
        # -----------------------------
        self.assertTrue(len(results) > 0)

        self.assertTrue(
            any(r.severity == NWFSeverity.CRITICAL for r in results),
            "IMMUTABILITY_BREACH が CRITICAL に昇格していない"
        )

        # -----------------------------
        # Engine停止検証
        # -----------------------------
        engine = StoryEngine(adapter=None)

        print("[TEST → Engine]", [r.severity for r in results])

        with self.assertRaises(RuntimeError):
            engine.evaluate_validation_results(results)


# =========================================================
# Main Guard
# =========================================================
if __name__ == "__main__":
    unittest.main()

# [EOF]