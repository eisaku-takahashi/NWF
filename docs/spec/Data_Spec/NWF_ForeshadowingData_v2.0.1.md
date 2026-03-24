Source: docs/spec/Data_Spec/NWF_ForeshadowingData_v2.0.1.md
Updated: 2026-03-25T04:08:00+09:00
PIC: Engineer / ChatGPT

# NWF ForeshadowingData v2.0.1

---

## 1. 概要

ForeshadowingData は物語内の伏線を管理するデータ構造である。  
v2.0.1 では、単なる伏線メモから発展し、**因果的整合性リンク・モデル (Causal Consistency Link Model)** として再定義され、設置から回収までの因果律を時間軸を超えて管理し、読者の驚きや納得感を制御する。

---

## 2. コアメタデータ

- foreshadowing_id: 一意識別子
- type: Foreshadowing Type（Explicit, Subtle, Red Herring, Retrospective 等）
- importance_level: 重要度
- validity_score: 妥当性 (0.0-1.0)

---

## 3. 因果アンカーポイント

- setup_point: 設置位置（Scene/Beat ID）
- payoff_point: 回収位置（Target Scene/Beat ID）

---

## 4. 論理要件

- target_state_change: 伏線が影響する状態変化
- prerequisites: 回収の前提条件（World/Character State 等）
- transformation_logic: 状態変化の適用ルール

---

## 5. 認知・ナラティブパラメータ

- salience: 読者への目立ちやすさ（Visibility）
- subjective_discovery: キャラクター視点での発見可能性
- discovery_timing: 回収のタイミング制御

---

## 6. 動的影響モデル

- tension_contribution: シーンやスレッドへの緊張度寄与
- predicted_catharsis_score: 回収時の感情的インパクトの予測値（カタルシス／驚き）

---

## 7. ライフサイクル & 状態管理

- lifecycle_state: planted / active / dormant / recovered / failed / subverted

---

## 8. 整合性エンジン統合

- consistency_checks: 未回収伏線や論理矛盾を検知するプロセス
- cross_thread_links: スレッド間の伏線依存関係管理

---

## 9. まとめ

v2.0.1 の ForeshadowingData は、物語の伏線を論理的かつ動的に管理することで、読者体験の制御やカタルシス演出を精密化するデータ構造である。

---

[EOF]