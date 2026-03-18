Source: docs/spec/Index/NWF_Dependency_Map_v2.0.0.md
Updated: 2026-03-19T02:00:00+09:00
PIC: Engineer / ChatGPT

# NWF Dependency Map v2.0.0

---

## 1. 概要

本ドキュメントは  
NWF Spec間の依存関係を定義する。

目的

- Spec間の関係性の明確化
- 設計構造の可視化
- 開発・理解効率の向上

---

## 2. 全体構造

NWFは以下の依存階層で構成される。

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

---

## 3. 依存関係の定義

### 3.1 Spec_Governance

すべてのSpecの基盤

---

### 3.2 Index

全体構造の入口

---

### 3.3 System_Architecture

全体設計の定義

依存先

Spec_Governance  

---

### 3.4 Core_Spec

基盤データ構造

依存先

System_Architecture  

---

### 3.5 Data_Spec

データフォーマット

依存先

Core_Spec  

---

### 3.6 Engine_Spec

処理エンジン

依存先

Core_Spec  
Data_Spec  

---

### 3.7 Execution_Spec

処理フロー

依存先

Engine_Spec  

---

### 3.8 AI_Interface

AI連携

依存先

Execution_Spec  

---

### 3.9 AI_Workflow_Spec

運用フロー

依存先

AI_Interface  

---

## 4. 設計原則

- 上位Specは下位Specに依存しない
- 下位Specは上位Specに依存する
- 循環依存は禁止

---

## 5. まとめ

本マップにより

- Spec構造の理解
- 開発効率向上
- AI処理精度向上

を実現する。

---

[EOF]