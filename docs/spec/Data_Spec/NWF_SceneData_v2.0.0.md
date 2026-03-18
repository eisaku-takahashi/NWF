Source: docs/spec/Data_Spec/NWF_SceneData_v2.0.0.md
Updated: 2026-03-18T10:32:00+09:00
PIC: Engineer / ChatGPT

# NWF SceneData v2.0.0

---

## 1. 概要

SceneData は物語内のシーン単位の出来事、登場人物、時間・場所情報を管理するデータ構造である。

---

## 2. データ構造

- scene_id: 一意識別子
- characters: 登場キャラクターIDリスト
- location: 場所
- time_span: 開始時刻と終了時刻
- events: シーン内の出来事
- state_changes: Scene による状態変化

---

## 3. まとめ

SceneData は物語の最小実行単位であるシーンの情報を統合管理するデータである。

---

[EOF]