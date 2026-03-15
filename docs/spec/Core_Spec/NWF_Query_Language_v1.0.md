# NWF Query Language v1.0

## 概要

NWF Query Language（NQL）は、NWF（Novel Writing Framework）の物語データを検索・抽出・分析するためのクエリ言語である。

NQLは以下の目的で設計されている。

- 物語データの高速検索
- Thread / Scene / Beat の関係解析
- キャラクター出現分析
- 伏線管理
- AIによる物語分析の支援

NQLはSQLの思想を参考にしつつ、物語構造に最適化されたクエリ構文を採用する。


## 対象データモデル

NQLは以下のNWFデータモデルに対して使用される。

- Character
- WorldRule
- Thread
- Scene
- Beat


## 基本クエリ構造

NQLの基本構文は以下の構造を持つ。

SELECT  
FROM  
WHERE  

SELECT は取得する対象を指定する。

FROM は検索対象のモデルを指定する。

WHERE は条件を指定する。


## 基本例

Sceneをすべて取得する例。

SELECT Scene  
FROM Scene


特定キャラクターが登場するSceneを検索する例。

SELECT Scene  
FROM Scene  
WHERE characters CONTAINS "Alice"


## Thread検索

特定のテーマを持つThreadを検索する。

SELECT Thread  
FROM Thread  
WHERE theme = "memory"


特定キャラクターに関連するThreadを取得する。

SELECT Thread  
FROM Thread  
WHERE characters CONTAINS "Alice"


## Scene検索

特定Threadに属するSceneを取得する。

SELECT Scene  
FROM Scene  
WHERE thread_id = "T001"


感情強度が一定以上のSceneを検索する。

SELECT Scene  
FROM Scene  
WHERE emotion_intensity > 0.7


## Beat検索

特定SceneのBeatを取得する。

SELECT Beat  
FROM Beat  
WHERE scene_id = "S001"


特定キャラクターが関与するBeatを検索する。

SELECT Beat  
FROM Beat  
WHERE characters CONTAINS "Alice"


## 伏線検索

伏線（Foreshadowing）を検索する。

SELECT Beat  
FROM Beat  
WHERE type = "foreshadow"


伏線の回収を検索する。

SELECT Beat  
FROM Beat  
WHERE type = "payoff"


伏線と回収のペアを解析する。

SELECT Beat  
FROM Beat  
WHERE foreshadow_id = "F001"


## キャラクター分析

キャラクターの出現Sceneを取得する。

SELECT Scene  
FROM Scene  
WHERE characters CONTAINS "Alice"


キャラクターの出現Beatを取得する。

SELECT Beat  
FROM Beat  
WHERE characters CONTAINS "Alice"


## 感情カーブ分析

感情強度の高いSceneを取得する。

SELECT Scene  
FROM Scene  
WHERE emotion_intensity > 0.8


物語のクライマックス候補を検索する。

SELECT Scene  
FROM Scene  
WHERE emotion_intensity > 0.9


## AI連携

NQLはAI解析のためのインターフェースとしても使用される。

AIは以下の用途でNQLを利用できる。

- 伏線検出
- キャラクター分析
- ストーリー構造解析
- プロット最適化


## 拡張性

NQLは以下の拡張を想定している。

- Graph検索
- 感情曲線解析
- 時系列解析
- AI補助クエリ


## 設計思想

NWF Query Language の設計思想は以下である。

- 物語構造に特化した検索言語
- AI解析と人間の理解の両立
- シンプルな構文
- 高い拡張性

NQLはNWFの物語データを効率的に探索・分析するための標準クエリ言語として使用される。