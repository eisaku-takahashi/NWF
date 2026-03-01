import os
from pathlib import Path

# ==========================
# 設定項目
# ==========================

# 対象ディレクトリ（"." で現在ディレクトリ）
ROOT_DIR = "."

# 除外するフォルダ(追加したPython仮想環境フォルダの対応)
EXCLUDE_DIRS = {
    ".venv",
    ".git",
    "__pycache__",
    "node_modules"
}

# 除外する拡張子
EXCLUDE_EXTENSIONS = {
    ".pyc",
    ".log",
    ".tmp"
}

# 出力ファイル名
OUTPUT_FILE = "project_structure.txt"


# ==========================
# メイン処理
# ==========================

def should_exclude(path: Path):
    if path.name in EXCLUDE_DIRS:
        return True
    if path.suffix in EXCLUDE_EXTENSIONS:
        return True
    return False


def build_tree(directory: Path, prefix=""):
    lines = []

    entries = [
        e for e in sorted(
            directory.iterdir(),
            key=lambda x: (x.is_file(), x.name.lower())
        )
        if not should_exclude(e)
    ]

    for index, entry in enumerate(entries):
        connector = "└── " if index == len(entries) - 1 else "├── "
        lines.append(prefix + connector + entry.name)

        if entry.is_dir():
            extension = "    " if index == len(entries) - 1 else "│   "
            lines.extend(build_tree(entry, prefix + extension))

    return lines


def main():
    root_path = Path(ROOT_DIR).resolve()
    print(f"Scanning: {root_path}")

    tree_lines = [root_path.name]
    tree_lines.extend(build_tree(root_path))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(tree_lines))

    print(f"\nStructure exported to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
