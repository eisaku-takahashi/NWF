Source: docs/spec/Engine_Spec/NWF_StoryEngine_v2.0.1.md
Updated: 2026-03-26T21:30:00+09:00
PIC: Engineer / ChatGPT

# NWF StoryEngine v2.0.1

---

## 1. 概要

Story Engine は NWF v2.0.1 の Orchestration Layer における中枢エンジンであり、全 Engine の統括者として動作する。  
物語全体の進行、下位 Engine への命令伝達、因果伝搬の整合性管理、演算結果の競合解決を担い、Story OS における最高次オーケストレーターとして機能する。

---

## 2. Core Architecture

### 2.1 入力データ
- **Query Command**: 外部入力およびユーザー指示
- **Thread Graph**: 物語内 Thread 構造
- **Initial State / World Parameters**: 物語開始時の State とルール

### 2.2 出力データ
- **Orchestrated Timeline**: Timeline Engine への整列済みシーケンス
- **Engine Invocation Sequence**: Dynamics / Execution Layer 各 Engine への実行指示
- **Simulation / Analysis 指示**: 各介入ポイントでの動的制御

### 2.3 内部ステート
- 現在進行中の Query 状態
- 各 Engine の呼び出し順序・依存関係・因果伝搬ログ
- StateData 更新履歴と競合管理

---

## 3. Execution Lifecycle

1. **Query 受信**
2. **初期条件チェック**
3. **Thread / Timeline 構造取得**
4. **Dynamics Engine 演算指示生成**
5. **Execution Layer Engine 実行順序設定**
6. **Simulation / Analysis 介入制御**
7. **Timeline 更新指示**
8. **結果統合と Narrative / Dialogue 出力**
9. **次の Query 受信待機**

---

## 4. Operational Algorithms

### 4.1 Causality Propagation Logic
- 下位 Engine による State 変化を統合
- 因果律に基づく Delta 適用順序の管理
- 複数 Thread 収束時の最終決定権を保持

### 4.2 Engine Synchronization
- Dynamics → Execution → Narrative の順序制御
- Simulation / Analysis からのフィードバック同期
- State 書き込み権限の調停

### 4.3 Error Handling & Rollback
- Analysis Engine が矛盾検知時にロールバックまたは補正シナリオ生成
- Timeline 収束や Narrative 出力における再試行ロジック

---

## 5. Intelligence Integration

- **Simulation Engine**: 未来予測演算
- **Analysis Engine**: 因果・論理矛盾検出
- 各演算ステップへの介入タイミングと再帰的フィードバック制御を管理

---

## 6. Constraint & Validation Rules

- Timeline 上の同時進行 Event の矛盾検出
- StateData 競合書き込みの防止
- Thread 収束の整合性維持
- Narrative / Dialogue 出力整合性チェック

---

## 7. Maintenance & Versioning

- 依存 Data Spec: `Data_Spec/NWF_Data_Spec_Index_v2.0.1.md`
- v2.0.1 標準に準拠した Engine Invocation Sequence の保守
- Orchestration Layer における因果伝搬アルゴリズム更新履歴管理

---

## 8. まとめ

Story Engine v2.0.1 は、全 Engine を統括する Orchestration Layer の中枢として、Query 受信から Narrative 出力までの全処理を制御する。  
因果伝搬、State 更新、Simulation / Analysis 介入、Thread 収束などの統合管理により、Story OS の動的挙動と物語整合性を保証する。

---

[EOF]