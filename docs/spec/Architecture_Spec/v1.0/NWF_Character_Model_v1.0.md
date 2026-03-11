# NWF Character Model v1.0

## 概要

NWF（Novel Writing Framework）における Character Model は、物語に登場するキャラクターを構造化して管理するためのモデルである。

物語においてキャラクターは、行動・感情・関係性を通じてストーリーを進行させる中心的な存在である。Character Model はキャラクターの属性、背景、役割、関係性を整理し、物語全体の構造の中で一貫した人物像を維持することを目的とする。

このモデルは以下を実現する。

キャラクター情報の体系化  
キャラクター関係の管理  
物語内での役割の明確化  
AIによるキャラクター理解の支援  


## Character Model の役割

Character Model は NWF において以下の役割を持つ。

登場人物の情報管理  
キャラクター関係の整理  
ストーリーにおける役割の定義  
キャラクター行動の整合性維持  


## Character Model の基本構造

Character Model は以下の主要要素で構成される。

Character  
CharacterRole  
CharacterTrait  
CharacterBackground  
CharacterRelationship  


## Character

Character は物語に登場する人物または知的存在を表す。

Character は以下の基本情報を持つ。

キャラクターID  
名前  
概要  
所属  
年齢  
性別  
種族  
職業  


## CharacterRole

CharacterRole はキャラクターが物語内で担う役割を定義する。

例

主人公  
対立者  
助言者  
仲間  
敵対者  

一人のキャラクターが複数の役割を持つこともある。


## CharacterTrait

CharacterTrait はキャラクターの性格や能力などの特徴を定義する。

例

性格  
価値観  
能力  
弱点  
信念  

これらの情報はキャラクター行動の判断材料となる。


## CharacterBackground

CharacterBackground はキャラクターの過去や背景を定義する。

例

出生  
育成環境  
過去の出来事  
人生の転機  
動機  

背景はキャラクターの行動原理に大きく影響する。


## CharacterRelationship

CharacterRelationship はキャラクター同士の関係を定義する。

例

家族関係  
友人関係  
師弟関係  
敵対関係  
恋愛関係  

この関係性は物語のドラマを生み出す重要な要素となる。


## Character と World の関係

キャラクターは World Model によって定義される世界の中で存在する。

World Model は以下の要素に影響を与える。

キャラクターの能力  
社会的立場  
文化的価値観  
行動可能範囲  


## Character と Story の関係

キャラクターは物語の進行において中心的な役割を持つ。

Character Model は以下の要素に影響する。

Thread の進行  
Scene の展開  
Beat における行動  


## Character と Emotional Curve

キャラクターは物語の感情的変化を体験する主体である。

Character Model は Emotional Curve と連携し、キャラクターの感情変化を追跡する。


## AI連携

Character Model は AI による物語生成および分析に利用される。

AIは以下の用途で Character Model を使用できる。

キャラクター行動の生成  
対話生成  
人物関係の分析  
キャラクター成長の追跡  


## Character Model の設計思想

NWF Character Model は以下の思想に基づいて設計されている。

キャラクター情報の構造化  
人物関係の明確化  
物語との強い連携  
AI理解可能な人物モデル  


## まとめ

Character Model は NWF におけるキャラクター管理の基盤となるモデルである。

このモデルにより登場人物の情報を体系的に管理し、物語構造と連携させることで、より一貫性のあるストーリー設計を実現する。