Source: docs/spec/Data_Spec/NWF_EmotionalCurveData_v2.0.1.md
Updated: 2026-03-25T06:22:00+09:00
PIC: Engineer / ChatGPT

# NWF EmotionalCurveData v2.0.1

---

## 1. 概要

EmotionalCurveData はキャラクターや状況の感情動態を動的に演算・管理するデータ構造である。
物語の進行に応じて、ConflictData やイベントから供給されるエネルギーを Valence（正負）・Intensity（強度）として出力し、物語全体のテンションやキャラクターの意思決定に影響を与える。

---

## 2. Dynamic Parameters

- emotion_id: 一意識別子
- subject_id: 感情主体（Character/Reader）
- emotion_model_type: 感情モデルタイプ（Valence-Arousal 2軸モデル等）
- valence: 正負方向 (-1.0～1.0)
- arousal: 活性度 (0.0～1.0)
- intensity_delta: 前ステップからの変化量
- velocity: 感情変化速度
- baseline: 平時の精神状態からの逸脱度
- tension_contribution: 物語全体のテンションへの寄与率
- trigger_link: 感情変化を引き起こした原因イベントID/ConflictID
- execution_step: シミュレーション実行ステップ
- narrative_order: 読者への提示順序

---

## 3. Causal & Temporal Data

- cause_effect_links: 他イベントやキャラクターからの感情影響追跡
- context: 状況情報や関連イベント
- timestamp: 記録時刻（演算ベース）

---

## 4. Impact & Output

- tension_contribution_score: 物語全体のテンションに与える影響値
- narrative_impact_metric: 読者体験への影響指標
- decision_influence: キャラクターの意思決定への影響度

---

## 5. State Management

- current_state: 現在の感情状態
- peak_value: 感情のピーク値
- recovery_rate: baseline への回復率
- lifecycle_state: `planted / active / dormant / recovered / failed / subverted` 等

---

## 6. Execution Flow Integration

シーンやビート実行時に感情値を更新し、次のスレッドや分岐選択に影響を与える。
Dynamic Feedback Loop により、キャラクターの感情変化は物語のテンション・成功率・次のアクション選択に反映される。

---

## 7. まとめ

EmotionalCurveData v2.0.1 は、キャラクターや物語全体の感情動態を動的に演算・管理する中核データであり、Story OS における「感情の演算可能変数化」を実現する。
ConflictData、ForeshadowingData、SceneData と統合されることで、読者体験の心理的起伏を精密に制御可能とする。

---

[EOF]