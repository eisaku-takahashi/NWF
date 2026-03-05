import json
from collections import Counter


class ThreadValidationError(Exception):
    pass


class ThreadEngine:

    def __init__(self, json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.threads = data["threads"]

    # ------------------------------
    # Basic Queries
    # ------------------------------

    def get_thread(self, thread_id):
        for t in self.threads:
            if t["id"] == thread_id:
                return t
        return None

    def get_open_threads(self):
        return [t for t in self.threads if t["status"] == "open"]

    def get_resolved_threads(self):
        return [t for t in self.threads if t["status"] == "resolved"]

    # ------------------------------
    # Dependency Validation
    # ------------------------------

    def validate_dependencies(self):

        ids = {t["id"] for t in self.threads}

        for t in self.threads:
            for dep in t.get("depends_on", []):
                if dep not in ids:
                    return False

        return True

    # ------------------------------
    # Graph
    # ------------------------------

    def build_thread_graph(self):

        graph = {}

        for t in self.threads:
            graph[t["id"]] = t.get("depends_on", [])

        return graph

    # ------------------------------
    # Dependency Chain
    # ------------------------------

    def get_dependency_chain(self, thread_id):

        chain = []
        visited = set()

        def dfs(tid):

            if tid in visited:
                return

            visited.add(tid)

            thread = self.get_thread(tid)
            if not thread:
                return

            chain.append(tid)

            for dep in thread.get("depends_on", []):
                dfs(dep)

        dfs(thread_id)

        return chain

    # ------------------------------
    # Foreshadow Analyzer
    # ------------------------------

    def get_unresolved_threads(self):

        return [t for t in self.threads if t["status"] != "resolved"]

    def get_foreshadow_stats(self):

        levels = [t.get("foreshadow_level", "none") for t in self.threads]

        return Counter(levels)

    def get_thread_type_stats(self):

        types = [t.get("type", "unknown") for t in self.threads]

        return Counter(types)

    def get_act_distribution(self):

        acts = []

        for t in self.threads:

            scene = t.get("setup_scene")

            if scene and scene.startswith("Act"):
                act = scene.split("-")[0]
                acts.append(act)

        return Counter(acts)

    # ------------------------------
    # Story Report
    # ------------------------------

    def generate_story_report(self):

        total = len(self.threads)
        open_threads = len(self.get_open_threads())

        foreshadow = self.get_foreshadow_stats()
        types = self.get_thread_type_stats()
        acts = self.get_act_distribution()

        report = {
            "total_threads": total,
            "open_threads": open_threads,
            "foreshadow_levels": dict(foreshadow),
            "thread_types": dict(types),
            "act_distribution": dict(acts),
        }

        return report