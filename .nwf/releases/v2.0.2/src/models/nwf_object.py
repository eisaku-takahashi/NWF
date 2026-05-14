"""
Source: src/models/nwf_object.py
Updated: 2026-04-07T03:49:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Core_Spec/NWF_Entity_ID_System_v2.0.1.md
    - docs/spec/Core_Spec/NWF_State_Transition_Model_v2.0.1.md
    - docs/spec/Data_Spec/NWF_Data_Spec_Index_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
Docstring:
    NWFObject 基本エンティティモデル。
    NWF システム内のすべてのエンティティの共通データ構造を定義する。
    EntityManager / StateManager / AuditLogManager / VersionManager と連携し、
    データの物理論理整合性および因果律を保証する。
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional

# JST タイムゾーン定義
JST = timezone(timedelta(hours=9))

__all__ = [
    "NWFObject"
]


class NWFObject:
    """
    NWF 基本オブジェクトクラス。

    すべてのエンティティ（Character, Event, Scene, Thread など）の
    共通データ構造を定義する。

    Attributes:
        subject_id (str): エンティティID
        entity_type (str): エンティティ種別
        state (str): 状態
        version (int): バージョン
        relationships (Dict[str, List[str]]): 関係IDリスト
        metadata (Dict[str, Any]): メタデータ
        attributes (Dict[str, Any]): エンティティ固有属性
    """

    REQUIRED_FIELDS = ["subject_id", "entity_type", "state", "metadata"]

    def __init__(
        self,
        subject_id: str,
        entity_type: str,
        state: str,
        metadata: Dict[str, Any],
        version: int = 1,
        relationships: Optional[Dict[str, List[str]]] = None,
        attributes: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        NWFObject 初期化。

        Args:
            subject_id (str): エンティティID
            entity_type (str): エンティティ種別
            state (str): 状態
            metadata (Dict[str, Any]): メタデータ
            version (int, optional): バージョン
            relationships (Dict[str, List[str]], optional): 関係
            attributes (Dict[str, Any], optional): 属性

        Raises:
            ValueError: 必須フィールド不正
        """

        self.subject_id = subject_id
        self.entity_type = entity_type
        self.state = state
        self.version = version
        self.relationships = relationships if relationships is not None else {}
        self.metadata = metadata
        self.attributes = attributes if attributes is not None else {}

        self._validate_required_fields()
        self._validate_types()

    def _validate_required_fields(self) -> None:
        """
        必須フィールド検証。
        """
        for field in self.REQUIRED_FIELDS:
            if getattr(self, field, None) is None:
                raise ValueError(f"Missing required field: {field}")

    def _validate_types(self) -> None:
        """
        型チェック検証。
        """
        if not isinstance(self.subject_id, str):
            raise ValueError("subject_id must be str")

        if not isinstance(self.entity_type, str):
            raise ValueError("entity_type must be str")

        if not isinstance(self.state, str):
            raise ValueError("state must be str")

        if not isinstance(self.relationships, dict):
            raise ValueError("relationships must be dict")

        for key, value in self.relationships.items():
            if not isinstance(value, list):
                raise ValueError("relationships values must be list of IDs")

        if not isinstance(self.metadata, dict):
            raise ValueError("metadata must be dict")

        if not isinstance(self.attributes, dict):
            raise ValueError("attributes must be dict")

    def update_state(self, new_state: str) -> None:
        """
        状態更新。

        Args:
            new_state (str): 新しい状態
        """
        self.state = new_state
        self._update_timestamp()

    def increment_version(self) -> None:
        """
        バージョン更新。
        """
        self.version += 1
        self._update_timestamp()

    def add_relationship(self, relation_type: str, target_id: str) -> None:
        """
        関係追加。

        Args:
            relation_type (str): 関係タイプ
            target_id (str): 対象ID
        """
        if relation_type not in self.relationships:
            self.relationships[relation_type] = []

        if target_id not in self.relationships[relation_type]:
            self.relationships[relation_type].append(target_id)

        self._update_timestamp()

    def _update_timestamp(self) -> None:
        """
        metadata の updated_at 更新。
        """
        if "updated_at" in self.metadata:
            self.metadata["updated_at"] = datetime.now(JST).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """
        オブジェクトを辞書へ変換。

        Returns:
            Dict[str, Any]: 辞書形式
        """
        return {
            "subject_id": self.subject_id,
            "entity_type": self.entity_type,
            "state": self.state,
            "version": self.version,
            "relationships": self.relationships,
            "metadata": self.metadata,
            "attributes": self.attributes
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NWFObject":
        """
        辞書からオブジェクト生成。

        Args:
            data (Dict[str, Any]): データ辞書

        Returns:
            NWFObject: 生成されたオブジェクト
        """
        return cls(
            subject_id=data.get("subject_id"),
            entity_type=data.get("entity_type"),
            state=data.get("state"),
            version=data.get("version", 1),
            relationships=data.get("relationships", {}),
            metadata=data.get("metadata", {}),
            attributes=data.get("attributes", {})
        )


if __name__ == "__main__":
    pass

# [EOF]