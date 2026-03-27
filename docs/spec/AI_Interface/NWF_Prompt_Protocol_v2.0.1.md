Source: docs/spec/AI_Interface/NWF_Prompt_Protocol_v2.0.1.md
Updated: 2026-03-28T07:32:00+09:00
PIC: Engineer / ChatGPT

# NWF Prompt Protocol v2.0.1

---

## 1. 概要

NWF Prompt Protocol v2.0.1 は、Story OS におけるシステム論理と AI 推論を接続するための実行プロトコルである。本プロトコルは単なるプロンプトテンプレートではなく、Execution Pipeline と連動して動作する「Story OS 実行インターフェース」として定義される。

Story OS では、AI は外部ツールではなく Engine Layer の一部として動作する。そのため Prompt Protocol は Execution Pipeline、Validation System、Analysis Engine、Error Model と統合された実行通信規格として設計される。

本プロトコルの目的は以下である。

- Story OS の実行フェーズに対応したプロンプト構造の定義
- AI 出力の再現性と構造化の保証
- Validation System と Analysis Engine のフィードバック統合
- Error Model に基づく Retry 制御
- Narrative 生成と Logic 演算の分離
- AI を Story OS の知能パーツとして安全に駆動する通信規律の確立

---

## 2. Phase-Specific Prompt Models

Prompt Protocol は Execution Pipeline の各フェーズに対応する Phase-aware Prompt 構造を持つ。

Execution Pipeline フェーズ対応:

1. Query Phase Prompt
2. Plan Phase Prompt
3. Execute Phase Prompt
4. Simulation Phase Prompt
5. Analysis Phase Prompt
6. Narrative Phase Prompt
7. Validation Phase Prompt
8. Save Phase Prompt

各フェーズでは以下の目的で AI が利用される。

### 2.1 Query Phase Prompt
- 要求内容の整理
- ストーリー生成目的の解析
- 制約条件の抽出

### 2.2 Plan Phase Prompt
- ストーリー構造設計
- Timeline / Event 構造計画
- Character Arc 設計

### 2.3 Execute Phase Prompt
- Event 内容生成
- 状態変化の定義
- 行動結果の生成

### 2.4 Simulation Phase Prompt
- 状態遷移シミュレーション
- 因果関係の検証
- WorldRule 適合確認

### 2.5 Analysis Phase Prompt
- 矛盾検出
- 構造分析
- 改善提案
- Integrity 評価

### 2.6 Narrative Phase Prompt
- 文章生成
- 描写生成
- 会話生成
- シーン構築

### 2.7 Validation Phase Prompt
- 検証結果説明
- 修正方針生成
- 再試算指示生成

### 2.8 Save Phase Prompt
- 出力要約
- メタデータ生成
- ログ生成

---

## 3. Internal Data Mapping

Prompt Protocol は Data_Spec v2.0.1 のデータ構造と対応関係を持つ。

Prompt Input と Data Layer の対応:

- characters → character_data
- timeline → timeline_data
- events → event_data
- world_rules → world_rule_data
- state_history → state_history_data
- event_log → event_log_data
- validation_result → validation_data
- integrity_score → integrity_data

Prompt Output は以下の形式で Data Layer に戻される。

- structured_json_output
- narrative_text_output
- analysis_report_output
- correction_directive_output
- retry_instruction_output

Logic 系フェーズでは JSON 出力を使用し、Narrative フェーズでは Text 出力を使用する。

---

## 4. Validation & Feedback Integration

Prompt Protocol は Validation System および Analysis Engine と統合される。

プロンプトには以下の Validation / Analysis 情報を含める。

- validation_status
- validation_errors
- validation_warnings
- integrity_score
- consistency_score
- analysis_feedback
- correction_directive
- retry_required_flag

Analysis Engine が矛盾や問題を検出した場合、Feedback Directive が生成され、次の Prompt に組み込まれる。

Feedback Directive の例:

- Timeline inconsistency detected
- Character motivation inconsistency
- Emotional curve imbalance
- Event causality conflict
- World rule violation

AI は Feedback Directive を基に修正生成を行う。

---

## 5. Error & Retry Handling

Prompt Protocol は Error Model と連携し Retry Protocol を実装する。

Retry 制御フィールド:

- error_code
- error_message
- retry_count
- max_retry_count
- retry_strategy
- context_reinjection_flag
- correction_priority

Retry Strategy 例:

- regenerate_output
- partial_regeneration
- constraint_adjustment
- context_reinjection
- engine_recalculation

最大リトライ回数を超えた場合、Execution Pipeline は停止または人間介入フェーズに移行する。

---

## 6. AI Agent Role Definitions

Story OS において AI は複数の役割を持つ Agent として動作する。

AI Agent Roles:

- Planner Agent
- Event Generator Agent
- Simulation Agent
- Analysis Agent
- Narrative Agent
- Validation Assistant Agent
- Summarization Agent

各 Agent は Execution Phase に応じて異なる Prompt Template を使用する。

Role 分離の目的:

- 推論の責務分離
- Narrative と Logic の混同防止
- Validation 精度向上
- 再現性の確保
- Debug 容易化

---

## 7. Stateful Prompt Management

Prompt Protocol は Stateful Prompt を採用する。

プロンプトに含まれる状態情報:

- current_execution_phase
- current_timeline_position
- active_characters
- recent_events
- state_delta
- emotional_state_summary
- integrity_score
- validation_status
- retry_count
- previous_feedback

Stateful Prompt により Story OS は連続した状態遷移を AI に認識させることができる。

---

## 8. Maintenance & Versioning

Prompt Protocol は以下の仕様変更と同期して更新される必要がある。

- Execution Pipeline 変更
- Engine 仕様変更
- Data Model 変更
- Validation Rule 変更
- Error Model 変更
- AI Interface 変更

Version 更新ルール:

- Prompt Structure 変更 → Minor Version Up
- Retry Protocol 変更 → Minor Version Up
- Phase Structure 変更 → Major Version Up
- Data Mapping 変更 → Minor Version Up

Prompt Protocol は Story OS の実行インターフェース仕様であり、Execution System の変更に最も影響を受ける仕様の一つである。

---

## 9. まとめ

NWF Prompt Protocol v2.0.1 は Story OS における AI との通信規律および実行プロトコルである。

本プロトコルの重要概念:

- Phase-aware Prompt
- Stateful Prompt
- Validation Integrated Prompt
- Feedback-driven Retry
- Logic / Narrative Separation
- AI Agent Role Separation
- Reproducible Prompt Execution
- Execution Pipeline Integration

本プロトコルにより Story OS は AI を単なる文章生成ツールではなく、論理実行エンジンの一部として統合し、自己修復可能な物語生成システムを実現する。

---

[EOF]