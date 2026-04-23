Source: docs/project/NWF_Development_Roadmap_v2.0.1.md
Updated: 2026-04-23T09:34:00+09:00  ← ★更新（Phase 3.4 完了反映）
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

## 2. 現状整理（2026-04-23 時点）

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

### ★追記：Phase 3.4 完了による到達点（今回追加）

（※既存構造は削除せず、拡張として追記）

- StoryEngine と ConsistencyValidator の完全統合完了
- CRITICAL エラー発生時の Engine による即時停止（フェイルセーフ）の確立
- Validation Pipeline（Validator → Adapter → Engine）の非破壊・単方向伝播の保証
- Engine が「最終意思決定者（Gatekeeper）」として確立

**重要結論（拡張）：**

> NWF は「安全装置（Validation Pipeline）を備えた完全な物語エンジン」へと進化完了。  
> データの矛盾や因果律崩壊を未然に防ぐ自律防衛機構が実稼働に入った。

---

### 2.3 現在のシステム状態

| レイヤ | 状態 |
|--------|------|
| Kernel | 完全稼働 |
| Infrastructure | 完成 |
| Autonomous | 完全稼働 |
| Agency | 稼働中 |
| Application | Engine（Validator統合完了） |

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

### Phase 3.4: Validator Integration（完了）

#### 実装内容・成果

- StoryEngine に `evaluate_validation_results()` を実装
- Validator → Adapter → Engine の完全接続確立
- CRITICAL 伝播時の即時停止（RuntimeError）を保証
- Monotonicity Rule の完全達成
- ValidationResult 非破壊性の保証

#### 修正理由（旧仕様との差分）

- 旧設計では Engine が Validator に依存していなかった
- 判定責務が分散していた（設計違反）
- → Engine に停止権限を集中（NWF_Error_Model 準拠）

---

### 🟡 Phase 3.5: World Rule Execution 強化（次フェーズ）

※重要設計方針：

- phase 3.5 の実質的設計前に Validator の分割設計を行う
- Validatorは「評価オーケストレーター」であり合成だけをする。ロジックは以下に具体的に示す通りに Evaluator にのみ分割して存在する
  - RuleEvaluator（World）: World Rule の評価ロジック（純関数）
  - TemporalEvaluator: Temporal Rule の評価ロジック（純関数）
  - EscalationEvaluator: Escalation Rule の評価ロジック（純関数）
- Validator の　Rule Scope / Priority 対応
- World Rule の評価ロジックは Validator に集約する
- Engine は評価結果を「解釈せず」最終判断のみ行う
- Engine は ValidationResult の内容（message / error_code）に依存した分岐を行ってはならない
- Engine が参照してよいのは severity のみとする
- Engine を分離（Phase 3.4 での設計を壊さずに拡張）: 
  StoryEngine
   ├─ GenerationStrategy（生成ロジック）
   └─ EvaluationGate（Phase 3.4 で実装）
- Rule 判定の二重実装を禁止（DRY + 責務分離）
- Validator は Engine の状態（実行結果・生成物）に依存してはならない

#### Phase 3.5 準備

##### 1. Validator分割のインターフェース定義

```python
class RuleEvaluator:
    def evaluate(context, entity) -> List[ValidationResult]

class TemporalEvaluator:
    def evaluate(context, entity) -> List[ValidationResult]

class EscalationEvaluator:
    def evaluate(results) -> List[ValidationResult]
```

#### 2. ValidationResultの拡張準備

```python
trace_id: str
span_id: str
source: str  # validator / temporal / escalation
```

##### 3. Ruleデータ構造（最初の1タスク）

Rule Scope のデータ構造定義

```python
{
    "rule_id": "...",
    "scope": "global | scene | entity",
    "priority": int,
    "condition": ...,
    "action": ...
}
```

#### 目的

World Rule の表現力と適用精度を拡張する

#### 対象

- src/integrity/consistency_validator.py
- src/workflow/workflow_context.py
- src/engine/story_engine.py

#### 内容

- Rule スコープ導入（global / scene / entity）
- Rule 優先順位（priority）解決
- Rule 合成（multiple rule resolution）
- Context.metadata 経由での統一参照

#### DoD

- 複数ルール競合時の決定論的解決
- Validator による完全検証
- Integration Test PASS

---

### 🟡 Phase 3.6: Temporal Rule Integration

- Validater の時間逆行対応
- Temporal Rule は Validation Pipeline に統合される
- 時間矛盾は ValidationResult として返却される
- Engine は時間矛盾を「直接判定しない」
- 時間の単調性（monotonic progression）はデフォルトとする
- allow_time_reversal=True の場合のみ例外的に非単調を許可

#### 目的

時間軸の制御と非線形ナラティブ対応

#### 対象

- src/core/metadata_manager.py
- src/integrity/consistency_validator.py

#### 内容

- allow_time_reversal の実装
- timeline_linearity 条件分岐
- 時間矛盾の動的検出

#### DoD

- 時間逆行シナリオが生成可能
- 時系列矛盾が CRITICAL で検出される

---

### Phase 3.7 Query Engine

#### 対象

- src/engine/query_engine.py

#### 内容

- Entity 検索
- 条件抽出
- Graph クエリ

#### DoD

- 任意条件検索成功
- パフォーマンス要件クリア

---

### 🟡 Phase 3.8: Observability & Error Escalation（新設）

※重要制約：

- Validator のログ対応（ログ地獄）
- ログ対応として phase 3.8 の実質的設計前にログポリシーと保存戦略を策定する
  - ログポリシー: 
    - CRITICAL → フルログ
    - ERROR    → サマリ + 件数
    - WARNING  → 集約
    - INFO     → オプション
  - 保存戦略: 
    - hot log   : 直近N件
    - cold log  : 圧縮保存
- エラー昇格（ERROR → CRITICAL）は許可される
- Escalationは独立レイヤーに固定
  - Validator → EscalationManager → Engine
- Engine は昇格ロジックを持たない
- エラー降格（CRITICAL → ERROR）は禁止（Monotonicity Rule）
- Trace ID は2層にする（分散トレース的構造）: 
  - trace_id      = workflow単位
  - span_id       = 処理単位（validator / engine / etc）
- ValidationResult は必ず Trace ID を継承する
- ERROR の扱い: 
  - カウント単位（entity / context / global）
  - 時間窓（1 transaction / sliding window）
  - 閾値（例: 3回）

#### 目的

Validation と Engine の可観測性と制御強化

#### 対象

- src/core/audit_logger.py
- src/integrity/validation_result.py
- src/engine/story_engine.py

#### 内容

- ValidationResult の JSON ログ化
- Entity ID / timestamp / rule を記録
- ERROR 蓄積による CRITICAL 昇格
- Trace ID による分散トレース

#### DoD

- 全 ValidationResult が永続化される
- エラー昇格テスト PASS
- Audit Log から完全再現可能

---

### Phase 4: Production Pipeline

#### 目的

実際の小説生成を可能にする

#### 対象

- Scene Pipeline
- Episode Builder

#### 内容

- Draft → Review → Release
- AI Rewrite Loop

#### DoD

- 1話生成成功

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

### 🔴 完了済
1. ConsistencyValidator 統合（Phase 3.4）

### ✅ 今後の課題

1. World Rule Execution 強化（Phase 3.5）※現在地
   - 理由：物語分岐の本体ロジックであり、Engineの出力品質を決定するため
2. Temporal Rule 統合（Phase 3.6）
   - 理由：時間軸の制御と非線形ナラティブ対応
3. Query Engine 実装（Phase 3.7）
   - 理由：Entity検索・条件抽出・Graphクエリ
4. Observability & Error Escalation（Phase 3.8）
   - 理由：ValidationとEngineの可観測性と制御強化
5. Production Pipeline 構築（Phase 4）
   - 理由：実際の小説生成を可能にする

### 各課題の順序依存

1. Phase 3.5（World Rule）
   ↓
2. Phase 3.6（Temporal）
   ↓
3. Phase 3.7（Query）
   ↓
4. Phase 3.8（Observability）

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

## 8. 結論（更新）

### 🔴 修正前（保持）

Phase 2 により「殻」は完成した。  
Phase 3.3 により「最小生成能力」が実証された。

---

### ✅ 修正後（拡張）

Phase 2 により「自律駆動の殻」は完成した。  
Phase 3.3 により「物語の最小生成能力」が実証され、  
Phase 3.4 により「因果律を担保する絶対的な安全装置（Validator統合）」が組み込まれた。
さらに、Engine は「生成器」ではなく「意思決定中枢」として再定義された。

次の段階は：

**確立された堅牢な基盤の上で、複雑な「世界法則（World Rule）」と「時間操作（Temporal）」を解き放つことである。**

---

[EOF]