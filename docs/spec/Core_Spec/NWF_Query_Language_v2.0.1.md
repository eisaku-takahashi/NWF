Source: docs/spec/Core_Spec/NWF_Query_Language_v2.0.1.md
Updated: 2026-03-22T20:36:00+09:00
PIC: Engineer / ChatGPT

# NWF Query Language v2.0.1

---

## 1. 概要

NWF Query Language（NQL）v2.0.1 は、NWF（Novel Writing Framework）の物語データを高精度に検索・抽出・分析するための拡張標準クエリ言語である。

v2.0.1 では Core Spec v2.0.1 の全18要素、特に Timeline, Relationship, Conflict, Execution Flow と同期し、物語の深層構造解析を可能とする。

主な目的は以下の通りである。

- STORY_TIME と NARRATIVE_TIME に基づく高度な時間軸フィルタリング
- キャラクター間、Thread間、Scene間の関係解析
- Event間の因果関係および状態遷移の追跡
- Emotional Intensity や Conflict Progress の集計・分析
- AIによる物語矛盾検出や未回収伏線の特定

NQL v2.0.1 は SQL 的直感性を維持しつつ、物語構造に特化した柔軟性と拡張性を提供する。

---

## 2. 対象データモデル

NQL v2.0.1 は以下の NWF データモデルを対象とする。

- Character
- WorldRule
- Thread
- Scene
- Beat
- Event
- Timeline
- Conflict
- Relationship

各モデルは v2.0.1 に基づく最新仕様を反映しており、深層物語解析に対応している。

---

## 3. 基本クエリ構造

NQL v2.0.1 の基本構文は以下を含む。

- SELECT：取得対象の指定
- FROM：検索対象のデータモデル指定
- WHERE：フィルタ条件指定
- MATCH / PATH：関係グラフ探索
- AGGREGATE：集計関数適用
- VALIDATE / UNRESOLVED：AIによる矛盾検証

構文例：

SELECT Scene  
FROM Scene  
WHERE STORY_TIME >= "T001" AND NARRATIVE_TIME <= "N010"  
MATCH Relationship WHERE weight > 0.5  
AGGREGATE AVG(emotion_intensity)  
VALIDATE UNRESOLVED foreshadow

---

## 4. Temporal & Dual-Axis Query

- STORY_TIME：物語内の実際時系列に基づく検索
- NARRATIVE_TIME：叙述順に基づく検索（回想、伏線、演出順序を反映）
- 両者を組み合わせることで、複雑な時制操作や伏線解析が可能

例：

SELECT Beat  
FROM Beat  
WHERE STORY_TIME > "2026-01-01" AND NARRATIVE_TIME < "N020"

---

## 5. Graph Traversal Operators

- Relationship Model v2.0.1 に基づき、有向グラフの探索を可能とする
- MATCH 句：指定条件のノード・エッジを検索
- PATH 句：ノード間の最短経路や関係連鎖を検索
- Weight によるフィルタリングで関係強度の解析が可能

例：

MATCH Relationship FROM Character WHERE weight >= 0.7 PATH TO Character

---

## 6. Causality & Transition Tracking

- Event 間の cause/effect を追跡
- State の変化（Transition）を記録
- 因果解析により、物語の論理整合性確認や伏線影響の分析が可能

例：

SELECT Event  
FROM Event  
WHERE cause = "E001" AND state_transition = "injury->recovery"

---

## 7. Aggregation & Analytics

- Emotional Intensity, Conflict Progress などの数値属性に対して集計が可能
- 使用可能な関数：AVG, SUM, PEAK, MIN, MAX 等

例：

SELECT AVG(emotion_intensity) AS avg_emotion  
FROM Scene  
WHERE thread_id = "T001"

---

## 8. AI Validation Syntax

- VALIDATE 句：物語の矛盾検出
- UNRESOLVED キーワード：回収されていない伏線の特定
- AIによる解析と人間による設計の補助を両立

例：

VALIDATE Scene UNRESOLVED foreshadow_id = "F001"

---

## 9. クエリ実行例

1. 特定キャラクターが登場する未回収伏線 Beat の検索

SELECT Beat  
FROM Beat  
WHERE characters CONTAINS "Alice"  
AND UNRESOLVED = true

2. Thread 内の Scene 間関係の最短経路探索

MATCH Relationship FROM Scene WHERE thread_id = "T002" PATH TO Scene

3. Emotional Intensity の平均値集計

SELECT AVG(emotion_intensity)  
FROM Scene  
WHERE thread_id = "T003"

---

## 10. 設計思想

- 時間軸と叙述軸を区別した高度な物語解析
- 関係グラフ探索による深層構造理解
- 因果・状態遷移の追跡による論理整合性確認
- AIによる矛盾検出と未回収伏線の特定を統合
- シンプルで拡張性の高いクエリ構文を維持

---

## 11. まとめ

NQL v2.0.1 は、NWF Core Spec v2.0.1 と完全に同期した高度な物語探索言語である。

- Temporal & Dual-Axis Query により時系列と叙述順を両立
- Graph Traversal により関係構造を解析
- Causality & Transition Tracking により論理整合性を確認
- Aggregation & Analytics により感情・葛藤を数値化
- AI Validation により伏線と矛盾を把握

これにより、NWF の物語データ解析、AI補助設計、深層構造理解が可能となる標準クエリ言語として機能する。

---

[EOF]