# NWF Data Model v1.0

## 概要

NWF（Novel Writing Framework）は物語を構造化データとして扱うフレームワークである。

従来の小説制作では物語は文章としてのみ管理されていたが、
NWFでは物語を複数のデータ要素に分解し、それらの関係性を
データ構造として管理する。

このドキュメントでは NWF における基本データモデルを定義する。

---

# NWF データ構造の基本概念

NWFでは物語は以下の主要要素によって構成される。

- World
- Character
- Thread
- Scene
- Beat

これらの要素は **Story Database** 内で相互に関連付けられる。

---

# Story Database

Story Database は物語のすべての情報を保持するデータ集合である。

主な役割

- 物語データの保存
- 要素間の参照管理
- 物語構造の一貫性保持

Story Database は通常 JSON 形式などの構造化データとして保存される。

---

# Core Entities

## World

World は物語世界の設定を表す。

例

- 世界観
- 社会構造
- 技術レベル
- 歴史
- ルール

World は物語の背景となる環境を定義する。

---

## Character

Character は物語に登場する主体である。

Character は以下の情報を持つ。

- 名前
- 役割
- 目的
- 動機
- 性格
- 他キャラクターとの関係

Character は Scene や Thread に参加する。

---

## Thread

Thread は物語のドラマラインを表す構造である。

Thread は以下の要素を持つ。

- Thread ID
- タイトル
- 種類
- 関連キャラクター
- 状態

Thread は Scene を通じて進行する。

例

- Main Plot Thread
- Sub Plot Thread
- Mystery Thread
- Character Arc Thread

---

## Scene

Scene は物語の出来事単位である。

Scene は Thread の状態を変化させるイベントとして機能する。

Scene の主な要素

- Scene ID
- 登場キャラクター
- 場所
- コンフリクト
- 結果

Scene は時系列に並び Scene Timeline を構成する。

---

## Beat

Beat は Scene 内部の最小ドラマ単位である。

Beat は物語の細かい変化を表す。

例

- 情報提示
- 感情変化
- 行動
- 対立
- 決断

Beat は Scene の内部構造を形成する。

---

# Entity Relationships

NWFのデータ要素は以下の関係を持つ。

World  
↓  
Character  
↓  
Thread  
↓  
Scene  
↓  
Beat

また、各要素は相互参照することが可能である。

例

- Character → Thread
- Thread → Scene
- Scene → Beat

---

# Data Representation

NWFではデータは通常以下の形式で管理される。

- JSON
- YAML
- Markdown

これにより

- 人間による編集
- Gitによるバージョン管理
- AIによる解析

を容易にする。

---

# NWF データモデルの目的

NWF Data Model の目的は以下である。

- 物語構造の明確化
- データとしての物語管理
- エンジン処理との統合
- AIによる分析と生成の支援

このデータモデルは NWF Core Architecture の基盤となる。