Source: docs/spec/Index/NWF_Spec_Master_Index_v2.0.1.md
Updated: 2026-03-29T05:28:00+09:00
PIC: Engineer / ChatGPT

# NWF Spec Master Index v2.0.1

---

## 1. 概要

本ドキュメントは  
NWF v2.0.1 における全 10 カテゴリ（Core, System_Architecture, Architecture, Data, Engine, Execution, AI_Interface, AI_Workflow, Spec_Governance, Index）を統合した **マスターインデックス** である。

目的

- 全スペックの俯瞰
- 依存関係とデータフローの明確化
- Recursive Integrity Gateway の起点設定
- 開発・執筆の高速化と誤操作防止

---

## 2. System Overview

NWF v2.0.1 は「Story OS」として、各 Spec が連鎖して仮想世界航空史の生成プロセスを支える。  
各 Spec は階層化され、データ・処理・AIフローが設計哲学に沿って流れる。

- **Layer 1: Philosophy & Core**  
  Core, System_Architecture（世界観・設計思想の定義）

- **Layer 2: Blueprint & Data**  
  Architecture, Data, Engine（物理制約・データ構造・処理仕様の定義）

- **Layer 3: Execution & Logic**  
  Execution, AI_Interface, AI_Workflow（動的生成パイプライン）

- **Layer 4: Governance**  
  Spec_Governance, Index（自己修復・品質管理・マスター索引）

---

## 3. Master Directory

| Category | File Name | Version | PIC | 概要 |
|----------|-----------|--------|-----|-----|
| Spec_Governance | NWF_Spec_Integrity_Check_v2.0.1.md | v2.0.1 | Engineer / ChatGPT | 仕様書整合性検証の起点 |
| Index | NWF_Spec_Master_Index_v2.0.1.md | v2.0.1 | Engineer / ChatGPT | 全スペック統合マスター索引 |
| Index | NWF_Spec_Roadmap_v2.0.1.md | v2.0.1 | Engineer / ChatGPT | 開発・運用ロードマップ |
| Index | NWF_Spec_Glossary_v2.0.1.md | v2.0.1 | Engineer / ChatGPT | 共通用語集 |
| System_Architecture | System_Architecture_v2.0.1.md | v2.0.1 | Engineer / ChatGPT | システム全体設計 |
| Core_Spec | Core_Spec_v2.0.1.md | v2.0.1 | Engineer / ChatGPT | 基盤データ構造と概念 |
| Architecture_Spec | Architecture_Spec_v2.0.1.md | v2.0.1 | Engineer / ChatGPT | 設計図・物理制約 |
| Data_Spec | Data_Spec_v2.0.1.md | v2.0.1 | Engineer / ChatGPT | JSON構造・データ形式 |
| Engine_Spec | Engine_Spec_v2.0.1.md | v2.0.1 | Engineer / ChatGPT | 各エンジン仕様 |
| Execution_Spec | Execution_Spec_v2.0.1.md | v2.0.1 | Engineer / ChatGPT | 処理フローとパイプライン |
| AI_Interface | AI_Interface_v2.0.1.md | v2.0.1 | Engineer / ChatGPT | AI連携仕様 |
| AI_Workflow_Spec | AI_Workflow_Spec_v2.0.1.md | v2.0.1 | Engineer / ChatGPT | AI運用フロー |

---

## 4. Structural Dependency Map

NWF Spec 階層依存図（Mermaid形式参考）

Layer 4 --> Layer 3 --> Layer 2 --> Layer 1

- 上位 Spec は下位 Spec に依存せず、下位 Spec は上位 Spec に依存する  
- 循環依存は禁止  
- Recursive Integrity Gateway から全 Spec に再帰的整合性チェックを実行可能

---

## 5. Recursive Integrity Status

- 本マスターインデックスを起点として、各 Spec の `Integrity Score` を 0-100 pts で算出  
- スコア集計により全体健全性を可視化  
- HITL（Human-in-the-Loop）承認ポイントを記録し、更新時に必ず確認

---

## 6. Maintenance & Lifecycle

- Semantic Versioning (Major.Minor.Patch) に従い管理  
- 更新フロー: Draft → Review → HITL Approval → Release  
- Index 更新時は必ず Dependency Map および Master Directory を同期

---

## 7. Quick Links

- NWF_Spec_Integrity_Check_v2.0.1.md  
- NWF_Spec_Roadmap_v2.0.1.md  
- NWF_Spec_Glossary_v2.0.1.md  
- 各カテゴリ v2.0.1 スペック

---

[EOF]