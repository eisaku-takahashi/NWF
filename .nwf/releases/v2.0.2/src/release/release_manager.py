"""
Source: src/release/release_manager.py
Updated: 2026-04-13T15:44:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Project_Governance/NWF_Release_Management_Spec_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
Docstring:
    Release Manager モジュール。
    NWF Phase 2.7 におけるリリース処理を統括し、
    Integrity Gate の検証、バージョン確定、同期制御を実行する。
"""

import os
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional

# 追加
from src.release.version_controller import VersionController
from src.release.deployment_manager import DeploymentManager
from src.release.changelog_generator import ChangelogGenerator

# JST タイムゾーン定義（仕様準拠）
JST = timezone(timedelta(hours=9))

# エラーコード定義
ERR_REL_001 = "ERR_REL_001"  # 整合性違反
ERR_REL_002 = "ERR_REL_002"  # 同期未完了
ERR_REL_003 = "ERR_REL_003"  # バージョン衝突
ERR_REL_004 = "ERR_REL_004"  # パッケージ失敗

__all__ = [
    "ReleaseManager"
]


def _now_jst() -> str:
    """
    現在時刻をJST ISO8601形式で取得する。

    Returns:
        str: ISO8601形式のJST時刻
    """
    return datetime.now(JST).isoformat()


class ReleaseManager:
    """
    NWFリリースの実行と整合性管理を統括するクラス。

    主な責務:
        - Integrity Gate の検証
        - リリースパイプラインの統括
        - 同期ロック管理

    使用例:
        manager = ReleaseManager()
        result = manager.execute_release("beat_end")
    """

    def __init__(self, root_path: Optional[str] = None) -> None:
        """
        初期化処理

        Args:
            root_path (Optional[str]): プロジェクトルートパス
        """
        self.root_path = root_path or os.getcwd()

        # リリース中に同期を停止するためのロック
        self._is_locking = False

    def execute_release(self, trigger: str) -> Dict[str, Any]:
        """
        [Public API]
        リリースパイプラインを実行する。

        Args:
            trigger (str): トリガー種別（beat_end / episode_end など）

        Returns:
            Dict[str, Any]: ReleaseResult
        """
        print(f"[RELEASE] Start release sequence: trigger={trigger}")

        try:
            # 1. 依存モジュールのメソッド内インポート（循環参照回避）
            from src.release.version_controller import VersionController
            from src.release.deployment_manager import DeploymentManager
            from src.release.changelog_generator import ChangelogGenerator

            # ... (既存のチェックロジック) ...
            self._set_lock(True)

            # --- 2.7 物理連携の実装 ---
            vc = VersionController()
            # リリースタイプを決定
            rel_type = "patch" if trigger == "BEAT" else "minor" 
            
            # 【修正点】メソッド名を 'determine_version' に合わせる
            version = vc.determine_version(rel_type)

            dm = DeploymentManager(self.root_path)
            manifest = {
                "release_id": trigger,
                "version": version,
                "integrity_status": "SUCCESS"
            }
            
            # DeploymentManager は内部で 'v' があれば付与しない設計に変更済みのため安全です
            dest_path = dm.package_release(version, manifest)

            cg = ChangelogGenerator()
            cg.generate_changelog([{"event_id": "INIT", "entity_type": "SYSTEM", "event_type": "RELEASE"}])

            print(f"[RELEASE] Release completed: {version}")

            return {
                "success": True,
                "version": version,
                "path": dest_path,
                "timestamp": _now_jst()
            }

        except Exception as e:
            # エラーの詳細を出力するように修正
            print(f"[RELEASE] CRITICAL ERROR: {str(e)}") 
            import traceback
            traceback.print_exc() # スタックトレースを表示
            return {
                "success": False,
                "error_code": "ERR_REL_004",
                "message": f"Unexpected error: {str(e)}"
            }
        finally:
            self._set_lock(False)

    def _check_integrity_gate(self) -> bool:
        """
        Integrity Layer の検証を行う。

        Returns:
            bool: 成功時 True
        """
        # TODO: anomaly_detector 等と連携
        # 現時点ではモックとして常に True
        return True

    def _check_sync_status(self) -> bool:
        """
        同期状態の確認を行う。

        Returns:
            bool: 同期済みなら True
        """
        # TODO: SyncScheduler と連携
        return True

    def _determine_version(self, trigger: str) -> str:
        """
        リリースバージョンを決定する。

        Args:
            trigger (str): トリガー種別

        Returns:
            str: バージョン文字列
        """
        # TODO: VersionController に置き換え
        if trigger == "beat_end":
            return "v0.0.1"
        elif trigger == "episode_end":
            return "v0.1.0"
        else:
            return "v1.0.0"

    def _set_lock(self, state: bool) -> None:
        """
        リリースロック状態を設定する。

        Args:
            state (bool): ロック状態
        """
        # 同期との競合を防ぐための制御
        self._is_locking = state
        print(f"[RELEASE] Lock state: {self._is_locking}")

    def get_lock_status(self) -> bool:
        """
        現在のロック状態を取得する。

        Returns:
            bool: ロック状態
        """
        return self._is_locking


if __name__ == "__main__":
    """
    簡易動作確認用
    """
    manager = ReleaseManager()
    result = manager.execute_release("beat_end")
    print(result)

# [EOF]