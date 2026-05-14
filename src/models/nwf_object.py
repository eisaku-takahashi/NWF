"""
Source: src/models/nwf_object.py
Updated: 2026-05-14T04:12:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Core_Spec/NWF_Entity_ID_System_v2.0.1.md
    - docs/spec/Core_Spec/NWF_State_Transition_Model_v2.0.1.md
    - docs/spec/Core_Spec/NWF_Story_Database_v2.0.1.md
    - docs/spec/Data_Spec/NWF_Data_Spec_Index_v2.0.1.md
    - docs/spec/Execution_Spec/NWF_Consistency_Validator_Spec_v2.0.1_Phase_3.5.md
    - docs/spec/Execution_Spec/NWF_Validation_System_v2.0.1.md
    - docs/spec/Execution_Spec/NWF_Validator_Orchestration_Spec_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
Docstring:
    NWFObject 基本エンティティモデル。

    NWF システム内のすべてのエンティティの共通データ構造を定義する。

    EntityManager / StateManager / AuditLogManager / VersionManager と連携し、
    データの物理論理整合性および因果律を保証する。

    Phase 3.5 における Spec とコードの同期検証に基づき、
    以下を保証する：

    - Entity ID は外部I/F上すべて str として扱う
    - StoryDB I/F と整合する subject_id 正規化
    - Validator / Engine / Mock 間のID型揺れ防止
    - metadata.updated_at の JST ISO8601 統一
    - Python 実装規約 v2.0.1 準拠
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional

# JST タイムゾーン定義
# NWF Time Policy により全システムで JST 固定
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
        subject_id (str):
            エンティティID。
            外部I/F上では必ず str として扱う。

        entity_type (str):
            エンティティ種別。

        state (str):
            状態。

        version (int):
            バージョン。

        relationships (Dict[str, List[str]]):
            関係IDリスト。

            relation_type -> target_id list の形式で保持する。

            target_id は StoryDB I/F 仕様に合わせ
            必ず str に正規化する。

        metadata (Dict[str, Any]):
            メタデータ。

        attributes (Dict[str, Any]):
            エンティティ固有属性。
    """

    REQUIRED_FIELDS = [
        "subject_id",
        "entity_type",
        "state",
        "metadata"
    ]

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
            subject_id (str):
                エンティティID。

                NWF Entity ID System v2.0.1 に基づき、
                外部I/F上は必ず str として扱う。

            entity_type (str):
                エンティティ種別。

            state (str):
                状態。

            metadata (Dict[str, Any]):
                メタデータ。

            version (int, optional):
                バージョン。

            relationships (Dict[str, List[str]], optional):
                関係情報。

            attributes (Dict[str, Any], optional):
                エンティティ固有属性。

        Raises:
            ValueError:
                必須フィールド不正。

            ValueError:
                型不正。
        """

        # ============================================================
        # Phase 3.5 修正:
        # 必須フィールドを str 正規化前に検証
        #
        # 修正理由:
        # None を str(None) -> "None" に変換すると
        # REQUIRED_FIELDS 検証をすり抜けるため
        # 事前に None を拒否する
        # ============================================================
        if subject_id is None:
            raise ValueError("subject_id is required")

        if entity_type is None:
            raise ValueError("entity_type is required")

        if state is None:
            raise ValueError("state is required")

        if metadata is None:
            raise ValueError("metadata is required")

        # ============================================================
        # Phase 3.5 修正:
        # Entity ID型揺れ防止のため str 正規化を追加
        # ============================================================
        self.subject_id = str(subject_id)

        # ============================================================
        # Phase 3.5 修正:
        # entity_type/state も外部I/F安定化のため str 化
        # ============================================================
        self.entity_type = str(entity_type)
        self.state = str(state)

        # ============================================================
        # Phase 3.5 追加:
        # version 型の明示的正規化
        #
        # 理由:
        # version が文字列等で渡された場合の
        # 状態不整合を防止する
        #
        # bool は int のサブクラスであるため、
        # True/False を version として受け入れない
        # ============================================================
        if isinstance(version, bool):
            raise ValueError("version must be int")

        try:
            self.version = int(version)
        except (TypeError, ValueError) as error:
            raise ValueError("version must be int") from error

        # ============================================================
        # Phase 3.5 修正:
        # relationships 内 target_id を str 正規化
        # ============================================================
        self.relationships = self._normalize_relationships(
            relationships if relationships is not None else {}
        )

        # ============================================================
        # Phase 3.5 修正:
        # metadata / attributes の None 安全化
        # ============================================================
        self.metadata = metadata
        self.attributes = attributes if attributes is not None else {}

        # ============================================================
        # Phase 3.5 修正:
        # metadata / attributes の型を事前検証
        #
        # 修正理由:
        # metadata が dict 以外の場合、
        # updated_at 設定時に TypeError が発生するため
        # 明示的に ValueError へ統一する
        # ============================================================
        if not isinstance(self.metadata, dict):
            raise ValueError("metadata must be dict")

        if not isinstance(self.attributes, dict):
            raise ValueError("attributes must be dict")

        # ============================================================
        # Phase 3.5 追加:
        # metadata.updated_at が未存在の場合に初期化
        # ============================================================
        if "updated_at" not in self.metadata:
            self.metadata["updated_at"] = datetime.now(JST).isoformat()

        self._validate_required_fields()
        self._validate_types()

    def _normalize_relationships(
        self,
        relationships: Dict[str, List[str]]
    ) -> Dict[str, List[str]]:
        """
        relationships 内IDの正規化。

        Entity ID System v2.0.1 に基づき、
        relation target ID を必ず str 化する。

        Args:
            relationships (Dict[str, List[str]]):
                関係辞書。

        Returns:
            Dict[str, List[str]]:
                正規化済み relationships。

        Raises:
            ValueError:
                relationships 構造不正。
        """

        if not isinstance(relationships, dict):
            raise ValueError("relationships must be dict")

        normalized_relationships: Dict[str, List[str]] = {}

        for relation_type, target_ids in relationships.items():

            # ========================================================
            # Phase 3.5 修正:
            # None を str(None) -> "None" に変換しない
            #
            # 修正理由:
            # relationship key の型揺れ防止仕様に反するため
            # ========================================================
            if relation_type is None:
                raise ValueError(
                    "relationship keys must not be None"
                )

            if not isinstance(target_ids, list):
                raise ValueError(
                    "relationships values must be list of IDs"
                )

            normalized_target_ids: List[str] = []

            for target_id in target_ids:

                # ====================================================
                # Phase 3.5 修正:
                # None を str(None) -> "None" に変換しない
                #
                # 修正理由:
                # Entity ID型揺れ防止仕様に反するため
                # ====================================================
                if target_id is None:
                    raise ValueError(
                        "relationship target IDs must not be None"
                    )

                normalized_target_ids.append(str(target_id))

            normalized_relationships[str(relation_type)] = (
                normalized_target_ids
            )

        return normalized_relationships

    def _validate_required_fields(self) -> None:
        """
        必須フィールド検証。

        Raises:
            ValueError:
                必須フィールド欠落。
        """

        for field in self.REQUIRED_FIELDS:
            if getattr(self, field, None) is None:
                raise ValueError(f"Missing required field: {field}")

    def _validate_types(self) -> None:
        """
        型チェック検証。

        Raises:
            ValueError:
                型不正。
        """

        if not isinstance(self.subject_id, str):
            raise ValueError("subject_id must be str")

        if not isinstance(self.entity_type, str):
            raise ValueError("entity_type must be str")

        if not isinstance(self.state, str):
            raise ValueError("state must be str")

        # ============================================================
        # bool は int のサブクラスであるため除外する
        # ============================================================
        if isinstance(self.version, bool):
            raise ValueError("version must be int")

        if not isinstance(self.version, int):
            raise ValueError("version must be int")

        if not isinstance(self.relationships, dict):
            raise ValueError("relationships must be dict")

        for key, value in self.relationships.items():

            if not isinstance(value, list):
                raise ValueError(
                    "relationships values must be list of IDs"
                )

            for target_id in value:
                if not isinstance(target_id, str):
                    raise ValueError(
                        "relationship target IDs must be str"
                    )

            if not isinstance(key, str):
                raise ValueError(
                    "relationship keys must be str"
                )

        if not isinstance(self.metadata, dict):
            raise ValueError("metadata must be dict")

        if not isinstance(self.attributes, dict):
            raise ValueError("attributes must be dict")

    def update_state(self, new_state: str) -> None:
        """
        状態更新。

        Args:
            new_state (str):
                新しい状態。
        """

        # ============================================================
        # Phase 3.5 修正:
        # None を str(None) -> "None" に変換しない
        # ============================================================
        if new_state is None:
            raise ValueError("new_state must not be None")

        self.state = str(new_state)

        # 状態変更時は updated_at を更新する
        self._update_timestamp()

    def increment_version(self) -> None:
        """
        バージョン更新。

        version をインクリメントし、
        updated_at を更新する。
        """

        self.version += 1

        # バージョン更新は監査対象
        self._update_timestamp()

    def add_relationship(
        self,
        relation_type: str,
        target_id: str
    ) -> None:
        """
        関係追加。

        Args:
            relation_type (str):
                関係タイプ。

            target_id (str):
                対象ID。

                StoryDB I/F と整合するため、
                必ず str として保持する。
        """

        # ============================================================
        # Phase 3.5 修正:
        # None を str(None) -> "None" に変換しない
        # ============================================================
        if relation_type is None:
            raise ValueError("relation_type must not be None")

        if target_id is None:
            raise ValueError("target_id must not be None")

        relation_type = str(relation_type)
        target_id = str(target_id)

        if relation_type not in self.relationships:
            self.relationships[relation_type] = []

        if target_id not in self.relationships[relation_type]:
            self.relationships[relation_type].append(target_id)

        # relationships 更新は監査対象
        self._update_timestamp()

    def _update_timestamp(self) -> None:
        """
        metadata.updated_at 更新。

        NWF Time Policy に基づき、
        JST ISO8601 形式で更新する。
        """

        self.metadata["updated_at"] = datetime.now(
            JST
        ).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """
        オブジェクトを辞書へ変換。

        Returns:
            Dict[str, Any]:
                辞書形式データ。
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
            data (Dict[str, Any]):
                データ辞書。

        Returns:
            NWFObject:
                生成されたオブジェクト。
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