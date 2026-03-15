# NWF Narrative Rendering v1.0

## 概要

NWF（Novel Writing Framework）における Narrative Rendering は、構造化された物語データを人間が読める物語テキストへ変換するプロセスを定義する。

NWFでは Thread・Scene・Beat などの構造データを保持するが、そのままでは小説として読むことはできない。そのため Rendering Engine によって Narrative（叙述）へ変換する必要がある。

Narrative Rendering の目的は以下である。

- 構造データから物語テキストを生成する  
- 物語の順序を統一する  
- AIによる文章生成を補助する  
- 人間の執筆作業を支援する  


## Narrative Rendering の位置

NWF Execution Flow において Narrative Rendering は最終段階に位置する。

処理の流れは以下の順序で行われる。

Project Initialization  
Data Loading  
Data Validation  
Structure Construction  
Graph Generation  
Query Execution  
Analysis Processing  
Narrative Rendering  


## Rendering の基本単位

Narrative Rendering は以下の階層構造をもとに行われる。

Thread  
Scene  
Beat  

この階層に従って物語が構築される。


## Thread Rendering

Thread は物語の大きな流れを表す。

Thread Rendering の役割は以下である。

- 物語の主要テーマを保持する  
- Scene の順序を管理する  
- 物語の進行ラインを維持する  

Thread は複数の Scene を含む。


## Scene Rendering

Scene は物語の一つの場面を表す。

Scene Rendering の役割は以下である。

- 場面の状況を提示する  
- キャラクターの行動を表現する  
- 物語の進行を担う  

Scene は複数の Beat によって構成される。


## Beat Rendering

Beat は物語の最小単位の出来事を表す。

Beat Rendering の役割は以下である。

- 行動  
- 発言  
- 感情変化  
- 小さな出来事  

Beat を組み合わせることで Scene が形成される。


## Narrative Rendering の処理段階

Narrative Rendering は以下の処理段階で行われる。

1 構造取得  
Thread / Scene / Beat 構造を取得する。

2 順序決定  
物語の時系列または演出順序を決定する。

3 Narrative 構築  
Scene と Beat を連結し Narrative を構築する。

4 テキスト生成  
AI またはテンプレートを利用して文章を生成する。

5 出力整形  
小説として読める形式に整形する。


## Rendering モード

NWFでは複数の Rendering モードを想定している。

Draft Rendering  
物語構造をそのままテキスト化する。

AI Assisted Rendering  
AIが文章生成を補助する。

Human Writing Mode  
人間の作家が執筆するための下書きを生成する。


## Narrative テンプレート

Rendering Engine は Narrative テンプレートを利用できる。

テンプレートは以下の情報を含む。

- Scene description  
- Character action  
- Dialogue  
- Emotional state  

これにより物語テキストを安定して生成できる。


## AI連携

Narrative Rendering は AI と密接に連携する。

AIは以下の処理を行うことができる。

- Scene description 生成  
- Dialogue 生成  
- キャラクター感情表現生成  
- 文体調整  

これにより物語生成を支援する。


## 出力形式

Narrative Rendering の出力形式は以下を想定する。

- Markdown  
- Plain Text  
- Novel Manuscript Format  


## 設計思想

NWF Narrative Rendering の設計思想は以下である。

- 構造と文章の分離  
- AIと人間の協働執筆  
- 再利用可能な物語構造  
- 柔軟な文章生成

Narrative Rendering は NWF において、構造化された物語を実際の小説として表現するための最終プロセスとして機能する。