#!/usr/bin/env python3
"""
NWF Structure Export Tool
Framework構造をテキスト出力するCLIツール
"""

import os
import argparse


DEFAULT_EXCLUDES = {".git", ".venv", "__pycache__"}


def generate_tree(root_path, exclude_dirs, max_depth=None):
    lines = []

    for root, dirs, files in os.walk(root_path):
        # 現在の階層レベル算出
        level = root.replace(root_path, "").count(os.sep)

        # depth制限チェック
        if max_depth is not None and level > max_depth:
            continue

        # 除外ディレクトリ処理
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        indent = "    " * level
        lines.append(f"{indent}{os.path.basename(root)}/")

        # depth制限内のみファイル表示
        if max_depth is None or level < max_depth:
            sub_indent = "    " * (level + 1)
            for f in files:
                lines.append(f"{sub_indent}{f}")

    return "\n".join(lines)


def export(output="project_structure.txt",
           exclude=None,
           depth=None):

    if exclude is None:
        exclude = DEFAULT_EXCLUDES

    root_path = os.getcwd()

    structure = generate_tree(
        root_path,
        set(exclude),
        depth
    )

    with open(output, "w", encoding="utf-8") as f:
        f.write(structure)

    print(f"Structure exported to {output}")


def main():
    parser = argparse.ArgumentParser(
        description="Export NWF project directory structure"
    )

    parser.add_argument(
        "--output",
        default="project_structure.txt",
        help="Output file name"
    )

    parser.add_argument(
        "--exclude",
        nargs="*",
        default=list(DEFAULT_EXCLUDES),
        help="Directories to exclude"
    )

    parser.add_argument(
        "--depth",
        type=int,
        default=None,
        help="Maximum depth of directory tree"
    )

    args = parser.parse_args()

    export(
        output=args.output,
        exclude=args.exclude,
        depth=args.depth
    )


if __name__ == "__main__":
    main()
