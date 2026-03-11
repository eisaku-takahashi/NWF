# NWF Execution Flow v1.0

## 概要

NWF（Novel Writing Framework）は、物語データを構造的に処理するための実行フローを定義する。

Execution Flow は以下の目的で設計されている。

- 物語データの読み込み
- データ整合性の検証
- Thread / Scene / Beat の構造処理
- 物語構造の分析
- 出力生成

このドキュメントでは NWF の標準実行フローを定義する。


## 実行フロー全体構造

NWFの基本実行フローは以下の段階で構成される。

1. Project Initialization  
2. Data Loading  
3. Data Validation  
4. Structure Construction  
5. Graph Generation  
6. Query Execution  
7. Analysis Processing  
8. Output Generation  


## Project Initialization

最初にNWFプロジェクトの初期化を行う。

主な処理

- プロジェクトディレクトリの確認
- 設定ファイルの読み込み
- データディレクトリの確認
- 実行環境の初期化


## Data Loading

物語データをロードする。

対象データ

- Character
- WorldRule
- Thread
- Scene
- Beat

データは以下の形式で保存される。

- JSON
- YAML
- Markdown

読み込まれたデータは内部データモデルへ変換される。


## Data Validation

読み込まれたデータの整合性を検証する。

主な検証内容

- IDの重複チェック
- 参照整合性チェック
- 必須フィールドの存在確認
- 型チェック


## Structure Construction

物語構造を構築する。

主な処理

- Thread と Scene の関連付け
- Scene と Beat の関連付け
- キャラクター出現情報の整理
- 時系列構造の構築

この段階で物語の基本構造が形成される。


## Graph Generation

物語構造をグラフ構造として生成する。

主なグラフ

- Thread Graph
- Scene Graph
- Character Graph
- Foreshadow Graph

グラフ構造は物語分析やAI処理に利用される。


## Query Execution

NWF Query Language（NQL）によるクエリを実行する。

主な用途

- 物語データ検索
- キャラクター分析
- 伏線検索
- 感情カーブ分析


## Analysis Processing

物語構造の分析処理を行う。

主な分析

- キャラクター出現分析
- Thread進行分析
- 伏線検出
- 感情カーブ解析
- 構造バランス解析


## Output Generation

分析結果や物語構造を出力する。

主な出力形式

- JSON
- Markdown
- レポート形式
- 可視化データ


## AI連携

Execution Flow は AI による物語解析を前提として設計されている。

AIは以下の用途でこのフローを利用できる。

- プロット分析
- 伏線管理
- キャラクター関係分析
- ストーリー最適化


## 実行フローの設計思想

NWF Execution Flow の設計思想は以下である。

- 明確な処理段階
- データ整合性の保証
- 分析と生成の分離
- AIとの高い親和性

この実行フローは NWF における標準的な物語処理パイプラインとして使用される。