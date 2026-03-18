Source: docs/spec/Data_Spec/NWF_TimelineData_v2.0.0.md
Updated: 2026-03-18T10:32:00+09:00
PIC: Engineer / ChatGPT

# NWF TimelineData v2.0.0

---

## 1. 概要

TimelineData は物語全体の時間構造（Timeline）と Scene 配置を管理するデータ構造である。

---

## 2. データ構造

- timeline_id: 一意識別子
- absolute_time: 絶対時間
- relative_time: 相対時間
- logical_time: 論理時間
- scene_placements: Scene ID と時間区間の対応
- parallel_events: 同時進行イベント情報

---

## 3. まとめ

TimelineData は物語の時間軸管理を統合的に行い、複雑な時系列構造の整合性を保証するデータである。

---

[EOF]