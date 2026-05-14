Source: docs/spec/Execution_Spec/NWF_Error_Model_v2.0.1.md
Updated: 2026-03-27T23:33:00+09:00
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

### 2.3 Intelligence Layer Error

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

本仕様により Story OS は矛盾を検知し、再計算を繰り返し、論理的整合性を維持したまま物語を完走する自己修復型システムとして動作する。

---

[EOF]