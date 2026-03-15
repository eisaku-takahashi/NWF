Source: docs/spec/System_Architecture/NWF_System_Architecture_v2.0.0.md
Updated: 2026-03-15T21:40:00+09:00
PIC: Engineer / ChatGPT

# NWF System Architecture v2.0.0

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 概要
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NWF System Architecture は  
Novel Writing Framework（NWF）全体の構造を定義する  
最上位レベルのアーキテクチャ仕様である。

本仕様は以下を目的とする。

・NWFシステムの構造定義  
・各コンポーネントの責務の明確化  
・データフローの統一  
・エンジン実行基盤の定義  
・AI連携構造の標準化  

NWF v2.0では、v1.0系アーキテクチャを拡張し  
以下の設計原則を導入する。

Modular Architecture  
Engine Driven Processing  
Structured Narrative Data  
AI Assisted Authoring  
Deterministic Execution Pipeline

本仕様は NWF v2.0 の **System-Level Specification** として機能する。


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. NWF Project Root
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NWFシステムは **NWF Project Root** を基準として構築される。

Specでは以下の表記を使用する。

NWF Project Root

または

<project_root>/

すべてのディレクトリ構造  
データ配置  
エンジン実行  
仕様参照  

はこのルートディレクトリを基準とする。

例

> D:\NWF

NWF Project Root は以下の主要ディレクトリで構成される。

docs  
engines  
schemas  
projects  
runtime  
tools  
tests  
archive

docs は仕様および設計文書を格納する。


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. System Architecture Overview
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NWF v2.0 は以下のレイヤー構造で設計される。

Specification Layer  
Core Model Layer  
Data Layer  
Engine Layer  
Execution Layer  
AI Interface Layer

これらのレイヤーは  
物語制作の構造化処理を実現する。


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. Specification Layer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Specification Layer は  
NWFのすべての仕様を定義する。

保存場所

> docs/spec/

主な仕様カテゴリ

Core Specification  
Architecture Specification  
Engine Specification  
Data Specification  
Execution Specification  
AI Workflow Specification  
Spec Governance


Specification Layer は  
NWFシステムの設計ルールおよび構造定義の  
唯一の公式仕様として機能する。


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5. Core Model Layer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Core Model Layer は  
物語構造の基本モデルを定義する。

主要モデル

Thread  
Scene  
Beat  
Character  
WorldRule  
Foreshadowing  
EmotionalCurve

これらのモデルは  
NWF物語構造の基礎となる。


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
6. Data Layer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Data Layer は  
物語データの保存と管理を行う。

保存形式

JSON

主なデータ構造

Story  
Thread  
Scene  
Beat  
Character  
World  
Foreshadowing  
EmotionalCurve

保存場所

> <project_root>/projects/

各ストーリーは  
独立した Story Database として管理される。


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
7. Engine Layer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Engine Layer は  
物語構造の解析および生成補助を行う。

主なエンジン

ThreadEngine  
SceneEngine  
BeatEngine  
ForeshadowingEngine  
EmotionalCurveEngine

各エンジンは以下の処理を行う。

・物語構造の検証  
・整合性チェック  
・構造解析  
・生成支援

エンジン実装は以下に配置される。

> <project_root>/engines/


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
8. Execution Layer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Execution Layer は  
エンジン実行の順序とパイプラインを管理する。

Execution Pipeline は以下の順序で実行される。

Story Load

↓

ThreadEngine

↓

SceneEngine

↓

BeatEngine

↓

ForeshadowingEngine

↓

EmotionalCurveEngine

↓

Validation System

↓

Analysis Output

このパイプラインは  
物語構造の完全な解析処理を提供する。


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
9. AI Interface Layer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AI Interface Layer は  
AIとNWFシステムの連携を提供する。

対象AI

Director  
Gemini

Engineer  
ChatGPT

Writer  
Claude

AIは以下の役割を持つ。

Director

・構造設計  
・物語ディレクション  

Engineer

・技術検証  
・構造整合性チェック  

Writer

・物語執筆  
・シーン生成


AI Interface Layer は  
AI Workflow Specification によって定義される。


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
10. Data Flow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NWF v2.0 の基本データフローは以下である。

Story Data (JSON)

↓

Engine Processing

↓

Validation System

↓

Narrative Analysis

↓

AI Assistance


この構造により  
物語制作の構造化処理が実現される。


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
11. Versioning
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NWF Specification は  
Semantic Versioning を採用する。

Version Format

major.minor.patch

例

v2.0.0  
v2.0.1  
v2.1.0


Major

フレームワーク構造変更


Minor

仕様拡張


Patch

軽微修正


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
12. Compatibility
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NWF v2.0 は  
v1.x 系仕様との **上位互換** を維持する。

互換対象

Core Models  
Data JSON Structures  
Engine Interfaces

既存の v1.x Story Data は  
v2.0 環境でも読み込み可能である。


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
13. Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NWF System Architecture v2.0 は  
以下の主要構造で構成される。

Specification Layer

Core Model Layer

Data Layer

Engine Layer

Execution Layer

AI Interface Layer

このアーキテクチャにより  
NWFは

物語構造  
データ管理  
エンジン処理  
AI支援

を統合した  
創作フレームワークとして機能する。

Version: v2.0.0

[EOF]