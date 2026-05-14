Source: docs/spec/AI_Interface/NWF_AI_Analysis_Interface_v2.0.1.md
Updated: 2026-03-28T07:50:00+09:00
PIC: Engineer / ChatGPT

# NWF AI Analysis Interface v2.0.1

---

## 1. 概要

NWF AI Analysis Interface v2.0.1 は、Story OS における「物語の自己修復」と「高次分析」を司るインテリジェント分析インターフェースである。本インターフェースは Analysis Engine と AI 推論を接続するための知能補完モジュールとして設計され、Story OS の自己修復ループの中核を担う。

Analysis Engine が数値・論理・構造整合性を検証するのに対し、AI Analysis は物語的意味、感情の流れ、因果の説得力、キャラクター動機、テーマの一貫性などの定性的評価を行う。

本インターフェースの目的は以下である。

・矛盾を単なるエラーではなく改善機会へ変換する  
・物語構造の品質向上  
・Execution Pipeline の自己修復ループ構築  
・Retry Directive の生成  
・Correction Directive の生成  
・Story Integrity の定性評価  
・Narrative Quality の評価  
・Validation 結果の意味解釈  

AI Analysis Interface は Story OS における「Critic（批評家）」兼「Director（演出家）」として機能する。

---

## 2. Layer Position & Role

Story OS のレイヤー構造において AI Analysis Interface は Engine Layer ではなく、Orchestration Layer に直結した知能補完モジュールとして位置付けられる。

レイヤー関係:

Core Layer  
System Architecture Layer  
Data Layer  
Engine Layer  
Execution Layer  
Orchestration Layer  
AI Analysis Interface  
Prompt Protocol  
AI Reasoning  
Narrative Generation  

AI Analysis Interface は以下のシステム間の橋渡しを行う。

・Analysis Engine → AI Analysis  
・Validation System → AI Analysis  
・Error Model → Retry Directive  
・Execution Pipeline → Correction Directive  
・Prompt Protocol → Analysis Prompt  
・Data Layer → Analysis Input Data  

つまり本インターフェースは「Analysis Engine の結果を物語的意味に変換し、修正方針として Execution System に戻す知能ブリッジ」である。

---

## 3. Engine vs. AI Analysis

Analysis Engine と AI Analysis の責務は明確に分離される。

Analysis Engine（定量・論理分析）:
・Timeline 整合性チェック
・State 遷移整合性
・Event 因果関係チェック
・World Rule 違反検出
・データスキーマ検証
・数値 Integrity Score 計算
・Validation Flag 出力

AI Analysis（定性・物語分析）:
・キャラクター動機の整合性評価
・感情曲線の自然性評価
・物語展開の説得力評価
・テーマ一貫性評価
・物語テンポ分析
・Narrative Quality 評価
・矛盾の説明生成
・修正案生成
・Retry Directive 生成
・構造改善提案

Analysis Engine は「何が間違っているか」を検出し、
AI Analysis は「なぜ問題か」「どう直すか」を提示する。

---

## 4. Validation-Analysis-Retry Flow

Story OS の自己修復フローは以下の順序で動作する。

1. Execution / Simulation 実行
2. Validation System がエラー検出
3. Analysis Engine が論理分析
4. AI Analysis が意味分析
5. Analysis Report 生成
6. Correction Directive 生成
7. Retry Directive 生成
8. Execution Pipeline が再実行
9. Integrity Score 更新
10. 正常になるまでループ

このループにより Story OS は自己修復型ストーリー生成システムとなる。

---

## 5. Execution Pipeline Integration

AI Analysis Interface は Execution Pipeline の複数フェーズで呼び出される。

介入ポイント:

Plan Phase 後  
Execute Phase 後  
Simulation Phase 後  
Analyze Phase  
Validation Phase 後  
Retry 前  

各フェーズでの役割:

Plan Phase:
・構造の妥当性評価
・伏線配置評価
・キャラクターアーク評価

Execute Phase:
・イベント動機整合性評価
・キャラクター行動妥当性

Simulation Phase:
・因果関係の説得力
・展開の自然性

Analyze Phase:
・全体構造評価
・テーマ一貫性
・物語強度評価

Validation Phase:
・エラーの意味解釈
・修正方針決定

Retry Phase:
・再生成プロンプト指示生成

---

## 6. Data I/O Standard

AI Analysis Interface の入力データは複数の Story Context を統合した分析コンテクストである。

Input Data:

event_log  
state_history  
timeline  
character_states  
validation_result  
analysis_engine_result  
integrity_score  
emotional_curve  
world_rules  
recent_events  
narrative_summary  

Output Data:

analysis_report  
correction_directive  
retry_directive  
integrity_score_adjustment  
narrative_feedback  
structure_feedback  
character_feedback  
timeline_feedback  
theme_feedback  

Analysis Report は人間可読テキストおよび構造化データの両方を持つ。

---

## 7. Correction Protocol

Correction Directive は Execution Pipeline を修正するための指示データである。

Correction Directive 例:

・Event の順序変更
・Character Motivation 修正
・State 遷移修正
・Timeline 再構築
・World Rule 例外追加
・Narrative Tone 調整
・伏線追加
・イベント削除
・イベント追加
・感情曲線調整

Retry Directive は次回 Prompt に注入される修正パラメータである。

Retry Directive 例:

・regenerate_event
・adjust_character_motivation
・recalculate_state_transition
・insert_foreshadowing
・rewrite_dialogue
・modify_emotional_curve
・timeline_reorder

Correction Directive は構造修正、
Retry Directive は再生成指示である。

---

## 8. Maintenance & Versioning

AI Analysis Interface は以下の仕様変更と同期して更新される必要がある。

Execution Pipeline 変更  
Analysis Engine 変更  
Validation System 変更  
Error Model 変更  
Prompt Protocol 変更  
Data Spec 変更  
Narrative Engine 変更  

Version 更新ルール:

分析フロー変更 → Minor Version Up  
入出力データ変更 → Minor Version Up  
Execution Pipeline 連携変更 → Major Version Up  
Correction Protocol 変更 → Minor Version Up  

AI Analysis Interface は Story OS の品質管理中枢であり、Execution System と最も密接に連動するインターフェースの一つである。

---

## 9. まとめ

NWF AI Analysis Interface v2.0.1 は Story OS における自己修復型ストーリー生成を実現するための知能分析インターフェースである。

本インターフェースの本質は以下である。

・Analysis Engine の結果を物語的意味へ翻訳する  
・矛盾を改善案へ変換する  
・Retry Directive を生成する  
・Story Quality を評価する  
・Narrative Quality を評価する  
・Execution Pipeline を修正軌道へ戻す  
・Story OS の品質制御を行う  

AI Analysis Interface は Story OS における

Validator  
Critic  
Editor  
Director  
Analyst  

の役割を統合した「物語品質管理知能モジュール」である。

---

[EOF]