"""
Source: tests/mocks/mock_story_db.py
Updated: 2026-05-16T03:53:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/project/NWF_Phase_3.5_Debug_Work_Plan_v20260502.md
    - docs/spec/Execution_Spec/NWF_Mock_Design_Guideline_v2.0.1.md
    - docs/spec/Core_Spec/NWF_Story_Database_v2.0.1.md
    - docs/spec/Core_Spec/NWF_Entity_ID_System_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
Docstring:
    MockStoryDB モジュール。

    Phase 3.5 の Validator / StoryDB Interface 検証用モック実装。
    StoryDB Interface Specification に準拠し、
    get(entity_id: str) -> Optional[Entity] を提供する。

    本モックは ConsistencyValidator の I/F 契約検証専用であり、
    DB内部構造への直接アクセスを禁止するため、
    公開メソッドは get() のみを提供する。

    Entity ID は外部 I/F 上で必ず str に正規化される。
"""

from typing import Any, Dict, Optional


__all__ = [
    "MockStoryDB",
]


class MockStoryDB:
    """
    StoryDB Interface 検証用モックDB。

    Validator が StoryDB 実装差異へ依存しないことを
    検証するための最小構成モック。

    内部データは defensive copy により保持し、
    外部からの直接変更を防止する。

    Args:
        data:
            Entity ID をキーとした Entity 辞書。
            すべてのキーは内部で str に正規化される。

    Example:
        db = MockStoryDB({
            "entity_001": entity
        })

        result = db.get("entity_001")
    """

    def __init__(self, data: Dict[Any, Any]):
        """
        MockStoryDB を初期化する。

        外部から渡された辞書を defensive copy し、
        ID型揺れを防止するためキーを str に正規化する。

        Args:
            data:
                Entity データ辞書。
        """

        # Entity ID の型揺れを防止するため、
        # すべてのキーを str に正規化して保持する。
        self._data: Dict[str, Any] = {
            str(key): value
            for key, value in data.items()
        }

    def get(self, entity_id: str) -> Optional[Any]:
        """
        Entity を取得する。

        StoryDB Interface Specification に従い、
        非存在時には None を返す。

        Validator が DB内部構造へ依存しないことを
        保証するため、本 I/F のみを公開する。

        Args:
            entity_id:
                取得対象 Entity ID。

        Returns:
            Optional[Any]:
                対応する Entity。
                存在しない場合は None。
        """

        # 外部 I/F 契約に従い、
        # 取得時にも Entity ID を str に正規化する。
        normalized_entity_id = str(entity_id)

        return self._data.get(normalized_entity_id)


if __name__ == "__main__":
    """
    モジュール単体確認用。

    MockStoryDB の基本動作確認を行う。
    """

    class DummyEntity:
        """
        テスト用簡易 Entity。
        """

        def __init__(self, entity_id: str):
            self.id = entity_id

    entity = DummyEntity("entity_001")

    mock_db = MockStoryDB({
        "entity_001": entity
    })

    result = mock_db.get("entity_001")

    print(result)


# [EOF]