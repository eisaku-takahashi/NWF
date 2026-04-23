"""
Source: tests/unit/test_validator_critical_only.py
Updated: 2026-04-23T06:22:00+09:00  # ★Phase 3.4 Engine単体CRITICAL停止テスト統合（evaluate接続）
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

    ★Phase 3.4 最終拡張（今回）:
    - Engine.evaluate_validation_results() を直接呼び出し
    - Engine単体でもCRITICAL停止が発火することを検証
    - Pipeline非依存での最終停止保証

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
    過去状態を返すモックDB
    """

    def __init__(self, previous_entities):
        self.previous_entities = previous_entities

    def get_previous_state(self, transaction_id: str):
        return {
            "global_vars": self.previous_entities
        }


# =========================================================
# Utility
# =========================================================
def create_context(current_entities):
    """
    WorkflowContext生成
    """

    context = WorkflowContext(
        metadata={},
        world_rules={},
        transaction=[],
        current_stardate=1.000001
    )

    context.transaction_id = str(uuid.uuid4())

    # ★ Validatorが参照するため直接注入
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
        - uuid を変更した場合に violation が発生
        - その violation が CRITICAL にマッピングされる

        ★追加検証（Phase 3.4）:
        - Engine.evaluate に渡した場合も停止すること
        - Pipeline非依存でCRITICALが維持されること
        """

        # -----------------------------
        # 旧状態（DB側）
        # -----------------------------
        prev_entity = DummyEntity("entity_001", "UUID_OLD")

        previous_entities = {
            "entity_001": prev_entity
        }

        story_db = MockStoryDB(previous_entities)

        # -----------------------------
        # 現在状態（変更あり）
        # -----------------------------
        current_entity = DummyEntity("entity_001", "UUID_NEW")  # ← 変更

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
        # デバッグ出力（明示的トレース）
        # -----------------------------
        print("DEBUG results:", results)
        print("DEBUG severities:", [r.severity for r in results])

        # -----------------------------
        # 検証（Validator単体）
        # -----------------------------
        # ★ 少なくとも1件は存在
        self.assertTrue(len(results) > 0)

        # ★ CRITICALが含まれること
        self.assertTrue(
            any(r.severity == NWFSeverity.CRITICAL for r in results),
            "IMMUTABILITY_BREACH が CRITICAL に昇格していない"
        )

        # =====================================================
        # ★ Phase 3.4 追加: Engine単体停止テスト
        # =====================================================

        # -----------------------------
        # 修正前（保持）
        # -----------------------------
        # 旧設計では Engine を経由しないため、
        # CRITICALが実際に停止に結びつくかは未検証だった
        #
        # 問題:
        # - Pipeline終端保証が存在しない
        # - CRITICALが「観測値」で終わる可能性

        # -----------------------------
        # 修正後（Engine.evaluate使用）
        # -----------------------------
        engine = StoryEngine(adapter=None)  # Validator単体テストのためAdapter不要

        # ★追加ログ（Engine注入直前）
        print("[TEST → Engine]", [r.severity for r in results])

        # ★最重要検証:
        # Engine単体でもCRITICALで停止すること
        with self.assertRaises(RuntimeError):
            engine.evaluate_validation_results(results)


# =========================================================
# Main Guard
# =========================================================
if __name__ == "__main__":
    unittest.main()

# [EOF]