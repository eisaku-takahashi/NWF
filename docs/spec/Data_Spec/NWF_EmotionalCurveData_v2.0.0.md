Source: docs/spec/Data_Spec/NWF_EmotionalCurveData_v2.0.0.md
Updated: 2026-03-18T10:32:00+09:00
PIC: Engineer / ChatGPT

# NWF EmotionalCurveData v2.0.0

---

## 1. 概要

EmotionalCurveData はキャラクターや状況の感情変化を定量化・記録するデータ構造である。

---

## 2. データ構造

- emotion_id: 一意識別子
- subject: 感情主体（キャラクターIDなど）
- emotion_type: 感情タイプ
- intensity_value: 強度 (0.0-1.0)
- valence: 正負方向 (-1.0~1.0)
- timestamp: 記録時刻
- context: 状況情報や関連イベント

---

## 3. まとめ

EmotionalCurveData は物語内の感情動態を数値として記録・分析するためのデータである。

---

[EOF]