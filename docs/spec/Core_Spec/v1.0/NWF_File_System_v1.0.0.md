# NWF File System v1.0

## 概要

NWF（Novel Writing Framework）は、物語データ・仕様書・エンジンコードを明確に分離したディレクトリ構造で管理する。

このドキュメントでは NWF の標準ファイルシステム構造を定義する。

NWFのファイル構造は以下の目的で設計されている。

- 物語データの整理
- フレームワーク仕様の管理
- エンジン実装の分離
- Gitによるバージョン管理の容易化


## NWF ルート構造

NWFプロジェクトのルートディレクトリは以下である。

Novel_Writing_Framework

このディレクトリがプロジェクトの最上位ディレクトリとなる。


## 基本ディレクトリ構造

NWFでは以下の主要ディレクトリを使用する。

Novel_Writing_Framework  
│  
├ docs  
├ engines  
├ story_db  
├ tools  
└ tests  


## docs ディレクトリ

docs はドキュメントを管理するディレクトリである。

docs  
│  
├ spec  
├ architecture  
├ templates  
└ projects  

主な用途は以下である。

- フレームワーク仕様書
- 設計ドキュメント
- テンプレート
- プロジェクト資料


## spec ディレクトリ

spec は NWF の公式仕様を管理するディレクトリである。

docs/spec  
│  
├ Core_Spec  
├ Engine_Spec  
├ Architecture_Spec  
└ AI_Interface  


## Core_Spec

Core_Spec は NWF の基本仕様を定義するディレクトリである。

docs/spec/Core_Spec  
│  
└ v1.0  

仕様はバージョンごとにディレクトリを分けて管理する。


## engines ディレクトリ

engines は NWF のエンジン実装を管理するディレクトリである。

engines  
│  
├ ThreadEngine  
├ SceneEngine  
├ BeatEngine  
└ RenderingEngine  

それぞれのエンジンが物語構造の処理を担当する。


## story_db ディレクトリ

story_db は物語データを保存するディレクトリである。

story_db  
│  
├ characters  
├ worlds  
├ threads  
├ scenes  
└ beats  

ここに物語のデータファイルを保存する。

通常は以下の形式で管理する。

- JSON
- YAML
- Markdown


## tools ディレクトリ

tools は NWF 開発を支援するツールを格納するディレクトリである。

例

- データ検証ツール
- 変換ツール
- 分析ツール


## tests ディレクトリ

tests はエンジンやデータのテストを行うためのディレクトリである。

例

- エンジン動作テスト
- データ整合性チェック
- サンプル物語データ


## バージョン管理

NWFは Git を使用してバージョン管理を行う。

管理対象は以下である。

- 仕様書
- エンジンコード
- 物語データ

これにより以下を実現する。

- 履歴管理
- 変更追跡
- 複数プロジェクトの管理


## File System 設計の目的

NWF File System の設計目的は以下である。

- 物語データとコードの分離
- フレームワーク仕様の明確化
- プロジェクト管理の効率化
- Git運用の最適化

このファイル構造は NWF の標準的な開発環境として使用される。