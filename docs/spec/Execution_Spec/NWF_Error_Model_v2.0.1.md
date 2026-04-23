Source: docs/spec/Execution_Spec/NWF_Error_Model_v2.0.1.md
Updated: 2026-04-22T11:11:00+09:00
PIC: Engineer / ChatGPT

# NWF Error Model v2.0.1

---

## 1. 概要

NWF Error Model は、NWF v2.0.1（Story OS）におけるエラー検知、例外処理、ロールバック、再演算、自己修復を統治する仕様である。

本モデルでは、エラーを単なる失敗や停止要因として扱わない。  
エラーは「システムの停止要因」ではなく、「整合性回復のための再実行トリガー」と定義される。

Story OS は物語の論理整合性、時間整合性、因果整合性、状態整合性、感情整合性を維持しながら物語を生成するシステムであるため、矛盾や不整合が検出された場合、Execution を停止するのではなく、Rollback と Recalculation を行い、整合性が回復するまで再計算を行う。

この自己修復型実行モデルを Self-Healing Narrative Execution Model と呼ぶ。

---

## 2. Error Classification

NWF におけるエラーはレイヤーごとに分類される。

### 2.1 Data Layer Error

Data Layer におけるエラーはデータ参照やスキーマに関する問題である。

主な Data Error:

- Reference Error  
  存在しない ID、参照不整合、リンク切れ
- Schema Error  
  必須フィールド欠落、型不一致、JSON 構造不正
- Status Error  
  不正なステータス遷移
- Integrity Field Missing  
  integrity_score や validation_result 欠落

これらは主に Query Engine および Data Validation 処理で検出される。

---

### 2.2 Engine Layer Error

Engine Layer では物語内部ロジックに関するエラーを扱う。

主な Engine Error:

- Temporal Error  
  時系列矛盾、未来イベント参照、時間逆行
- Causal Error  
  原因なし結果、因果ループ、イベント順序矛盾
- State Error  
  キャラクター状態遷移不正、状態不整合
- Emotional Error  
  感情曲線の急激な断絶、不自然な感情変化

これらは各 Engine が検出し、Analysis Engine に報告する。

---

#### 2.3 Intelligence Layer Error

Intelligence Layer では物語全体の整合性を扱う。

主な Intelligence Error:

- Integrity Error  
  物語全体の整合性崩壊
- Consistency Error  
  複数 Thread 間の矛盾
- Narrative Logic Error  
  物語構造破綻
- Simulation Divergence  
  状態シミュレーション破綻

Integrity Error は最も重要なエラー種別であり、Analysis Engine が最終判定を行う。

---

### 2.4 Presentation Layer Error

Presentation Layer では文章生成に関するエラーを扱う。

主な Presentation Error:

- Narrative Generation Error  
  文章生成失敗
- Style Error  
  文体不整合
- Missing Narrative Segment  
  必要なシーンの文章欠落

Presentation Layer Error は Narrative Engine が報告する。

---

## 3. Engine Error Responsibility Matrix

各 Engine のエラー検出責任は以下の通り。

Query Engine
- Reference Error
- Schema Error
- Data Access Error

Story Engine
- Structure Error
- Thread Inconsistency
- Arc Structure Error

Timeline Engine
- Temporal Error
- Timeline Conflict
- Time Range Error

Event Engine
- Causal Error
- Event Dependency Error
- Event Ordering Error

Simulation Engine
- State Error
- State Transition Error
- Simulation Divergence

EmotionalCurve Engine
- Emotional Error
- Emotional Curve Discontinuity
- Tension Balance Error

Analysis Engine
- Integrity Error
- Consistency Error
- Cross Engine Conflict
- Validation Failure

Narrative Engine
- Narrative Generation Error
- Style Error
- Missing Narrative Segment

Analysis Engine は全エラーの最終判断と Rollback 指示を行う中央管理エンジンである。

---

## 4. Validation & Detection Flow

Error Detection は Execution Pipeline の各フェーズに配置された Validation Gate によって行われる。

Validation Flow の基本構造:

1. Engine Execution
2. Engine Self Validation
3. Execution Log 出力
4. Analysis Engine にログ送信
5. Analysis Engine Cross Validation
6. Integrity Score 計算
7. Gate 判定
8. Pass または Rollback

Narrative Engine 実行前には必ず Integrity Check Gate を通過しなければならない。

Integrity Score が閾値を下回る場合、Narrative Engine は実行されない。

---

### 🔴【拡張】Severity Monotonicity Rule（最重要追加）

【追加理由】  
Phase 3.4 において以下の重大な設計欠陥が確認された：

- CRITICAL が途中で ERROR にダウングレードされる
- 中間層（Adapter / Auditor）で情報が破壊される
- Validation Pipeline が非可逆構造になっている

---

### ✔ ルール定義

一度発生した Severity は上位層で減衰してはならない。

---

### ✔ 正式仕様

- CRITICAL → ERROR / WARNING / INFO への変換は禁止
- ERROR → WARNING / INFO への変換は禁止
- WARNING → INFO への変換は禁止

---

### ✔ 許可される変換

- INFO → WARNING → ERROR → CRITICAL（昇格のみ許可）

---

### ✔ 違反例（旧実装）

以下は**仕様違反として禁止**：

- is_valid を基準に再評価して ERROR 固定化
- 複数 ValidationResult を集約し最小Severityに丸める
- dict変換時に文字列処理で誤変換

---

### ✔ 修正方針（Phase 3.4）

- ❌ 集約ロジック削除（ただし履歴としてコメント保持）
- ❌ is_validベース判定削除（理由：情報ロスを引き起こすため）
- ❌ ERROR固定ロジック削除（理由：Severityの意味を破壊するため）
- ✅ ValidationResult を完全保持（Pass-through）
- ✅ 最大Severity選択（必要時のみ）

---

### ✔ 旧仕様との関係

従来仕様では「集約」や「簡略化」が明示的に禁止されていなかったため、実装側で最適化として導入されていた。  
しかしこの設計は Validation Pipeline における情報破壊を引き起こし、結果として CRITICAL 消失問題を発生させた。

そのため本仕様では：

- 集約処理は**非推奨 → 禁止**
- ValidationResult は**不変データとして扱う**

へと方針を明確化した。

---

### ✔ コメント（最重要）

このルールは Validation Pipeline を「情報非破壊構造」に変換するための中核仕様である。

---

## 5. Rollback & Recalculation Logic

Error が検出された場合、Execution は Rollback され、再演算が行われる。

Rollback 単位は以下の 2 種類が存在する。

1. Engine Tier Rollback  
   エラーを発生させた Engine Tier まで戻る。
2. Phase Rollback  
   Execution Pipeline のフェーズ単位で戻る。

Rollback 対応表:

Temporal Error → Timeline Engine まで Rollback  
Causal Error → Event Engine まで Rollback  
State Error → Simulation Engine まで Rollback  
Emotional Error → EmotionalCurve Engine まで Rollback  
Integrity Error → Story Engine または Timeline Engine まで Rollback  

Recalculation には最大試行回数を設定する。

recalculation_max_attempts を超えた場合、Execution Abort 状態に遷移する。

---

### 🔴【補足追加】SeverityとRollbackの関係

【追加理由】  
従来仕様では Severity と Rollback の関係が暗黙的であり、実装依存になっていたため明文化する。

---

### ✔ 追加仕様

- CRITICAL → 即時 Rollback + Execution 停止（Engine判断）
- ERROR → Rollback対象（ただし Execution継続可能）
- WARNING → Rollbackなし（監視対象）
- INFO → 影響なし

---

### ✔ 修正前の問題点

- ERROR と CRITICAL の扱いが曖昧
- Engineごとに判断が分散
- blocking判定が統一されていなかった

---

### ✔ 修正後

- blocking判定は ValidationResult.is_blocking() に統一
- Engine が最終判断を行う
- 判定ロジックの重複を排除

---

## 6. Error Codes & Status Definition

NWF では標準 Error Code 体系を定義する。

Error Code カテゴリ:

DATA_ERROR  
ENGINE_ERROR  
TEMPORAL_ERROR  
CAUSAL_ERROR  
STATE_ERROR  
EMOTIONAL_ERROR  
INTEGRITY_ERROR  
NARRATIVE_ERROR  
EXECUTION_ABORT  
SYSTEM_ERROR  

Execution Status は以下の状態を持つ。

- healthy
- warning
- recovering
- fatal
- aborted
- completed

各データオブジェクトおよび ExecutionLog は以下のフィールドを持つ。

- status
- integrity_score
- validation_result
- error_code
- error_message
- retry_count
- rollback_flag

---

### 🔴【補足】Execution Status と Severity の対応

| Severity | Status |
|----------|--------|
| INFO | healthy |
| WARNING | warning |
| ERROR | recovering |
| CRITICAL | fatal |

（※本対応は実装依存であったものを仕様として明文化した）

---

## 7. Logging & Persistence

すべての Engine は Execution Log を出力しなければならない。

Execution Log に記録される情報:

- engine_name
- execution_phase
- input_data_id
- output_data_id
- validation_result
- integrity_score
- error_code
- error_message
- timestamp
- retry_count
- rollback_flag

Execution Log は Data Layer に永続化され、Analysis Engine が参照する。

Query Engine を介してすべてのログにアクセス可能とする。

Logging System は以下の目的で使用される。

- Error Detection
- Rollback 判断
- Execution Monitoring
- Performance Analysis
- Debug
- Story Integrity Audit

---

### 🔴【拡張】Severity Trace Logging

【追加理由】  
Phase 3.4 デバッグにおいて「どこでCRITICALが消えたか」が追跡不能であったため。

---

### ✔ 追加仕様

すべての Validation Pipeline 層で以下をログ出力する：

- Validator直後
- Adapter後
- Auditor後
- Engine直前

ログ形式：

- severity list
- transaction_id
- stardate

---

### ✔ 例（旧実装との差分明示）

従来：ログ出力なし（追跡不能）

追加後：

print([r.severity for r in results])

---

### ✔ 目的

- CRITICAL消失箇所の特定
- Pipelineの透明性確保
- Debug容易性向上
- 監査可能性の強化

---

## 8. Maintenance & Versioning

本 Error Model は以下の仕様と完全同期する必要がある。

Core_Spec v2.0.1  
System_Architecture v2.0.1  
Architecture_Spec v2.0.1  
Data_Spec v2.0.1  
Engine_Spec v2.0.1  
Execution_Pipeline v2.0.1  
Engine_Order v2.0.1  

Engine 追加、Execution Pipeline 変更、Data Model 変更、Analysis Logic 変更が発生した場合、本ドキュメントを更新する。

Error Model は Story OS の信頼性と整合性を保証する中核仕様である。

---

## 9. まとめ

NWF Error Model v2.0.1 は以下を定義する。

- エラーの再定義（Failure ではなく Recalculation Trigger）
- レイヤー別 Error 分類
- Engine Error Responsibility
- Validation Gate と Detection Flow
- Rollback と Recalculation ロジック
- Error Code と Status モデル
- Logging と永続化
- Execution Abort 条件
- 自己修復型 Execution モデル

---

### 🔴【最終追加まとめ】

Phase 3.4 により以下が追加・明文化された：

- Severity Monotonicity Rule（最重要）
- Validation Pipeline 非破壊設計（Pass-through原則）
- Rollback と Severity の明確な関係
- Severity Trace Logging
- blocking判定の単一責務化

---

### ✔ 最終状態

- CRITICAL は必ず Engine まで伝播する
- RuntimeError が確実に発火する
- Validation Pipeline が情報非破壊構造になる
- デバッグが構造的に可能になる
- 監査ログによる完全追跡が可能になる

---

[EOF]