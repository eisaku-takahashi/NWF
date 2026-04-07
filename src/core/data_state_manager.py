"""
Source: src/core/data_state_manager.py
Updated: 2026-04-07T20:42:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Core_Spec/NWF_Data_Model_v2.0.1.md
    - docs/spec/Core_Spec/NWF_State_Transition_Model_v2.0.1.md
    - docs/spec/Kernel_Spec/NWF_Kernel_Audit_System_Spec_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
Docstring:
    Data State Manager モジュール。

    DataStateMachine による論理検証を通過した状態遷移を、
    実データへ適用するオーケストレーション層。

    MetadataManager / VersionManager / AuditLogManager と連携し、
    因果律（Causality）を保証する。
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, Any

# ============================================================
# Time Policy (JST)
# ============================================================

JST = timezone(timedelta(hours=9))

# ============================================================
# Constants
# ============================================================

STATE_REVIEW = "REVIEW"
STATE_APPROVED = "APPROVED"

# ============================================================
# Public Interface
# ============================================================

__all__ = [
    "DataStateManager",
]

# ============================================================
# Utility Functions
# ============================================================

def now_jst_iso() -> str:
    """
    JST の現在時刻を ISO8601 形式で取得する。

    Returns:
        str: 現在時刻（ISO8601形式）
    """
    return datetime.now(JST).isoformat()

# ============================================================
# Data State Manager
# ============================================================

class DataStateManager:
    """
    Data State Manager

    状態遷移を「論理 → メタデータ → 状態 → バージョン → 監査」の順で
    原子的に実行するオーケストレーションコンポーネント。

    Args:
        state_machine: DataStateMachine
        metadata_manager: MetadataManager
        version_manager: VersionManager
        audit_log_manager: AuditLogManager
    """

    def __init__(
        self,
        state_machine,
        metadata_manager,
        version_manager,
        audit_log_manager,
    ):
        """
        初期化

        Args:
            state_machine: DataStateMachine
            metadata_manager: MetadataManager
            version_manager: VersionManager
            audit_log_manager: AuditLogManager
        """
        self.state_machine = state_machine
        self.metadata_manager = metadata_manager
        self.version_manager = version_manager
        self.audit_log_manager = audit_log_manager

    # --------------------------------------------------------
    # Main API
    # --------------------------------------------------------

    def change_state(
        self,
        entity: Dict[str, Any],
        next_state: str,
        actor_id: str,
        transaction_id: str,
    ) -> Dict[str, Any]:
        """
        Entity の状態を変更する（Hotfix準拠）

        Args:
            entity (Dict[str, Any]): 対象 Entity
            next_state (str): 遷移先状態
            actor_id (str): 操作者ID
            transaction_id (str): トランザクションID

        Returns:
            Dict[str, Any]: 更新後 Entity

        Raises:
            ValueError: 入力不正
            Exception: 状態遷移エラー（StateMachine由来）
        """

        # ----------------------------------------------------
        # 入力検証（因果律保証のため必須）
        # ----------------------------------------------------

        if not isinstance(entity, dict):
            raise ValueError("entity must be dict")

        if not actor_id:
            raise ValueError("actor_id is required")

        if not transaction_id:
            raise ValueError("transaction_id is required")

        if "state" not in entity:
            raise ValueError("entity must have 'state'")

        if "subject_id" not in entity:
            raise ValueError("entity must have 'subject_id'")

        current_state = entity.get("state")

        # ----------------------------------------------------
        # 1. 状態遷移の論理検証（Hotfix対応）
        # ----------------------------------------------------
        self.state_machine.validate_transition(current_state, next_state)

        # ----------------------------------------------------
        # 2. Immutableコピー生成
        # ----------------------------------------------------
        updated_entity = dict(entity)

        # ----------------------------------------------------
        # 3. Metadata更新（委譲）
        # ----------------------------------------------------
        updated_entity = self.metadata_manager.update_metadata(
            updated_entity,
            actor_id=actor_id,
            transaction_id=transaction_id,
        )

        # ----------------------------------------------------
        # 4. 状態適用
        # ----------------------------------------------------
        updated_entity["state"] = next_state

        # ----------------------------------------------------
        # 5. Version管理（論理確定ポイントのみ）
        # ----------------------------------------------------
        if next_state in [STATE_REVIEW, STATE_APPROVED]:
            updated_entity = self.version_manager.increment_version(updated_entity)

        # ----------------------------------------------------
        # 6. 監査ログ記録（最終確定）
        # ----------------------------------------------------
        self.audit_log_manager.record_event(
            event_type="STATE_TRANSITION",
            actor_id=actor_id,
            target_id=updated_entity.get("subject_id"),
            payload={
                "from": current_state,
                "to": next_state,
            },
            transaction_id=transaction_id,
        )

        return updated_entity


# ============================================================
# Main Guard
# ============================================================

if __name__ == "__main__":
    print("DataStateManager module (Hotfix Applied)")


# [EOF]