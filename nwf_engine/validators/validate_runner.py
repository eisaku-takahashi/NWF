# nwf_engine\validators\validate_runner.py


import os
import json


def run_validations(project_path, mode="all"):

    results = []

    # -----------------------------
    # 1) Project validation (必須)
    # -----------------------------
    from .project_validator import validate_project
    project_result = validate_project(project_path)
    results.append(project_result)

    if project_result["status"] == "ERROR":
        return results

    # -----------------------------
    # 2) project_config 読み込み
    # -----------------------------
    config_path = os.path.join(project_path, "project_config.json")

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception:
        return results  # project validator が既にERROR出している前提

    required_engines = config.get("required_engines", [])

    # -----------------------------
    # 3) Emotion validation
    # -----------------------------
    if mode in ("all", "emotion") and "emotion" in required_engines:
        from .emotion_validator import validate_emotion
        results.append(validate_emotion(project_path))

    # -----------------------------
    # 4) Thread validation
    # -----------------------------
    if mode in ("all", "thread") and "thread" in required_engines:
        from .thread_checker import validate_threads
        results.append(validate_threads(project_path))

    return results