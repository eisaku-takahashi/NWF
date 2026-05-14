Source: docs/spec/Execution_Spec/NWF_Error_Model_v2.0.1.md
Updated: 2026-04-25T07:40:00+09:00
PIC: Engineer / ChatGPT

# NWF Error Model v2.0.1（Refactored）

---

## 1. 概要

NWF Error Model は、Story OS におけるエラーの定義、分類、伝播、Rollback、および整合性維持のための基本原則を規定する。

本モデルにおいてエラーは「失敗」ではなく、

**整合性回復を駆動する再計算トリガー**

として扱われる。

---

## 2. 設計原則

本モデルは以下の原則に従う：

- 非停止（Non-Blocking by Default）
- 自己修復（Self-Healing）
- 非破壊（Immutable / Pass-through）
- 単調性（Monotonicity）
- 決定論（Deterministic）

---

## 3. Error Classification

エラーはレイヤーごとに分類される。

---

### 3.1 Data Layer Error

データ構造および参照整合性に関するエラー。

- Reference Error
- Schema Error
- Status Error
- Integrity Field Missing

---

### 3.2 Engine Layer Error

物語内部ロジックに関するエラー。

- Temporal Error
- Causal Error
- State Error
- Emotional Error

---

### 3.3 Intelligence Layer Error

物語全体の整合性に関するエラー。

- Integrity Error
- Consistency Error
- Narrative Logic Error
- Simulation Divergence

---

### 3.4 Presentation Layer Error

生成物（文章・表現）に関するエラー。

- Narrative Generation Error
- Style Error
- Missing Narrative Segment

---

## 4. Engine Error Responsibility

各 Engine は以下の責務を持つ。

Query Engine:
- Reference Error
- Schema Error

Story Engine:
- Structure Error
- Thread Inconsistency

Timeline Engine:
- Temporal Error

Event Engine:
- Causal Error

Simulation Engine:
- State Error

EmotionalCurve Engine:
- Emotional Error

Analysis Engine:
- Integrity Error
- Consistency Error
- Cross Engine Conflict

Narrative Engine:
- Narrative Generation Error
- Style Error

---

## 5. Validation & Detection Flow

基本フロー：

1. Engine Execution
2. Self Validation
3. Execution Log 出力
4. Analysis Engine 送信
5. Cross Validation
6. Integrity Score 計算
7. Gate 判定
8. Pass / Rollback

---

## 6. Severity Model

### 6.1 定義

| Severity | 意味 |
|----------|------|
| INFO | 正常 |
| WARNING | 軽微な問題 |
| ERROR | 修復対象 |
| CRITICAL | 致命的破綻 |

---

### 6.2 Status 対応

| Severity | Status |
|----------|--------|
| INFO | healthy |
| WARNING | warning |
| ERROR | recovering |
| CRITICAL | fatal |

---

## 7. Severity Monotonicity Rule（最重要）

### 7.1 原則

一度発生した Severity は減衰してはならない。

---

### 7.2 禁止事項

- CRITICAL → ERROR / WARNING / INFO
- ERROR → WARNING / INFO
- WARNING → INFO

---

### 7.3 許可

- INFO → WARNING → ERROR → CRITICAL

---

### 7.4 実装指針

- ValidationResult は完全保持
- 集約禁止
- 書き換え禁止

---

## 8. ValidationResult 不変性

- immutable（frozen）前提
- 既存結果の変更禁止
- Pass-through構造を維持

---

## 9. Rollback & Recalculation

### 9.1 基本動作

エラー検出時：

- Rollback 実行
- 再計算（Recalculation）

---

### 9.2 Rollback 単位

1. Engine Tier Rollback
2. Phase Rollback

---

### 9.3 Severity別動作

| Severity | 動作 |
|----------|------|
| CRITICAL | 即時停止 + Rollback |
| ERROR | Rollback対象 |
| WARNING | 継続 |
| INFO | 無視 |

---

### 9.4 最大試行回数

- recalculation_max_attempts を超過した場合：
  → Execution Abort

---

## 10. Logging Specification

### 10.1 必須ログ

- engine_name
- execution_phase
- validation_result
- integrity_score
- error_code
- error_message
- timestamp
- retry_count
- rollback_flag

---

### 10.2 Severity Trace Logging

すべての層で以下を出力：

- severity list
- transaction_id
- stardate

目的：

- CRITICAL伝播の追跡
- Debug容易化
- 監査対応

---

## 11. Error Code System

カテゴリ：

- DATA_ERROR
- ENGINE_ERROR
- TEMPORAL_ERROR
- CAUSAL_ERROR
- STATE_ERROR
- EMOTIONAL_ERROR
- INTEGRITY_ERROR
- NARRATIVE_ERROR
- EXECUTION_ABORT
- SYSTEM_ERROR

---

## 12. Execution Status

状態：

- healthy
- warning
- recovering
- fatal
- aborted
- completed

---

## 13. Escalation Logic との関係

本仕様は以下を前提とする：

- ERROR累積によるCRITICAL昇格は別仕様で管理
- 本モデルは「個別エラーの意味と扱い」のみを定義する

参照：

- NWF_Escalation_Logic_Spec_v2.0.1

---

## 14. 制約事項

- ValidationResult は正規化済み前提
- scope / target_id は外部仕様に依存
- 集約・簡略化は禁止

---

## 15. 将来拡張

### Phase 3.6

- Temporal-aware Error Handling
- Location Resolution
- Dynamic Threshold（Escalation側）

---

### Phase 4以降

- Probabilistic Error Model
- Anomaly Detection
- Adaptive Recovery

---

## 16. 結論

本モデルにより：

- エラーは停止要因ではなく再計算トリガーとなる
- Validation Pipeline は非破壊構造となる
- Severity は完全に保存される
- Rollback は統一的に制御される

---

### ✔ 最終状態

- ValidationResult は完全不変
- Severity は単調増加のみ
- Engine は責務単位でエラーを検出
- Analysis Engine が最終整合性を判断

---

### 🔴 重要

本仕様は「エラーの意味と伝播」を定義する。

**統計的昇格（Escalation）は別仕様に完全分離される。**

---

[EOF]