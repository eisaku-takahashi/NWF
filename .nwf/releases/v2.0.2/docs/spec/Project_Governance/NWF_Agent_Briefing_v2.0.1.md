Source: docs/spec/Project_Governance/NWF_Agent_Briefing_v2.0.1.md
Updated: 2026-04-05T23:20:00+09:00
PIC: Engineer / ChatGPT

# NWF Agent Briefing v2.0.1

---

## 1. 概要

本ドキュメントは、NWF（Narrative Workflow Framework）におけるエージェント（Antigravity 上で動作する Claude Sonnet）に対し、現在のシステム設計、思想、および作業分担を明確に伝達するためのブリーフィング資料である。

NWF は Phase 2.1（Core Data Control）を完了し、今後は複数 AI による分業体制のもとで開発・運用が行われる。本資料は、エージェントが迷うことなく適切に行動するための「行動指針」として機能する。

---

## 2. システム概要と設計思想

### 2.1 Spec-Driven Architecture
NWF は **Spec-Driven Architecture** を採用する。
すべての仕様は Markdown（docs/spec）として記述され、それが唯一の真実（Single Source of Truth）である。

実装（src/）およびデータ（data/）は、常に仕様に従属する。

---

### 2.2 Causality System（因果律システム）
NWF の中核は以下の関係で定義される。

- Transaction + Audit Log = Causality

すべてのデータ変更は Transaction として記録され、Audit Log に保存される。
ログに存在しない変更は「発生していない」とみなす。

---

### 2.3 Immutability / Append-Only

- データは不変（Immutable）である
- 更新は上書きではなく「新規追加（Append）」として処理される

現在の状態は、Audit Log の累積結果としてのみ再構築される。

---

## 3. AI 分業体制（Role Sharing Protocol）

NWF は以下の役割分担に基づき運用される。

### 3.1 Gemini（Web / 監督）
- システム全体のアーキテクチャ設計
- 仕様の整合性チェック
- フェーズ進行管理

---

### 3.2 ChatGPT（Web / エンジニア）
- 実装プロトタイプ作成
- 詳細仕様書の執筆
- ドキュメント整備

---

### 3.3 Claude（Web / 執筆）
- 物語コンテンツ（小説）の生成
- Narrative Layer における創作活動（将来フェーズ）

---

### 3.4 Antigravity Agent（Claude Sonnet / 検証・自動化）
- ローカル環境でのコード実行
- テストおよびバリデーション
- ファイル操作（作成・更新・削除）
- GitHub への commit / push
- 最終的な整合性確認

---

## 4. エージェントの責務

### 4.1 作業開始前の必須確認
- 必ず logs/audit/NWF_data_state_log_v2.0.1.md を読み込むこと
- 最新の Transaction を把握し、状態を理解すること

---

### 4.2 仕様準拠の厳守
- docs/spec/ 配下の仕様が最優先である
- src/ 実装と仕様に矛盾がある場合は以下を遵守する

1. 勝手に仕様を変更しない
2. 必ず差異を報告する
3. 指示を待つ

---

### 4.3 禁止事項
- Audit Log を経由しないデータ変更
- 既存データの破壊的変更（上書き）
- 未検証の仕様変更

---

## 5. 直近のドキュメント更新予定

Documentation Governance に基づき、以下のドキュメントが更新対象である。

### 5.1 新規作成
- docs/spec/System_Architecture/NWF_Philosophy_v2.0.1.md
- docs/spec/Engine_Spec/NWF_Engine_Architecture_v2.0.1.md
- docs/spec/Kernel_Spec/NWF_Concurrency_Control_v2.0.1.md
- docs/spec/Kernel_Spec/NWF_Temporal_Management_v2.0.1.md

---

### 5.2 既存更新
- docs/project/NWF_Development_Roadmap_v2.0.1.md
- docs/spec/Kernel_Spec/NWF_Kernel_Audit_System_Spec_v2.0.1.md
- docs/spec/Execution_Spec/NWF_Validation_System_v2.0.1.md
- docs/spec/AI_Workflow_Spec/NWF_AI_Collaboration_Model_v2.0.1.md
- docs/spec/Spec_Governance/NWF_Spec_Migration_Report_v2.0.1.md

---

## 6. システム状態（Phase 状況）

- Phase 1: Spec System → 完了
- Phase 2.1: Core Data Control → 完了
- 現在フェーズ: Phase 2.2 以降へ移行準備中

---

## 7. まとめ

本ブリーフィングは、NWF におけるエージェントの「行動原則」を定義するものである。

エージェントは以下を常に遵守すること：

- 仕様（Spec）を最優先とする
- Audit Log を因果の唯一の記録として扱う
- データの不変性を破らない
- 不明点は必ず報告する

NWF は「物語の因果律を管理する OS」であり、本エージェントはその整合性を維持する最終防衛線である。

---

[EOF]