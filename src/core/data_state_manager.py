"""
Source: src/core/data_state_manager.py
Updated: 2026-04-04T18:20:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Core_Spec/NWF_Data_Model_v2.0.1.md
    - docs/spec/Core_Spec/NWF_State_Transition_Model_v2.0.1.md
    - docs/spec/Core_Spec/NWF_Entity_ID_System_v2.0.1.md
    - docs/spec/Kernel_Spec/NWF_Kernel_Audit_System_Spec_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
Docstring:
    Data State Manager モジュール。
    Entity の状態遷移、バージョン状態管理、Integrity Check トリガー、
    Audit Log 記録のオーケストレーションを行う。
    NWF Core Data Control Layer の中心モジュール。
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional

# JST タイムゾーン定義
JST = timezone(timedelta(hours=9))

# 状態定義
STATE_DRAFT = "DRAFT"
STATE_REVIEW = "REVIEW"
STATE_APPROVED = "APPROVED"
STATE_FROZEN = "FROZEN"
STATE_ARCHIVED = "ARCHIVED"

VALID_STATES = {
    STATE_DRAFT,
    STATE_REVIEW,
    STATE_APPROVED,
    STATE_FROZEN,
    STATE_ARCHIVED,
}

# 状態遷移ルール
STATE_TRANSITIONS = {
    STATE_DRAFT: [STATE_REVIEW, STATE_ARCHIVED],
    STATE_REVIEW: [STATE_APPROVED, STATE_DRAFT, STATE_ARCHIVED],
    STATE_APPROVED: [STATE_FROZEN, STATE_ARCHIVED],
    STATE_FROZEN: [STATE_ARCHIVED],
    STATE_ARCHIVED: [],
}

__all__ = [
    "DataStateManager",
]


def get_current_timestamp() -> str:
    """
    現在のJST時刻をISO8601形式で取得する。

    Returns:
        str: ISO8601形式のタイムスタンプ
    """
    return datetime.now(JST).isoformat()


class DataStateManager:
    """
    Data State Manager

    Entity の状態遷移を管理し、
    状態遷移時に Audit Log / Integrity Check / Version Control などの
    各システムとの連携を行う。

    Responsibilities:
        - Entity State 管理
        - State Transition Validation
        - State Transition 実行
        - Audit Log 記録
        - Integrity Check Trigger
        - Version Freeze 管理
    """

    def __init__(self, audit_logger=None, integrity_checker=None, version_manager=None):
        """
        DataStateManager 初期化

        Args:
            audit_logger: Audit Logger インスタンス
            integrity_checker: Integrity Checker インスタンス
            version_manager: Version Manager インスタンス
        """
        self.audit_logger = audit_logger
        self.integrity_checker = integrity_checker
        self.version_manager = version_manager

    def validate_state_transition(self, current_state: str, new_state: str) -> bool:
        """
        状態遷移が有効かどうかを検証する。

        Args:
            current_state (str): 現在の状態
            new_state (str): 遷移先の状態

        Returns:
            bool: 遷移可能なら True

        Raises:
            ValueError: 不正な状態遷移
        """
        if current_state not in VALID_STATES:
            raise ValueError(f"Invalid current state: {current_state}")

        if new_state not in VALID_STATES:
            raise ValueError(f"Invalid new state: {new_state}")

        allowed_states = STATE_TRANSITIONS.get(current_state, [])

        if new_state not in allowed_states:
            raise ValueError(
                f"Invalid state transition: {current_state} -> {new_state}"
            )

        return True

    def change_state(self, entity: Dict[str, Any], new_state: str, actor_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Entity の状態を変更する。

        Args:
            entity (dict): Entity データ
            new_state (str): 新しい状態
            actor_id (str, optional): 操作主体 ID

        Returns:
            dict: 更新された Entity
        """
        current_state = entity.get("state")

        # 状態遷移検証
        self.validate_state_transition(current_state, new_state)

        # Integrity Check トリガー（REVIEW 移行時）
        if new_state == STATE_REVIEW and self.integrity_checker:
            self.integrity_checker.run_entity_check(entity)

        # Version Freeze 処理
        if new_state == STATE_FROZEN and self.version_manager:
            self.version_manager.freeze_entity_version(entity)

        # 状態更新
        entity["state"] = new_state
        entity["updated_at"] = get_current_timestamp()

        # Audit Log 記録
        self._log_state_change(entity, current_state, new_state, actor_id)

        return entity

    def freeze_entity(self, entity: Dict[str, Any], actor_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Entity を FROZEN 状態にする。

        Args:
            entity (dict): Entity
            actor_id (str): 操作主体

        Returns:
            dict: 更新された Entity
        """
        return self.change_state(entity, STATE_FROZEN, actor_id)

    def archive_entity(self, entity: Dict[str, Any], actor_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Entity を ARCHIVED 状態にする。

        Args:
            entity (dict): Entity
            actor_id (str): 操作主体

        Returns:
            dict: 更新された Entity
        """
        return self.change_state(entity, STATE_ARCHIVED, actor_id)

    def _log_state_change(
        self,
        entity: Dict[str, Any],
        old_state: str,
        new_state: str,
        actor_id: Optional[str],
    ) -> None:
        """
        状態遷移を Audit Log に記録する。

        Args:
            entity (dict): Entity
            old_state (str): 変更前状態
            new_state (str): 変更後状態
            actor_id (str): 操作主体
        """
        if not self.audit_logger:
            return

        log_entry = {
            "timestamp": get_current_timestamp(),
            "event_type": "STATE_CHANGE",
            "entity_id": entity.get("id"),
            "old_state": old_state,
            "new_state": new_state,
            "actor_id": actor_id,
        }

        self.audit_logger.log_event(log_entry)


if __name__ == "__main__":
    # 簡易テスト
    manager = DataStateManager()

    test_entity = {
        "id": "CHR-TEST-001",
        "state": "DRAFT",
        "created_at": get_current_timestamp(),
        "updated_at": get_current_timestamp(),
    }

    test_entity = manager.change_state(test_entity, "REVIEW")
    test_entity = manager.change_state(test_entity, "APPROVED")

    print(test_entity)

# [EOF]