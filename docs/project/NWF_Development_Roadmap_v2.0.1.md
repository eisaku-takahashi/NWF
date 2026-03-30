Source: docs/project/NWF_Development_Roadmap_v2.0.1.md
Updated: 2026-03-31T21:00:00+09:00
PIC: Architect / ChatGPT

# NWF Development Roadmap v2.0.1

---

## 1. Overview

NWF (Narrative Workflow Framework) は単なる執筆支援ツールではなく、
**物語生成・管理・最適化を行う Story OS（物語生成基盤）**として設計される。

従来の物語制作は以下のような属人的プロセスで行われてきた。

* アイデア
* プロット
* 執筆
* 推敲
* 公開

NWFではこれを **データ・ロジック・パイプラインとして再定義**する。

### Story = Data + Logic + Pipeline

| 要素           | 内容                                             |
| ------------ | ---------------------------------------------- |
| Data         | Character / World / Thread / Scene / Emotion 等 |
| Logic        | Story Engine / Thread Engine / Validation      |
| Pipeline     | Episode → Scene → Draft → Review → Release     |
| Governance   | Integrity / Spec / Version 管理                  |
| Optimization | Feedback → Spec Update                         |

NWFの開発ロードマップは、
**OS 開発と同じフェーズ構造**で進行する。

### 開発循環構造

Spec → Engine → Workflow → Production → Optimization → Spec

これは一度作って終わりではなく、
**Recursive Story Generation System**として継続的に進化する。

---

## 2. NWF Architecture Overview

NWF Story OS は以下の5層構造で構成される。

| Layer      | 内容                                         |
| ---------- | ------------------------------------------ |
| Spec       | JSON Schema / Data Model / Rules           |
| Engine     | Thread Engine / Validation / Generator     |
| Workflow   | Author Workflow / CLI / Automation         |
| Production | Episode / Scene / Draft / Release          |
| Governance | Integrity / Logging / Audit / Optimization |

### モジュール構成

| Module    | 役割                              |
| --------- | ------------------------------- |
| Core      | Schema / State Machine / Config |
| Engine    | Story Logic / Generation        |
| IO        | File / JSON / Import Export     |
| Interface | CLI / Prompt / UI               |
| Governor  | Integrity / Audit / Version     |

### Module Boundary

| Module    | Responsibility                       |
| --------- | ------------------------------------ |
| Core      | Data model / schema / state          |
| Engine    | Story generation logic               |
| IO        | File operations                      |
| Interface | User interaction                     |
| Governor  | Validation / Audit / Release control |

モジュール境界を明確にすることで、
**Spec変更とEngine変更を分離**できる。

---

## 3. Development Phases

NWF Story OS 開発は以下の Phase で進行する。

| Phase   | 名称                        | 内容                              |
| ------- | ------------------------- | ------------------------------- |
| Phase 1 | Spec Foundation           | Schema / Data Model             |
| Phase 2 | Core Engine               | Thread Engine / Validation      |
| Phase 3 | Workflow                  | Author Workflow / CLI           |
| Phase 4 | Production Pipeline       | Story Production System         |
| Phase 5 | Governance / Optimization | Logging / Audit / Feedback Loop |

### Phase Flow

```
Phase1 → Phase2 → Phase3 → Phase4 → Phase5
                 ↑                     ↓
                 ← Recursive Optimization ←
```

---

## 4. Phase Definition of Done

各 Phase の完了条件（Definition of Done）を明確にする。

| Phase   | Definition of Done                            |
| ------- | --------------------------------------------- |
| Phase 1 | 全 Schema 定義完了、JSON Validation 成功              |
| Phase 2 | Thread Engine が Thread → Scene を生成可能          |
| Phase 3 | Author Workflow が CLI で実行可能                   |
| Phase 4 | Episode → Scene → Draft → Release Pipeline 稼働 |
| Phase 5 | Logging / Audit / Feedback Loop 稼働            |

### Phase 完了条件詳細

#### Phase 1

* Character Schema
* World Schema
* Thread Schema
* Scene Schema
* Emotion Schema
* Validation Script

#### Phase 2

* Thread Engine
* Scene Generator
* Continuity Check
* State Machine

#### Phase 3

* CLI
* Project Init
* Draft Generate
* Validation Run
* Build Episode

#### Phase 4

* Episode Pipeline
* Draft → Review → Release
* Version 管理
* Export

#### Phase 5

* Audit Logs
* Metrics
* Feedback
* Spec Update Loop

---

## 5. MVP Definition

### NWF-Core MVP

MVP（Minimum Viable Product）は
**Thread → Scene → Draft を生成できる最小構成**。

| Component  | MVP                        |
| ---------- | -------------------------- |
| Schema     | Character / Thread / Scene |
| Engine     | Thread Engine              |
| Workflow   | Draft Generator            |
| Validation | JSON Schema Validation     |
| Output     | Draft Markdown             |
| Logging    | Basic Logs                 |

### MVP Pipeline

```
Thread JSON
   ↓
Thread Engine
   ↓
Scene List
   ↓
Draft Generator
   ↓
Draft Markdown
```

MVP の目的は **Story Engine が動くこと**であり、
Production / Governance は MVP 以降に追加する。

---

## 6. Dependency Graph / Implementation Order

実装順序は Spec First に従う。

### Dependency Graph

| Order | Module              |
| ----- | ------------------- |
| 1     | Schema              |
| 2     | Validation          |
| 3     | State Machine       |
| 4     | Thread Engine       |
| 5     | Scene Generator     |
| 6     | Draft Generator     |
| 7     | CLI                 |
| 8     | Production Pipeline |
| 9     | Logging             |
| 10    | Audit               |
| 11    | Optimization Loop   |

### Implementation Order Diagram

```
Schema
  ↓
Validation
  ↓
State Machine
  ↓
Thread Engine
  ↓
Scene Generator
  ↓
Draft Generator
  ↓
CLI / Workflow
  ↓
Production Pipeline
  ↓
Logging / Audit
  ↓
Optimization Loop
```

---

## 7. Directory and Module Structure

### Directory Structure

```
NWF/
 ├── docs/
 ├── specs/
 ├── engine/
 ├── workflow/
 ├── production/
 ├── governor/
 ├── scripts/
 ├── projects/
 ├── logs/
 └── config/
```

### Phase / Directory / Script 対応表

| Phase   | Directory  | Script             |
| ------- | ---------- | ------------------ |
| Phase 1 | specs      | validate_schema.py |
| Phase 2 | engine     | thread_engine.py   |
| Phase 3 | workflow   | cli.py             |
| Phase 4 | production | build_episode.py   |
| Phase 5 | governor   | audit_log.py       |

---

## 8. Data State Machine

NWF ではすべてのデータは状態を持つ。

### State Machine

| State     | 意味        |
| --------- | --------- |
| Draft     | 作成中       |
| Validated | Schema OK |
| Approved  | 人間レビュー OK |
| Committed | 本採用       |
| Archived  | 保管        |

### State Transition

```
Draft → Validated → Approved → Committed → Archived
```

Human-in-the-Loop Governance により
**Approved は必ず人間が行う。**

---

## 9. Project Lifecycle

### OS 開発ライフサイクル

| Stage        | 内容               |
| ------------ | ---------------- |
| Concept      | 設計思想             |
| Spec         | Schema / Rules   |
| Engine       | Logic            |
| Workflow     | Author Tools     |
| Production   | Story Production |
| Optimization | 改良               |
| Next Version | Spec Update      |

### 作品制作ライフサイクル

| Stage     | 内容    |
| --------- | ----- |
| Idea      | コンセプト |
| World     | 世界設定  |
| Character | 登場人物  |
| Thread    | 物語構造  |
| Scene     | シーン   |
| Draft     | 下書き   |
| Review    | 推敲    |
| Release   | 公開    |
| Feedback  | 反応    |
| Improve   | 改良    |

---

## 10. Testing Strategy

### テスト戦略

| Test Type        | 内容               |
| ---------------- | ---------------- |
| Schema Test      | JSON Schema      |
| Logic Test       | Engine           |
| Pipeline Test    | Episode Pipeline |
| Prompt Test      | LLM Prompt       |
| Integration Test | End-to-End       |

### テストレイヤ

```
Schema Test
   ↓
Engine Test
   ↓
Pipeline Test
   ↓
Integration Test
```

---

## 11. Logging and Audit Policy

### Logging Policy

| Log            | 内容         |
| -------------- | ---------- |
| Engine Log     | 生成ログ       |
| Validation Log | Schema     |
| Pipeline Log   | Production |
| Audit Log      | 承認・変更      |
| Error Log      | エラー        |

### Log Rotation

| Policy  | 内容      |
| ------- | ------- |
| Daily   | 通常ログ    |
| Weekly  | Audit   |
| Monthly | Archive |

監査ログは削除不可。

---

## 12. Config Hierarchy

設定は階層構造を持つ。

| Level   | Config       |
| ------- | ------------ |
| System  | NWF 全体       |
| Model   | LLM / Engine |
| Project | 作品設定         |
| Episode | 個別設定         |

### Hierarchy

```
system.yaml
   ↓
model.yaml
   ↓
project.yaml
   ↓
episode.yaml
```

---

## 13. Developer Workflow

### Spec-First Workflow

```
1. Spec 作成
2. Schema 作成
3. Validation 作成
4. Engine 実装
5. Test
6. CLI
7. Release
```

### 開発フロー

| Step       | 内容         |
| ---------- | ---------- |
| Spec       | Data Model |
| Engine     | Logic      |
| Test       | Validation |
| Workflow   | CLI        |
| Release    | Version    |
| Production | Story      |
| Feedback   | Improve    |

---

## 14. Release and Versioning Strategy

### Version 種類

| Version            | 内容             |
| ------------------ | -------------- |
| Spec Version       | Schema         |
| Engine Version     | Engine         |
| Workflow Version   | CLI            |
| Production Version | Story Pipeline |
| OS Version         | NWF 全体         |

### Release Flow

```
Spec Freeze
   ↓
Engine Release
   ↓
Workflow Release
   ↓
Production Release
   ↓
Version Tag
```

---

## 15. Story Production Pipeline

### Pipeline

```
World
Character
Thread
Scene
Emotion
   ↓
Episode Plan
   ↓
Scene Draft
   ↓
Draft
   ↓
Review
   ↓
Release
```

### Episode Production Table

| Step    | Output     |
| ------- | ---------- |
| Thread  | Structure  |
| Scene   | Scene List |
| Draft   | Text       |
| Review  | Edited     |
| Release | Published  |

---

## 16. Recursive Optimization Loop

NWF は自己改善ループを持つ。

### Optimization Loop

```
Story Production
      ↓
Metrics / Feedback
      ↓
Problem Detection
      ↓
Spec Update
      ↓
Engine Update
      ↓
Next Production
```

### Integrity Driven Development

重要な思想：

* Integrity First
* Spec First
* Human Approval
* Audit Trail
* Version Control
* Recursive Improvement

---

## 17. Final Roadmap Summary

### NWF Story OS 開発全体図

```
Spec
 ↓
Engine
 ↓
Workflow
 ↓
Production
 ↓
Governance
 ↓
Optimization
 ↓
Spec Update
```

### NWF 開発思想まとめ

| Principle                       | 説明       |
| ------------------------------- | -------- |
| NWF は執筆ツールではない                  | Story OS |
| Spec First                      | 仕様が先     |
| Human in Loop                   | 人間承認     |
| Recursive                       | 再帰改善     |
| Integrity                       | 一貫性      |
| Story = Data + Logic + Pipeline | 物語の再定義   |
| OS Development Model            | OS開発型    |
| Version Governance              | 版管理      |

NWF は物語を書くためのツールではなく、
**物語を生成・管理・進化させる OS である。**

このロードマップは
**NWF Story OS を構築するための最上位設計文書である。**

---

[EOF]