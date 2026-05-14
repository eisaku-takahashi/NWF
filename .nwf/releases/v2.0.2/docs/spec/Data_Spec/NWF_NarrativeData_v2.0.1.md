Source: docs/spec/Data_Spec/NWF_NarrativeData_v2.0.1.md
Updated: 2026-03-25T02:52:00+09:00
PIC: Engineer / ChatGPT

# NWF_NarrativeData_v2.0.1

---

## 1. 概要

NWF_NarrativeData_v2.0.1 は、物語シミュレーションの「事実（Story）」を読者が体験する「語り（Narrative）」へと変換する **動的情報提示レイヤー（Dynamic Information Disclosure Layer）** である。  
各スレッド・シーンの進行状況に応じて、提示情報の範囲・順序・信頼性を制御し、Story OS 上でのナラティブ生成と読者体験の最適化を実現する。

---

## 2. Core Metadata

- narrative_id: 一意識別子
- narrative_style: 語りのスタイル（例: 一人称, 三人称限定視点, 全知全能）
- global_perspective_mode: 物語全体の視点制御モード（例: objective, subjective）

---

## 3. POV Configuration

- focus_character_id: 焦点キャラクター
- knowledge_mapping: キャラクターが知る事実や記憶状態
- linguistic_bias: 語彙・口調・語りのトーン

---

## 4. Information Disclosure Logic

- disclosure_rules: ルールベースの情報開示制御
- state_based_filtering: キャラクター・読者状態に応じたフィルタリング
- foreshadowing_management: 伏線表示・回収の管理

---

## 5. Temporal & Sequential Control

- narrative_order_mapping: 読者提示順序
- flashback_flashforward_anchors: 回想・未来提示のアンカー
- multi_thread_synthesis: 並行スレッド情報の統合

---

## 6. Content Block Architecture

- content_blocks: 表示内容ブロックのリスト
  - block_id: 一意識別子
  - state: revealed / hidden / foreshadowed / revised
  - source_data_link: 対応する SceneData/Beat
  - rendering_metadata: 表示装飾や強調情報

---

## 7. Execution Flow Integration

- simulation_result_integration: スレッド・シーン実行結果からナラティブブロックを生成
- dynamic_update: 実行中に内容・状態を更新可能

---

## 8. まとめ

NWF_NarrativeData_v2.0.1 は、Story OS 上での動的ナラティブ生成を可能にするデータ基盤であり、  
読者体験の最適化、視点制御、情報開示の戦略的管理を実現する中心的構造である。

---

[EOF]