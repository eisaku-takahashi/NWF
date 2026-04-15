"""
Source: src/integrity/consistency_validator.py
Updated: 2026-04-15T09:37:00+09:00  # 修正後更新
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Project_Governance/NWF_Recursive_Integrity_Spec_v2.0.1.md
    - docs/spec/Core_Spec/NWF_State_Transition_Model_v2.0.1.md
    - docs/spec/Core_Spec/NWF_World_Rule_Model_v2.0.1.md
    - docs/spec/Architecture_Spec/NWF_Narrative_Consistency_Model_v2.0.1.md  # 追加（Spec準拠）
    - docs/spec/Kernel_Spec/NWF_Kernel_Core_Concept_v2.0.1.md  # 追加（不変性チェック用）
    - src/workflow/workflow_context.py
    - src/integrity/integrity_checker.py
Docstring:
    Consistency Validator モジュール。
    WorkflowContext と ValidationResult を入力として受け取り、
    因果律・状態遷移・世界設定・エンティティ連続性の観点から
    論理的整合性（Causal Integrity）を検証する。

    Phase 3.1 対応：
    - 再帰的整合性チェック追加
    - 不変性チェック（Kernel Guard）追加
"""

from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional

from src.workflow.workflow_context import WorkflowContext
from src.integrity.integrity_checker import ValidationResult

# JST タイムゾーン定義
JST = timezone(timedelta(hours=9))

__all__ = [
    "ConsistencyResult",
    "ConsistencyValidator",
]


class ConsistencyResult:
    """
    論理整合性検証結果コンテナ
    """

    def __init__(self, transaction_id: str):
        self.is_consistent: bool = True
        self.violations: List[str] = []
        self.context_snapshot: Dict[str, Any] = {}
        self.transaction_id: str = transaction_id
        self.timestamp: datetime = datetime.now(JST)


class ConsistencyValidator:
    """
    因果律整合性検証クラス
    """

    def __init__(self, story_db: Optional[Any] = None):
        """
        初期化処理

        Args:
            story_db (Optional[Any]): 過去データ参照用ストレージ
        """
        self.story_db = story_db
        self.world_rules: Dict[str, Any] = {}

    def validate(
        self,
        context: WorkflowContext,
        prev_result: ValidationResult
    ) -> ConsistencyResult:
        """
        論理整合性検証メイン処理
        """

        res = ConsistencyResult(context.transaction_id)

        # スナップショット保存（監査用）
        res.context_snapshot = self._create_context_snapshot(context)

        # ------------------------------
        # 修正前:
        # if not prev_result.is_valid:
        #     res.is_consistent = False
        #     res.violations.append("SKIP: Structural integrity failure.")
        #     return res
        #
        # 修正後:
        # Structuralエラーでも不変性チェックは実行する（Spec準拠）
        # ------------------------------
        if not prev_result.is_valid:
            res.violations.append("WARN: Structural integrity failed, partial validation executed.")

        # ------------------------------
        # Phase 3.1 追加: 不変性チェック（最優先）
        # ------------------------------
        self._check_immutability(context, res)

        # 不変性違反は即停止（Spec要件）
        if not res.is_consistent:
            return res

        # ------------------------------
        # 既存チェック
        # ------------------------------
        self._check_state_transition(context, res)
        self._check_world_rule_violation(context, res)

        # ------------------------------
        # 修正前:
        # self._check_entity_continuity(context, res)
        #
        # 修正後:
        # 再帰的整合性チェックへ拡張
        # ------------------------------
        self._check_recursive_consistency(context, res)

        return res

    def _create_context_snapshot(self, context: WorkflowContext) -> Dict[str, Any]:
        """
        コンテキストスナップショット生成
        """
        return {
            "transaction_id": context.transaction_id,
            "metadata": context.metadata,
            "created_at": context.created_at.isoformat(),
            "updated_at": context.updated_at.isoformat(),
        }

    # ------------------------------
    # Phase 3.1 追加
    # ------------------------------
    def _check_immutability(self, context: WorkflowContext, res: ConsistencyResult) -> None:
        """
        Kernel不変性チェック

        なぜ必要か：
        - UUIDや生成日時の改ざんはシステム整合性を破壊するため
        """

        immutable_fields = ["uuid", "created_at", "origin_event_id"]

        current_entities = context.global_vars

        if not self.story_db:
            return

        try:
            previous_state = self.story_db.get_previous_state(context.transaction_id)
        except Exception:
            return

        previous_entities = previous_state.get("global_vars", {})

        for entity_id, current_obj in current_entities.items():
            prev_obj = previous_entities.get(entity_id)

            if not prev_obj:
                continue

            for field in immutable_fields:
                if hasattr(prev_obj, field) and hasattr(current_obj, field):
                    if getattr(prev_obj, field) != getattr(current_obj, field):
                        res.is_consistent = False
                        res.violations.append(
                            f"IMMUTABILITY_BREACH: {entity_id}.{field} modified"
                        )
                        return  # 即停止

    def _check_state_transition(self, context: WorkflowContext, res: ConsistencyResult) -> None:
        """
        状態遷移チェック（変更なし）
        """

        current_state = context.metadata.get("state")
        prev_state = context.metadata.get("previous_state")

        allowed_transitions = {
            "IDLE": ["READY"],
            "READY": ["RUNNING"],
            "RUNNING": ["COMPLETED", "FAILED", "SUSPEND"],
            "SUSPEND": ["RUNNING", "ABORTED"],
            "COMPLETED": ["IDLE"],
            "FAILED": ["IDLE"],
            "ABORTED": ["IDLE"],
        }

        if prev_state and current_state:
            if current_state not in allowed_transitions.get(prev_state, []):
                res.is_consistent = False
                res.violations.append(
                    f"ERR_CAUSAL_001: Invalid state transition {prev_state} -> {current_state}"
                )

    def _check_world_rule_violation(self, context: WorkflowContext, res: ConsistencyResult) -> None:
        """
        世界設定違反チェック（既存）
        """

        if context.metadata.get("world_rule_violation"):
            res.is_consistent = False
            res.violations.append(
                "ERR_CAUSAL_002: World rule violation detected."
            )

    # ------------------------------
    # 修正前:
    # def _check_entity_continuity(...)
    #
    # 修正後:
    # 再帰的整合性チェックへ拡張
    # ------------------------------
    def _check_recursive_consistency(self, context: WorkflowContext, res: ConsistencyResult) -> None:
        """
        再帰的整合性チェック

        なぜ必要か：
        - エンティティ単体ではなく、Scene / Threadとの整合性を保証するため
        """

        if not self.story_db:
            return

        try:
            previous_state = self.story_db.get_previous_state(context.transaction_id)
        except Exception:
            res.violations.append("WARN_CAUSAL_003: Failed to retrieve previous state.")
            return

        current_entities = context.global_vars
        previous_entities = previous_state.get("global_vars", {})

        for entity_id, current_obj in current_entities.items():
            prev_obj = previous_entities.get(entity_id)

            if not prev_obj:
                continue

            # ------------------------------
            # 既存ロジック（保持）
            # ------------------------------
            if hasattr(prev_obj, "is_alive") and hasattr(current_obj, "is_alive"):
                if prev_obj.is_alive is False and current_obj.is_alive is True:
                    res.is_consistent = False
                    res.violations.append(
                        f"ERR_CAUSAL_004: Entity resurrection detected ({entity_id})"
                    )

            # ------------------------------
            # Phase 3.1 追加: 再帰チェック（簡易2階層）
            # ------------------------------
            related_scenes = getattr(current_obj, "related_scenes", [])

            for scene_id in related_scenes:
                scene = current_entities.get(scene_id)

                if not scene:
                    continue

                # 死亡キャラがSceneに存在していないか
                if hasattr(current_obj, "is_alive") and current_obj.is_alive is False:
                    if hasattr(scene, "characters") and entity_id in scene.characters:
                        res.is_consistent = False
                        res.violations.append(
                            f"ERR_CAUSAL_005: মৃত entity {entity_id} appears in scene {scene_id}"
                        )


if __name__ == "__main__":
    # テスト用簡易実行
    pass

# [EOF]