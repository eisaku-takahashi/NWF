# NWF Story Database Model v1.0

## 概要

NWF（Novel Writing Framework）における Story Database Model は、物語を構成するすべての要素を体系的に保存・管理するためのデータベース構造を定義するモデルである。

物語はキャラクター、世界設定、ストーリー構造、感情変化、伏線など複数の要素によって構成される。Story Database Model はこれらの要素を統合的に管理し、物語の設計・分析・生成を可能にすることを目的とする。

このモデルは以下を実現する。

物語構成要素の統合管理  
ストーリー構造の体系化  
データとしての物語の保存  
AIによる物語分析の支援  


## Story Database Model の役割

Story Database Model は NWF において以下の役割を持つ。

物語データの集中管理  
各モデル間の関係管理  
物語構造の永続化  
分析および生成のためのデータ基盤提供  


## Story Database の基本構造

Story Database は複数のモデルによって構成される。

Character Model  
World Model  
Thread Model  
Scene Model  
Beat Model  
Emotional Curve Model  
Foreshadowing Model  


## Character データ

Character データは物語に登場するキャラクターの情報を管理する。

主な情報

キャラクターID  
名前  
役割  
性格  
背景  
人物関係  


## World データ

World データは物語世界の設定を管理する。

主な情報

世界名  
物理法則  
社会制度  
文化  
歴史  
地理  


## Thread データ

Thread は物語の主要なストーリーラインを表す。

主な情報

Thread ID  
テーマ  
ストーリー概要  
関連キャラクター  
関連 Scene  


## Scene データ

Scene は物語の場面単位を表す。

主な情報

Scene ID  
所属 Thread  
場所  
登場キャラクター  
シーン概要  
感情強度  


## Beat データ

Beat は Scene を構成する最小単位の出来事を表す。

主な情報

Beat ID  
所属 Scene  
行動  
発言  
感情変化  
イベント  


## Emotional Curve データ

Emotional Curve は物語の感情的な起伏を表す。

主な情報

感情強度  
感情の種類  
キャラクターの感情変化  
物語全体の感情カーブ  


## Foreshadowing データ

Foreshadowing は伏線とその回収を管理する。

主な情報

伏線ID  
伏線の内容  
設置された Scene または Beat  
回収ポイント  
関連 Thread  


## モデル間の関係

Story Database 内では各モデルが相互に関連する。

World は Character の行動環境を定義する。  
Character は Thread と Scene の主体となる。  
Thread は複数の Scene を持つ。  
Scene は複数の Beat によって構成される。  
Beat は物語の出来事を表す。  
Emotional Curve は Scene や Beat に影響する。  
Foreshadowing は Beat や Scene に埋め込まれる。


## データ保存形式

Story Database は以下の形式で保存されることを想定する。

JSON  
YAML  
Markdown  

これらの形式は人間とAIの双方が扱いやすい。


## AI連携

Story Database Model は AI による物語解析および生成を支援する。

AIは以下の用途でデータベースを利用できる。

物語構造の分析  
キャラクター関係の理解  
伏線の検出  
プロット生成  


## Story Database Model の設計思想

NWF Story Database Model は以下の思想に基づいて設計されている。

物語要素の構造化  
モデル間関係の明確化  
AI利用を前提としたデータ設計  
再利用可能なストーリーデータ


## まとめ

Story Database Model は NWF における物語データ管理の中心となるモデルである。

このモデルにより物語の構造をデータとして保存・分析し、AI支援によるストーリー設計や物語生成を可能にする。