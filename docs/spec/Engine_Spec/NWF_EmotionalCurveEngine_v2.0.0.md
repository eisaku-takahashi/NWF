Source: docs/spec/Engine_Spec/NWF_EmotionalCurveEngine_v2.0.0.md
Updated: 2026-03-17T22:20:00+09:00
PIC: Engineer / ChatGPT

# NWF EmotionalCurveEngine v2.0.0

---

## 1. 概要

Emotional Curve Engine は State変化を数値化し、感情として評価・可視化するエンジンである。

---

## 2. 感情の定義

感情とは State差分に対する評価関数の出力である。

emotion = f(state_delta, expectation, context)

---

## 3. Engine の役割

- 感情状態の算出
- 感情曲線生成
- 体験分析

---

## 4. データ構造

emotional_state は以下を持つ。

- state_reference
- emotion_type
- intensity_value (0.0 - 1.0)
- valence (-1.0 - 1.0)

---

## 5. 評価規則

intensity_value は以下で算出される。

intensity_value = abs(state_delta) * expectation_gap

valence は以下で決定される。

valence = sign(goal_alignment)

---

## 6. 変換ロジック

- State差分取得
- 期待値との差分算出
- 感情タイプ分類
- 数値スコア化

---

## 7. 制約

- intensity_value は 0.0 以上 1.0 以下
- valence は -1.0 から 1.0

---

## 8. 他Engineとの連携

- State Engine: 入力
- Beat Engine: 変化起点
- Character Engine: 主観補正

---

## 9. 処理フロー

- State取得
- 差分計算
- 感情評価
- 曲線生成

---

## 10. まとめ

Emotional Curve Engine は State変化を感情として定量化するエンジンである。

---

[EOF]