Source: docs/spec/Core_Spec/NWF_File_System_v2.0.0.md
Updated: 2026-03-16T13:43:00+09:00
PIC: Engineer / ChatGPT

# NWF File System v2.0.0

---

## 1. 概要

本ドキュメントは **Novel Writing Framework (NWF)** における
ファイルシステム構造を定義する。

NWF は物語制作のためのフレームワークであり、
物語データ、仕様書、エンジン、ツールを
**構造化されたディレクトリとして管理する。**

本仕様は以下を定義する。

* NWF Project Root
* NWFの標準ディレクトリ構造
* データ保存ディレクトリ
* エンジン配置構造
* 小説プロジェクト管理構造
* Spec内で使用するパス表記ルール

---

## 2. NWF Project Root

すべての NWF システムは **NWF Project Root** を基準として構築される。

Specでは以下の表記を使用する。

NWF Project Root

または

<project_root>/

すべてのディレクトリおよびファイルパスは
このルートからの **相対パス** として定義される。

実際に構築する NWF システムの
**NWF Project Root フォルダ名は `NWF` を使用する。**

---

## 3. NWF 標準ディレクトリ構造

NWF の標準ディレクトリ構造は以下とする。

```
<project_root>/
│
├─ docs/
│  ├─ project/
│  └─ spec/
│     ├─ Index/
│     ├─ System_Architecture/
│     ├─ Core_Spec/
│     ├─ Architecture_Spec/
│     ├─ Engine_Spec/
│     ├─ AI_Interface/
│     ├─ Data_Spec/
│     ├─ Execution_Spec/
│     ├─ AI_Workflow_Spec/
│     └─ Spec_Governance/
│
├─ data/
│  ├─ threads/
│  ├─ scenes/
│  ├─ characters/
│  └─ world_rules/
│
├─ engines/
│  ├─ thread_engine/
│  ├─ scene_engine/
│  ├─ character_engine/
│  ├─ plot_engine/
│  └─ world_rule_engine/
│
├─ novel_projects/
│  └─ project_template/
│     ├─ threads/
│     ├─ scenes/
│     ├─ characters/
│     ├─ world_rules/
│     └─ manuscript/
│
└─ tools/
   └─ validation/
```

この構造は **NWF v2.0 の標準レイアウト**として定義される。

---

## 4. docs ディレクトリ

```
docs/
```

docs ディレクトリは
**NWF システムのドキュメントを管理するディレクトリ**である。

---

### 4.1 docs/project

```
docs/project/
```

このディレクトリは
**NWF プロジェクト管理用ドキュメントを保存する。**

ここでいう **NWF プロジェクト**とは
フレームワーク自体の開発プロジェクトを指す。

各小説プロジェクトとは **別の概念**である。

---

### 4.2 docs/spec

```
docs/spec/
```

このディレクトリは
**NWF 仕様書（Specification）を保存する。**

Spec はカテゴリごとにサブディレクトリで管理される。

```
docs/spec/
│
├─ Index/
├─ System_Architecture/
├─ Core_Spec/
├─ Architecture_Spec/
├─ Engine_Spec/
├─ AI_Interface/
├─ Data_Spec/
├─ Execution_Spec/
├─ AI_Workflow_Spec/
└─ Spec_Governance/
```

---

## 5. data ディレクトリ

```
data/
```

data ディレクトリは
**NWF が扱う物語データを保存する。**

```
data/
│
├─ threads/
├─ scenes/
├─ characters/
└─ world_rules/
```

各ディレクトリには
対応するデータモデルの JSON データが保存される。

---

## 6. engines ディレクトリ

```
engines/
```

engines ディレクトリは
**NWF の物語処理エンジンを保存する。**

```
engines/
│
├─ thread_engine/
├─ scene_engine/
├─ character_engine/
├─ plot_engine/
└─ world_rule_engine/
```

各エンジンは
NWF Data Model を処理するソフトウェアコンポーネントである。

---

## 7. novel_projects ディレクトリ

```
novel_projects/
```

novel_projects ディレクトリは
**NWF を使用して制作される小説プロジェクトを管理する。**

```
novel_projects/
│
└─ project_template/
   ├─ threads/
   ├─ scenes/
   ├─ characters/
   ├─ world_rules/
   └─ manuscript/
```

project_template は
新しい小説プロジェクトを作成するための
**テンプレート構造**を定義する。

---

## 8. tools ディレクトリ

```
tools/
```

tools ディレクトリは
**NWF の補助ツールを保存する。**

```
tools/
│
└─ validation/
```

validation ディレクトリには
データ検証ツールや構造チェックツールなどを配置する。

---

## 9. Path Convention

Spec 内で使用するパスは以下のルールに従う。

* ルートは **NWF Project Root**
* すべて **相対パス**で記述する
* OS依存の絶対パスは使用しない
* Windows / Linux / macOS で共通に使用可能な表記を採用する

例

```
docs/spec/Core_Spec/NWF_File_System_v2.0.0.md
```

---

## 10. まとめ

NWF File System は
Novel Writing Framework のファイル構造を定義する基盤仕様である。

本仕様では以下を定義した。

* NWF Project Root
* 標準ディレクトリ構造
* Spec管理ディレクトリ
* 物語データ保存構造
* エンジン配置構造
* 小説プロジェクト構造
* パス表記ルール

この構造により
NWF は **拡張可能で整理された物語制作環境**を提供する。

---

[EOF]