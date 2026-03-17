Source: docs/spec/Engine_Spec/NWF_ForeshadowingEngine_v2.0.0.md
Updated: 2026-03-17T22:20:00+09:00
PIC: Engineer / ChatGPT

# NWF ForeshadowingEngine v2.0.0

---

## 1. 概要

Foreshadowing Engine は未来のState変化への参照と整合性を管理するエンジンである。

---

## 2. 伏線の定義

伏線とは未来Stateへの因果リンクである。

---

## 3. Engine の役割

- 伏線生成
- 状態リンク管理
- 回収検証

---

## 4. データ構造

foreshadowing は以下を持つ。

- setup_point
- target_state
- resolution_point
- validity_score (0.0 - 1.0)

---

## 5. 評価規則

validity_score は以下で算出される。

validity_score = consistency * causality * visibility

---

## 6. 変換ロジック

- setup時にtarget_stateを登録
- Timeline上で一致確認
- resolution時に一致判定

---

## 7. 制約

- setup_point < resolution_point
- target_state は存在必須

---

## 8. 他Engineとの連携

- State Engine: 状態参照
- Timeline Engine: 時間保証
- Scene Engine: 表示位置

---

## 9. 処理フロー

- 伏線登録
- 状態リンク
- 回収検証

---

## 10. まとめ

Foreshadowing Engine は未来状態との整合性を保証するエンジンである。

---

[EOF]