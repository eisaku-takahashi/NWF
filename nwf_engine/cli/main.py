# nwf_engine\cli\main.py


import argparse
import sys
import os
import json

from nwf_engine.tools import export_structure


def create_project(name, path=None, create_readme=False):

    base_path = path if path else os.path.join("projects", name)

    if os.path.exists(base_path):
        print("ERROR: Project already exists.")
        return

    # フォルダ作成
    os.makedirs(base_path)
    os.makedirs(os.path.join(base_path, "EmotionalCurve"))
    os.makedirs(os.path.join(base_path, "ThreadEngine"))

    # project_config.json
    config = {
        "project_name": name,
        "version": "0.1.0",
        "required_engines": ["emotion", "thread"]
    }

    with open(
        os.path.join(base_path, "project_config.json"),
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

    # global_curve.json
    with open(
        os.path.join(base_path, "EmotionalCurve", "global_curve.json"),
        "w",
        encoding="utf-8"
    ) as f:
        json.dump({"global_curve": []}, f, indent=4, ensure_ascii=False)

    # threads_master.json
    with open(
        os.path.join(base_path, "ThreadEngine", "threads_master.json"),
        "w",
        encoding="utf-8"
    ) as f:
        json.dump({"threads": []}, f, indent=4, ensure_ascii=False)

    # README
    if create_readme:
        with open(
            os.path.join(base_path, "README.md"),
            "w",
            encoding="utf-8"
        ) as f:
            f.write(f"# {name}\n\nCreated with NWF.\n")

    print(f"Project '{name}' created successfully.")


def main():
    parser = argparse.ArgumentParser(
        prog="nwf",
        description="Novel Writing Framework Engine CLI"
    )

    subparsers = parser.add_subparsers(dest="command")


    # --- validate コマンド ---
    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument(
        "--type",
        choices=["all", "emotion", "thread"],
        default="all"
    )


    # --- new コマンド ---
    new_parser = subparsers.add_parser(
        "new",
        help="Create a new project"
    )
    new_parser.add_argument(
        "name",
        help="Project name"
    )
    new_parser.add_argument(
        "--path",
        help="Project path (default: projects/name)"
    )
    new_parser.add_argument(
        "--readme",
        action="store_true",
        help="Create README.md"
    )


    # --- export コマンド ---
    export_parser = subparsers.add_parser(
        "export",
        help="Export project structure"
    )
    export_parser.add_argument(
        "--depth",
        type=int,
        default=None,
        help="Limit directory depth"
    )

    args = parser.parse_args()

    # --- 実行部 ---
    if args.command == "export":
        export_structure.export(depth=args.depth)
    elif args.command == "new":
        create_project(args.name, args.path, args.readme)
    elif args.command == "validate":
        from nwf_engine.validators.validate_runner import run_validations
        
        project_path = os.getcwd()
        results = run_validations(project_path, args.type)

        for result in results:
            print(f"[{result['validator']}] {result['status']}")
            for d in result["details"]:
                print(f"  - {d}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()