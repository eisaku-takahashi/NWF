"""
Source: src/loader/spec_registry.py
Updated: 2026-04-09T01:24:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Core_Spec/NWF_Entity_ID_System_v2.0.1.md
    - docs/spec/Kernel_Spec/NWF_Kernel_Audit_System_Spec_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
    - docs/spec/Data_Spec/NWF_Data_Spec_Index_v2.0.1.md
Docstring:
    Spec Registry モジュール（再構築版）。

    検証済み Spec を subject_id をキーとして保持する
    不変（Immutable）な Spec Index を構築する。

    SpecLoader と連携し、
    transaction_id による因果律を保持しながら登録される。

    一度 lock() されると、すべての書き込み操作は禁止される。
"""

# ============================================================
# Imports
# ============================================================

from typing import Dict, Optional, Any
from threading import RLock
import copy

# ============================================================
# Public Interface
# ============================================================

__all__ = [
    "SpecRegistry",
    "RegistryLockedError",
    "DuplicateSpecError",
    "SpecNotFoundError",
]

# ============================================================
# Exceptions
# ============================================================

class RegistryLockedError(Exception):
    """レジストリロック状態での更新操作エラー"""
    pass


class DuplicateSpecError(Exception):
    """重複登録エラー"""
    pass


class SpecNotFoundError(Exception):
    """Spec 未発見エラー"""
    pass


# ============================================================
# Classes
# ============================================================

class SpecRegistry:
    """
    Spec Registry（不変インデックス）

    特徴:
        - subject_id を主キーとする
        - transaction_id による因果律保持
        - lock() 後は完全不変
        - スレッド安全（RLock）
    """

    def __init__(self):
        """初期化"""
        self._storage: Dict[str, Dict[str, Any]] = {}
        self._transaction_map: Dict[str, str] = {}
        self._lock_flag: bool = False
        self._lock = RLock()

    # --------------------------------------------------------
    # Registry Management
    # --------------------------------------------------------

    def register(self, spec: Dict[str, Any], transaction_id: str) -> None:
        """
        Spec 登録

        Args:
            spec (Dict[str, Any]): Spec（metadata 含む）
            transaction_id (str): トランザクションID

        Raises:
            RegistryLockedError: ロック後の書き込み
            DuplicateSpecError: 重複登録
            ValueError: 必須フィールド欠落
        """
        with self._lock:

            # ロック状態チェック
            if self._lock_flag:
                raise RegistryLockedError("Registry is locked")

            # 必須フィールド検証（D7準拠）
            subject_id = spec.get("subject_id")
            if not subject_id:
                raise ValueError("subject_id is required")

            # Anti-Zombie（versionチェック）
            version = spec.get("version")
            if version != "v2.0.1":
                raise ValueError(f"Invalid version: {version}")

            # 重複チェック
            if subject_id in self._storage:
                raise DuplicateSpecError(subject_id)

            # 登録
            self._storage[subject_id] = spec

            # 因果律リンク
            self._transaction_map[subject_id] = transaction_id

    def lock(self) -> None:
        """
        レジストリをロック（不可逆）

        一度ロックすると解除不可。
        """
        with self._lock:
            self._lock_flag = True

    # --------------------------------------------------------
    # Lookup Methods
    # --------------------------------------------------------

    def get_spec(self, subject_id: str) -> Optional[Dict[str, Any]]:
        """
        Spec 取得

        Args:
            subject_id (str): 主キー

        Returns:
            Optional[Dict[str, Any]]: Spec（コピー）
        """
        spec = self._storage.get(subject_id)
        if spec is None:
            return None

        # 不変性確保のためコピー返却
        return copy.deepcopy(spec)

    def get_transaction_id(self, subject_id: str) -> Optional[str]:
        """
        Spec の transaction_id を取得

        Args:
            subject_id (str)

        Returns:
            Optional[str]
        """
        return self._transaction_map.get(subject_id)

    def exists(self, subject_id: str) -> bool:
        """
        登録確認

        Args:
            subject_id (str)

        Returns:
            bool
        """
        return subject_id in self._storage

    def size(self) -> int:
        """
        登録数取得

        Returns:
            int
        """
        return len(self._storage)

    # --------------------------------------------------------
    # State
    # --------------------------------------------------------

    def is_locked(self) -> bool:
        """
        ロック状態確認

        Returns:
            bool
        """
        return self._lock_flag


# ============================================================
# Main Guard
# ============================================================

if __name__ == "__main__":
    print("Spec Registry Module (Immutable)")

# [EOF]