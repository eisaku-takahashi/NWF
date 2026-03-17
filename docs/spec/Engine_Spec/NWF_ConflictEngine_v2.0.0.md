Source: docs/spec/Engine_Spec/NWF_ConflictEngine_v2.0.0.md
Updated: 2026-03-17T22:20:00+09:00
PIC: Engineer / ChatGPT

# NWF ConflictEngine v2.0.0

---

## 1. 概要

Conflict Engine は対立構造を定義し、State変化を駆動するエンジンである。

---

## 2. 対立の定義

対立は目的・状態の不一致である。

---

## 3. Engine の役割

- 対立生成
- 強度評価
- 解決管理

---

## 4. データ構造

conflict は以下を持つ。

- conflict_id
- actors
- related_states
- intensity_score
- resolution_status

---

## 5. 評価規則

intensity_score は以下で算出される。

intensity_score = goal_difference * resource_conflict * urgency

---

## 6. 変換ロジック

- 状態差分取得
- 対立強度算出
- State変化誘発

---

## 7. 制約

- actors は2以上
- intensity_score は 0.0 - 1.0

---

## 8. 他Engineとの連携

- Character Engine
- State Engine
- Beat Engine

---

## 9. 処理フロー

- 対立生成
- 強度評価
- 解決判定

---

## 10. まとめ

Conflict Engine は物語の駆動力となるエンジンである。

---

[EOF]