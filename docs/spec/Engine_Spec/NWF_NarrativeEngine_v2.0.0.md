Source: docs/spec/Engine_Spec/NWF_NarrativeEngine_v2.0.0.md
Updated: 2026-03-17T22:20:00+09:00
PIC: Engineer / ChatGPT

# NWF NarrativeEngine v2.0.0

---

## 1. 概要

Narrative Engine は物語の語り構造と情報開示を制御するエンジンである。

---

## 2. 語りの定義

語りは以下を持つ。

- point_of_view
- narration_order
- information_scope

---

## 3. Engine の役割

- 視点制御
- 情報開示制御
- 時系列再構成

---

## 4. データ構造

narrative は以下を持つ。

- narrative_id
- pov
- timeline_mapping
- disclosure_control

---

## 5. 評価規則

情報開示は以下で決定される。

visible_info = total_info * disclosure_control

---

## 6. 変換ロジック

- Timeline取得
- 順序再構成
- 情報フィルタリング

---

## 7. 制約

- timeline_mapping は整合性必須
- pov は単一または明示的切替

---

## 8. 他Engineとの連携

- Timeline Engine
- Scene Engine
- Foreshadowing Engine

---

## 9. 処理フロー

- 視点設定
- 情報制御
- 出力順調整

---

## 10. まとめ

Narrative Engine は物語の見せ方を制御するエンジンである。

---

[EOF]