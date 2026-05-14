Source: docs/spec/Execution_Spec/NWF_Engine_Order_v2.0.1.md
Updated: 2026-03-27T22:38:00+09:00
PIC: Engineer / ChatGPT

# NWF Engine Order v2.0.1

---

## 1. Overview

Engine Order は、NWF v2.0.1（Story OS）における全エンジンの実行順序を単純な直列順序として定義するものではなく、エンジン間の入出力依存関係に基づく「Dependency-Driven Execution Model（依存関係駆動実行モデル）」として定義される。

Story OS において物語生成は、複数のエンジンが相互に依存しながら状態を更新していくプロセスであり、各エンジンは必要な入力データが確定した時点で実行される。

本仕様の目的は以下である。

- エンジン間の論理依存関係の明確化
- 実行優先順位（Execution Priority）の定義
- Execution Pipeline との整合性確保
- フィードバックおよびロールバック処理の定義
- 将来のエンジン追加時の統合ルール策定

Engine Order は Story OS の実行規律を司る中核仕様である。

---

## 2. Engine Inventory & Layering

NWF v2.0.1 における正式エンジンとレイヤー配置は以下の通りとする。

### 2.1 Interface Layer
Interface Layer は外部データおよび内部データへのアクセスを管理する。

- Query Engine  
  すべてのエンジンのデータ取得ゲートウェイ。  
  全エンジンは直接データストアにアクセスせず、必ず Query Engine を介して読み取りを行う。

### 2.2 Structural Layer
Structural Layer は物語の構造と時間軸を定義する。

- Story Engine  
  物語構造（Thread、Arc、Structure）を定義する。
- Timeline Engine  
  物語内の時間軸、時系列イベント枠を定義する。

### 2.3 Dynamics Layer
Dynamics Layer は物語内で実際に発生する事象と感情変化を管理する。

- Event Engine  
  イベントの発生、結果、状態変化の確定。
- EmotionalCurve Engine  
  感情曲線、テンション、物語の熱量制御。

### 2.4 Intelligence Layer
Intelligence Layer は状態予測および整合性検証を行う。

- Simulation Engine  
  イベント結果に基づく状態遷移予測。
- Analysis Engine  
  全ログを横断し整合性、矛盾、因果関係の検証を行う。

### 2.5 Presentation Layer
Presentation Layer は文章生成を担当する。

- Narrative Engine  
  構造、イベント、感情、状態をもとに文章生成を行う。

---

## 3. Dependency Graph Model

Engine Order は直列順序ではなく、有向依存関係グラフとして定義される。

基本依存関係フローは以下の通り。

Query Engine
↓
Story Engine / Timeline Engine（並列実行可能）
↓
Event Engine
↓
Simulation Engine
↓
EmotionalCurve Engine
↓
Analysis Engine
↓
Narrative Engine

Analysis Engine からは各エンジンへのフィードバックエッジが存在し、整合性問題が検出された場合は前段階へロールバックして再計算を行う。

### 3.1 Dependency Tier 定義

Engine Dependency Tier を以下のように定義する。

Tier 0  
Query Engine

Tier 1  
Story Engine  
Timeline Engine

Tier 2  
Event Engine

Tier 3  
Simulation Engine

Tier 4  
EmotionalCurve Engine

Tier 5  
Analysis Engine

Tier 6  
Narrative Engine

上位 Tier のエンジンは、下位 Tier の出力が確定するまで実行してはならない。

---

## 4. Lifecycle Phase Mapping

Execution Pipeline の Lifecycle Phase とエンジンの担当領域を以下にマッピングする。

Phase 1: Initialization Phase  
- Query Engine  
- Story Engine  
- Timeline Engine  

Phase 2: Event Generation Phase  
- Event Engine  

Phase 3: Simulation Phase  
- Simulation Engine  

Phase 4: Emotional Adjustment Phase  
- EmotionalCurve Engine  

Phase 5: Analysis & Validation Phase  
- Analysis Engine  

Phase 6: Narrative Generation Phase  
- Narrative Engine  

このフェーズ構造により、Execution Pipeline と Engine Order の整合性を維持する。

---

## 5. Feedback & Rollback Logic

Analysis Engine は全エンジンのログを横断的に検証し、以下の問題を検出する。

- 時系列矛盾
- 因果関係矛盾
- キャラクター状態矛盾
- 感情曲線不整合
- 物語構造破綻

Integrity Score が閾値を下回った場合、以下のロールバックを実行する。

問題種別 → ロールバック先

- Timeline 矛盾 → Timeline Engine
- Event 因果矛盾 → Event Engine
- 状態遷移矛盾 → Simulation Engine
- 感情曲線問題 → EmotionalCurve Engine
- 構造問題 → Story Engine

Analysis Engine は Narrative Engine の実行を許可または停止する最終ゲートとして機能する。

---

## 6. Integration Rules

将来的に Scene Engine、Beat Engine などのサブエンジンを追加する場合、以下のルールに従う。

1. 新エンジンは必ず Dependency Tier を定義すること
2. 入力データの提供元エンジンを明示すること
3. 出力データを利用するエンジンを明示すること
4. Query Engine を介したデータアクセスルールを遵守すること
5. Execution Pipeline の Lifecycle Phase に所属させること
6. Analysis Engine の検証対象ログを定義すること

これにより Engine Ecosystem の整合性を維持する。

---

## 7. Maintenance & Versioning

本ドキュメントは以下の仕様と完全同期する必要がある。

- Core_Spec v2.0.1
- System_Architecture v2.0.1
- Architecture_Spec v2.0.1
- Data_Spec v2.0.1
- Engine_Spec v2.0.1
- Execution_Pipeline v2.0.1

Engine の追加、削除、依存関係変更が発生した場合、本ドキュメントのバージョンを更新し、Execution Pipeline と同時に改訂すること。

Engine Order は Story OS の実行論理回路であり、全エンジン仕様の上位統治ドキュメントとして扱う。

---

## 8. Summary

NWF Engine Order v2.0.1 は以下を定義する。

- エンジンレイヤー構造
- エンジン依存関係グラフ
- Execution Tier
- Lifecycle Phase 対応
- フィードバックおよびロールバック
- 将来エンジン統合ルール

本仕様により、Story OS は依存関係駆動型の自律的物語生成システムとして動作する。

---

[EOF]