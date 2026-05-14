Source: docs/spec/AI_Workflow_Spec/NWF_AI_Human_In_The_Loop_v2.0.1.md
Updated: 2026-04-04T15:38:00+09:00
PIC: Engineer / ChatGPT

# NWF AI Human In The Loop v2.0.1

---

## 1. 概要

本ドキュメントは、NWF v2.0.1 における Human-in-the-Loop（人間介在型意思決定モデル）を定義する。

NWF システムは完全自動実行システムではなく、AI が提案・生成・分析・改稿を行い、人間（Architect / Director / Editor）が承認・修正・最終決定を行う Governance 型意思決定システムとして設計される。

また、本仕様は NWF_Kernel_Audit_System と連携し、人間のすべての承認・却下・上書き決定を監査ログとして記録し、意思決定の説明責任（Accountability）とトレーサビリティを確保する。

本仕様は以下を定義する。
- 人間の意思決定権限
- Execution Pipeline 上の承認ゲート
- AI 評価に対する Human Override
- 意思決定履歴（Decision Log）
- Audit Log との連携
- バージョン確定プロセス

Human は NWF における最終意思決定主体であり、AI は意思決定支援および生成エンジンとして機能する。

---

## 2. Human-AI Collaboration Model

NWF における Human と AI の役割分担を以下のように定義する。

### 2.1 AI の役割

AI は以下を担当する。
- コンテンツ生成
- 分析（Structure / Consistency / Integrity）
- Rewrite Directive 作成
- Rewrite 実行
- Integrity Score 計算
- Parallel Variant 生成
- データ整理・履歴管理
- Integrity Check 実行
- レポート生成

AI は「提案・生成・分析・改稿・評価・整理」を担当する。

### 2.2 Human の役割

Human は以下を担当する。
- コンセプト承認
- Variant 選択
- Rewrite 指示の承認・修正
- Loop 継続 / 停止 判断
- スコアに関係なく採用 / 却下 決定
- 手動編集
- 最終稿確定
- Version Freeze
- 公開 / Export
- システム設定変更
- 最終承認

Human は「判断・承認・選択・統治・最終決定」を担当する。

---

## 3. Approval Gate Specification

Execution Pipeline 上に Human Approval Gate を配置する。
Gate が存在するステップでは、Human の承認が得られるまで Pipeline は停止する。

### 3.1 Human Approval Gate フラグ

Execution Node に以下のフラグを持たせる。

wait_for_human_approval = true

このフラグが true の場合、次のステップへ進む前に Human Decision を待機する。

### 3.2 主な介入ポイント

Human が介入する主要ポイントは以下。

1. Initial Concept Approval  
2. Parallel Variant Selection  
3. Rewrite Directive Review  
4. Loop Continue Decision  
5. Final Approval  
6. Version Freeze  
7. Export Approval  

すべての Approval Gate 通過時には Audit Log にイベントを記録する。

---

## 4. Authority & Role Hierarchy

Human の権限は Role-Based Access Control（RBAC）により管理する。

### 4.1 Role 定義

Observer  
閲覧のみ可能。編集・承認・設定変更は不可。

Editor  
文章の手動編集、Rewrite Directive の微調整が可能。

Director  
Variant の採択、Rewrite Loop 継続/停止、Threshold 変更が可能。

Architect  
システム設定変更、Version Freeze、最終承認、Export が可能。

### 4.2 権限階層

Observer < Editor < Director < Architect

最終決定権は Architect が持つ。

すべての権限操作は actor_id と role を含めて Audit Log に記録する。

---

## 5. Human Override Mechanism

AI の評価結果に対して Human は強制的に意思決定を上書きできる。

### 5.1 Integrity Score Override

Human は以下の操作を実行できる。
- force_approve
- force_reject
- score_adjustment

最終決定優先順位は以下。

human_decision > human_score > integrity_score > ai_recommendation

AI の評価は参考情報であり、最終決定は常に Human が行う。

Override 実行時には Audit Log に override_event を記録する。

---

## 6. Parallel Variant Selection

Parallel Workflow により複数 Variant が生成される。
Human は以下の操作を行う。

- variant_select
- variant_merge
- variant_reject
- variant_rewrite
- variant_regenerate

Variant 選択結果は Decision Log および Audit Log に記録される。

---

## 7. Directive Correction Workflow

AI が生成した Rewrite Directive は Human により添削・修正される。

Workflow は以下。

1. AI Analysis
2. Rewrite Directive Generated
3. Human Review Directive
4. Directive Edit / Approve / Reject
5. Rewrite Execution
6. Re-Analysis
7. Loop Continue Decision

Human は Rewrite Loop の方向性を制御する役割を持つ。

Directive の編集内容、承認、却下はすべて監査ログへ記録する。

---

## 8. Decision Log & Audit Log Integration

すべての Human Decision は Decision Log と Audit Log の両方に記録される。

記録する情報は以下。
- decision_timestamp
- actor_id
- actor_role
- decision_type
- selected_variant
- rejected_variant
- directive_edited
- score_override
- loop_continue
- final_approval
- version_freeze
- decision_comment
- transaction_id

Decision Log は意思決定履歴管理用、
Audit Log は監査・証跡管理用として機能する。

Decision Log と Audit Log は transaction_id により必ず紐付ける。

---

## 9. Finalization & Version Freeze

作品または成果物の完成プロセスを定義する。

### 9.1 Final Approval
Human が最終稿を承認する。

### 9.2 Version Freeze
Version を固定し、Rewrite Loop と Parallel Workflow を停止する。

### 9.3 Export
以下の形式で出力可能。
- Markdown
- PDF
- EPUB
- JSON Archive

Version Freeze、Export 実行時には必ず Audit Log に finalization_event を記録する。

Version Freeze 後は内容変更不可とする。

---

## 10. Exception Handling

Human が一定時間応答しない場合の挙動を定義する。

### 10.1 Timeout
Human Approval Gate で一定時間応答がない場合

- pipeline_pause
- auto_approve
- auto_reject
- default_variant_selection

いずれかのポリシーを設定可能とする。

Timeout 発生時は timeout_event を Audit Log に記録する。

### 10.2 Emergency Stop
Human はいつでも Execution Pipeline を停止できる。
Emergency Stop 実行時は emergency_stop_event を監査ログへ記録する。

---

## 11. Audit Logging Requirements for HITL

Human-In-The-Loop におけるすべての操作は監査対象イベントとする。

監査対象イベント例:
- approval_event
- rejection_event
- override_event
- variant_selection_event
- directive_edit_event
- loop_decision_event
- final_approval_event
- version_freeze_event
- export_event
- emergency_stop_event

各イベントには以下の情報を必ず含める。
- event_id
- transaction_id
- actor_id
- actor_role
- event_type
- target_object
- decision_comment
- timestamp_jst

これにより Human 意思決定の完全なトレーサビリティを保証する。

---

## 12. まとめ

Human-in-the-Loop モデルにおいて、
AI は生成・分析・改稿・評価を行うエンジンであり、
Human は意思決定・選択・承認・最終判断を行う統治層である。

NWF は
AI Automation System ではなく
Human Decision Governance System の上に構築された
Human-AI Collaborative Governance System として定義される。

本 Human-in-the-Loop 仕様は Governance Layer の中核であり、
すべての意思決定は Audit System により記録・追跡・検証可能でなければならない。

---

[EOF]