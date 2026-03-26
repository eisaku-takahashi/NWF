Source: docs/spec/Engine_Spec/NWF_Engine_Spec_Index_v2.0.1.md
Updated: 2026-03-26T18:44:00+09:00
PIC: Engineer / ChatGPT

# NWF Engine Spec Index v2.0.1

---

## 1. 概要

NWF Engine Spec Index は、Story OS（NWF v2.0.1）における Engine 群の階層構造、役割分担、実行パイプライン、データフロー、および Engine 間依存関係を定義するアーキテクチャ・マップである。

本ドキュメントは単なる Engine 仕様ファイルの一覧ではなく、Story OS における「物語生成・シミュレーションを実行する演算機構（Engine System）」全体の構造と動作原理を定義することを目的とする。

Story OS において物語は以下によって生成される。

- Data（状態・構造・関係）
- Engine（演算・更新・生成）
- Pipeline（実行順序）
- Narrative（出力）

Engine Index はこれらのうち Engine と Pipeline を統合的に定義する中核ドキュメントである。

---

## 2. Engine Layer Architecture

NWF v2.0.1 では Engine は以下の 5 層構造で定義される。

### 2.1 Orchestration Layer

最上位統合レイヤー。  
全 Engine の実行を統括し、Story 全体の生成・シミュレーションを管理する。

対象 Engine

- Story Engine

役割

- Engine 実行順序の管理
- Story 生成フローの制御
- Simulation / Analysis の呼び出し
- Narrative 出力の統合

Story Engine は Story OS の統合制御エンジンである。

---

### 2.2 Structural Layer

物語の構造（時間・ストーリーライン）を定義するレイヤー。

対象 Engine

- Thread Engine
- Timeline Engine

役割

- Thread Graph 構築
- Timeline 構築
- Scene 配置制約
- Thread 収束点定義
- 時系列整合性保証

Structural Layer は物語の骨格と時間軸を定義する。

---

### 2.3 Dynamics Layer

物語の状態・関係・対立・イベントなど、動的変化を計算するレイヤー。

対象 Engine

- State Engine
- Character Engine
- Conflict Engine
- Event Engine
- Relationship Engine
- World Engine
- Information Engine

役割

- State 管理
- Character 意思決定
- Conflict 強度計算
- Event 発生
- Relationship 変化
- World 状態管理
- Information 管理

Dynamics Layer は物語世界の状態変化を計算する。

---

### 2.4 Execution & Presentation Layer

Scene、Beat、Narrative など、実際の物語体験として生成・表現するレイヤー。

対象 Engine

- Scene Engine
- Beat Engine
- Narrative Engine
- Dialogue Engine
- Foreshadowing Engine
- EmotionalCurve Engine

役割

- Scene 生成
- Beat 生成
- Narrative 順序制御
- Dialogue 生成
- Foreshadowing 管理
- Emotional Curve 計算

Execution Layer はデータを物語体験へ変換するレイヤーである。

---

### 2.5 Intelligence Layer

分析・検索・シミュレーションなどの知的処理を担当するレイヤー。

対象 Engine

- Simulation Engine
- Analysis Engine
- Query Engine

役割

- What-if シミュレーション
- 物語分析
- データ検索・抽出
- Engine 実行支援

Intelligence Layer は Story OS の分析・推論機構である。

---

## 3. Engine Catalog

本節では各 Engine の役割と担当ドメインを定義する。

### 3.1 Story Engine
最上位統合 Engine。全 Engine の実行を管理する。

### 3.2 Thread Engine
ストーリーライン構造（Thread Graph）を生成する。

### 3.3 Timeline Engine
時間軸と Scene 配置を管理する。

### 3.4 State Engine
物語内の状態（Character / Relationship / World / Information）を管理する。

### 3.5 Scene Engine
Scene 単位で出来事を生成・管理する。

### 3.6 Beat Engine
Scene 内の最小ドラマ単位を生成する。

### 3.7 Character Engine
キャラクターの意思決定と行動生成を行う。

### 3.8 Conflict Engine
対立構造を生成し State 変化を駆動する。

### 3.9 Event Engine
物語イベントを生成し State 遷移を発生させる。

### 3.10 Foreshadowing Engine
伏線の設定と回収整合性を管理する。

### 3.11 EmotionalCurve Engine
State 変化を感情として数値化する。

### 3.12 Narrative Engine
語り順序と情報開示を制御する。

### 3.13 Dialogue Engine
キャラクター対話を生成する。

### 3.14 World Engine
世界設定および世界状態を管理する。

### 3.15 Information Engine
情報・秘密・認識状態を管理する。

### 3.16 Relationship Engine
キャラクター間関係状態を管理する。

### 3.17 Simulation Engine
物語シミュレーションを実行する。

### 3.18 Analysis Engine
物語構造・感情・テンポ等を分析する。

### 3.19 Query Engine
NWF データの検索・抽出を行う。

---

## 4. Operational Pipeline（Execution Workflow）

NWF v2.0.1 における標準実行パイプラインは以下。

Query  
→ Story  
→ Structural Layer  
→ Dynamics Layer  
→ Execution Layer  
→ Narrative Output  

詳細フロー

1. Query Engine が要求を受信
2. Story Engine が実行フローを生成
3. Thread Engine が Thread Graph を生成
4. Timeline Engine が Timeline を構築
5. State Engine が初期 State を生成
6. Character / Conflict / Event Engine が Dynamics を計算
7. Scene Engine が Scene を生成
8. Beat Engine が Beat を生成
9. EmotionalCurve Engine が感情曲線を生成
10. Foreshadowing Engine が伏線整合性を確認
11. Narrative Engine が語り順序を構築
12. Dialogue Engine が対話を生成
13. Story Engine が最終 Narrative を出力
14. Analysis / Simulation Engine が評価・再計算を行う

---

## 5. Inter-Engine Dependencies

Engine 依存関係は基本的に上位レイヤーから下位レイヤーへ向かう。

依存方向

Story  
→ Structural  
→ Dynamics  
→ Execution  
→ Narrative  

ただし Intelligence Layer は全 Engine に介入可能。

### 5.1 因果伝搬ルール（Causality Propagation）

例

Conflict Engine が State を更新  
→ State Engine が状態変更  
→ EmotionalCurve Engine が感情更新  
→ Beat Engine が Beat 変化  
→ Scene Engine が Scene 変化  
→ Narrative Engine が語り変化  

このように State 変化は Engine 間を伝搬する。

State は全 Engine の共通データ基盤である。

---

## 6. Engine Registry & Versioning

Engine Spec v2.0.1 対応状況を管理する。

Engine 一覧

- Story Engine
- Thread Engine
- Timeline Engine
- State Engine
- Scene Engine
- Beat Engine
- Character Engine
- Conflict Engine
- Event Engine
- Foreshadowing Engine
- EmotionalCurve Engine
- Narrative Engine
- Dialogue Engine
- World Engine
- Information Engine
- Relationship Engine
- Simulation Engine
- Analysis Engine
- Query Engine

Engine Registry は Data Spec の Engine Registry Table と連携する。

---

## 7. まとめ

NWF Engine System は Story OS において以下の役割を持つ。

- Structural Layer が物語構造を定義
- Dynamics Layer が状態変化を計算
- Execution Layer が物語体験を生成
- Intelligence Layer が分析・シミュレーションを実行
- Story Engine が全 Engine を統合制御

つまり NWF において Engine とは

「データを物語体験へ変換する演算機構」

である。

Engine Layer Architecture と Execution Pipeline によって、
Story OS は一貫した因果構造を持つ物語生成システムとして動作する。

本ドキュメントは Engine 全体構造の基準仕様であり、
すべての Engine Spec は本 Index に従う。

---

[EOF]