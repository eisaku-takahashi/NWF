# NWF System Architecture v1.0.1

## 概要

NWF System Architecture は、Novel Writing Framework 全体の構造を定義する。

本アーキテクチャは以下の要素で構成される。

Core Model  
Engine System  
Data Layer  
AI Interface  
Execution Pipeline

## NWF Project Root

NWF システムは NWF Project Root を基準として構築される。

Specでは以下の表記を使用する。

NWF Project Root

または

<project_root>/

すべてのディレクトリ構造およびデータ配置はこのルートを基準とする。

## System Components

NWFは以下の主要コンポーネントで構成される。

Core Specification  
Architecture Specification  
Engine Specification  
Data Specification  
Execution Specification  
AI Workflow Specification

## Data Layer

Data Layer は物語データを管理する。

stories ディレクトリに Story Database が保存される。

## Engine Layer

Engine Layer は物語構造の処理を担当する。

ThreadEngine  
SceneEngine  
BeatEngine  
ForeshadowingEngine  
EmotionalCurveEngine

## Version

Version: v1.0.1