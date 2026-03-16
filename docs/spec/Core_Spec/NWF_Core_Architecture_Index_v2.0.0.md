Source: docs/spec/Core_Spec/NWF_Core_Architecture_Index_v2.0.0.md
Updated: 2026-03-16T13:43:00+09:00
PIC: Engineer / ChatGPT

# NWF Core Architecture Index v2.0.0

---

## 1. 概要

本ドキュメントは **NWF Core Specification のインデックス**である。

Core Spec は **Novel Writing Framework (NWF)** の最も基本的な構造を定義する仕様群であり、
NWF システム全体の基盤となる。

NWF Core は主に以下の役割を持つ。

* 物語データ構造の定義
* 物語構造モデルの定義
* データ保存構造の定義
* 物語処理フローの定義
* NWFエンジンが扱う基本データモデルの定義

Core Spec は **NWF 全体の基盤仕様**であり、
すべての Engine / AI / Tooling はこの仕様に依存する。

---

## 2. Core Specification Scope

NWF Core Specification は以下の領域を定義する。

* Terminology（用語定義）
* Data Model（データモデル）
* Narrative Structure Model（物語構造モデル）
* File System Layout（ファイル構造）
* Query Language（クエリ言語）
* Execution Model（処理フロー）
* Narrative Rendering（文章生成処理）

---

## 3. Core Components

NWF Core は以下の仕様ドキュメントで構成される。

### 3.1 Glossary

NWFで使用される基本用語を定義する。

NWF_Glossary

---

### 3.2 Data Model

NWFで扱うすべての物語データの基本構造を定義する。

NWF_Data_Model

---

### 3.3 Thread Graph Model

物語の構造を **Thread Graph** として定義する。

NWF_Thread_Graph_Model

Thread Graph は以下の要素を表現する。

* Plot Structure（プロット構造）
* Narrative Dependency（物語依存関係）
* Foreshadowing Relation（伏線関係）

---

### 3.4 Scene Model

物語の Scene 構造を定義する。

NWF_Scene_Model

Scene は以下の役割を持つ。

* Narrative Unit（物語単位）
* Character Interaction（キャラクター相互作用）
* Plot Progression（プロット進行）

---

### 3.5 Beat Model

Scene 内の最小単位を **Beat** として定義する。

NWF_Beat_Model

Beat は以下のような物語の瞬間的変化を表す。

* Emotion Change（感情変化）
* Action（行動）
* Dialogue（会話）

---

### 3.6 File System

NWFのファイル構造を定義する。

NWF_File_System

すべてのデータは **NWF Project Root** を基準として配置される。

---

### 3.7 Query Language

NWF Query Language は
物語データの検索・分析・AI処理を行うための専用クエリ仕様である。

NWF_Query_Language

---

### 3.8 Execution Flow

NWFの処理フローを定義する。

NWF_Execution_Flow

Execution Flow は以下を含む。

* Engine Pipeline
* Narrative Processing
* Data Transformation

---

### 3.9 Narrative Rendering

NWFデータから最終的な文章を生成する処理を定義する。

NWF_Narrative_Rendering

Rendering は以下の役割を持つ。

* Scene → Text Transformation
* Narrative Formatting
* AI Story Generation Support

---

## 4. NWF Project Root

NWF システムは **NWF Project Root** を基準として構築される。

Specでは以下の表記を使用する。

NWF Project Root

または

<project_root>/

すべてのディレクトリ構造およびデータ配置は
このルートを基準として定義される。

実際に構築する NWF システムの **NWF Project Root フォルダ名は `NWF` を使用する。**

---

## 5. Core Spec Dependency

Core Spec は以下の上位仕様に依存する。

NWF_System_Architecture

Engine Spec / AI Spec / Plugin Spec は
Core Spec に依存する。

---

## 6. Development Environment

NWF のローカル開発環境は **Antigravity** を使用する。

Spec 作成・編集・管理は
Antigravity 環境で行われる。

---

## 7. Specification Versioning

Spec のバージョン管理ルールは
Spec Governance に定義される。

各 Spec ファイルは
**バージョン付きファイル名**で管理される。

例

Spec_Name_v2.0.0.md

---

## 8. まとめ

NWF Core Specification は
Novel Writing Framework の基本構造を定義する基盤仕様である。

Core Spec は以下の要素を統合的に定義する。

* 物語データモデル
* 物語構造モデル
* ファイル管理構造
* クエリシステム
* 実行フロー
* 文章生成処理

これらの仕様は **NWF System Architecture** の下で動作し、
NWF Engine / AI / Tooling のすべての基盤として機能する。

---

[EOF]
