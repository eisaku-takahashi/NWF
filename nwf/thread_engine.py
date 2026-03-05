import json


class ThreadValidationError(Exception):
    pass


class ThreadEngine:

    def __init__(self, json_path):

        with open(json_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        self.threads = self.data.get("threads", [])

        self.thread_map = {
            thread["id"]: thread
            for thread in self.threads
        }

    # -----------------------------
    # v0.3 API
    # -----------------------------

    def get_thread(self, thread_id):

        return self.thread_map.get(thread_id)

    def get_open_threads(self):

        return [
            t for t in self.threads
            if t.get("status") == "open"
        ]

    def get_resolved_threads(self):

        return [
            t for t in self.threads
            if t.get("status") == "resolved"
        ]

    def get_emotion_peaks(self):

        return [
            t for t in self.threads
            if t.get("emotion") == "peak"
        ]

    def get_emotion_valleys(self):

        return [
            t for t in self.threads
            if t.get("emotion") == "valley"
        ]

    # -----------------------------
    # v0.4 API
    # -----------------------------

    def validate_dependencies(self):

        errors = []

        for thread in self.threads:

            deps = thread.get("depends_on", [])

            for dep in deps:

                if dep not in self.thread_map:

                    errors.append(
                        f"{thread['id']} depends_on unknown thread {dep}"
                    )

        if errors:
            raise ThreadValidationError(
                "\n".join(errors)
            )

        return True

    def build_thread_graph(self):

        graph = {}

        for thread in self.threads:

            graph[thread["id"]] = thread.get("depends_on", [])

        return graph

    def get_dependency_chain(self, thread_id):

        chain = []
        visited = set()

        def walk(tid):

            if tid in visited:
                return

            visited.add(tid)
            chain.append(tid)

            thread = self.thread_map.get(tid)

            if not thread:
                return

            for dep in thread.get("depends_on", []):

                walk(dep)

        walk(thread_id)

        return chain