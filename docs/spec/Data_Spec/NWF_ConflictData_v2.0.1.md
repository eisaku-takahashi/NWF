Source: docs/spec/Data_Spec/NWF_ConflictData_v2.0.1.md
Updated: 2026-03-25T03:24:00+09:00
PIC: Engineer / ChatGPT

# NWF ConflictData v2.0.1

---

## 1. 概要

ConflictData は物語内の対立や葛藤を **動的葛藤シミュレーション・モデル** として管理するデータ構造である。  
Thread や Scene における「何が対立し、どうエスカレートし、どう解消（あるいは失敗）したか」を演算し、感情曲線（Emotional Curve）や世界の状態を動的に変化させることを目的とする。

---

## 2. Core Metadata

- conflict_id: 一意識別子
- conflict_type: Internal / External / Social / etc.
- importance_level: 優先度 / インパクトの重要度

---

## 3. Participants & Stakes

- involved_characters: 関与キャラクターIDリスト
- goal_alignment: 各キャラクターの目標の整合性・対立方向
- stakes: 各キャラクターが失う・得るリスクや報酬の定量・定性データ

---

## 4. Temporal & Causal Data

- origin_event_id: 対立を引き起こした原因イベントのID
- timeline_span: 開始時刻・終了時刻
- lifecycle_state: planned / latent / active / escalated / peaked / resolved / failed / transformed

---

## 5. Simulation Parameters

- intensity_curve: 現在の対立強度（0.0-1.0）
- escalation_triggers: エスカレーションを発生させる条件
- tension_output_ratio: Scene/Thread への波及率

---

## 6. Resolution & Branching Logic

- resolution_path: 解決ルートの候補
- branching_conditions: 失敗・膠着時の分岐条件（IF シミュレーション）
- state_change_deltas: World / Character の状態変化

---

## 7. Narrative Impact

- emotional_arc_links: 対立が感情曲線に与える影響
- reader_impact_type: カタルシス、絶望、サスペンスなど読者への影響指標

---

## 8. Execution Flow Integration

- Scene 実行に伴い、Conflict の状態を動的に更新するプロセスを含む。

---

[EOF]