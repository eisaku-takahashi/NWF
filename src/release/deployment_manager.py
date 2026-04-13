"""
Source: src/release/deployment_manager.py
Updated: 2026-04-13T16:44:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Project_Governance/NWF_Release_Management_Spec_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
Docstring:
    Deployment Manager モジュール。
    Spec / Code / Data を三位一体でパッケージングし、
    不変なリリース成果物として保存・アーカイブする。
"""

import os
import shutil
import json
import hashlib
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List

# JST定義
JST = timezone(timedelta(hours=9))

# 公開インターフェース
__all__ = [
    "DeploymentManager"
]


class DeploymentManager:
    """
    リリース対象のファイルをパッケージング・アーカイブ化する。

    Args:
        root_path (str): プロジェクトルートパス

    Returns:
        None

    Raises:
        Exception: パッケージング失敗時

    使用例:
        dm = DeploymentManager("/project/root")
        path = dm.package_release("2.0.1", manifest)
        dm.archive_release(path)
    """

    def __init__(self, root_path: str):
        """
        初期化処理

        なぜ必要か:
            リリース対象の基準ディレクトリと出力先を統一管理するため
        """
        self.root_path = root_path
        self.release_base_dir = os.path.join(root_path, ".nwf", "releases")

        # セキュリティ上除外すべき対象
        self.exclude_patterns = [
            "secrets",
            ".env",
            "__pycache__",
            ".git",
            ".venv"
        ]

        # 出力ディレクトリが存在しない場合は生成
        os.makedirs(self.release_base_dir, exist_ok=True)

    def package_release(self, version: str, manifest: Dict[str, Any]) -> str:
        """
        [仕様 6.3] パッケージング実行

        Args:
            version (str): リリースバージョン
            manifest (Dict): ReleaseManifest

        Returns:
            str: パッケージディレクトリパス

        Raises:
            Exception: 処理失敗時
        """
        # 修正前 (src/release/deployment_manager.py 内)
        # dest_path = os.path.join(self.release_base_dir, f"v{version}")
        #
        # 修正後：version 文字列が既に 'v' で始まっている可能性を考慮する
        clean_version = version if version.startswith('v') else f"v{version}"
        dest_path = os.path.join(self.release_base_dir, clean_version)

        print(f"[DEPLOY] Packaging release to: {dest_path}")

        # なぜ削除するか:
        # 同一バージョン再生成時の不整合防止
        if os.path.exists(dest_path):
            shutil.rmtree(dest_path)

        os.makedirs(dest_path, exist_ok=True)

        targets = ["docs/spec", "src", "data"]

        for target in targets:
            src_dir = os.path.join(self.root_path, target)
            dst_dir = os.path.join(dest_path, target)

            if os.path.exists(src_dir):
                self._copy_with_filter(src_dir, dst_dir)

        # Manifest書き込み
        manifest_path = os.path.join(dest_path, "manifest.json")

        # snapshot_hash生成
        manifest["snapshot_hash"] = self._generate_hash(dest_path)
        manifest["created_at"] = datetime.now(JST).isoformat()

        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

        return dest_path

    def _copy_with_filter(self, src: str, dst: str):
        """
        フィルタリング付きコピー

        なぜ必要か:
            機密情報や不要ファイルの混入を防ぐため
        """
        def ignore_func(directory, contents):
            ignored = []
            for item in contents:
                for pattern in self.exclude_patterns:
                    if pattern in item:
                        ignored.append(item)
            return ignored

        shutil.copytree(
            src,
            dst,
            ignore=ignore_func,
            dirs_exist_ok=True
        )

    def _generate_hash(self, path: str) -> str:
        """
        ディレクトリ全体のハッシュ生成

        なぜ必要か:
            リリースの完全性検証（改ざん検知）のため
        """
        hash_obj = hashlib.sha256()

        for root, dirs, files in os.walk(path):
            for file in sorted(files):
                file_path = os.path.join(root, file)

                with open(file_path, "rb") as f:
                    while chunk := f.read(8192):
                        hash_obj.update(chunk)

        return hash_obj.hexdigest()

    def archive_release(self, package_path: str) -> bool:
        """
        パッケージをZIP形式でアーカイブ

        Args:
            package_path (str): パッケージパス

        Returns:
            bool: 成功可否

        Raises:
            None
        """
        try:
            archive_path = shutil.make_archive(
                package_path,
                "zip",
                package_path
            )

            print(f"[DEPLOY] Archive created: {archive_path}")
            return True

        except Exception as e:
            print(f"[DEPLOY] Archive failed: {e}")
            return False


if __name__ == "__main__":
    # 簡易テスト
    dm = DeploymentManager(os.getcwd())

    test_manifest = {
        "release_id": "test",
        "version": "2.0.1",
        "release_type": "patch",
        "timeline_id": "test_timeline",
        "integrity_status": "SUCCESS"
    }

    path = dm.package_release("2.0.1", test_manifest)
    dm.archive_release(path)


# [EOF]