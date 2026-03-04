import os
import shutil
import json

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates", "minimal_project")


def create_project(name, path=None, readme=False):
    target_base = path if path else os.path.join(os.getcwd(), "projects")
    target_path = os.path.join(target_base, name)

    if os.path.exists(target_path):
        raise FileExistsError(f"{target_path} already exists.")

    shutil.copytree(TEMPLATE_DIR, target_path)

    # project_config更新
    config_path = os.path.join(target_path, "project_config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    config["project_name"] = name

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

    if readme:
        with open(os.path.join(target_path, "README.md"), "w", encoding="utf-8") as f:
            f.write(f"# {name}\n\nCreated with NWF\n")

    print(f"Project '{name}' created at {target_path}")
