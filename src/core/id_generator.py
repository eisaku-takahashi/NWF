"""
Source: src/core/id_generator.py
Updated: 2026-04-04T23:26:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Core_Spec/NWF_Entity_ID_System_v2.0.1.md
    - docs/spec/Kernel_Spec/NWF_Kernel_Audit_System_Spec_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
Docstring:
    ID Generator モジュール。
    NWF v2.0.1 におけるすべての ID（Entity, Transaction, Log, Event 等）を生成する。
    ID フォーマットは [PREFIX]-[UUID] 形式を採用し、
    システム全体の一意性保証およびトレーサビリティの基盤となる。
"""

import uuid
import re
from typing import Optional

# 定数定義
ID_PATTERN = re.compile(r"^[A-Z]{3,4}-[0-9a-f\-]{36}$")

__all__ = [
    "IDGenerator"
]


def generate_uuid() -> str:
    """
    UUID を生成するユーティリティ関数。
    
    Returns:
        str: UUID 文字列
    """
    return str(uuid.uuid4())


class IDGenerator:
    """
    NWF ID Generator クラス。

    NWF システム内で使用されるすべての ID を生成する。
    ID は Prefix + UUID 形式で生成される。
    """

    def __init__(self):
        """
        IDGenerator 初期化。
        特別な状態は持たないが、将来的な分散 ID 管理のためクラス化している。
        """
        pass

    def generate_id(self, prefix: str) -> str:
        """
        汎用 ID 生成メソッド。

        Args:
            prefix (str): ID プレフィックス

        Returns:
            str: 生成された ID
        """
        prefix = prefix.upper()
        return f"{prefix}-{generate_uuid()}"

    def generate_transaction_id(self) -> str:
        """
        Transaction ID を生成する。

        Returns:
            str: Transaction ID
        """
        return self.generate_id("TXN")

    def generate_log_id(self) -> str:
        """
        Audit Log ID を生成する。

        Returns:
            str: Log ID
        """
        return self.generate_id("LOG")

    def generate_event_id(self) -> str:
        """
        Event ID を生成する。

        Returns:
            str: Event ID
        """
        return self.generate_id("EVT")

    def generate_entity_id(self, entity_prefix: str) -> str:
        """
        Entity ID を生成する。

        Args:
            entity_prefix (str): Entity プレフィックス（CHR, SCE, PLT など）

        Returns:
            str: Entity ID
        """
        return self.generate_id(entity_prefix)

    def validate_id(self, id_str: str) -> bool:
        """
        ID が NWF 形式に準拠しているか検証する。

        Args:
            id_str (str): 検証対象 ID

        Returns:
            bool: 有効な ID の場合 True
        """
        if not isinstance(id_str, str):
            return False
        return bool(ID_PATTERN.match(id_str))


if __name__ == "__main__":
    # 動作確認用
    generator = IDGenerator()

    print(generator.generate_transaction_id())
    print(generator.generate_log_id())
    print(generator.generate_event_id())
    print(generator.generate_entity_id("CHR"))

# [EOF]