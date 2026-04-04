"""
Source: src/core/version_manager.py
Updated: 2026-04-04T20:54:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Core_Spec/NWF_Data_Model_v2.0.1.md
    - docs/spec/Core_Spec/NWF_State_Transition_Model_v2.0.1.md
    - docs/spec/Execution_Spec/NWF_Validation_System_v2.0.1.md
    - docs/spec/Kernel_Spec/NWF_Kernel_Audit_System_Spec_v2.0.1.md
Docstring:
    Version Manager モジュール。
    NWF システムにおける Entity のバージョン管理（スナップショット生成・履歴管理・ロールバック）を担う。
"""

import os
import json
import hashlib
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional

# JST タイムゾーン定義
JST = timezone(timedelta(hours=9))

__all__ = [
    "VersionManager"
]


# Utility Functions

def _now_iso() -> str:
    """現在時刻を ISO8601 (JST) で返す"""
    return datetime.now(JST).isoformat()


def _calculate_hash(data: Dict[str, Any]) -> str:
    """データの整合性チェック用ハッシュを生成する"""
    json_str = json.dumps(data, sort_keys=True).encode("utf-8")
    return "sha256:" + hashlib.sha256(json_str).hexdigest()


def _increment_patch(version: str) -> str:
    """SemVer の Patch をインクリメント"""
    major, minor, patch = map(int, version.split("."))
    patch += 1
    return f"{major}.{minor}.{patch}"


# Classes

class VersionManager:
    """
    Entity のバージョン管理を行うクラス

    主な責務:
    - スナップショット作成
    - バージョン履歴管理
    - ロールバック処理
    - 差分検出
    """

    def __init__(self, base_dir: str = "data/state/versions"):
        """
        Args:
            base_dir (str): バージョン保存ディレクトリ
        """
        self.base_dir = base_dir

        # ディレクトリが存在しない場合は作成
        os.makedirs(self.base_dir, exist_ok=True)

    def _get_entity_dir(self, entity_id: str) -> str:
        """Entity ごとの保存ディレクトリ取得"""
        path = os.path.join(self.base_dir, entity_id)
        os.makedirs(path, exist_ok=True)
        return path

    def create_snapshot(
        self,
        entity: Dict[str, Any],
        actor_id: str,
        change_summary: str = "update"
    ) -> Dict[str, Any]:
        """
        スナップショットを作成する

        Args:
            entity (Dict): 対象 Entity
            actor_id (str): 操作者 ID
            change_summary (str): 変更概要

        Returns:
            Dict: バージョン情報
        """

        entity_id = entity["subject_id"]
        current_version = entity.get("version", "1.0.0")

        # Patch インクリメント
        new_version = _increment_patch(current_version)

        # スナップショットデータ
        snapshot_data = {
            "entity": entity,
            "version": new_version,
            "timestamp": _now_iso()
        }

        # 保存パス
        entity_dir = self._get_entity_dir(entity_id)
        file_path = os.path.join(entity_dir, f"{new_version}.json")

        # JSON 保存（Atomicを意識し簡易実装）
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(snapshot_data, f, ensure_ascii=False, indent=2)

        # ハッシュ生成
        integrity_hash = _calculate_hash(snapshot_data)

        # バージョンメタ情報
        version_info = {
            "version_id": new_version,
            "subject_id": entity_id,
            "parent_version_id": current_version,
            "timestamp": _now_iso(),
            "actor_id": actor_id,
            "change_summary": change_summary,
            "snapshot_path": file_path,
            "integrity_hash": integrity_hash
        }

        return version_info

    def get_version_history(self, entity_id: str) -> List[str]:
        """
        バージョン履歴を取得

        Args:
            entity_id (str): Entity ID

        Returns:
            List[str]: バージョン一覧
        """

        entity_dir = self._get_entity_dir(entity_id)

        versions = []
        for file in os.listdir(entity_dir):
            if file.endswith(".json"):
                versions.append(file.replace(".json", ""))

        # ソート（簡易）
        return sorted(versions)

    def rollback_to(self, entity_id: str, version_id: str) -> Optional[Dict[str, Any]]:
        """
        指定バージョンへロールバック

        Args:
            entity_id (str): Entity ID
            version_id (str): 対象バージョン

        Returns:
            Optional[Dict]: Entity データ
        """

        entity_dir = self._get_entity_dir(entity_id)
        file_path = os.path.join(entity_dir, f"{version_id}.json")

        if not os.path.exists(file_path):
            return None

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # DRAFT として再展開する前提
        entity = data.get("entity")
        if entity:
            entity["state"] = "DRAFT"

        return entity

    def diff_versions(
        self,
        entity_id: str,
        v1: str,
        v2: str
    ) -> Dict[str, Any]:
        """
        2バージョン間の差分を取得

        Args:
            entity_id (str): Entity ID
            v1 (str): version1
            v2 (str): version2

        Returns:
            Dict: 差分
        """

        def load(version):
            path = os.path.join(self._get_entity_dir(entity_id), f"{version}.json")
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)["entity"]

        data1 = load(v1)
        data2 = load(v2)

        diff = {}

        # 簡易差分（キー単位）
        keys = set(data1.keys()) | set(data2.keys())
        for k in keys:
            if data1.get(k) != data2.get(k):
                diff[k] = {
                    "from": data1.get(k),
                    "to": data2.get(k)
                }

        return diff

    def freeze_version(self, entity: Dict[str, Any]) -> bool:
        """
        バージョンを FROZEN 状態にする

        Args:
            entity (Dict): Entity

        Returns:
            bool: 成功可否
        """

        # 状態変更（DataStateManager に委譲するのが理想だが簡易実装）
        if entity.get("state") == "APPROVED":
            entity["state"] = "FROZEN"
            return True

        return False


# Main Guard

if __name__ == "__main__":
    # 簡易テスト
    vm = VersionManager()

    sample_entity = {
        "subject_id": "CHR-TEST",
        "version": "1.0.0",
        "state": "DRAFT",
        "content": {"name": "test"}
    }

    info = vm.create_snapshot(sample_entity, actor_id="AI-TEST")
    print(info)

# [EOF]