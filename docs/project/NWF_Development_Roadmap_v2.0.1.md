Source: docs/project/NWF_Development_Roadmap_v2.0.1.md
Updated: 2026-04-17T11:25:00+09:00
PIC: Engineer / ChatGPT

# NWF Development Roadmap v2.0.1

---

## 1. 概要

NWF（Narrative Workflow Framework）は、  
物語生成・管理・進化を統合する Narrative Operating System（Story OS）である。

本ロードマップは、Phase 2.8 までに構築された  
「自律駆動基盤（Autonomous Shell）」を前提とし、

**実際に人間が連載小説を制作できる状態へ到達するまでの開発指針**を定義する。

---

## 2. 現状整理（2026-04-17 時点）

### 2.1 到達地点

Phase 2.1 〜 2.8 の完了により、以下が成立：

- Audit Log による完全トレーサビリティ
- Event-Driven Architecture の確立
- Workflow + HITL による意思決定制御
- GitHub Sync / Release の自動化
- System Orchestrator による自律実行

**結論：**  
NWF は「自律的に動く OS」として完成済み

---

### 2.2 Phase 3.3 完了による到達点

- Story Engine Skeleton 実装完了
- Entity → Graph → Timeline の最小変換成功
- World Rule によるナラティブ分岐確認
- Integration Test 全件 PASS

**重要結論：**

> NWF は「静的データベース」から「動的ナラティブ生成エンジン」へ進化完了

---

### 2.3 現在のシステム状態

| レイヤ | 状態 |
|--------|------|
| Kernel | 完全稼働 |
| Infrastructure | 完成 |
| Autonomous | 完全稼働 |
| Agency | 稼働中 |
| Application | Engine 最小実装完了 |

---

## 3. アーキテクチャ（再定義）

### 3.1 5層構造

| Layer | 名称 | 役割 |
|------|------|------|
| L1 | Kernel | ID / Audit / State 管理 |
| L2 | Infrastructure | Spec / Validation / Integrity |
| L3 | Autonomous | Automation / Orchestrator |
| L4 | Agency | HITL / AI Workflow |
| L5 | Application | Engine / Production |

---

## 4. Phase 再構築（実装進捗反映）

---

### Phase 2: Autonomous Foundation（完了）

期間：〜2026-04-14

#### 内容

- Phase 2.1 Core Data Control
- Phase 2.2 Spec Loader
- Phase 2.3 HITL
- Phase 2.4 Workflow Engine
- Phase 2.5 Recursive Integrity
- Phase 2.6 GitHub Sync
- Phase 2.7 Release Manager
- Phase 2.8 Automation

#### 成果

- 自律駆動 OS 完成
- 統合テスト PASS
- Audit Log 完全記録

---

### Phase 3: Logic Injection & Engine Integration（現在）

#### 目的

自律基盤に「物語の法則（ロジック）」を注入する

---

#### Phase 3.1 Logic Injection（完了）

対象：

- src/integrity/consistency_validator.py
- src/integrity/integrity_checker.py

実装内容：

- 因果律検証
- World Rule 適用
- Narrative Consistency チェック

DoD：

- Spec と完全一致
- 不整合データの拒否

---

#### Phase 3.2 Temporal Management（完了）

対象：

- src/core/metadata_manager.py

実装内容：

- JST と作中時間の同期
- 時系列矛盾検知

DoD：

- Timeline 一貫性保証

---

#### Phase 3.3 Engine Skeleton（完了）

対象：

- src/engine/story_engine.py

実装内容：

- Entity → Story Graph 変換
- Timeline 生成
- World Rule による分岐制御

DoD：

- 最小ストーリー構造出力可能
- Integration Test PASS

---

### 🔴 Phase 3.4: Validator Integration（新設・最優先）

#### 目的

Story Engine と ConsistencyValidator の完全統合

#### 背景（未接続ポイント）

- validator.validate() 未使用
- WorkflowContext 未接続
- World Rule の参照経路が不統一

#### 実装内容

- StoryEngine → validator.validate(context, result)
- context._metadata["world_rules"] 経由へ統一
- エラーコード体系導入（例：ERR_WORLD_RULE_001）

#### DoD

- World Rule 判定が Validator に完全移行
- Engine は「生成専用」に分離

---

### 🟡 Phase 3.5: World Rule Execution 強化（拡張）

#### 目的

World Rule の表現力強化

#### 実装内容

- スコープ（global / scene / entity）
- 優先順位解決
- ルール合成

#### DoD

- 複雑な世界設定を表現可能

---

### 🟡 Phase 3.6: Temporal Rule Integration（拡張）

#### 目的

時間ルールの完全統合

#### 未実装要素

- allow_time_reversal
- timeline_linearity 条件分岐

#### 実装内容

- MetadataManager + Validator 連携
- 時間整合性の動的制御

#### DoD

- 時間逆行作品に対応

---

### Phase 3.7 Query Engine

対象：

- src/engine/query_engine.py

実装内容：

- データ検索
- 条件抽出

DoD：

- 任意条件での検索成功

---

### Phase 4: Production Pipeline

#### 目的

実際の小説生成を可能にする

---

#### Phase 4.1 Scene Pipeline

- Scene → Draft → Review → Release

---

#### Phase 4.2 AI Rewrite Loop

- 自動修正
- 一貫性維持

---

#### Phase 4.3 Episode Builder

対象：

- Episode 1（試験作品）

DoD：

- 1話分の完全生成成功

---

### Phase 5: Narrative Operation

#### 目的

人間による連載運用の実現

---

#### Phase 5.1 Authoring Workflow

- Human + AI 協調執筆

---

#### Phase 5.2 Continuous Publishing

- GitHub + Release 連携
- 自動公開

---

#### Phase 5.3 Feedback Loop

- 読者フィードバック → Spec 更新

---

### Phase 6: Governance & Optimization

#### 内容

- Spec 統合
- Core / Kernel 重複排除
- 自動最適化ループ

---

## 5. 重要課題（Critical Path 更新）

1. ConsistencyValidator 統合（Phase 3.4）
2. World Rule Execution 強化（Phase 3.5）
3. Temporal Rule 統合（Phase 3.6）
4. Query Engine 実装（Phase 3.7）
5. Production Pipeline 構築（Phase 4）

---

## 6. Definition of Done（更新版）

すべての機能は以下を満たす必要がある：

1. Spec-Code 一致
2. Integration Test PASS
3. Audit Log 記録
4. GitHub 自動同期

---

## 7. 最終到達目標

NWF は以下を達成する：

- 人間が物語を書く OS
- AI が補助・検証する環境
- 因果律を破らない物語生成
- 世界設定に応じて変化するナラティブ生成

---

## 8. 結論

Phase 2 により「殻」は完成した。

Phase 3.3 により：

**「物語の最小生成能力」が実証された。**

次の段階は：

**ロジック統合（Validator）と世界法則強化による“完全な物語エンジン化”である。**

---

[EOF]