"""
Source: src/workflow/workflow_context.py
Updated: 2026-04-11T06:41:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Project_Governance/NWF_Workflow_Engine_Spec_v2.0.1.md
Docstring:
    WorkflowContext モジュール。
    transaction_id 単位での実行時データを管理する。
    Engine 間のデータ共有は本 Context を介してのみ行う。
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional

# JST タイムゾーン定義
JST = timezone(timedelta(hours=9))

# 公開インターフェース
__all__ = [
    "WorkflowContext",
]


class WorkflowContext:
    """
    Workflow 実行時の共有データを管理するクラス。

    Context は transaction 単位で生成され、
    global_vars / local_vars によってスコープを分離する。
    """

    def __init__(self, transaction_id: str) -> None:
        """
        初期化処理。

        Args:
            transaction_id (str): トランザクションID
        """
        now = datetime.now(JST).isoformat()

        # なぜ必要か：
        # transaction単位で完全に分離されたデータ空間を提供するため
        self._transaction_id: str = transaction_id
        self._global_vars: Dict[str, Any] = {}
        self._local_vars: Dict[str, Any] = {}
        self._metadata: Dict[str, Any] = {}

        self._created_at: str = now
        self._updated_at: str = now

    def get_transaction_id(self) -> str:
        """
        transaction_id を取得する。

        Returns:
            str: transaction_id
        """
        return self._transaction_id

    def get_global(self, key: str) -> Optional[Any]:
        """
        global_vars から値を取得する。

        Args:
            key (str): キー

        Returns:
            Optional[Any]: 値
        """
        return self._global_vars.get(key)

    def set_global(self, key: str, value: Any) -> None:
        """
        global_vars に値を設定する。

        Args:
            key (str): キー
            value (Any): 値
        """
        # なぜ必要か：
        # Engine 間で共有される不変データを管理するため
        self._global_vars[key] = value
        self._update_timestamp()

    def get_local(self, key: str) -> Optional[Any]:
        """
        local_vars から値を取得する。

        Args:
            key (str): キー

        Returns:
            Optional[Any]: 値
        """
        return self._local_vars.get(key)

    def set_local(self, key: str, value: Any) -> None:
        """
        local_vars に値を設定する。

        Args:
            key (str): キー
            value (Any): 値
        """
        # なぜ必要か：
        # Executor 内の一時データを安全に管理するため
        self._local_vars[key] = value
        self._update_timestamp()

    def get_metadata(self, key: str) -> Optional[Any]:
        """
        metadata を取得する。

        Args:
            key (str): キー

        Returns:
            Optional[Any]: 値
        """
        return self._metadata.get(key)

    def set_metadata(self, key: str, value: Any) -> None:
        """
        metadata を設定する。

        Args:
            key (str): キー
            value (Any): 値
        """
        self._metadata[key] = value
        self._update_timestamp()

    def snapshot(self) -> Dict[str, Any]:
        """
        Context のスナップショットを取得する。

        Returns:
            Dict[str, Any]: Context 全体のコピー
        """
        # なぜ必要か：
        # HITL 介入時に状態を完全保存するため
        return {
            "transaction_id": self._transaction_id,
            "global_vars": dict(self._global_vars),
            "local_vars": dict(self._local_vars),
            "metadata": dict(self._metadata),
            "created_at": self._created_at,
            "updated_at": self._updated_at,
        }

    def clear_local(self) -> None:
        """
        local_vars をクリアする。

        Executor 実行単位でリセットする用途。
        """
        self._local_vars.clear()
        self._update_timestamp()

    def finalize(self) -> None:
        """
        Context を終了処理する。

        GC ポリシーに従い、データを解放する。
        """
        # なぜ必要か：
        # 長期保持を防ぎ、メモリリークを回避するため
        self._global_vars.clear()
        self._local_vars.clear()
        self._metadata.clear()
        self._update_timestamp()

    def _update_timestamp(self) -> None:
        """
        更新時刻を更新する。
        """
        self._updated_at = datetime.now(JST).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """
        Context を辞書形式で取得する。

        Returns:
            Dict[str, Any]: Context 全体
        """
        return {
            "transaction_id": self._transaction_id,
            "global_vars": self._global_vars,
            "local_vars": self._local_vars,
            "metadata": self._metadata,
            "created_at": self._created_at,
            "updated_at": self._updated_at,
        }


if __name__ == "__main__":
    # 簡易動作確認
    ctx = WorkflowContext(transaction_id="test_tx")

    ctx.set_global("story", "example")
    ctx.set_local("temp", 123)

    print(ctx.to_dict())

    snapshot = ctx.snapshot()
    print("Snapshot:", snapshot)

    ctx.finalize()
    print("After finalize:", ctx.to_dict())

# [EOF]