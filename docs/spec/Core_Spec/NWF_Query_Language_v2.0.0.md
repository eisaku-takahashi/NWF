Source: docs/spec/Core_Spec/NWF_Query_Language_v2.0.0.md
Updated: 2026-03-17T08:00:00+09:00
PIC: Engineer / ChatGPT

# NWF Query Language v2.0.0

---

## 1. 概要

NWF Query Language（NQL）は、NWF（Novel Writing Framework）の物語データを検索・抽出・分析するための標準クエリ言語である。

NQLは物語構造データに対して柔軟な検索と分析を行うことを目的として設計されている。  
Thread、Scene、Beat などの物語構造要素を対象とし、キャラクター関係、伏線構造、感情カーブなどを効率的に分析できる。

NQLの主な目的は次の通りである。

- 物語データの高速検索
- Thread / Scene / Beat の関係解析
- キャラクター出現分析
- 伏線構造の管理
- AIによる物語分析の支援

NQLは SQL の思想を参考にしつつ、物語構造に最適化されたシンプルな構文を採用している。

---

## 2. 対象データモデル

NQLは以下の NWF データモデルに対して使用される。

- Character
- WorldRule
- Thread
- Scene
- Beat

これらのデータモデルは NWF Core Spec によって定義された物語構造要素である。

---

## 3. 基本クエリ構造

NQLの基本構文は次の3つの要素で構成される。

SELECT  
FROM  
WHERE  

各要素の役割は次の通りである。

SELECT  
取得するデータの種類を指定する。

FROM  
検索対象のデータモデルを指定する。

WHERE  
検索条件を指定する。

この構造は SQL に類似しているが、物語構造データに最適化されている。

---

## 4. 基本クエリ例

すべての Scene を取得する例。

SELECT Scene  
FROM Scene

特定キャラクターが登場する Scene を検索する例。

SELECT Scene  
FROM Scene  
WHERE characters CONTAINS "Alice"

---

## 5. Thread 検索

Thread を対象とした検索例を示す。

特定のテーマを持つ Thread を検索する。

SELECT Thread  
FROM Thread  
WHERE theme = "memory"

特定キャラクターに関連する Thread を取得する。

SELECT Thread  
FROM Thread  
WHERE characters CONTAINS "Alice"

---

## 6. Scene 検索

Scene を対象とした検索例を示す。

特定 Thread に属する Scene を取得する。

SELECT Scene  
FROM Scene  
WHERE thread_id = "T001"

感情強度が一定以上の Scene を検索する。

SELECT Scene  
FROM Scene  
WHERE emotion_intensity > 0.7

---

## 7. Beat 検索

Beat を対象とした検索例を示す。

特定 Scene の Beat を取得する。

SELECT Beat  
FROM Beat  
WHERE scene_id = "S001"

特定キャラクターが関与する Beat を検索する。

SELECT Beat  
FROM Beat  
WHERE characters CONTAINS "Alice"

---

## 8. 伏線検索

NQLでは伏線（Foreshadowing）構造を検索することができる。

伏線を検索する例。

SELECT Beat  
FROM Beat  
WHERE type = "foreshadow"

伏線の回収を検索する例。

SELECT Beat  
FROM Beat  
WHERE type = "payoff"

伏線と回収の関連を検索する例。

SELECT Beat  
FROM Beat  
WHERE foreshadow_id = "F001"

これにより物語内の伏線構造を分析できる。

---

## 9. キャラクター分析

キャラクターに関連する物語構造を分析することができる。

キャラクターが登場する Scene を取得する。

SELECT Scene  
FROM Scene  
WHERE characters CONTAINS "Alice"

キャラクターが関与する Beat を取得する。

SELECT Beat  
FROM Beat  
WHERE characters CONTAINS "Alice"

---

## 10. 感情カーブ分析

NQLは感情強度データを利用した物語分析を行うことができる。

感情強度が高い Scene を取得する。

SELECT Scene  
FROM Scene  
WHERE emotion_intensity > 0.8

物語のクライマックス候補を検索する。

SELECT Scene  
FROM Scene  
WHERE emotion_intensity > 0.9

このような検索により物語の感情構造を解析できる。

---

## 11. AI連携

NQLはAIによる物語解析のインターフェースとして利用することができる。

AIは次の用途で NQL を使用できる。

- 伏線検出
- キャラクター関係分析
- ストーリー構造解析
- プロット最適化
- 感情カーブ分析

NQLは AI による物語理解と分析を支援するための重要な構成要素である。

---

## 12. 拡張性

NQLは将来的な拡張を考慮して設計されている。

想定される拡張例は次の通りである。

- Graph 検索
- 感情曲線解析
- 時系列解析
- AI補助クエリ
- 複雑なストーリー構造分析

この拡張性により、NQLは長期的に発展可能な物語検索言語となる。

---

## 13. 設計思想

NWF Query Language の設計思想は次の通りである。

- 物語構造に特化した検索言語
- AI解析と人間理解の両立
- シンプルで読みやすい構文
- 高い拡張性

NQLは NWF における物語データ探索と分析のための標準クエリ言語として機能する。

---

## 14. まとめ

NWF Query Language（NQL）は、NWFの物語構造データを検索・分析するための標準クエリ言語である。

Thread、Scene、Beat を中心とした物語構造に対して柔軟な検索を行うことができ、AIによる物語解析と人間による物語設計の両方を支援する。

NQLは NWF の分析機能を支える重要な基盤技術である。

---

[EOF]