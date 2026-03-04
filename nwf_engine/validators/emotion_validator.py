# nwf_engine\validators\emotion_validator.py


import os
import json

EMOTION_DIR = "EmotionalCurve"


def validate_emotion(project_path):

    result = {
        "validator": "emotion",
        "status": "OK",
        "details": []
    }

    emotion_dir = os.path.join(project_path, EMOTION_DIR)
    global_curve_path = os.path.join(emotion_dir, "global_curve.json")

    # (1) ディレクトリ存在チェック
    if not os.path.isdir(emotion_dir):
        result["status"] = "ERROR"
        result["details"].append(f"{EMOTION_DIR} directory not found") # 改善(任意)
        return result
    
    # (2) global_curve.json存在チェック
    if not os.path.isfile(global_curve_path):
        result["status"] = "ERROR"
        result["details"].append("global_curve.json not found")
        return result

    # (3) JSON整合性チェック
    try:
        with open(global_curve_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:    # 例外の完全捕捉
        result["status"] = "ERROR"
        result["details"].append(f"Failed to read global_curve.json: {e}")
        return result

    # (4) 空ファイル対応
    if not isinstance(data, dict):
        result["status"] = "ERROR"
        result["details"].append("global_curve.json root must be an object")
        return result

    # ▼ 進化部分 ▼
    if "global_curve" not in data:
        result["status"] = "ERROR"
        result["details"].append("global_curve key missing")
        return result

    if not isinstance(data["global_curve"], list):
        result["status"] = "ERROR"
        result["details"].append("global_curve must be a list")
        return result

    if len(data["global_curve"]) == 0:
        result["status"] = "WARNING"
        result["details"].append("global_curve is empty")

    return result