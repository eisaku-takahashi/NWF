Source: docs/spec/AI_Workflow_Spec/NWF_AI_Collaboration_Model_v2.0.1.md
Updated: 2026-04-06T13:10:00+09:00
PIC: Engineer / ChatGPT

# NWF AI Collaboration Model v2.0.1

---

## 1. 概要

本ドキュメントは、NWF v2.0.1 における AI Collaboration Model（AI 協調作業モデル）を定義するものである。

NWF における AI Collaboration Model は、単なる AI 支援ツールではなく、System Engine（論理・因果律）と AI Agent（創造・文脈生成）が、人間（Architect / Director）を最終意思決定者として協調動作する自律ワークフローシステムである。

本モデルは以下の目的を持つ。

- AI と System Engine の責務分離
- 人間の最終承認を含む Human-in-the-Loop の実現
- 全 AI 出力の監査・追跡可能性の確保
- Execution Pipeline との統合
- Audit System への完全な履歴保存

---

## 2. AI Agent Roles 定義

NWF v2.0.1 では、AI は単一の存在ではなく、複数の役割（Role）を持つ Agent 群として定義される。

### 2.1 Agent Roles 一覧

| Role | 責務 | 関連 Engine |
| --- | --- | --- |
| Architect (Director) | 人間。最終意思決定、承認、方向性決定 | 全 Engine |
| Orchestrator | Agent の実行順序制御、タスク管理、競合解決 | Execution Pipeline |
| Author Agent | 文章、ナラティブ、コンテンツ生成 | Narrative / Story Engine |
| Logic Agent | 因果律、ルール、整合性チェック | Simulation / Event Engine |
| Analyst Agent | データ分析、感情曲線、品質評価 | Analysis / Emotional Engine |
| Chronicle Agent | 時間軸、履歴、世界線管理 | Timeline Engine |

### 2.2 Architect（Human）の役割

Architect は以下の権限を持つ。

- Goal の設定
- Agent 出力の承認 / 修正 / 棄却
- Commit の最終承認
- Spec 変更の承認
- System の方向性決定

AI はいかなる場合も Architect の承認なしに Audit Log へ Commit できない。

---

## 3. Engine と Agent の責務分離

NWF において、System Engine と AI Agent は明確に役割が分離される。

### 3.1 System Engine（論理・制約）

System Engine の責務は以下とする。

- 因果律の適用
- データ型検証
- Temporal 整合性検証
- 状態遷移検証
- Validation 実行
- Audit Commit 管理
- 物理的・論理的に不可能な状態の排除

Engine は Hard Constraints（強制制約）を提供する。

### 3.2 AI Agent（創造・提案）

AI Agent の責務は以下とする。

- コンテンツ生成
- 提案（Draft）生成
- 文脈理解
- 意味的整合性評価
- 改善提案
- Rewrite / Refinement

AI Agent は Creative Proposals（創造的提案）を生成するが、
最終的な正当性は Engine によって検証される。

### 3.3 Engine と Agent の関係

関係は以下の通り。

1. Agent が Draft を生成
2. Engine が Validation を実行
3. Validation を通過したデータのみ Commit 可能
4. Architect が最終承認
5. Audit System に記録

---

## 4. AI Workflow Pipeline

AI Collaboration Workflow は、4-Step Loop として定義される。

### 4.1 4-Step Loop

1. Briefing
2. Generation
3. Cross-Validation
4. Review & Commit

### 4.2 Briefing

入力:

- Goal
- Constraints
- Spec Version
- Context Data
- Temporal Range

Orchestrator または Architect が Workflow を開始する。

### 4.3 Generation（Parallel Execution）

複数 Agent が並行して Draft を生成する。

例:

- Author Agent → コンテンツ生成
- Logic Agent → ルール適用
- Analyst Agent → 品質評価
- Chronicle Agent → 時系列整合性確認

### 4.4 Cross-Validation

以下の検証を実行する。

- Engine Validation（論理検証）
- Analyst Validation（意味・品質検証）
- Temporal Validation（時間整合性）
- Concurrency Validation（競合検証）
- Spec Validation（Spec 準拠検証）

### 4.5 Review & Commit

1. Architect がレビュー
2. 修正 / 承認 / 棄却
3. 承認されたデータに UUID を付与
4. Audit System に Commit
5. State が確定

---

## 5. Draft / Validation / Commit 状態モデル

AI Workflow におけるデータ状態は以下のように定義される。

| State | 説明 |
| --- | --- |
| Ghost | Agent 出力直後の未確定状態 |
| Draft | 編集可能状態 |
| Validated | Engine Validation 通過 |
| Approved | Architect 承認済み |
| Committed | Audit Log に記録済み |
| Archived | 履歴保存状態 |

状態遷移は Execution Pipeline に従う。

---

## 6. Execution Pipeline との統合

AI Workflow は Execution Pipeline のフックポイントに接続される。

### 6.1 Pipeline Hook Points

| Pipeline Stage | AI Workflow Action |
| --- | --- |
| Fetch | Context / Temporal Data 取得 |
| Pre-Execute | AI Draft 生成 |
| Execute | Engine 計算 + AI 推論 |
| Post-Execute | AI 評価・分析 |
| Validate | Engine Validation |
| Commit | Audit System 書き込み |

AI Workflow は Pipeline の外側ではなく、Pipeline に統合される。

---

## 7. AI Workflow Governance

AI は Spec Governance に従う必要がある。

### 7.1 Immutability

AI は以下を変更できない。

- 過去の Audit Log
- Commit 済みデータ
- UUID
- Timestamp
- Kernel Data

### 7.2 Traceability

以下を全て Audit Log に記録する。

- Prompt
- AI Response
- Validation Result
- Approval Result
- Commit User
- Timestamp
- Spec Version

すべての AI 出力は再現可能でなければならない。

### 7.3 Spec Alignment

AI は以下を守る必要がある。

- 現在の Spec Version
- Data Format
- Metadata Rules
- Validation Rules
- Naming Rules
- Execution Rules

Spec に違反する出力は Validation Error とする。

---

## 8. Agent 拡張モデル

NWF AI System は拡張可能な Agent Architecture を採用する。

### 8.1 Plugin Agent Architecture

新しい Agent を追加可能。

例:

- World Rule Agent
- Physics Agent
- Economy Agent
- Character Behavior Agent
- Dialogue Agent
- Visual Design Agent

### 8.2 Self-Refinement Loop

AI は以下のループを実行可能。

1. Draft 作成
2. Self Analysis
3. Rewrite
4. Validation
5. Improvement Proposal

これを Rewrite Loop と呼ぶ。

---

## 9. AI Collaboration Architecture Summary

NWF AI Collaboration Model は三層構造で定義される。

| Layer | Component | 役割 |
| --- | --- | --- |
| Layer 1 | Kernel | 監査・時間・不変データ |
| Layer 2 | Engine | 論理・因果律・検証 |
| Layer 3 | Workflow | AI と Human の協働作業 |

### 9.1 三権分立モデル

NWF System は以下の三権構造を持つ。

| Role | 機能 |
| --- | --- |
| Kernel | 絶対的な事実の管理 |
| Engine | 論理と因果律の管理 |
| Human / AI Workflow | 意思決定と創造 |

この構造により、

- データの不変性
- 論理の整合性
- 創造性
- 人間の意思決定

を同時に実現する。

---

## 10. まとめ

NWF AI Collaboration Model は以下を実現するためのシステムである。

- AI と Engine の責務分離
- Human-in-the-Loop Workflow
- 完全な監査可能性
- Execution Pipeline 統合
- Spec Governance 準拠
- Agent 拡張可能な Architecture

本モデルは NWF v2.0.1 における AI Workflow の基盤仕様となる。

---

[EOF]