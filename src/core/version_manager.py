"""
Source: src/core/version_manager.py
Updated: 2026-04-07T22:55:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Core_Spec/NWF_Data_Model_v2.0.1.md
    - docs/spec/Core_Spec/NWF_Entity_ID_System_v2.0.1.md
    - docs/spec/Execution_Spec/NWF_Validation_System_v2.0.1.md
    - docs/spec/Kernel_Spec/NWF_Kernel_Audit_System_Spec_v2.0.1.md
Docstring:
    Version Manager モジュール。
    NWF システムにおいて Entity のバージョン管理を担い、
    version(int) の増分・スナップショット生成・整合性検証を行う。
    すべての変更は transaction_id に紐付けられ、監査可能性を保証する。
"""

import os
import json
import hashlib
from datetime import datetime, timezone, timedelta
from typing import Dict, Any

# JST タイムゾーン定義
JST = timezone(timedelta(hours=9))

# 定数
DEFAULT_BASE_DIR = "data/state/versions"

__all__ = [
    "VersionManager"
]


# Utility Functions

def _now_iso() -> str:
    """
    現在時刻を ISO8601 (JST) 形式で取得する

    Returns:
        str: JST の現在時刻
    """
    return datetime.now(JST).isoformat()


def _calculate_hash(data: Dict[str, Any]) -> str:
    """
    データの整合性検証用 SHA-256 ハッシュを生成する

    Args:
        data (Dict[str, Any]): ハッシュ対象データ

    Returns:
        str: ハッシュ値
    """
    json_str = json.dumps(data, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(json_str).hexdigest()


# Classes

class VersionManager:
    """
    Entity のバージョン管理を行うクラス

    主な責務:
    - version(int) の増分管理
    - スナップショット保存
    - ハッシュによる整合性検証
    - transaction_id による因果関係の固定
    """

    def __init__(self, base_dir: str = DEFAULT_BASE_DIR):
        """
        Args:
            base_dir (str): スナップショット保存ディレクトリ
        """
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    # Internal Utility

    def _get_entity_dir(self, subject_id: str) -> str:
        """
        Entity ごとの保存ディレクトリ取得

        Args:
            subject_id (str): Entity ID

        Returns:
            str: ディレクトリパス
        """
        path = os.path.join(self.base_dir, subject_id)
        os.makedirs(path, exist_ok=True)
        return path

    def _create_snapshot(self, entity: Dict[str, Any], transaction_id: str) -> Dict[str, Any]:
        """
        スナップショットを生成・保存する（内部処理）

        Args:
            entity (Dict[str, Any]): 対象 Entity
            transaction_id (str): トランザクションID

        Returns:
            Dict[str, Any]: スナップショット情報
        """

        # 必須フィールド確認
        subject_id = entity.get("subject_id")
        version = entity.get("version")

        if not subject_id or version is None:
            raise ValueError("subject_id and version are required for snapshot")

        # スナップショット対象データ（state は含めない：不変性保証）
        snapshot_payload = {
            "attributes": entity.get("attributes", {}),
            "relationships": entity.get("relationships", {})
        }

        # ハッシュ生成
        integrity_hash = _calculate_hash(snapshot_payload)

        snapshot = {
            "subject_id": subject_id,
            "version": version,
            "transaction_id": transaction_id,
            "hash": integrity_hash,
            "snapshot_data": snapshot_payload,
            "created_at": _now_iso()
        }

        # 保存
        entity_dir = self._get_entity_dir(subject_id)
        file_path = os.path.join(entity_dir, f"{version}.json")

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, ensure_ascii=False, indent=2)

        return snapshot

    # Public Methods

    def increment_version(self, entity: Dict[str, Any], transaction_id: str) -> Dict[str, Any]:
        """
        Entity の version を +1 し、スナップショットを生成する

        Args:
            entity (Dict[str, Any]): 対象 Entity
            transaction_id (str): トランザクションID

        Returns:
            Dict[str, Any]: 更新後 Entity

        Raises:
            ValueError: transaction_id が未指定の場合
        """

        # transaction_id 必須チェック
        if not transaction_id:
            raise ValueError("transaction_id is required")

        # version は int のみ許可
        current_version = int(entity.get("version", 0))
        next_version = current_version + 1

        # version 更新（state は絶対に変更しない）
        entity["version"] = next_version

        # スナップショット生成
        self._create_snapshot(entity, transaction_id)

        return entity

    def verify_integrity(self, entity: Dict[str, Any]) -> bool:
        """
        最新スナップショットとの整合性を検証する

        Args:
            entity (Dict[str, Any]): 対象 Entity

        Returns:
            bool: 整合性 OK = True
        """

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
    # 簡易テスト
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

    updated = vm.increment_version(test_entity, transaction_id="TX-TEST-001")
    print(updated)

# [EOF]