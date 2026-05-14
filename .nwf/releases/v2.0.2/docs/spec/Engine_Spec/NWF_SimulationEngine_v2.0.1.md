Source: docs/spec/Engine_Spec/NWF_SimulationEngine_v2.0.1.md
Updated: 2026-03-27T05:04:00+09:00
PIC: Engineer / ChatGPT

# NWF SimulationEngine v2.0.1

---

## 1. 概要

Simulation Engine は NWF（Novel Writing Framework）v2.0.1 において、未来の状態変化および因果連鎖を予測するための Intelligence Layer の中核エンジンである。

本エンジンは実際の StateData を直接変更せず、仮想実行環境上で複数の可能世界（Worldline）を試算し、その結果を Story Engine に提供することで、最適な物語進行の意思決定を支援する。

---

## 2. 設計思想

Simulation Engine は以下の思想に基づく。

- 物語を「分岐可能な未来空間」として扱う
- 実世界と仮想世界を厳密に分離する
- 因果律に基づく確率的予測を行う
- Story Engine の意思決定を補助する知能として機能する

---

## 3. Core Architecture

### 3.1 入力データ

- query_data（シミュレーション要求）
- state_snapshot（現在状態のコピー）
- timeline_reference（現在の時間構造）
- thread_graph（構造情報）

### 3.2 出力データ

- simulation_report
  - probability_distribution
  - causality_stability_score (0.0 - 1.0)
  - ending_reachability (0.0 - 1.0)
  - risk_assessment (0.0 - 1.0)

### 3.3 仮想実行環境

Simulation Engine は以下の仮想環境上で動作する。

- virtual_state_space
- virtual_timeline
- simulation_context

---

## 4. Simulation Modes

Simulation Engine は以下のモードを持つ。

### 4.1 Predictive Mode

- 現在状態から未来への順方向予測
- 時系列に沿った因果展開を試算

### 4.2 Branch Mode

- 複数の選択肢を分岐として展開
- 各分岐の結果を比較

### 4.3 What-if Mode

- 条件変更による影響分析
- State または Event の改変による結果差分を評価

### 4.4 Convergence Mode

- 複数 Thread の合流可能性を評価
- Timeline 上の収束点の成立確率を算出

---

## 5. Simulation Algorithms

### 5.1 基本アルゴリズム

1. state_snapshot の生成
2. virtual_timeline の構築
3. 分岐生成（必要に応じて）
4. 各分岐の因果連鎖を展開
5. 状態遷移の評価
6. 結果の統計処理

---

### 5.2 確率計算モデル

結果の確率は以下の要素に基づいて算出される。

- state_transition_probability
- conflict_resolution_probability
- character_decision_weight

---

### 5.3 因果安定性評価

causality_stability_score は以下で算出される。

causality_stability_score = consistency * continuity * constraint_satisfaction

---

## 6. Execution Lifecycle

Simulation Engine の処理は以下のライフサイクルで実行される。

1. Story Engine からの呼び出し
2. クエリ解析
3. スナップショット生成
4. 仮想シミュレーション実行
5. 結果集計
6. レポート生成
7. Story Engine へ返却

---

## 7. Resource Management

Simulation Engine は計算資源の制御を行う。

### 7.1 Depth 制限

- 最大探索深度（max_depth）を設定
- 過剰な未来展開を防止

### 7.2 Breadth 制限

- 分岐数（branch_factor）を制限
- 組み合わせ爆発を抑制

### 7.3 Cost 制御

- 計算コスト上限（max_cost）を設定
- 高負荷処理の中断または簡略化

---

## 8. Interaction with Analysis Engine

Simulation Engine は Analysis Engine と連携する。

### 8.1 フィードバックループ

- Simulation 実行
- Analysis による矛盾検出
- 問題がある場合、再試算

### 8.2 役割分離

- Simulation: 未来の可能性を予測
- Analysis: 論理整合性を検証

---

## 9. Story Engine との連携

Simulation Engine は Story Engine の指示に従い動作する。

- 分岐点での到達可能性評価
- リスクスコアの提供
- 最適経路選択の支援

Story Engine は Simulation 結果をもとに、実 Timeline への反映を決定する。

---

## 10. 制約

- 実 StateData を直接変更してはならない
- 仮想環境でのみ演算を行う
- 計算資源制限を遵守する

---

## 11. Data Spec 依存関係

Simulation Engine は以下の Data Spec に依存する。

- StateData v2.0.1
- TimelineData v2.0.1
- ThreadData v2.0.1
- QueryData v2.0.1

---

## 12. まとめ

Simulation Engine v2.0.1 は、物語の未来を仮想空間で計算し、最適な進行を導く予測エンジンである。

実世界の状態を保護しながら、複数の可能性を試算することで、Story OS における高度な意思決定を実現する。

---

[EOF]