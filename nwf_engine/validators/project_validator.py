# nwf_engine\validators\project_validator.py


import os
import json


def validate_project(project_path):

    result = {
        "validator": "project",
        "status": "OK",
        "details": []
    }

    config_path = os.path.join(project_path, "project_config.json")

    # 存在チェック
    if not os.path.isfile(config_path):
        result["status"] = "ERROR"
        result["details"].append("project_config.json not found")
        return result

    # JSON整合性
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        result["status"] = "ERROR"
        result["details"].append(f"Failed to read project_config.json: {e}")
        return result

    # root型チェック
    if not isinstance(data, dict):
        result["status"] = "ERROR"
        result["details"].append("project_config.json root must be an object")
        return result

    # 必須キー
    required_keys = ["project_name", "version", "required_engines"]

    for key in required_keys:
        if key not in data:
            result["status"] = "ERROR"
            result["details"].append(f"{key} missing")

    if result["status"] == "ERROR":
        return result

    # 型チェック
    if not isinstance(data["required_engines"], list):
        result["status"] = "ERROR"
        result["details"].append("required_engines must be a list")

    return result