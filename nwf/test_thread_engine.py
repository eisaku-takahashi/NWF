from nwf.thread_engine import ThreadEngine


def main():

    print("===== ThreadEngine v0.5 Test =====\n")

    json_path = "projects/test_project/ThreadEngine/threads_master.json"

    engine = ThreadEngine(json_path)

    # ------------------------------
    # Thread取得
    # ------------------------------

    print("----- Thread S1 -----")
    print(engine.get_thread("S1"))
    print()

    # ------------------------------
    # Open / Resolved
    # ------------------------------

    print("----- Open Threads -----")
    print(engine.get_open_threads())
    print()

    print("----- Resolved Threads -----")
    print(engine.get_resolved_threads())
    print()

    # ------------------------------
    # Dependency Validation
    # ------------------------------

    print("----- Dependency Validation -----")
    print("OK:", engine.validate_dependencies())
    print()

    # ------------------------------
    # Thread Graph
    # ------------------------------

    print("----- Thread Graph -----")

    graph = engine.build_thread_graph()

    for k, v in graph.items():
        print(k, "->", v)

    print()

    # ------------------------------
    # Dependency Chain
    # ------------------------------

    print("----- Dependency Chain (S3) -----")
    print(engine.get_dependency_chain("S3"))
    print()

    # ------------------------------
    # Foreshadow Analyzer
    # ------------------------------

    print("----- Foreshadow Stats -----")
    print(engine.get_foreshadow_stats())
    print()

    print("----- Thread Type Stats -----")
    print(engine.get_thread_type_stats())
    print()

    print("----- Act Distribution -----")
    print(engine.get_act_distribution())
    print()

    # ------------------------------
    # Story Report
    # ------------------------------

    print("----- Story Report -----")

    report = engine.generate_story_report()

    for k, v in report.items():
        print(k, ":", v)

    print()


if __name__ == "__main__":
    main()