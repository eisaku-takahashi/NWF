Source: docs/spec/Engine_Spec/NWF_CharacterEngine_v2.0.0.md
Updated: 2026-03-17T22:20:00+09:00
PIC: Engineer / ChatGPT

# NWF CharacterEngine v2.0.0

---

## 1. 概要

Character Engine はキャラクターの状態と意思決定を管理するエンジンである。

---

## 2. キャラクターの定義

キャラクターは以下を持つ。

- character_id
- goal
- traits
- current_state

---

## 3. Engine の役割

- 状態管理
- 意思決定
- 行動生成

---

## 4. データ構造

character は以下を持つ。

- character_id
- state_reference
- goal_state
- relationships

---

## 5. 評価規則

行動は以下で決定される。

action = argmax(utility(goal_state, current_state, traits))

---

## 6. 変換ロジック

- 状態評価
- 目標との差分計算
- 行動選択

---

## 7. 制約

- goal_state 必須
- state_reference 必須

---

## 8. 他Engineとの連携

- State Engine
- Conflict Engine
- EmotionalCurve Engine

---

## 9. 処理フロー

- 状態取得
- 意思決定
- 行動生成

---

## 10. まとめ

Character Engine は意思決定主体を管理するエンジンである。

---

[EOF]