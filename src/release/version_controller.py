"""
Source: src/release/version_controller.py
Updated: 2026-04-13T16:27:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Project_Governance/NWF_Release_Management_Spec_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
    - src/core/version_manager.py
Docstring:
    Version Controller モジュール。
    NWF におけるリリース種別（Beat / Episode / Milestone）に基づき、
    セマンティックバージョン（Major.Minor.Patch）を制御する。
    VersionManager と連携し、バージョンの取得・更新・検証を行う。
"""

import re
from typing import Tuple, Optional
from datetime import datetime, timezone, timedelta

__all__ = [
    "VersionController"
]

# JST タイムゾーン定義
JST = timezone(timedelta(hours=9))


class VersionController:
    """
    NWFのリリースバージョン管理を行うクラス。

    セマンティックバージョニングと物語構造（Beat / Episode / Milestone）を対応付け、
    正しいバージョン遷移を保証する。
    """

    def __init__(self, version_manager: Optional[object] = None):
        """
        初期化処理

        Args:
            version_manager: 外部の VersionManager インスタンス（任意）
        """
        self.version_manager = version_manager
        self.current_version = self._load_current_version()

    def _load_current_version(self) -> str:
        """
        現在のバージョンを取得する

        Returns:
            str: 現在のバージョン（vX.Y.Z形式）
        """
        if self.version_manager:
            return self.version_manager.get_version()
        # フォールバック（開発用デフォルト）
        return "v2.0.1"

    def determine_version(self, release_type: str) -> str:
        """
        [I/F Contract] 次のバージョンを決定する

        Args:
            release_type (str): "patch" | "minor" | "major"

        Returns:
            str: 次のバージョン（vX.Y.Z形式）

        Raises:
            ValueError: 不正なリリースタイプ
        """
        next_version = self.increment_version(self.current_version, release_type)

        if not self.validate_version_flow(next_version):
            raise ValueError("Version regression detected")

        return f"v{next_version}"

    def increment_version(self, current_version: str, release_type: str) -> str:
        """
        バージョンをインクリメントする

        Args:
            current_version (str): 現在のバージョン
            release_type (str): "patch" | "minor" | "major"

        Returns:
            str: インクリメント後のバージョン（X.Y.Z形式）

        Raises:
            ValueError: 不正な形式またはタイプ
        """
        major, minor, patch = self._parse_version(current_version)

        if release_type.lower() == "major":
            major += 1
            minor = 0
            patch = 0
        elif release_type.lower() == "minor":
            minor += 1
            patch = 0
        elif release_type.lower() == "patch":
            patch += 1
        else:
            raise ValueError(f"Invalid release_type: {release_type}")

        return f"{major}.{minor}.{patch}"

    def _parse_version(self, version_str: str) -> Tuple[int, int, int]:
        """
        バージョン文字列をパースする

        Args:
            version_str (str): vX.Y.Z または X.Y.Z

        Returns:
            tuple: (major, minor, patch)

        Raises:
            ValueError: 不正なフォーマット
        """
        clean_version = version_str.lstrip("v")
        match = re.match(r"(\d+)\.(\d+)\.(\d+)", clean_version)

        if not match:
            raise ValueError(f"Invalid version format: {version_str}")

        return tuple(map(int, match.groups()))

    def validate_version_flow(self, next_version: str) -> bool:
        """
        バージョンが前進しているか検証する

        Args:
            next_version (str): 次のバージョン

        Returns:
            bool: True（正常）/ False（異常）
        """
        current_tuple = self._parse_version(self.current_version)
        next_tuple = self._parse_version(next_version)

        return next_tuple > current_tuple

    def commit_version(self, new_version: str) -> bool:
        """
        VersionManager にバージョンを反映する

        Args:
            new_version (str): vX.Y.Z形式

        Returns:
            bool: 成功可否
        """
        if not self.version_manager:
            return False

        timestamp = datetime.now(JST).isoformat()

        return self.version_manager.set_version(
            version=new_version,
            updated_at=timestamp
        )


if __name__ == "__main__":
    # 簡易テスト（デバッグ用）
    vc = VersionController()

    print("Current:", vc.current_version)
    print("Next Patch:", vc.determine_version("patch"))
    print("Next Minor:", vc.determine_version("minor"))
    print("Next Major:", vc.determine_version("major"))

# [EOF]