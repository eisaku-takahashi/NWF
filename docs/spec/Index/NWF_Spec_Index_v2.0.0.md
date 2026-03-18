Source: docs/spec/Index/NWF_Spec_Index_v2.0.0.md
Updated: 2026-03-19T02:08:00+09:00
PIC: Engineer / ChatGPT

# NWF Specification Index v2.0.0

---

## 1. 概要

本ドキュメントは  
NWF（Novel Writing Framework）における  
**全Specの統合インデックス**である。

目的

- Spec全体構造の可視化
- 各Specへの導線提供
- 理解順序の明確化
- 依存関係の把握

---

## 2. NWF Project Root

すべてのパスは  
NWF Project Root を基準とする。

表記

<project_root>/

すべてのSpecは  
このルートからの相対パスで記述する。

---

## 3. Spec構造

NWF Specは以下のカテゴリで構成される。

- Spec_Governance
- Index
- System_Architecture
- Core_Spec
- Data_Spec
- Engine_Spec
- Execution_Spec
- AI_Interface
- AI_Workflow_Spec

---

## 4. 推奨読書順

以下の順序で読むことを推奨する。

1. Spec_Governance  
2. Index  
3. System_Architecture  
4. Core_Spec  
5. Data_Spec  
6. Engine_Spec  
7. Execution_Spec  
8. AI_Interface  
9. AI_Workflow_Spec  

---

## 5. 各Specの役割

### 5.1 Spec_Governance

Specルール・記述規約・バージョン管理を定義する。

---

### 5.2 Index

Spec全体の構造と導線を提供する。

---

### 5.3 System_Architecture

NWF全体の構造と設計思想を定義する。

---

### 5.4 Core_Spec

基盤データ構造および基本概念を定義する。

---

### 5.5 Data_Spec

JSON構造およびデータフォーマットを定義する。

---

### 5.6 Engine_Spec

各エンジンの仕様を定義する。

---

### 5.7 Execution_Spec

処理フロー・パイプライン・検証を定義する。

---

### 5.8 AI_Interface

AIとのインターフェース仕様を定義する。

---

### 5.9 AI_Workflow_Spec

AI活用フローおよび運用方法を定義する。

---

## 6. 依存関係

NWF Specは以下の依存階層で構成される。

Spec_Governance  
↓  
Index  
↓  
System_Architecture  
↓  
Core_Spec  
↓  
Data_Spec  
↓  
Engine_Spec  
↓  
Execution_Spec  
↓  
AI_Interface  
↓  
AI_Workflow_Spec  

補足

- 上位Specは下位Specに依存しない  
- 下位Specは上位Specに依存する  
- 循環依存は禁止  

---

## 7. 適用ルール

すべてのSpecは以下に従う。

- NWF Spec Standard  
- NWF Markdown Format  
- NWF Specification Versioning  
- NWF Spec Writing Guidelines  

---

## 8. バージョン管理

すべてのSpecは  
Semantic Versioning に従う。

形式

Major.Minor.Patch

例

v2.0.0

---

## 9. 関連ドキュメント

- docs/spec/Index/NWF_Dependency_Map_v2.0.0.md  

---

## 10. まとめ

本インデックスは

- Spec全体構造の整理
- 理解導線の最適化
- 依存関係の明確化
- フレームワーク全体の可視化

を目的とする。

---

[EOF]