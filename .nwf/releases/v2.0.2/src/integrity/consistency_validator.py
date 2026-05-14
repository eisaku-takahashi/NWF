"""
Source: src/integrity/consistency_validator.py
Updated: 2026-04-12T05:47:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Project_Governance/NWF_Recursive_Integrity_Spec_v2.0.1.md
    - docs/spec/Core_Spec/NWF_State_Transition_Model_v2.0.1.md
    - docs/spec/Core_Spec/NWF_World_Rule_Model_v2.0.1.md
    - src/workflow/workflow_context.py
    - src/integrity/integrity_checker.py
Docstring:
    Consistency Validator モジュール。
    WorkflowContext と ValidationResult を入力として受け取り、
    因果律・状態遷移・世界設定・エンティティ連続性の観点から
    論理的整合性（Causal Integrity）を検証する。
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

    Attributes:
        is_consistent (bool): 整合性が保たれているか
        violations (List[str]): 検出された違反一覧
        context_snapshot (Dict[str, Any]): 検証時のコンテキストスナップショット
        transaction_id (str): トランザクションID
        timestamp (datetime): 検証時刻（JST）
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

    WorkflowContext および ValidationResult を基に、
    状態遷移・世界設定・エンティティ連続性を検証する。
    """

    def __init__(self, story_db: Optional[Any] = None):
        """
        初期化処理

        Args:
            story_db (Optional[Any]): 過去データ参照用ストレージ（DataStateManager等）
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

        Args:
            context (WorkflowContext): 現在のワークフローコンテキスト
            prev_result (ValidationResult): 構造整合性検証結果

        Returns:
            ConsistencyResult: 論理整合性検証結果
        """

        res = ConsistencyResult(context.transaction_id)

        # スナップショット保存（監査用）
        res.context_snapshot = self._create_context_snapshot(context)

        # 構造エラーがある場合はスキップ
        if not prev_result.is_valid:
            res.is_consistent = False
            res.violations.append("SKIP: Structural integrity failure.")
            return res

        # 各種チェック
        self._check_state_transition(context, res)
        self._check_world_rule_violation(context, res)
        self._check_entity_continuity(context, res)

        return res

    def _create_context_snapshot(self, context: WorkflowContext) -> Dict[str, Any]:
        """
        コンテキストスナップショット生成

        なぜ必要か：
        - 監査ログとして検証時の状態を保存するため
        - HITL 時の再現性確保のため

        Args:
            context (WorkflowContext): 対象コンテキスト

        Returns:
            Dict[str, Any]: スナップショットデータ
        """
        return {
            "transaction_id": context.transaction_id,
            "metadata": context.metadata,
            "created_at": context.created_at.isoformat(),
            "updated_at": context.updated_at.isoformat(),
        }

    def _check_state_transition(self, context: WorkflowContext, res: ConsistencyResult) -> None:
        """
        状態遷移の因果律チェック

        なぜ必要か：
        - 不正な状態遷移（例：RUNNING → READY）を防ぐため

        Args:
            context (WorkflowContext)
            res (ConsistencyResult)
        """

        current_state = context.metadata.get("state")
        prev_state = context.metadata.get("previous_state")

        # 状態遷移ルール（簡易定義）
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
        世界設定違反チェック

        なぜ必要か：
        - 物理法則や世界観を逸脱した出力を防ぐため

        Args:
            context (WorkflowContext)
            res (ConsistencyResult)
        """

        # 仮実装：metadata に world_rule_flag がある場合チェック
        if context.metadata.get("world_rule_violation"):
            res.is_consistent = False
            res.violations.append(
                "ERR_CAUSAL_002: World rule violation detected."
            )

    def _check_entity_continuity(self, context: WorkflowContext, res: ConsistencyResult) -> None:
        """
        エンティティ連続性チェック

        なぜ必要か：
        - キャラクターやオブジェクトの状態が時系列で矛盾しないようにするため

        Args:
            context (WorkflowContext)
            res (ConsistencyResult)
        """

        if not self.story_db:
            # DB未接続時はスキップ（設計上許容）
            return

        transaction_id = context.transaction_id

        try:
            previous_state = self.story_db.get_previous_state(transaction_id)
        except Exception:
            # 取得失敗時は警告として扱う
            res.violations.append(
                "WARN_CAUSAL_003: Failed to retrieve previous state."
            )
            return

        current_entities = context.global_vars
        previous_entities = previous_state.get("global_vars", {})

        for entity_id, current_obj in current_entities.items():
            prev_obj = previous_entities.get(entity_id)

            if not prev_obj:
                continue

            # 例：生存フラグの逆転チェック
            if hasattr(prev_obj, "is_alive") and hasattr(current_obj, "is_alive"):
                if prev_obj.is_alive is False and current_obj.is_alive is True:
                    res.is_consistent = False
                    res.violations.append(
                        f"ERR_CAUSAL_004: Entity resurrection detected ({entity_id})"
                    )


if __name__ == "__main__":
    # テスト用簡易実行
    pass

# [EOF]