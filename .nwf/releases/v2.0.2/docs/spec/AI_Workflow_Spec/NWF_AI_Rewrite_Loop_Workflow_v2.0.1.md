Source: docs/spec/AI_Workflow_Spec/NWF_AI_Rewrite_Loop_Workflow_v2.0.1.md
Updated: 2026-03-28T20:59:00+09:00
PIC: Engineer / ChatGPT

# NWF AI Rewrite Loop Workflow v2.0.1

---

## 1. 概要

NWF AI Rewrite Loop Workflow は、NWF v2.0.1（Story OS）における品質改善の中核アルゴリズムであり、物語生成・分析・編集を循環させることで作品品質を段階的に向上させる自己改善型フィードバック制御システムである。

本ワークフローの目的は、Story OS を単なるコンテンツ生成システムではなく、Integrity Score を制御指標として分析と改稿を繰り返し、最終的に高品質な作品へ収束させる知能的循環系として動作させることである。

Rewrite Loop は Execution Pipeline の内部に存在するサブループとして定義され、Generation・Analysis・Editing の各 Workflow を統合して動作する。

---

## 2. Loop Architecture

Rewrite Loop は以下のフィードバックサイクルで構成される。

### Rewrite Loop Feedback Cycle

1. Draft Submission  
   Generation Workflow により生成された初稿または改稿データを受け取る。

2. Diagnostic Analysis  
   Analysis Workflow により構造・伏線・キャラクター・テーマ・整合性などの多層分析を実施する。

3. Score Verification  
   Integrity Engine により Integrity Score を算出し、ユーザー定義閾値と比較する。

4. Directive Issue  
   スコアが閾値未満の場合、Analysis Interface を通じて Editing Workflow に対する修正指示（Directive）を生成する。

5. Targeted Editing  
   Editing Workflow により Directive に基づく構造修正・文章修正・演出強化などの改稿を行う。

6. State Update  
   修正済みデータを Data Spec に保存し、バージョン番号を更新する。

7. Re-entry / Exit  
   スコア条件に応じて Rewrite Loop を継続または終了する。

この一連の処理を 1 Cycle と定義する。

---

## 3. Core Logic & Scoring

Rewrite Loop の継続・終了は Integrity Score によって制御される。

### Loop Control Logic

Loop Continue 条件  
Integrity Score < User_Defined_Threshold

Loop Finish 条件  
Integrity Score >= User_Defined_Threshold

### Forced Terminate 条件

以下のいずれかに該当する場合、Rewrite Loop を強制終了する。

1. 最大リライト回数 Max_Retry_Count 到達
2. スコア改善停滞 Stagnation Detect
   連続 3 回の Rewrite Cycle において Integrity Score の有意な向上がない場合
3. Human Stop
   作者または管理者による手動停止

Rewrite Loop は品質向上を目的とするが、無限ループを防ぐため終了条件を必ず持つ。

---

## 4. State Machine Specification

Rewrite Loop は状態遷移モデル（State Machine）として定義される。

### State Definitions

IDLE  
システム待機状態

GENERATING  
物語生成フェーズ

ANALYZING  
作品分析フェーズ

EDITING  
改稿・修正フェーズ

FINALIZING  
最終版確定フェーズ

HUMAN_INTERVENTION  
人間介入フェーズ

### State Transition

IDLE → Start → GENERATING

GENERATING → Generation Complete → ANALYZING

ANALYZING → Integrity Score < Threshold → EDITING

EDITING → Revision Complete → ANALYZING

ANALYZING → Integrity Score >= Threshold → FINALIZING

EDITING / ANALYZING → Error or Stagnation → HUMAN_INTERVENTION

HUMAN_INTERVENTION → Resume → ANALYZING または EDITING

この状態遷移モデルにより Rewrite Loop の動作が明確に定義される。

---

## 5. Analysis-Editing Feedback Interface

Analysis Workflow と Editing Workflow は Directive を介して接続される。

### Directive Information Structure

Directive には以下の情報が含まれる。

- 問題箇所
- 問題カテゴリ（構造・キャラクター・伏線・テンポ・文章など）
- 修正方針
- 優先度
- 参考改善例
- 期待される効果
- 影響範囲

Editing Workflow は Directive を入力として改稿を行い、改稿結果は再び Analysis Workflow に送られる。

これにより Analysis → Directive → Editing → Analysis の情報循環が形成される。

---

## 6. Human-in-the-Loop Supervisory

Rewrite Loop には人間の監督権限が存在する。

### Human Control Functions

1. Integrity Score Threshold の設定
2. Rewrite Loop 最大回数の設定
3. 特定 Directive の承認・却下
4. 強制終了
5. 特定バージョンの採用
6. 手動編集後の Loop 再開

Story OS は完全自動ではなく、人間の創作意図を最終的な意思決定とする Human-in-the-Loop モデルを採用する。

---

## 7. Version & History Management

Rewrite Loop では各 Cycle ごとにバージョン管理を行う。

### Versioning Rules

- Rewrite Cycle 実行ごとに Minor Version を +1
- 各バージョンに Integrity Score を記録
- 最高スコアのバージョンを Best Version として保持
- スコアが低下した場合は Best Version にロールバック可能

### Best Version Preservation Algorithm

1. 新バージョン生成
2. Integrity Score 計算
3. 最高スコアと比較
4. 高い場合 Best Version 更新
5. 低い場合 Best Version を維持
6. 必要に応じてロールバック

これにより品質の単調増加に近い挙動を実現する。

---

## 8. Optimization Strategies

Rewrite Loop の最適化戦略として以下を採用できる。

### Parallel Rewrite Strategy

- 同一 Draft から複数の改稿案を並列生成
- 各案を Analysis Workflow で評価
- Integrity Score が最も高い案を採用
- A/B テスト型評価方式

### Local Optimization Strategy

- 全体改稿ではなく問題箇所のみ局所改稿
- Rewrite Cost を削減
- 収束速度向上

### Structural First Strategy

改稿優先順位：

1. 構造
2. キャラクター
3. 伏線
4. テーマ
5. テンポ
6. 文章表現

上位構造から修正することで効率的に Integrity Score を向上させる。

---

## 9. Stagnation & Termination

Rewrite Loop は改善停滞を検出する必要がある。

### Stagnation Detection

以下の条件で停滞と判定する。

- 3 Cycle 連続で Score 改善率が閾値未満
- 修正量が増えているのに Score が上昇しない
- Analysis Directive が同一内容を繰り返す

### Termination Conditions

Rewrite Loop 終了条件：

1. Integrity Score が閾値到達
2. Max Retry Count 到達
3. Stagnation Detection
4. Human Stop
5. System Error

Rewrite Loop は無限に続くのではなく、必ず終了条件を持つ制御ループとして設計される。

---

## 10. まとめ

NWF AI Rewrite Loop Workflow は Story OS における品質改善エンジンであり、

Generate → Analyze → Edit → Analyze → Improve

というフィードバック制御ループによって作品品質を段階的に向上させる自己改善型システムである。

この Rewrite Loop により Story OS は単なる文章生成システムではなく、分析・評価・改稿を繰り返して作品を最適化する知能的創作システムとして機能する。

Rewrite Loop は NWF v2.0.1 における品質保証・品質向上・バージョン管理・人間介入を統合する中核 Workflow である。

---

[EOF]