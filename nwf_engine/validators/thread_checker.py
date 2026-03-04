# nwf_engine\validators\thread_checker.py


import os
import json


def validate_threads(project_path):
    
    result = {
        "validator": "thread",
        "status": "OK",
        "details": []
    }

    thread_dir = os.path.join(project_path, "ThreadEngine")

    if not os.path.isdir(thread_dir):
        result["status"] = "ERROR"
        result["details"].append("ThreadEngine directory not found")
        return result
    
    thread_path = os.path.join(
        project_path,
        "ThreadEngine",
        "threads_master.json"
    )

    if not os.path.isfile(thread_path):
        result["status"] = "ERROR"
        result["details"].append("threads_master.json not found")
        return result

    try:
        with open(thread_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        result["status"] = "ERROR"
        result["details"].append(f"Failed to read threads_master.json: {e}")
        return result

    # -----------------------------
    # 基本構造チェック
    # -----------------------------
    if not isinstance(data, dict):
        result["status"] = "ERROR"
        result["details"].append("threads_master.json root must be an object")
        return result

    if "threads" not in data:
        result["status"] = "ERROR"
        result["details"].append("threads key missing")
        return result

    if not isinstance(data["threads"], list):
        result["status"] = "ERROR"
        result["details"].append("threads must be a list")
        return result

    if len(data["threads"]) == 0:
        result["status"] = "WARNING"
        result["details"].append("threads list is empty")

    # -----------------------------
    # 未回収スレッド検出
    # -----------------------------
    unresolved = []

    for thread in data["threads"]:
        if not isinstance(thread, dict):
            result["status"] = "ERROR"
            result["details"].append("Each thread must be an object")
            return result

        if "id" not in thread:
            result["status"] = "ERROR"
            result["details"].append("Thread missing id")
            return result

        if "status" not in thread:
            result["status"] = "ERROR"
            result["details"].append(f"Thread {thread.get('id', '?')} missing status")
            return result

        if thread["status"] != "resolved":
            unresolved.append(thread["id"])

    if unresolved:
        result["status"] = "WARNING"
        result["details"].append(
            "Unresolved threads: " + ", ".join(unresolved)
        )

    return result