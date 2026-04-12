"""
Source: src/integration/repository_watcher.py
Updated: 2026-04-13T08:46:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Project_Governance/NWF_GitHub_Sync_Spec_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
    - src/integrity/anomaly_detector.py
    - src/core/data_state_manager.py
Docstring:
    Repository Watcher モジュール。
    ローカルリポジトリの変更を監視し、Integrity Layer を通過した変更のみを
    SyncEvent として生成・管理する。
"""

import os
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any

# JSTタイムゾーン定義
JST = timezone(timedelta(hours=9))

__all__ = [
    "RepositoryWatcher"
]


class RepositoryWatcher:
    """
    ローカルリポジトリの変更を監視し、整合性チェック後の同期イベントを生成するクラス。

    概要:
        - docs/spec, src, data の三層のみ監視
        - ignore_patterns に該当するファイルは除外
        - Integrity Layer を通過した変更のみ SyncEvent 化

    Args:
        target_dirs (List[str]): 監視対象ディレクトリ

    Returns:
        None
    """

    def __init__(self, target_dirs: List[str] = None) -> None:
        """
        初期化処理

        Args:
            target_dirs (List[str]): 監視対象ディレクトリ

        Returns:
            None
        """
        self.target_dirs = target_dirs or ["docs/spec", "src", "data"]

        # 無視対象（ノイズ除去）
        self.ignore_patterns = [
            ".venv",
            "__pycache__",
            ".git",
            ".nwf/temp_sync"
        ]

        # 変更イベント蓄積
        self.pending_changes: List[Dict[str, Any]] = []

    def detect_changes(self) -> List[Dict[str, Any]]:
        """
        Public API:
        変更されたファイルを検出し SyncEvent を生成

        Returns:
            List[Dict[str, Any]]: SyncEvent のリスト
        """

        # なぜ必要か:
        # Git同期は「論理的な変更単位」で行う必要があるため、
        # 検出した変更をまとめて返す

        changes = []

        # 簡易スナップショット方式（Phase 2ではこれを採用）
        for root, _, files in os.walk("."):
            for file_name in files:
                file_path = os.path.join(root, file_name)

                # スコープフィルタ
                if not self._is_target(file_path):
                    continue

                # SyncEvent生成
                event = self._create_sync_event(file_path)

                # Integrityチェック
                if self._verify_integrity_before_queue(event):
                    changes.append(event)

        # 内部キューに保持
        self.pending_changes.extend(changes)

        return changes

    def filter_scope(self, paths: List[str]) -> List[str]:
        """
        Public API:
        監視対象スコープのパスのみ抽出

        Args:
            paths (List[str]): ファイルパス一覧

        Returns:
            List[str]: フィルタ済みパス
        """

        # なぜ必要か:
        # 三位一体（Spec/Code/Data）以外を排除するため

        filtered = [
            p for p in paths
            if any(p.startswith(d) for d in self.target_dirs)
            and not any(ig in p for ig in self.ignore_patterns)
        ]

        return filtered

    def _is_target(self, path: str) -> bool:
        """
        内部関数:
        対象パスかどうか判定

        Args:
            path (str): ファイルパス

        Returns:
            bool
        """

        # スコープ確認
        if not any(path.startswith(d) for d in self.target_dirs):
            return False

        # 除外パターン確認
        if any(ig in path for ig in self.ignore_patterns):
            return False

        return True

    def _create_sync_event(self, path: str) -> Dict[str, Any]:
        """
        SyncEvent生成ユーティリティ

        Args:
            path (str): ファイルパス

        Returns:
            Dict[str, Any]: SyncEvent構造
        """

        # なぜ必要か:
        # I/F Contract に準拠したイベント形式を統一するため

        timestamp = datetime.now(JST).isoformat()

        event = {
            "event_id": f"EVT-{hash(path)}",
            "entity_id": path,
            "event_type": "FILE_CHANGE",
            "timestamp": timestamp,
            "status": "DETECTED"
        }

        return event

    def _verify_integrity_before_queue(self, event: Dict[str, Any]) -> bool:
        """
        Integrity Layer を通過しているか確認

        Args:
            event (Dict[str, Any]): SyncEvent

        Returns:
            bool: True の場合のみキュー追加
        """

        # なぜ必要か:
        # Integrity First 原則により、未検証データの同期を防ぐ

        try:
            # TODO:
            # anomaly_detector の状態確認処理をここに実装
            # 現段階では仮実装として True を返す

            return True

        except Exception:
            # 例外時は安全側に倒す（同期禁止）
            return False


if __name__ == "__main__":
    """
    簡易動作確認
    """

    watcher = RepositoryWatcher()
    changes = watcher.detect_changes()

    for change in changes:
        print(change)


# [EOF]