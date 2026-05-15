"""
Source: tests/unit/test_validator_critical_only.py
Updated: 2026-05-15T22:39:00+09:00  # ★Phase 3.5 Spec同期検証反映
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Execution_Spec/NWF_Validator_And_Context_Contract_v2.0.1.md
    - docs/spec/Execution_Spec/NWF_Consistency_Validator_Spec_v2.0.1_Phase_3.5.md
    - docs/spec/Execution_Spec/NWF_Validation_System_v2.0.1.md
    - docs/spec/Execution_Spec/NWF_Validator_Orchestration_Spec_v2.0.1.md
    - docs/spec/Execution_Spec/NWF_Mock_Design_Guideline_v2.0.1.md
    - docs/spec/Core_Spec/NWF_Entity_ID_System_v2.0.1.md
    - docs/spec/Core_Spec/NWF_Story_Database_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
    - docs/project/NWF_Phase_3.5_Debug_Work_Plan_v20260502.md
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
    - UUID Missing Policy を考慮したSpec同期検証を追加
    - INFO混在禁止仕様を追加検証
    - StoryDB Interface統一仕様との整合性確認を追加

    注意：
    - story_db を利用して過去状態を注入し、意図的に不変性違反を発生させる
    - 副作用なし・完全決定論的
    - Entity ID は外部I/F上すべて str として扱う
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
# 公開インターフェース
# =========================================================
# 修正追加：
# NWF Python Implementation Rules v2.0.1
# 「Encapsulation / 公開インターフェース規則」準拠
__all__ = [
    "DummyEntity",
    "MockStoryDB",
    "create_context",
    "TestValidatorCriticalOnly"
]


# =========================================================
# モック定義
# =========================================================
class DummyEntity:
    """
    不変フィールドを持つエンティティ

    Args:
        entity_id (str): Entity ID
        uuid_val (Optional[str]): UUID値

    Notes:
        - Entity ID は Spec 準拠で str 固定
        - UUID Missing Policy 検証のため None 許容
    """

    def __init__(self, entity_id: str, uuid_val):
        # 修正前:
        # self.id = entity_id
        #
        # 修正後:
        # Entity ID型揺れ排除のため str に正規化
        self.id = str(entity_id)

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
    - 本番 StoryDB Interface 契約との同期維持

    Notes:
        - get(entity_id: str) -> Optional[Entity]
        - 非存在時は None を返す
    """

    # -------------------------------------------------
    # 修正前コード（削除禁止ポリシーによりコメント保持）
    # -------------------------------------------------
    # 理由：
    # - Validator は get_previous_state を使用していない
    # - StoryDB I/F 仕様と不整合
    # - Mock内部構造漏洩の原因
    #
    # def __init__(self, previous_entities):
    #     self.previous_entities = previous_entities
    #
    # def get_previous_state(self, transaction_id: str):
    #     return {
    #         "global_vars": self.previous_entities
    #     }

    # -------------------------------------------------
    # 修正後コード（Spec準拠）
    # -------------------------------------------------
    def __init__(self, data: dict):
        """
        Args:
            data (dict): Entity辞書
        """

        # 修正前:
        # self._data = data
        #
        # 修正後:
        # Entity ID の型揺れ防止のため
        # key を str に正規化
        self._data = {
            str(key): value
            for key, value in data.items()
        }

    def get(self, entity_id: str):
        """
        entity_id に対応する過去Entityを取得する

        Args:
            entity_id (str): エンティティID

        Returns:
            Optional[Entity]:
                過去状態（存在しない場合はNone）
        """

        # 修正前:
        # return self._data.get(str(entity_id))
        #
        # 修正後:
        # StoryDB Interface Spec に完全準拠
        normalized_id = str(entity_id)

        return self._data.get(normalized_id)


# =========================================================
# Utility Functions
# =========================================================
def create_context(current_entities):
    """
    WorkflowContext生成

    Args:
        current_entities (dict):
            現在のエンティティ群

    Returns:
        WorkflowContext

    Notes:
        - Validator が参照する global_vars を注入
        - transaction_id は str UUID を使用
    """

    context = WorkflowContext(
        metadata={},
        world_rules={},
        transaction=[],
        current_stardate=1.000001
    )

    # -------------------------------------------------
    # 修正前:
    # context.transaction_id = str(uuid.uuid4())
    #
    # 修正後:
    # Entity / Transaction 系I/Fは
    # 外部公開型を str に統一
    # -------------------------------------------------
    context.transaction_id = str(uuid.uuid4())

    # Validatorが参照する現在状態
    context.global_vars = current_entities

    return context


# =========================================================
# Test Class
# =========================================================
class TestValidatorCriticalOnly(unittest.TestCase):
    """
    Validator単体CRITICAL生成保証テスト
    """

    def test_immutability_breach_generates_critical(self):
        """
        IMMUTABILITY_BREACH → CRITICAL が生成されること

        検証内容：
        - uuid変更で violation が発生
        - CRITICALにマッピングされる
        - INFOが混在しない
        - Engineで停止する

        Spec同期検証：
        - StoryDB I/F準拠
        - Entity ID str 正規化
        - Severity Monotonicity Rule
        - UUID比較仕様
        """

        # -------------------------------------------------
        # 旧状態（DB）
        # -------------------------------------------------
        prev_entity = DummyEntity(
            entity_id="entity_001",
            uuid_val="UUID_OLD"
        )

        previous_entities = {
            "entity_001": prev_entity
        }

        story_db = MockStoryDB(previous_entities)

        # -------------------------------------------------
        # 現在状態（変更あり）
        # -------------------------------------------------
        current_entity = DummyEntity(
            entity_id="entity_001",
            uuid_val="UUID_NEW"
        )

        current_entities = {
            "entity_001": current_entity
        }

        context = create_context(current_entities)

        # -------------------------------------------------
        # Validator実行
        # -------------------------------------------------
        validator = ConsistencyValidator(
            story_db=story_db
        )

        results = validator.validate(
            context,
            current_entity
        )

        # -------------------------------------------------
        # DEBUGログ
        # -------------------------------------------------
        # 修正前:
        # print("DEBUG results:", results)
        # print("DEBUG severities:", [r.severity for r in results])
        #
        # 修正後:
        # DEBUGログを維持しつつ用途を明文化
        print("DEBUG results:", results)
        print(
            "DEBUG severities:",
            [r.severity for r in results]
        )

        # -------------------------------------------------
        # Validator単体検証
        # -------------------------------------------------

        # 結果存在確認
        self.assertTrue(
            len(results) > 0,
            "ValidationResult が生成されていない"
        )

        # CRITICAL存在確認
        self.assertTrue(
            any(
                r.severity == NWFSeverity.CRITICAL
                for r in results
            ),
            "IMMUTABILITY_BREACH が CRITICAL に昇格していない"
        )

        # -------------------------------------------------
        # 修正追加：
        # INFO混在禁止仕様検証
        #
        # Work Plan:
        # violation存在時はINFOを生成しない
        # -------------------------------------------------
        self.assertFalse(
            any(
                r.severity == NWFSeverity.INFO
                for r in results
            ),
            "Violation存在時に INFO が混在している"
        )

        # -------------------------------------------------
        # Engine停止検証
        # -------------------------------------------------
        engine = StoryEngine(adapter=None)

        print(
            "[TEST → Engine]",
            [r.severity for r in results]
        )

        with self.assertRaises(RuntimeError):
            engine.evaluate_validation_results(results)

    def test_uuid_missing_policy_does_not_generate_critical(self):
        """
        UUID Missing Policy 検証

        検証内容：
        - previous.uuid is None
        - current.uuid is None

        の場合、
        violation として扱わないことを確認する

        対応Spec：
        - NWF_Consistency_Validator_Spec_v2.0.1_Phase_3.5
        - 10.6 UUID Missing Policy
        """

        # -------------------------------------------------
        # 旧状態（UUIDなし）
        # -------------------------------------------------
        prev_entity = DummyEntity(
            entity_id="entity_002",
            uuid_val=None
        )

        previous_entities = {
            "entity_002": prev_entity
        }

        story_db = MockStoryDB(previous_entities)

        # -------------------------------------------------
        # 現在状態（UUIDなし）
        # -------------------------------------------------
        current_entity = DummyEntity(
            entity_id="entity_002",
            uuid_val=None
        )

        current_entities = {
            "entity_002": current_entity
        }

        context = create_context(current_entities)

        validator = ConsistencyValidator(
            story_db=story_db
        )

        results = validator.validate(
            context,
            current_entity
        )

        print(
            "DEBUG UUID Missing Policy results:",
            results
        )

        # -------------------------------------------------
        # 修正追加：
        # UUID Missing Policy 検証
        #
        # None 同士は violation 扱いしない
        # -------------------------------------------------
        self.assertFalse(
            any(
                r.severity == NWFSeverity.CRITICAL
                for r in results
            ),
            "UUID Missing Policy に違反している"
        )


# =========================================================
# Main Guard
# =========================================================
if __name__ == "__main__":
    unittest.main()

# [EOF]