Source: docs/spec/Data_Spec/NWF_ThreadData_v2.0.0.md
Updated: 2026-03-18T10:32:00+09:00
PIC: Engineer / ChatGPT

# NWF ThreadData v2.0.0

---

## 1. 概要

ThreadData は物語のストーリーライン（Thread）の構造・進行・依存関係を管理するデータ構造である。

---

## 2. データ構造

- thread_id: 一意識別子
- description: ストーリーライン説明
- related_threads: 関連 Thread ID リスト
- scenes: 関連 Scene ID リスト
- status: 進行状態
- dependencies: 依存関係情報

---

## 3. まとめ

ThreadData は物語の骨格である Thread の構造・進行・整合性を管理するデータである。

---

[EOF]