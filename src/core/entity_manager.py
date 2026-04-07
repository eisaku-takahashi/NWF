"""
Source: src/core/entity_manager.py
Updated: 2026-04-07T22:20:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Core_Spec/NWF_Data_Model_v2.0.1.md
    - docs/spec/Core_Spec/NWF_Entity_ID_System_v2.0.1.md
    - docs/spec/Core_Spec/NWF_State_Transition_Model_v2.0.1.md
    - docs/spec/Core_Spec/NWF_File_System_v2.0.1.md
    - docs/spec/Kernel_Spec/NWF_Kernel_Audit_System_Spec_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
Docstring:
    Entity Manager モジュール。

    Entity の生成・取得・更新・論理削除を統制し、
    物理（File）・論理（State）・時間（Audit）を transaction_id で統合する。
"""

import json
import os
from typing import Dict, Optional, Any

from src.models.nwf_object import NWFObject
from src.core.id_generator import IdGenerator
from src.core.metadata_manager import MetadataManager
from src.core.data_state_manager import DataStateManager
from src.core.data_state_machine import DataStateMachine
from src.core.version_manager import VersionManager
from src.core.audit_log_manager import AuditLogManager

# ============================================================
# Constants
# ============================================================

DEFAULT_ENTITY_DIR = "data/state/entities"

# ============================================================
# Public Interface
# ============================================================

__all__ = [
    "EntityManager",
]

# ============================================================
# Entity Manager
# ============================================================

class EntityManager:
    """
    EntityManager クラス。

    Entity のライフサイクル管理と因果律同期を担う。
    """

    def __init__(
        self,
        entity_dir: str = DEFAULT_ENTITY_DIR,
        id_generator: Optional[IdGenerator] = None,
        metadata_manager: Optional[MetadataManager] = None,
        state_manager: Optional[DataStateManager] = None,
        version_manager: Optional[VersionManager] = None,
        audit_log_manager: Optional[AuditLogManager] = None,
    ):
        """
        初期化処理。
        """

        self.entity_dir = entity_dir
        self.registry: Dict[str, NWFObject] = {}

        self.id_generator = id_generator or IdGenerator()
        self.metadata_mgr = metadata_manager or MetadataManager()
        self.version_mgr = version_manager or VersionManager()
        self.audit_mgr = audit_log_manager or AuditLogManager()

        # Hotfix: DataStateMachine 実インスタンスを必ず渡す
        self.state_mgr = state_manager or DataStateManager(
            state_machine=DataStateMachine(),
            metadata_manager=self.metadata_mgr,
            version_manager=self.version_mgr,
            audit_log_manager=self.audit_mgr,
        )

        os.makedirs(self.entity_dir, exist_ok=True)

    # ========================================================
    # Create
    # ========================================================

    def create_entity(
        self,
        entity_type: str,
        attributes: Dict[str, Any],
        actor_id: str,
        transaction_id: str,
    ) -> NWFObject:

        if not transaction_id:
            raise ValueError("transaction_id is required")

        subject_id = self.id_generator.generate_id(entity_type)

        metadata = self.metadata_mgr.create_metadata(
            actor_id=actor_id,
            transaction_id=transaction_id,
        )

        entity = NWFObject(
            subject_id=subject_id,
            entity_type=entity_type,
            state="DRAFT",
            attributes=attributes,
            relationships={},
            metadata=metadata,
            version=1,
        )

        self._save_entity(entity)
        self.registry[subject_id] = entity

        event_id = self.audit_mgr.record_event(
            event_type="ENTITY_CREATED",
            actor_id=actor_id,
            target_id=subject_id,
            payload={"entity_type": entity_type},
            transaction_id=transaction_id,
        )

        self.metadata_mgr.update_audit_context(
            entity.metadata,
            transaction_id=transaction_id,
            event_id=event_id,
        )

        self._save_entity(entity)

        return entity

    # ========================================================
    # Read
    # ========================================================

    def get_entity(self, subject_id: str) -> Optional[NWFObject]:

        if subject_id in self.registry:
            return self.registry[subject_id]

        path = self._get_entity_path(subject_id)
        if not os.path.exists(path):
            return None

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        entity = NWFObject.from_dict(data)
        self.registry[subject_id] = entity
        return entity

    # ========================================================
    # Update
    # ========================================================

    def update_entity(
        self,
        subject_id: str,
        updates: Dict[str, Any],
        actor_id: str,
        transaction_id: str,
    ) -> bool:

        if not transaction_id:
            raise ValueError("transaction_id is required")

        entity = self.get_entity(subject_id)
        if not entity:
            return False

        entity_dict = entity.to_dict()

        entity_dict = self.metadata_mgr.update_metadata(
            entity_dict,
            actor_id=actor_id,
            transaction_id=transaction_id,
        )

        entity_dict["attributes"].update(updates)

        entity_dict = self.version_mgr.increment_version(entity_dict)

        updated_entity = NWFObject.from_dict(entity_dict)
        self._save_entity(updated_entity)

        event_id = self.audit_mgr.record_event(
            event_type="ENTITY_UPDATED",
            actor_id=actor_id,
            target_id=subject_id,
            payload={"updates": updates},
            transaction_id=transaction_id,
        )

        self.metadata_mgr.update_audit_context(
            updated_entity.metadata,
            transaction_id=transaction_id,
            event_id=event_id,
        )

        self._save_entity(updated_entity)
        self.registry[subject_id] = updated_entity

        return True

    # ========================================================
    # Delete (Logical)
    # ========================================================

    def delete_entity(
        self,
        subject_id: str,
        actor_id: str,
        transaction_id: str,
    ) -> bool:

        if not transaction_id:
            raise ValueError("transaction_id is required")

        entity = self.get_entity(subject_id)
        if not entity:
            return False

        entity_dict = entity.to_dict()

        # Hotfix: next_state に修正
        updated_dict = self.state_mgr.change_state(
            entity=entity_dict,
            next_state="ARCHIVED",
            actor_id=actor_id,
            transaction_id=transaction_id,
        )

        updated_entity = NWFObject.from_dict(updated_dict)

        self._save_entity(updated_entity)

        event_id = self.audit_mgr.record_event(
            event_type="ENTITY_DELETED",
            actor_id=actor_id,
            target_id=subject_id,
            payload={"state": "ARCHIVED"},
            transaction_id=transaction_id,
        )

        self.metadata_mgr.update_audit_context(
            updated_entity.metadata,
            transaction_id=transaction_id,
            event_id=event_id,
        )

        self._save_entity(updated_entity)
        self.registry[subject_id] = updated_entity

        return True

    # ========================================================
    # Internal
    # ========================================================

    def _get_entity_path(self, subject_id: str) -> str:
        return os.path.join(self.entity_dir, f"{subject_id}.json")

    def _save_entity(self, entity: NWFObject) -> None:
        try:
            with open(self._get_entity_path(entity.subject_id), "w", encoding="utf-8") as f:
                json.dump(entity.to_dict(), f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise IOError(f"Failed to save entity: {entity.subject_id}") from e


# ============================================================
# Main Guard
# ============================================================

if __name__ == "__main__":
    print("EntityManager ready.")


# [EOF]