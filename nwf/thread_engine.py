import json
from pathlib import Path


class ThreadEngine:

    def __init__(self, json_path: str):
        self.json_path = Path(json_path)
        self.data = None
        self.threads = []

    # -----------------------------
    # JSON Load
    # -----------------------------

    def load(self):

        if not self.json_path.exists():
            raise FileNotFoundError(f"JSON file not found: {self.json_path}")

        with open(self.json_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        self.threads = self.data.get("threads", [])

    # -----------------------------
    # Thread取得
    # -----------------------------

    def get_thread(self, thread_id: str):

        for thread in self.threads:
            if thread["id"] == thread_id:
                return thread

        return None

    # -----------------------------
    # open threads
    # -----------------------------

    def get_open_threads(self):

        return [
            t for t in self.threads
            if t.get("status") == "open"
        ]

    # -----------------------------
    # resolved threads
    # -----------------------------

    def get_resolved_threads(self):

        return [
            t for t in self.threads
            if t.get("status") == "resolved"
        ]

    # -----------------------------
    # emotion peak
    # -----------------------------

    def get_emotion_peaks(self):

        peaks = []

        for t in self.threads:

            if "emotion_peak" in t:
                peaks.append({
                    "thread_id": t["id"],
                    "scene": t["emotion_peak"]
                })

        return peaks

    # -----------------------------
    # emotion valley
    # -----------------------------

    def get_emotion_valleys(self):

        valleys = []

        for t in self.threads:

            if "emotion_valley" in t:
                valleys.append({
                    "thread_id": t["id"],
                    "scene": t["emotion_valley"]
                })

        return valleys