"""
Source: src/core/version_manager.py
Updated: 2026-04-07T23:45:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Core_Spec/NWF_Data_Model_v2.0.1.md
    - docs/spec/Core_Spec/NWF_Entity_ID_System_v2.0.1.md
    - docs/spec/Kernel_Spec/NWF_Kernel_Audit_System_Spec_v2.0.1.md
    - docs/spec/Execution_Spec/NWF_Validation_System_v2.0.1.md
Docstring:
    Version Manager モジュール。
    Entity の version(int) を管理し、スナップショット生成・整合性保証・監査連携を行う。
    すべての変更は transaction_id に紐付けられ、因果律の追跡可能性を保証する。
"""

import os
import json
import hashlib
from datetime import datetime, timezone, timedelta
from typing import Dict, Any

# JST タイムゾーン
JST = timezone(timedelta(hours=9))

# 定数
BASE_DIR = "data/state/versions"

__all__ = [
    "VersionManager"
]


# Utility Functions

def _now_iso() -> str:
    """
    現在時刻を ISO8601 (JST) 形式で取得

    Returns:
        str
    """
    return datetime.now(JST).isoformat()


def _calculate_hash(data: Dict[str, Any]) -> str:
    """
    SHA-256 ハッシュ生成

    Args:
        data (Dict[str, Any])

    Returns:
        str
    """
    json_str = json.dumps(data, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(json_str).hexdigest()


# Classes

class VersionManager:
    """
    Version 管理クラス

    責務:
    - version(int) の単純増分
    - スナップショット生成
    - ハッシュによる整合性保証
    - transaction_id による因果固定
    """

    def __init__(self, base_dir: str = BASE_DIR):
        """
        Args:
            base_dir (str): 保存ディレクトリ
        """
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    # Internal Methods

    def _get_entity_dir(self, subject_id: str) -> str:
        """
        Entity ごとの保存ディレクトリ取得

        Args:
            subject_id (str)

        Returns:
            str
        """
        path = os.path.join(self.base_dir, subject_id)
        os.makedirs(path, exist_ok=True)
        return path

    def _create_snapshot(self, entity: Dict[str, Any], transaction_id: str) -> Dict[str, Any]:
        """
        スナップショット作成（内部処理）

        Args:
            entity (Dict[str, Any])
            transaction_id (str)

        Returns:
            Dict[str, Any]
        """

        subject_id = entity.get("subject_id")
        version = entity.get("version")

        if not subject_id:
            raise ValueError("subject_id is required")

        if version is None:
            raise ValueError("version is required")

        # スナップショット対象（stateは含めない）
        snapshot_payload = {
            "attributes": entity.get("attributes", {}),
            "relationships": entity.get("relationships", {})
        }

        # ハッシュ生成
        integrity_hash = _calculate_hash(snapshot_payload)

        snapshot = {
            "subject_id": subject_id,
            "version": int(version),
            "transaction_id": transaction_id,
            "hash": integrity_hash,
            "snapshot_data": snapshot_payload,
            "created_at": _now_iso()
        }

        entity_dir = self._get_entity_dir(subject_id)
        file_path = os.path.join(entity_dir, f"{version}.json")

        # 保存（物理保証）
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, ensure_ascii=False, indent=2)

        return snapshot

    # Public Methods

    def increment_version(self, entity: Dict[str, Any], transaction_id: str) -> Dict[str, Any]:
        """
        version を +1 しスナップショット生成

        Args:
            entity (Dict[str, Any])
            transaction_id (str)

        Returns:
            Dict[str, Any]

        Raises:
            ValueError
        """

        # Guard: transaction_id 必須
        if not transaction_id:
            raise ValueError("transaction_id is required")

        # version は int 強制
        current_version = int(entity.get("version", 0))
        next_version = current_version + 1

        # version 更新（stateには触れない）
        entity["version"] = next_version

        # スナップショット生成
        self._create_snapshot(entity, transaction_id)

        return entity

    def verify_integrity(self, entity: Dict[str, Any], transaction_id: str) -> bool:
        """
        スナップショットとの整合性検証

        Args:
            entity (Dict[str, Any])
            transaction_id (str)

        Returns:
            bool
        """

        if not transaction_id:
            raise ValueError("transaction_id is required")

        subject_id = entity.get("subject_id")
        version = entity.get("version")

        if not subject_id or version is None:
            return False

        entity_dir = self._get_entity_dir(subject_id)
        file_path = os.path.join(entity_dir, f"{version}.json")

        if not os.path.exists(file_path):
            return False

        with open(file_path, "r", encoding="utf-8") as f:
            snapshot = json.load(f)

        expected_hash = snapshot.get("hash")

        current_payload = {
            "attributes": entity.get("attributes", {}),
            "relationships": entity.get("relationships", {})
        }

        current_hash = _calculate_hash(current_payload)

        return expected_hash == current_hash


# Main Guard

if __name__ == "__main__":
    vm = VersionManager()

    test_entity = {
        "subject_id": "CHR-TEST",
        "entity_type": "CHARACTER",
        "state": "DRAFT",
        "attributes": {"name": "test"},
        "relationships": {},
        "metadata": {},
        "version": 1
    }

    result = vm.increment_version(test_entity, transaction_id="TX-001")
    print(result)

# [EOF]