# NWF Specification Index v1.0.1

## 概要

本ドキュメントは NWF (Novel Writing Framework) の仕様書全体のインデックスである。

NWF Spec は物語構造をデータモデルとして定義し、AI支援による物語生成・分析・編集を可能にするフレームワークである。

本インデックスは、NWF Spec の各仕様ドキュメントの構造と役割を示す。

## NWF Project Root

NWF仕様において、すべてのファイルパスは NWF Project Root を基準として記述される。

NWF Project Root は小説プロジェクトおよびフレームワークのルートディレクトリを指す。

Spec上では以下の表記を使用する。

NWF Project Root

または

<project_root>/

すべてのファイルパスはこのルートを基準とした相対パスとして解釈される。

## Specification Structure

NWF Spec は以下の構造で構成される。

Index  
System Architecture  
Core Spec  
Architecture Spec  
Engine Spec  
AI Interface  
Data Spec  
Execution Spec  
AI Workflow Spec  
Spec Governance

## Spec Conventions

NWF Spec は以下の共通ルールに従う。

- すべてのパスは NWF Project Root を基準とする
- Spec ファイルはバージョン付きファイル名で管理される
- バージョン管理の詳細は Spec Governance に定義される

## Version

Version: v1.0.1