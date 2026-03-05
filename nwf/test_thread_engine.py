from nwf.thread_engine import ThreadEngine

engine = ThreadEngine(
    "projects/test_project/ThreadEngine/threads_master.json"
)

engine.load()

print("----- Thread S1 -----")
print(engine.get_thread("S1"))

print("\n----- Open Threads -----")
print(engine.get_open_threads())

print("\n----- Resolved Threads -----")
print(engine.get_resolved_threads())

print("\n----- Emotion Peaks -----")
print(engine.get_emotion_peaks())

print("\n----- Emotion Valleys -----")
print(engine.get_emotion_valleys())