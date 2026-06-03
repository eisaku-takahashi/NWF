Source: docs/project/NWF_Phase_3.5_Validation_Integration_Audit_Work_Plan_v20260604.md
Updated: 2026-06-04T06:04:00+09:00
PIC: Engineer / Codex

# NWF Phase 3.5 Validation Integration Audit Work Plan v20260604

---

## 1. 概要

本ドキュメントは、
NWF v2.0.1 Phase 3.5 Debug Synchronization 完了後に実施する
Validation Integration Audit の作業計画を定義する。

本監査は、以下 Debug Work Plan の完了状態を前提とする。

```text
docs/project/NWF_Phase_3.5_Debug_Work_Plan_v20260524.md
docs/project/NWF_Phase_3.5_Debug_Work_Plan_v20260525.md
```

本計画の目的は、
ValidationResult を中心とした Validation Pipeline 全体について、
Spec / Code / Test の契約整合性を最終確認することである。

対象となる主な経路は以下である。

```text
StoryEngine
↓
ValidatorIntegrationAdapter
↓
ConsistencyValidator
↓
RuleEvaluator / EscalationEvaluator
↓
ValidationResult
```

前提条件:

* rollback 非実施
* validate(entity, context) contract 固定
* ValidationResult strict schema 維持
* Adapter architecture 維持
* Validator Orchestrator architecture 維持
* Severity Monotonicity Rule 維持
* UUID Missing Policy 維持
* Legacy validator compatibility 維持
* StoryDB Interface 統一維持

---

## 2. Cross-Spec Synchronization

本作業計画は以下ドキュメントと同期する。

```text
docs/spec/Spec_Governance/NWF_Spec_Standard_v2.0.1.md
docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
docs/spec/Execution_Spec/NWF_Validation_System_v2.0.1.md
docs/spec/Execution_Spec/NWF_Validator_And_Context_Contract_v2.0.1.md
docs/spec/Execution_Spec/NWF_Validator_Orchestration_Spec_v2.0.1.md
docs/spec/Execution_Spec/NWF_Consistency_Validator_Spec_v2.0.1_Phase_3.5.md
docs/spec/Execution_Spec/NWF_Rule_Engine_Contract_v2.0.1.md
docs/spec/Execution_Spec/NWF_Escalation_Logic_Spec_v2.0.1.md
docs/spec/Core_Spec/NWF_Story_Database_v2.0.1.md
docs/project/NWF_Phase_3.5_Work_Plan_v20260428.md
docs/project/NWF_Phase_3.5_Debug_Work_Plan_v20260525.md
```

優先順位:

1. Debug Work Plan v20260525
2. Execution Spec
3. Core Spec
4. Spec Governance
5. Code comments / legacy notes

---

## 3. 現在確認済み状態

以下は Phase 3.5 Debug Synchronization において完了済みである。

* WorkflowContext callable contract synchronization
* StoryEngine constructor synchronization
* ValidatorIntegrationAdapter argument order synchronization
* ConsistencyValidator execution flow synchronization
* test_validator_critical_only synchronization
* pytest verification via repository .venv

確認済みコマンド:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

確認済み結果:

```text
2 passed
```

注意:

通常の PATH 側 Python では pytest が存在しない可能性があるため、
本計画では原則として repository `.venv` 経由で pytest を実行する。

---

## 4. 監査対象ファイル

### 4.1 Core Validation Files

```text
src/integrity/validation_result.py
src/integrity/validator_integration_adapter.py
src/integrity/consistency_validator.py
src/integrity/escalation_evaluator.py
src/integrity/rule_evaluator.py
```

### 4.2 Engine / Context Files

```text
src/engine/story_engine.py
src/workflow/workflow_context.py
```

### 4.3 Test Files

```text
tests/unit/test_validator_critical_only.py
tests/integration_phase_3_4_validator.py
tests/integration_phase_3_5_world_rules.py
```

### 4.4 Related Work Plan Files

```text
docs/project/NWF_Phase_3.5_Work_Plan_v20260428.md
docs/project/NWF_Phase_3.5_Debug_Work_Plan_v20260524.md
docs/project/NWF_Phase_3.5_Debug_Work_Plan_v20260525.md
```

---

## 5. Audit Work Plan

---

### Step 1. ValidationResult strict schema 最終監査

対象:

```text
src/integrity/validation_result.py
```

監査内容:

* rule_id 必須
* scope 必須
* target_id 必須
* invalid 時 violated_rules 必須
* invalid 時 violated_rules includes rule_id
* ERROR / CRITICAL 時 is_valid=False
* INFO 時 is_valid=True
* is_blocking() が CRITICAL のみ True
* code / error_code alias synchronization
* immutable dataclass 維持

禁止事項:

* strict schema rollback
* invalid result の violated_rules 空許容
* ValidationResult 側への Legacy compatibility 汚染
* severity downgrade

DoD:

* strict schema が Spec と一致
* Adapter 側補完責務との境界が明確
* ValidationResult architecture 維持

---

### Step 2. ValidatorIntegrationAdapter と ValidationResult の完全契約整合確認

対象:

```text
src/integrity/validator_integration_adapter.py
src/integrity/validation_result.py
```

監査内容:

* validator.validate(target, context) 呼び出し維持
* None result は RuntimeError
* empty list result は RuntimeError
* ValidationResult list empty は RuntimeError
* Legacy bool result conversion
* Legacy dict result conversion
* Legacy object result conversion
* rule_id fallback
* scope fallback
* target_id fallback
* violated_rules fallback
* violated_rules includes rule_id
* severity inference
* error_code mapping
* transaction_id / stardate propagation

禁止事項:

* Adapter 内部で results の順序に意味を持たせること
* results[0] 依存
* ValidationResult 本体へ Legacy 吸収責務を移すこと
* validate(context, target) への rollback

DoD:

* Adapter が strict schema を満たす ValidationResult のみ返す
* Legacy compatibility は Adapter 責務として保持
* validate(entity, context) contract と完全一致

---

### Step 3. EscalationEvaluator / RuleEvaluator の I/F 整合確認

対象:

```text
src/integrity/escalation_evaluator.py
src/integrity/rule_evaluator.py
src/integrity/consistency_validator.py
```

監査内容:

RuleEvaluator:

* process(rules, entity, context) I/F
* evaluate(context, entity, rules) legacy compatibility
* empty rules 時の no-op behavior
* deterministic evaluation order
* condition engine delegation
* ValidationResult strict schema compatibility

EscalationEvaluator:

* evaluate(results, context) I/F
* input list mutation 禁止
* ERROR → CRITICAL escalation
* Severity Monotonicity Rule
* threshold behavior
* context optional behavior
* ConsistencyValidator からの呼び出し整合

ConsistencyValidator:

* rule_evaluator.process(rules, entity, context)
* escalation_evaluator.evaluate(results, context)
* escalation routing の結果結合仕様

禁止事項:

* evaluate_escalation など存在しない I/F への依存
* RuleEvaluator 引数順序 mismatch
* EscalationEvaluator による severity downgrade
* input ValidationResult mutation

DoD:

* Evaluator I/F が ConsistencyValidator と一致
* ValidationResult strict schema と矛盾しない
* deterministic behavior が維持される

---

### Step 4. StoryEngine.generate_story_graph() の validator 呼び出し経路確認

対象:

```text
src/engine/story_engine.py
src/integrity/validator_integration_adapter.py
src/integrity/consistency_validator.py
```

監査内容:

* StoryEngine.generate_story_graph() が validator_adapter.execute(context, target) を呼ぶこと
* Adapter 内部で validator.validate(target, context) に変換されること
* ValidationResult empty list が RuntimeError になること
* evaluate_validation_results() が CRITICAL で RuntimeError を発生させること
* result.is_blocking() == True の routing
* Engine が error_code / message に依存して分岐しないこと
* Engine は severity のみを停止判断に使用すること

禁止事項:

* Engine が Validator 内部構造に依存すること
* Engine が ValidationResult を修正すること
* Engine が CRITICAL を suppress すること
* Adapter bypass

DoD:

* StoryEngine → Adapter → Validator の呼び出し経路が contract と一致
* CRITICAL stop routing が維持される
* Engine / Validator 責務分離が維持される

---

### Step 5. Phase 3.5 Work Plan v20260428 の未消化項目確認

対象:

```text
docs/project/NWF_Phase_3.5_Work_Plan_v20260428.md
```

確認項目:

* 全回帰テスト実行
* Deterministic 保証の最終確認
* Validator 仕様の最終明文化
* Spec Governance 準拠の最終統合確認
* Phase 3.6 への接続条件

特に確認するテスト:

```text
tests/integration_phase_3_5_world_rules.py
```

DoD:

* Work Plan v20260428 の未消化項目が一覧化される
* Phase 3.5 完了条件と Phase 3.6 移行条件が分離される
* 次作業が曖昧性なく定義される

---

### Step 6. pytest 明示実行および integration test 確認

実行前提:

```powershell
cd D:\NWF
```

基本実行:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

個別実行候補:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/unit/test_validator_critical_only.py -q
```

```powershell
.\.venv\Scripts\python.exe -m pytest tests/integration_phase_3_4_validator.py -q
```

```powershell
.\.venv\Scripts\python.exe -m pytest tests/integration_phase_3_5_world_rules.py -q
```

確認項目:

* collected test count
* import error
* AttributeError
* TypeError
* strict schema violation
* contract mismatch
* deterministic failure
* RuntimeError routing
* CRITICAL stop routing
* INFO suppression

DoD:

* pytest の実行経路が明確
* 収集された test 件数を記録
* pass / fail / skip を記録
* fail がある場合は Work Plan として次 Debug Plan を分離

---

### Step 7. mypy / ruff / lint 系の有無と実行可否確認

対象:

```text
pyproject.toml
setup.cfg
tox.ini
requirements*.txt
.venv
```

確認内容:

* mypy が利用可能か
* ruff が利用可能か
* flake8 等の lint tool が利用可能か
* 既存設定ファイルが存在するか
* 実行時に project policy と矛盾しないか

実行候補:

```powershell
.\.venv\Scripts\python.exe -m mypy src
```

```powershell
.\.venv\Scripts\python.exe -m ruff check src tests
```

注意:

ツールが未導入の場合、本 Work Plan では依存追加を行わない。
導入が必要な場合は別 Work Plan として扱う。

DoD:

* 利用可能な static analysis tool が明確
* 実行可否が記録される
* 未導入ツールは未導入として記録される
* dependency installation は別判断とする

---

## 6. Execution Order

推奨実行順序:

```text
Step 1
↓
Step 2
↓
Step 3
↓
Step 4
↓
Step 5
↓
Step 6
↓
Step 7
```

理由:

ValidationResult strict schema を最初に確定しない限り、
Adapter / Evaluator / Engine の契約監査結果が安定しないため。

---

## 7. Definition of Done

本 Work Plan の完了条件:

* ValidationResult strict schema 監査完了
* ValidatorIntegrationAdapter 契約監査完了
* RuleEvaluator / EscalationEvaluator I/F 監査完了
* StoryEngine.generate_story_graph() validation route 監査完了
* Phase 3.5 Work Plan v20260428 未消化項目整理完了
* pytest 実行結果記録完了
* integration test 実行可否確認完了
* mypy / ruff / lint 実行可否確認完了
* rollback 非実施
* Validation architecture 維持
* strict schema 維持
* Severity Monotonicity Rule 維持
* UUID Missing Policy 維持

---

## 8. リスクと対策

| リスク | 対策 |
| --- | --- |
| PATH 側 Python に pytest が存在しない | repository `.venv` を使用する |
| integration test が pytest に収集されない | 個別ファイル指定で実行する |
| Legacy compatibility が ValidationResult 本体へ混入する | Adapter 責務として境界確認する |
| Evaluator I/F が複数併存する | ConsistencyValidator 呼び出し経路を SSoT として確認する |
| Work Plan v20260428 と Debug Plan v20260525 の完了条件が混在する | Debug 完了条件と Phase 3.5 最終監査条件を分離する |
| lint tool 未導入 | 依存追加せず、未導入として記録する |

---

## 9. 最終方針

本 Work Plan は、
Phase 3.5 Debug Synchronization 後の Validation Integration Audit を目的とする。

したがって本計画では、
機能追加ではなく、以下を最優先する。

* Contract 整合性確認
* strict schema 確認
* routing 確認
* deterministic behavior 確認
* test execution path 確認
* static analysis availability 確認

本計画の完了により、
Phase 3.5 Validation 周辺の統合整合性を確定し、
Phase 3.6 Temporal Rule Integration へ進むための前提を明確化する。

---

[EOF]
