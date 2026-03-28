Source: docs/spec/AI_Workflow_Spec/NWF_AI_Human_In_The_Loop_v2.0.1.md
Updated: 2026-03-28T21:58:00+09:00
PIC: Engineer / ChatGPT

# NWF AI Human In The Loop v2.0.1

---

## 1. 概要

本ドキュメントは、NWF v2.0.1（Story OS）における Human-in-the-Loop（人間介在型意思決定モデル）を定義する。
Story OS は完全自動生成システムではなく、AI が提案・生成・分析・改稿を行い、人間（作者・監督）が選択・修正・最終決定を行う共創型意思決定システムとして設計される。

本仕様は以下を定義する。
- 人間の意思決定権限
- Execution Pipeline 上の承認ゲート
- AI 評価に対する Human Override
- 意思決定履歴（Decision Log）
- バージョン確定プロセス

Human は Story OS における最終意思決定主体であり、AI は意思決定支援および生成エンジンとして機能する。

---

## 2. Human-AI Collaboration Model

Story OS における Human と AI の役割分担を以下のように定義する。

### 2.1 AI の役割
AI は以下を担当する。
- コンセプト生成
- プロット生成
- 本文生成
- 分析（Structure / Emotion / Consistency）
- Rewrite Directive 作成
- Rewrite 実行
- Integrity Score 計算
- Parallel Variant 生成
- データ整理・履歴管理

AI は「提案・生成・分析・改稿」を担当する。

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

Human は「判断・承認・選択・最終決定」を担当する。

---

## 3. Approval Gate Specification

Execution Pipeline 上に Human Approval Gate を配置する。
Gate が存在するステップでは、Human の承認が得られるまで Pipeline は停止する。

### 3.1 Human Approval Gate フラグ
Execution Node に以下のフラグを持たせる。

Wait_For_Human_Approval = true

このフラグが true の場合、次のステップへ進む前に Human Decision を待機する。

### 3.2 主な介入ポイント

Human が介入する主要ポイントは以下。

1. Initial Concept Approval  
   テーマ、ジャンル、Integrity Threshold、Loop 設定などの初期設定を確定する。

2. Parallel Variant Selection  
   複数生成された Draft / Plot / Scene から採用案を選択する。

3. Rewrite Directive Review  
   AI が生成した Rewrite Directive を承認・修正・却下する。

4. Loop Continue Decision  
   Rewrite Loop を継続するか、終了するかを判断する。

5. Final Approval  
   最終稿を承認し、Version Freeze を実行する。

---

## 4. Authority & Role Hierarchy

Human の権限は Role-Based Access Control（RBAC）により管理する。

### 4.1 Role 定義

Observer  
閲覧のみ可能。編集・承認・設定変更は不可。

Editor  
文章の手動編集、Rewrite Directive の微調整が可能。

Director  
Parallel Variant の採択、Rewrite Loop 継続/停止、Threshold 変更が可能。

Architect (Owner)  
システム設定変更、Version Freeze、最終承認、Export が可能。

### 4.2 権限階層

Observer < Editor < Director < Architect

最終決定権は Architect が持つ。

---

## 5. Human Override Mechanism

AI の評価結果に対して Human は強制的に意思決定を上書きできる。

### 5.1 Integrity Score Override

AI が算出する Integrity Score に対して Human Score を追加する。

Human は以下の操作を実行できる。
- Force Approve（強制採用）
- Force Reject（強制却下）
- Score Adjustment（スコア補正）

最終決定優先順位は以下。

Human Decision > Human Score > Integrity Score > AI Recommendation

AI の評価は参考情報であり、最終決定は常に Human が行う。

---

## 6. Parallel Variant Selection

Parallel Workflow により複数 Variant が生成される。
Human は以下の操作を行う。

- Variant A 採用
- Variant A + B Merge
- Variant Reject
- Variant Rewrite 指示
- 新 Variant 生成指示

Variant 選択は Decision Log に保存される。

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

---

## 8. Decision History & Audit Log

すべての Human Decision は Decision Log として保存される。

記録する情報は以下。
- Decision Timestamp
- User Role
- Selected Variant
- Rejected Variant
- Directive Edited
- Score Override
- Loop Continue / Stop
- Final Approval
- Version Freeze

Decision Log は創作過程の監査ログとして機能する。

---

## 9. Finalization & Version Freeze

作品完成プロセスを定義する。

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

Version Freeze 後は内容変更不可とする。

---

## 10. Exception Handling

Human が一定時間応答しない場合の挙動を定義する。

### 10.1 Timeout
Human Approval Gate で一定時間応答がない場合
- Pipeline Pause 継続
- Auto Approve
- Auto Reject
- Default Variant Selection

いずれかのポリシーを設定可能とする。

### 10.2 Emergency Stop
Human はいつでも Execution Pipeline を停止できる。

---

## 11. まとめ

Human-in-the-Loop モデルにおいて、
AI は生成・分析・改稿・評価を行うエンジンであり、
Human は意思決定・選択・承認・最終判断を行う統治層である。

Story OS は
AI Automation System ではなく
Human Decision Governance System の上に構築された
Human-AI Collaborative Creation System として定義される。

この Human-in-the-Loop モデルは Story OS 全体のガバナンス層として機能する。

---

[EOF]