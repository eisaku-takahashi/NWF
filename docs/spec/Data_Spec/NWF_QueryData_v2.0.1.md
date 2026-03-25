Source: docs/spec/Data_Spec/NWF_QueryData_v2.0.1.md
Updated: 2026-03-26T04:42:00+09:00
PIC: Engineer / ChatGPT

# NWF QueryData v2.0.1

---

## 1. 概要

QueryData は NWF v2.0.1（Story OS）において、データ検索・分析・因果追跡・シミュレーション実行を統合的に定義する **「統合データアクセス・分析・シミュレーション命令言語（Unified Data Access & Simulation Command）」** である。

本データは、Data Layer（State / Event / Scene / Character 等）と Engine Layer（Query / Analysis / Simulation / Narrative）を接続し、複雑な物語構造を横断的に解析・操作するための中核インターフェースとして機能する。

---

## 2. コアメタデータ

- query_id: 一意識別子
- query_type: クエリ種別（causality_trace / dependency_analysis / knowledge_audit / if_simulation / search / aggregation 等）
- priority: 実行優先度（0.0-1.0）
- execution_engine: 実行対象エンジン（query_engine / analysis_engine / simulation_engine）

---

## 3. 対象およびスコープ定義

- target_scope: 対象データドメイン（character / state / event / scene / timeline / relationship / information 等）
- entity_scope: 対象エンティティIDリストまたは条件
- time_scope: 時間範囲（absolute_time / relative_time / timeline_range / alternate_timeline）
- narrative_scope: Narrative Order / Execution Order のどちらを対象とするか

---

## 4. コマンドロジック

- filter_conditions: 抽出条件式（属性・状態・関係性に基づく条件）
- aggregation_rules: 集計ルール（count / sum / average / distribution 等）
- causality_depth: 因果関係探索の深度（整数値）
- dependency_scope: 依存関係の探索範囲（direct / indirect / full_graph）

---

## 5. シミュレーションパラメータ（任意）

- delta_injection: 仮定する状態変化（IF 条件）
- branching_logic: 分岐条件および評価基準
- prediction_horizon: 未来予測の深さ（時間またはステップ数）

---

## 6. ナラティブおよび知識クエリ

- perception_filter: 観測主体（character_id / reader）ごとの認識フィルタ
- knowledge_state_condition: 「誰が何を知っているか」の条件式
- disclosure_state: 情報公開状態（hidden / foreshadowed / revealed）

---

## 7. 出力仕様

- output_format: 出力形式（node_list / graph / timeline / scalar_value / report）
- visualization_metadata: グラフ可視化や表示に関する補助情報
- sorting_rules: 並び替え条件
- limit: 出力件数制限

---

## 8. 依存関係および相互作用

- related_data_specs: 参照する DataSpec（StateData / EventData / SceneData / TimelineData / NarrativeData 等）
- causality_model_link: Core における因果モデルとの接続情報
- execution_flow_link: Execution_Flow における実行位置や役割

---

## 9. まとめ

QueryData v2.0.1 は、単なる検索条件定義を超え、

- データ横断検索
- 因果関係の遡及・分析
- 依存関係グラフの展開
- ナラティブと知識状態の照会
- IF シミュレーションおよび未来予測

を統合的に扱う、Story OS の知的インターフェースである。

本データ構造により、物語全体を「問い合わせ可能なシステム」として扱い、分析・検証・生成を高精度に実行することが可能となる。

---

[EOF]