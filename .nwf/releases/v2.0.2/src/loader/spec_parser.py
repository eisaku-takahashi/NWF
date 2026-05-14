"""
Source: src/loader/spec_parser.py
Updated: 2026-04-03T07:53:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Architecture_Spec/Spec_Loader_Architecture.md
    - docs/spec/Data_Spec/Spec_Data_Model.md
    - docs/spec/Spec_Governance/Spec_Metadata_Format.md
Docstring:
    Spec Parser モジュール。
    Markdown Spec ファイルから Metadata、Sections、Tables、Code Blocks を抽出し、
    SpecDocument オブジェクトへ構造化する。
"""

import re
import yaml
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Dict, List

# JST Timezone 定義
JST = timezone(timedelta(hours=9))

__all__ = [
    "SpecMetadata",
    "SpecDocument",
    "SpecParser"
]


@dataclass
class SpecMetadata:
    """
    Spec Metadata データクラス
    """
    id: str
    title: str
    version: str
    category: str
    dependencies: List[str]
    status: str
    last_updated: str


@dataclass
class SpecDocument:
    """
    Spec Document データクラス
    """
    metadata: SpecMetadata
    sections: Dict[str, str]
    tables: List[List[str]]
    code_blocks: List[str]
    raw_content: str
    file_path: str


class SpecParser:
    """
    SpecParser クラス

    Markdown Spec を解析し、SpecDocument を生成する。
    """

    def parse_file(self, file_path: str) -> SpecDocument:
        """
        Spec ファイルを解析

        Args:
            file_path (str): Spec Markdown ファイルパス

        Returns:
            SpecDocument
        """
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        metadata = self._extract_metadata(content)
        sections = self._split_sections(content)
        tables = self._extract_tables(content)
        code_blocks = self._extract_code_blocks(content)

        spec_doc = SpecDocument(
            metadata=metadata,
            sections=sections,
            tables=tables,
            code_blocks=code_blocks,
            raw_content=content,
            file_path=file_path
        )

        self._validate_spec(spec_doc)

        return spec_doc

    def _extract_metadata(self, content: str) -> SpecMetadata:
        """
        YAML Front Matter から Metadata 抽出
        """
        meta_match = re.search(r"^---(.*?)---", content, re.DOTALL)
        if not meta_match:
            raise ValueError("Metadata block not found")

        meta_text = meta_match.group(1)
        meta_dict = yaml.safe_load(meta_text)

        return SpecMetadata(
            id=meta_dict.get("id"),
            title=meta_dict.get("title"),
            version=meta_dict.get("version"),
            category=meta_dict.get("category"),
            dependencies=meta_dict.get("dependencies", []),
            status=meta_dict.get("status", ""),
            last_updated=meta_dict.get("last_updated", "")
        )

    def _split_sections(self, content: str) -> Dict[str, str]:
        """
        Markdown 見出しでセクション分割
        """
        sections = {}
        current_title = None
        lines = content.splitlines()

        for line in lines:
            if line.startswith("#"):
                current_title = line.strip("# ").strip()
                sections[current_title] = ""
            elif current_title:
                sections[current_title] += line + "\n"

        return sections

    def _extract_tables(self, content: str) -> List[List[str]]:
        """
        Markdown Table 抽出
        """
        tables = []
        lines = content.splitlines()
        table = []

        for line in lines:
            if "|" in line:
                table.append(line)
            else:
                if table:
                    tables.append(table)
                    table = []

        if table:
            tables.append(table)

        return tables

    def _extract_code_blocks(self, content: str) -> List[str]:
        """
        コードブロック抽出
        """
        code_blocks = re.findall(r"```(.*?)```", content, re.DOTALL)
        return code_blocks

    def _validate_spec(self, spec_doc: SpecDocument) -> None:
        """
        Spec 整合性チェック
        """
        if not spec_doc.metadata.id:
            raise ValueError("Spec ID is missing")

        if not spec_doc.metadata.title:
            raise ValueError("Spec title is missing")

        if not spec_doc.metadata.version:
            raise ValueError("Spec version is missing")

        if not spec_doc.metadata.category:
            raise ValueError("Spec category is missing")


if __name__ == "__main__":
    """
    テスト実行
    """
    parser = SpecParser()
    # テスト用ファイルパス
    # parser.parse_file("docs/spec/sample.md")

# [EOF]