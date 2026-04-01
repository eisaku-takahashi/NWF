"""
Source: src/models/nwf_object.py
Updated: 2026-04-02T03:14:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Data_Spec/NWF_Data_Model_v2.0.1.md
    - docs/spec/Engine_Spec/NWF_State_Machine_Spec_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
Docstring:
    NWFObject モデル定義モジュール。
    NWF における最小単位のデータエンティティを表現する。
    本クラスは「データ保持」と「バリデーション」のみを責務とし、
    状態変更（status の変更）は一切行わない。
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
import uuid

# 公開インターフェース
__all__ = ["NWFObject", "NWFObjectValidationError"]

# JST タイムゾーン
JST = timezone(timedelta(hours=9))


class NWFObjectValidationError(Exception):
    """
    NWFObject のバリデーションエラー。
    """
    pass


class NWFObject:
    """
    NWF のコアデータエンティティ。

    Attributes:
        id (str): 一意識別子（UUID）。
        type (str): オブジェクトタイプ。
        title (str): タイトル。
        content (Dict[str, Any]): ペイロードデータ。
        status (str): 状態（StateMachine 管理）。
        version (str): バージョン（SemVer）。
        dependencies (List[str]): 依存オブジェクトID。
        created_at (str): 作成日時（JST）。
        updated_at (str): 更新日時（JST）。
        created_by (str): 作成者。
        approved_by (Optional[str]): 承認者。
        approved_at (Optional[str]): 承認日時。
        metadata (Dict[str, Any]): 拡張メタデータ。
    """

    def __init__(
        self,
        type: str,
        title: str,
        content: Dict[str, Any],
        created_by: str,
        id: Optional[str] = None,
        status: str = "DRAFT",
        version: str = "1.0.0",
        dependencies: Optional[List[str]] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        approved_by: Optional[str] = None,
        approved_at: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        NWFObject を初期化する。

        Args:
            type (str): オブジェクトタイプ。
            title (str): タイトル。
            content (Dict[str, Any]): データ本体。
            created_by (str): 作成者。
            id (Optional[str]): UUID。
            status (str): 初期状態。
            version (str): バージョン。
            dependencies (Optional[List[str]]): 依存関係。
            created_at (Optional[str]): 作成日時。
            updated_at (Optional[str]): 更新日時。
            approved_by (Optional[str]): 承認者。
            approved_at (Optional[str]): 承認日時。
            metadata (Optional[Dict[str, Any]]): メタデータ。

        Raises:
            NWFObjectValidationError: 入力値が不正な場合。
        """

        now = datetime.now(JST).isoformat()

        self.id: str = id if id else str(uuid.uuid4())
        self.type: str = type
        self.title: str = title
        self.content: Dict[str, Any] = content
        self.status: str = status
        self.version: str = version
        self.dependencies: List[str] = dependencies if dependencies else []
        self.created_at: str = created_at if created_at else now
        self.updated_at: str = updated_at if updated_at else now
        self.created_by: str = created_by
        self.approved_by: Optional[str] = approved_by
        self.approved_at: Optional[str] = approved_at
        self.metadata: Dict[str, Any] = metadata if metadata else {}

        # 初期バリデーション
        self.validate()

    def validate(self) -> None:
        """
        オブジェクトの整合性を検証する。

        Raises:
            NWFObjectValidationError: 不正な値が存在する場合。
        """

        if not self.id:
            raise NWFObjectValidationError("id は必須です。")

        if not self.type:
            raise NWFObjectValidationError("type は必須です。")

        if not isinstance(self.content, dict):
            raise NWFObjectValidationError("content は dict 型である必要があります。")

        if not isinstance(self.dependencies, list):
            raise NWFObjectValidationError("dependencies は list 型である必要があります。")

        if not self.created_by:
            raise NWFObjectValidationError("created_by は必須です。")

    def to_dict(self) -> Dict[str, Any]:
        """
        オブジェクトを辞書形式に変換する。

        Returns:
            Dict[str, Any]: シリアライズされたデータ。
        """
        return {
            "id": self.id,
            "type": self.type,
            "title": self.title,
            "content": self.content,
            "status": self.status,
            "version": self.version,
            "dependencies": self.dependencies,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "created_by": self.created_by,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NWFObject":
        """
        辞書から NWFObject を生成する。

        Args:
            data (Dict[str, Any]): 入力データ。

        Returns:
            NWFObject: 生成されたオブジェクト。
        """
        return cls(
            id=data.get("id"),
            type=data["type"],
            title=data.get("title", ""),
            content=data.get("content", {}),
            status=data.get("status", "DRAFT"),
            version=data.get("version", "1.0.0"),
            dependencies=data.get("dependencies", []),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            created_by=data.get("created_by", "system"),
            approved_by=data.get("approved_by"),
            approved_at=data.get("approved_at"),
            metadata=data.get("metadata", {}),
        )


if __name__ == "__main__":
    # 動作確認
    obj = NWFObject(
        type="story",
        title="Test Story",
        content={"text": "Hello NWF"},
        created_by="tester"
    )
    print(obj.to_dict())

# [EOF]