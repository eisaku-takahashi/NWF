from nwf.thread_engine import ThreadEngine
from nwf.thread_engine import ThreadValidationError


JSON_PATH = "projects/test_project/ThreadEngine/threads_master.json"


def main():

    engine = ThreadEngine(JSON_PATH)

    print("===== ThreadEngine v0.4 Test =====\n")

    # ----------------------------
    # Thread取得テスト
    # ----------------------------

    print("----- Thread S1 -----")
    print(engine.get_thread("S1"))

    # ----------------------------
    # Open Threads
    # ----------------------------

    print("\n----- Open Threads -----")
    print(engine.get_open_threads())

    # ----------------------------
    # Resolved Threads
    # ----------------------------

    print("\n----- Resolved Threads -----")
    print(engine.get_resolved_threads())

    # ----------------------------
    # Emotion Peaks
    # ----------------------------

    print("\n----- Emotion Peaks -----")
    print(engine.get_emotion_peaks())

    # ----------------------------
    # Emotion Valleys
    # ----------------------------

    print("\n----- Emotion Valleys -----")
    print(engine.get_emotion_valleys())

    # ----------------------------
    # Dependency Validation
    # ----------------------------

    print("\n----- Dependency Validation -----")

    try:
        result = engine.validate_dependencies()
        print("OK:", result)

    except ThreadValidationError as e:
        print("ERROR:")
        print(e)

    # ----------------------------
    # Thread Graph
    # ----------------------------

    print("\n----- Thread Graph -----")

    graph = engine.build_thread_graph()

    for k, v in graph.items():
        print(f"{k} -> {v}")

    # ----------------------------
    # Dependency Chain Test
    # ----------------------------

    print("\n----- Dependency Chain (S3) -----")

    chain = engine.get_dependency_chain("S3")

    print(chain)


if __name__ == "__main__":
    main()