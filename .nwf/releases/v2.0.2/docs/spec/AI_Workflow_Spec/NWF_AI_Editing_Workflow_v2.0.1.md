Source: docs/spec/AI_Workflow_Spec/NWF_AI_Editing_Workflow_v2.0.1.md
Updated: 2026-03-28T20:29:00+09:00
PIC: Engineer / ChatGPT

# NWF AI Editing Workflow v2.0.1

---

## 1. 概要

本ドキュメントは、NWF v2.0.1 (Story OS) における改稿・改善・洗練プロセスを定義する。
Editing Workflow は単なる文章修正ではなく、Analysis Workflow によって生成された Directive（修正指示）を実行し、
物語の構造・表現・品質を再構築するための「実行層」として機能する。

Analysis が診断であるならば、Editing は治療である。
本 Workflow は Rewrite Loop の中核処理であり、物語品質を段階的に向上させることを目的とする。

---

## 2. Directive-Driven Editing 概念

NWF v2.0.1 における Editing は Directive Driven Editing と呼ばれる。

従来の Editing
文章を修正する

NWF Editing
Analysis → Directive → Editing → Re-Analysis → Quality Improvement

Editing は Analysis の結果を実際の修正へ変換する実行エンジンである。

Editing の役割
・Issue の解釈
・Rewrite Directive の実行
・構造修正
・文章修正
・テンポ調整
・感情強化
・文体統一
・品質改善
・Re-Analysis への引き渡し

---

## 3. Editing Layer Strategy

Editing は物語のデータ階層ごとに異なる修正を行う。

### 3.1 Thread Editing
・プロット再構成
・サブプロット追加 / 削除
・伏線再配置
・終盤再設計
・テーマ強化
・Thread 統合 / 分離

### 3.2 Scene Editing
・Scene 追加 / 削除
・Scene 並び替え
・Scene Goal 修正
・対立強化
・情報量調整
・テンポ調整

### 3.3 Beat Editing
・イベント追加 / 削除
・行動動機修正
・感情変化調整
・情報開示タイミング変更
・セリフ改善

### 3.4 Narrative Editing
・描写強化
・文体統一
・冗長削除
・語彙調整
・セリフ自然化
・感情描写強化

---

## 4. End-to-End Editing Workflow

Editing Workflow は以下の 7 ステップで構成される。

### Step 1 Directive Interpretation
Analysis Interface から渡された Rewrite Directive を解析する。

解析項目
・target_layer
・target_id
・problem_description
・rewrite_instruction
・priority
・expected_effect

### Step 2 Edit Planning
Editor ロールが修正方針を決定する。

決定内容
・修正対象レイヤー
・修正範囲
・構造修正の必要性
・部分修正か全面修正か
・Writer への指示内容

### Step 3 Structural Reconstruction
構造に問題がある場合、Thread / Scene / Beat 構造を再構築する。

例
・Scene の追加
・Scene 順序変更
・伏線再配置
・イベント再配置
・プロット再設計

### Step 4 Creative Rewriting
Writer が指示に基づき本文を再生成する。

修正内容
・描写修正
・セリフ修正
・行動動機追加
・心理描写追加
・情報追加 / 削除

### Step 5 Tone & Style Alignment
Director が前後の文章との整合性を調整する。

調整項目
・文体
・語彙
・トーン
・キャラクター口調
・テンポ
・テーマ一貫性

### Step 6 Refinement (Polishing)
文章の仕上げを行う。

・冗長削除
・表現改善
・感情強化
・読みやすさ向上
・リズム調整

### Step 7 Handover to Re-Analysis
修正後データを Analysis Workflow に戻す。
Integrity Score を再評価する。

---

## 5. Rewrite Directive Execution

Directive は Editing 操作に変換される。

### 5.1 Thread Layer Directive
操作例
・プロット分岐修正
・伏線再配置
・サブプロット統合
・エンディング再設計
・テーマ強化

### 5.2 Scene Layer Directive
操作例
・Scene 追加
・Scene 削除
・Scene 並び替え
・対立追加
・Scene Goal 修正

### 5.3 Beat Layer Directive
操作例
・行動動機追加
・イベント追加
・情報開示タイミング変更
・感情変化調整
・セリフ変更

### 5.4 Narrative Layer Directive
操作例
・文体統一
・描写具体化
・セリフ改善
・冗長削除
・心理描写追加

---

## 6. Multi-Agent Collaboration

Editing Workflow は複数 Agent によって実行される。

### 6.1 Editor
役割
・Issue 解釈
・Directive 解釈
・修正方針決定
・修正計画作成
・Writer への指示

Editor は設計者である。

### 6.2 Writer
役割
・文章修正
・描写生成
・セリフ生成
・Scene 再執筆
・Beat 修正

Writer は実装者である。

### 6.3 Director
役割
・全体整合性確認
・テーマ維持
・トーン統一
・品質最終調整
・Rewrite 範囲判断

Director は統括者である。

---

## 7. Integrity Maintenance

Editing によって新たな矛盾が発生する可能性があるため、
以下の整合性維持規律を守る必要がある。

・World Rule 違反禁止
・Timeline 矛盾禁止
・キャラクター設定維持
・伏線整合性維持
・因果関係維持
・テーマ一貫性維持

Editing 完了後は必ず Analysis Workflow を再実行する。

---

## 8. Human Review & Approval

Human は以下のタイミングで介入する。

・Directive 承認
・Rewrite 計画承認
・修正結果レビュー
・Rewrite 継続判断
・最終完成判断

Human は最終意思決定者である。

---

## 9. Partial Rewrite vs Total Rewrite

### Partial Rewrite
一部 Scene / Beat / Narrative のみ修正する。
Integrity Score が中程度の場合に使用。

### Total Rewrite
Thread / 構造レベルで再設計する。
Integrity Score が低い場合に使用。

判断基準例
Integrity Score
90以上 完成
80以上 部分修正
70以上 Rewrite
70未満 構造修正
60未満 全面 Rewrite

---

## 10. Versioning & Rollback

Editing Workflow ではバージョン管理を行う。

管理内容
・Draft Version
・Rewrite Version
・Directive History
・Integrity Score History
・Change Log

これにより過去バージョンへ Rollback 可能とする。

---

## 11. まとめ

NWF AI Editing Workflow は
物語の文章を修正するプロセスではなく、

Analysis Engine が発見した問題を修正し、
物語を段階的に完成へ近づけるための
「指示駆動型改稿エンジン」である。

Story OS において

Generate Engine が物語を生成し、
Analysis Engine が問題を発見し、
Editing Engine が物語を改善する。

この三層ループによって
物語品質は継続的に向上する。

Editing Workflow は Rewrite Loop の中心であり、
Story OS の品質向上を担う中核システムである。

---

[EOF]