Source: docs/spec/Core_Spec/NWF_Execution_Flow_v2.0.1.md
Updated: 2026-03-22T18:18:00+09:00
PIC: Engineer / ChatGPT

# NWF Execution Flow v2.0.1

---

## 1. 概要

Execution Flow は NWF（Novel Writing Framework）における標準的な処理パイプラインを定義する。
本ドキュメントでは Core Spec v2.0.1 の全モデルを統合し、データロードから物語論理検証、AI生成、フィードバックまでを一貫して制御する実行アーキテクチャを定義する。

Execution Flow は NWF における「物語エンジンの実行カーネル」として機能する。

Execution Flow の目的は以下である。

物語データの読み込み  
データ整合性検証  
エンティティ構築  
関係構築  
時間同期  
因果関係確定  
世界ルール適用  
物語論理整合性検証  
物語構造生成  
分析処理  
AI生成  
出力生成  
フィードバック学習  

---

## 2. Execution Lifecycle

Execution Flow v2.0.1 では以下のライフサイクルを定義する。

Initialization  
Ingestion  
Synthesis  
Validation  
Generation  
Feedback  

各フェーズの役割は以下の通り。

Initialization  
システム初期化と設定読み込み

Ingestion  
物語データの読み込みと検証

Synthesis  
物語構造・関係・時間・因果の統合

Validation  
物語論理の整合性検証

Generation  
分析・生成・出力処理

Feedback  
AIおよび人間による修正・最適化フィードバック

---

## 3. Execution Flow 全体パイプライン

Execution Flow v2.0.1 の標準パイプラインは以下の順序で実行される。

1 Project Initialization  
2 Data Loading  
3 Data Validation  
4 Entity Construction  
5 Relationship Construction  
6 Timeline Alignment  
7 Causality Resolution  
8 World Rule Application  
9 Story Logic Validation  
10 Graph Generation  
11 Query Execution  
12 Analysis Processing  
13 AI Generation  
14 Output Generation  
15 Feedback Loop  

---

## 4. Project Initialization

プロジェクト環境の初期化を行う。

主な処理

プロジェクトディレクトリ確認  
設定ファイル読み込み  
Spec バージョン確認  
実行環境初期化  
AI Engine 初期化  

---

## 5. Data Loading (Ingestion Phase)

物語データをロードする。

対象データ

character  
world_rule  
thread  
scene  
beat  
event  
timeline  
conflict  
relationship  

対応フォーマット

json  
yaml  
markdown  

読み込まれたデータは内部データモデルへ変換される。

---

## 6. Data Validation

データの形式および参照整合性を検証する。

主な検証項目

entity_id 重複チェック  
参照整合性チェック  
必須フィールド検証  
データ型検証  
Spec バージョン整合性  

---

## 7. Entity Construction

ロードされたデータから内部エンティティを構築する。

対象エンティティ

character  
thread  
scene  
beat  
event  
timeline  
conflict  
relationship  
world_rule  

この段階で物語データは内部オブジェクトとして管理される。

---

## 8. Relationship Construction

エンティティ間の関係を構築する。

主な関係

character_to_character  
thread_to_scene  
scene_to_beat  
event_to_scene  
thread_to_conflict  
character_to_conflict  
event_to_timeline  

Relationship Model v2.0.1 はこの段階で統合される。

---

## 9. Logic Processing Layer

Execution Flow v2.0.1 では Logic Processing Layer を新設する。
このレイヤは物語論理を確定させる最重要フェーズである。

Logic Processing Layer は以下のフェーズで構成される。

Timeline Alignment  
Causality Resolution  
World Rule Application  

---

## 10. Timeline Alignment

Timeline Model v2.0.1 を使用し、
Thread / Scene / Event を時間軸上で同期する。

処理内容

story_time 同期  
narrative_time 順序確定  
timeline_layer 管理  
sync_point 同期  
並行 Timeline 管理  
分岐 Timeline 管理  

Timeline Model v2.0.1 はこの段階で統合される。

---

## 11. Causality Resolution

Event Model を使用し、
イベント間の因果関係を確定する。

処理内容

cause_event_id 解決  
effect_event_id 解決  
因果関係グラフ生成  
因果矛盾検出  
因果順序確定  

この段階で Causality Graph が生成される。

---

## 12. World Rule Application

World Rule Model を適用し、
物語世界のルールをイベントと状態に反映する。

例

魔法ルール  
物理法則  
社会制度  
キャラクター能力制約  
時間移動ルール  

World Rule はイベント結果や状態遷移に影響を与える。

---

## 13. Story Logic Validation

物語としての論理整合性を検証する。

検証内容

時間矛盾  
因果矛盾  
キャラクター存在矛盾  
世界ルール違反  
同時存在矛盾  
死亡後登場矛盾  
関係性矛盾  

このフェーズは Data Validation とは異なり、
物語論理レベルの整合性を検証する。

---

## 14. Graph Generation

物語構造をグラフとして生成する。

生成されるグラフ

thread_graph  
scene_graph  
character_graph  
timeline_graph  
relationship_graph  
conflict_graph  
causality_graph  
story_graph  

Story Graph は NWF の統合物語構造グラフである。

---

## 15. Query Execution

NWF Query Language による検索・抽出処理を行う。

用途

イベント検索  
キャラクター分析  
伏線検索  
タイムライン検索  
関係性検索  

---

## 16. Analysis Processing

物語構造の分析処理を行う。

主な分析

キャラクター出現分析  
Thread 進行分析  
Timeline 分析  
Conflict 分析  
伏線検出  
構造バランス分析  
感情曲線分析  

分析結果はレポートまたはデータとして出力される。

---

## 17. AI Generation

AI Engine による生成・最適化処理を行う。

AI の役割

プロット生成  
イベント生成  
キャラクター関係生成  
伏線生成  
構造最適化  
物語矛盾修正提案  
物語シミュレーション  

AI Engine は各フェーズに介入可能とする。

AI 介入ポイント

Data Loading  
Relationship Construction  
Timeline Alignment  
Story Logic Validation  
Analysis  
Generation  

---

## 18. Output Generation

処理結果を出力する。

出力形式

json  
markdown  
analysis_report  
visualization_data  
story_graph_data  

出力データは可視化ツールや AI システムで利用される。

---

## 19. Feedback Loop

AI および人間によるフィードバックループを定義する。

フィードバック対象

キャラクター設定  
関係性  
Timeline  
イベント構造  
物語構造  
プロット  
世界設定  

フィードバック結果はデータに反映され、
Execution Flow は再実行される。

このループにより物語は反復的に改善される。

---

## 20. Core Spec 統合タイミング

各 Spec が Execution Flow のどの段階で統合されるかを示す。

Data Model → Data Loading  
Entity ID System → Data Validation  
Relationship Model → Relationship Construction  
Timeline Model → Timeline Alignment  
Event Model → Causality Resolution  
World Rule Model → World Rule Application  
Conflict Model → Graph Generation / Analysis  
Query Language → Query Execution  
Analysis Spec → Analysis Processing  

---

## 21. Execution Flow テキストフロー図

Execution Flow v2.0.1 の全体フローを示す。

Initialization
↓
Data Loading
↓
Data Validation
↓
Entity Construction
↓
Relationship Construction
↓
Timeline Alignment
↓
Causality Resolution
↓
World Rule Application
↓
Story Logic Validation
↓
Graph Generation
↓
Query Execution
↓
Analysis Processing
↓
AI Generation
↓
Output Generation
↓
Feedback Loop
↓
Re-Execution

---

## 22. まとめ

Execution Flow v2.0.1 は NWF Core Spec v2.0.1 全体を統合する
物語エンジンの実行パイプラインである。

Execution Flow は以下の役割を持つ。

データ読み込み  
データ検証  
エンティティ構築  
関係構築  
時間同期  
因果関係確定  
世界ルール適用  
物語論理検証  
グラフ生成  
分析処理  
AI生成  
出力生成  
フィードバックループ  

Execution Flow は NWF における
物語宇宙を動作させる OS カーネルとして機能する。

---

[EOF]