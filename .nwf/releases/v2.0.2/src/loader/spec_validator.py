"""
Source: src/loader/spec_validator.py
Updated: 2026-04-09T02:44:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
    - docs/spec/Execution_Spec/NWF_Validation_System_v2.0.1.md
    - docs/spec/Core_Spec/NWF_Entity_ID_System_v2.0.1.md
    - data/schema/metadata_schema.json
Docstring:
    Spec Validator モジュール。
    SpecLoader から渡される Metadata を検証し、
    NWF v2.0.1 の正典として許可可能かを判定する Gatekeeper。
"""

# ============================================================
# Imports
# ============================================================

from typing import Dict, Any, List
import re
import json
import os

# ============================================================
# Constants / Settings
# ============================================================

REQUIRED_VERSION = "v2.0.1"

FORBIDDEN_VERSION_KEYWORDS = [
    "FROZEN",
    "DEPRECATED",
    "OLD"
]

ALLOWED_CATEGORIES = {
    "Core",
    "Architecture",
    "Data",
    "Engine",
    "Execution",
    "AI_Interface",
    "Workflow",
    "Governance",
    "Kernel",
    "Index",
    "Project",
    "Guide"
}

# D7 命名規則（簡易版：英大文字 + アンダースコア + 数字）
D7_PATTERN = r"^[A-Z0-9_]+$"

# ============================================================
# Public Interface
# ============================================================

__all__ = [
    "SpecValidator",
]

# ============================================================
# Classes
# ============================================================

class SpecValidator:
    """
    SpecValidator クラス

    Metadata を検証し、NWF 正典として有効かを判定する。
    """

    def __init__(self, schema_path: str = "data/schema/metadata_schema.json"):
        """
        初期化

        Args:
            schema_path (str): metadata_schema.json のパス
        """
        self.schema_path = schema_path
        self._schema = self._load_schema(schema_path)

    # --------------------------------------------------------
    # Public Methods
    # --------------------------------------------------------

    def validate(self, metadata: Dict[str, Any]) -> bool:
        """
        Metadata を検証

        Args:
            metadata (Dict[str, Any]): Spec Metadata

        Returns:
            bool: 検証結果
        """
        try:
            # 1. Schema Validation（構造チェック）
            if not self._validate_schema_stub(metadata):
                return False

            # 2. 必須項目チェック
            if not self._validate_required_fields(metadata):
                return False

            # 3. Version Validation
            if not self._validate_version(metadata):
                return False

            # 4. Anti-Zombie
            if not self._check_anti_zombie(metadata):
                return False

            # 5. D7 Compliance
            if not self._validate_d7(metadata):
                return False

            # 6. Category Validation
            if not self._validate_category(metadata):
                return False

            # 7. Dependency Validation
            if not self._validate_dependencies(metadata):
                return False

            return True

        except Exception:
            # 例外発生時は不正データとして拒絶
            return False

    # --------------------------------------------------------
    # Internal Methods
    # --------------------------------------------------------

    def _load_schema(self, path: str) -> Dict[str, Any]:
        """
        JSON Schema 読み込み（存在しない場合は空）

        なぜ必要か:
            将来的な厳密バリデーションに備えるため
        """
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _validate_schema_stub(self, metadata: Dict[str, Any]) -> bool:
        """
        Schema Validation Stub

        なぜStubか:
            jsonschema導入前の段階的実装
        """
        # 最低限 required チェック
        required = ["subject_id", "version", "category"]
        for key in required:
            if key not in metadata:
                return False
        return True

    def _validate_required_fields(self, metadata: Dict[str, Any]) -> bool:
        """
        必須フィールド検証
        """
        if not metadata.get("subject_id"):
            return False
        if not metadata.get("version"):
            return False
        if not metadata.get("category"):
            return False
        return True

    def _validate_version(self, metadata: Dict[str, Any]) -> bool:
        """
        Version 完全一致チェック
        """
        return metadata.get("version") == REQUIRED_VERSION

    def _check_anti_zombie(self, metadata: Dict[str, Any]) -> bool:
        """
        Anti-Zombie チェック

        なぜ必要か:
            過去仕様・凍結仕様の混入防止
        """
        version = metadata.get("version", "")
        for keyword in FORBIDDEN_VERSION_KEYWORDS:
            if keyword in version.upper():
                return False
        return True

    def _validate_d7(self, metadata: Dict[str, Any]) -> bool:
        """
        D7 Compliance

        - subject_id 必須
        - id の単独使用禁止
        """
        subject_id = metadata.get("subject_id")

        if not subject_id:
            return False

        # D7 命名規則チェック
        if not re.match(D7_PATTERN, subject_id):
            return False

        # id フィールド単独禁止
        if "id" in metadata and not metadata.get("subject_id"):
            return False

        return True

    def _validate_category(self, metadata: Dict[str, Any]) -> bool:
        """
        Category 検証
        """
        category = metadata.get("category")
        return category in ALLOWED_CATEGORIES

    def _validate_dependencies(self, metadata: Dict[str, Any]) -> bool:
        """
        Dependency 検証

        なぜ必要か:
            Resolver 前段で不正 ID を排除するため
        """
        deps: List[str] = metadata.get("dependencies", [])

        if not isinstance(deps, list):
            return False

        for dep in deps:
            if not isinstance(dep, str):
                return False
            if not re.match(D7_PATTERN, dep):
                return False

        return True


# ============================================================
# Main Guard
# ============================================================

if __name__ == "__main__":
    print("Spec Validator Module")

# [EOF]