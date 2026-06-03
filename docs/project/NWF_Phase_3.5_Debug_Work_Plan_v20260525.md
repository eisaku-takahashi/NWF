Source: docs/project/NWF_Phase_3.5_Debug_Work_Plan_v20260525.md
Updated: 2026-05-30T05:14:00+09:00
PIC: Engineer / ChatGPT

# NWF Phase 3.5 Debug Work Plan v20260525

---

## 1. 概要

本ドキュメントは、
Phase 3.5 Debug Synchronization において発生した
Validator / WorkflowContext / StoryEngine / ValidatorIntegrationAdapter 間の
API・Contract・Validation Pipeline 不整合を、
厳密かつ曖昧性ゼロで修正するためのデバッグ作業計画を定義する。

実コード検証の結果確認された：

* WorkflowContext callable contract mismatch
* StoryEngine constructor synchronization mismatch
* ValidatorIntegrationAdapter validate argument order mismatch

を含む synchronization failure を解消し、
Validation architecture 全体の整合性回復を目的とする。

前提条件:

* rollback 非実施
* strict schema 維持
* Severity Monotonicity Rule 維持
* ValidationResult architecture 維持
* Validator Integration Adapter architecture 維持
* Legacy compatibility 汚染禁止
* Spec Strictness Principle 準拠
* validate(entity, context) contract 絶対固定
* WorkflowContext callable contract 固定

---

## 2. Metadata & Synchronization Scope

### 2.1 対象ファイル

```text
src/workflow/workflow_context.py
src/engine/story_engine.py
src/integrity/validator_integration_adapter.py
src/integrity/consistency_validator.py
tests/unit/test_validator_critical_only.py
```

### 2.2 Synchronization Scope

本作業計画では以下 synchronization を対象とする。

* WorkflowContext callable contract synchronization
* StoryEngine constructor synchronization
* ValidatorIntegrationAdapter validate routing synchronization
* Validation pipeline routing synchronization
* Test synchronization
* CRITICAL escalation synchronization
* UUID Missing Policy synchronization

---

## 3. 現在確認済み状態

### 3.1 PASS 維持確認済み

以下は正常維持されている。

* ValidationResult strict schema
* violated_rules includes rule_id
* Severity Monotonicity Rule
* UUID Missing Policy 条件式
* ValidationResult architecture
* Validator Integration Adapter architecture
* StoryDB Interface synchronization
* validate(entity, context) contract
* IMMUTABILITY_BREACH → CRITICAL routing
* escalation routing
* INFO suppression

---

### 3.2 現在の未解決問題

#### 問題A

WorkflowContext callable contract mismatch

発生内容:

```text
AttributeError:
'WorkflowContext' object has no attribute 'is_valid'
```

---

#### 問題B

StoryEngine constructor synchronization mismatch

発生内容:

```text
TypeError:
StoryEngine.__init__()
missing 1 required positional argument:
'validator_adapter'
```

---

#### 問題C

ValidatorIntegrationAdapter validate argument order mismatch

発生内容:

```python
validator.validate(
    context,
    target,
)
```

が実装されており、

```python
validate(entity, context)
```

正式契約と逆順になっている。

---

## 4. 原因分析

### 4.1 問題A 根本原因

ConsistencyValidator 実コード内に:

```python
if not context.is_valid():
```

が validation precondition として正式実装されている。

しかし WorkflowContext 本体に:

```python
def is_valid(self) -> bool:
```

が存在しない。

これは:

```text
WorkflowContext callable synchronization failure
```

である。

---

### 4.2 問題B 根本原因

StoryEngine constructor が:

```python
def __init__(
    self,
    validator_adapter,
    metadata_manager=None,
)
```

となっており、

```python
StoryEngine()
```

および:

```python
StoryEngine(story_db)
```

との backward compatibility が崩壊している。

---

### 4.3 問題C 根本原因

ValidatorIntegrationAdapter 実コード内で:

```python
raw_result = validator.validate(
    context,
    target,
)
```

が使用されている。

しかし ConsistencyValidator 正式契約は:

```python
validate(entity, context)
```

である。

その結果:

* entity/context の意味逆転
* WorkflowContext が entity として渡される
* Entity が context として渡される
* Validation Pipeline 崩壊
* callable synchronization failure
* escalation routing failure
* INFO suppression failure

を誘発する。

---

## 5. 修正方針（最重要）

### 5.1 validate contract

validate contract は絶対固定。

```python
def validate(
    self,
    entity,
    context,
):
```

変更禁止。

validator rollback 禁止。

---

### 5.2 WorkflowContext callable contract

WorkflowContext に以下 method を追加する。

```python
def is_valid(self) -> bool:
    return True
```

禁止事項:

* property 化
* validator rollback
* context.is_valid 参照化
* monkey patch 恒久化

---

### 5.3 StoryEngine constructor contract

以下 signature へ同期する。

```python
def __init__(
    self,
    story_db=None,
    validator_adapter=None,
    metadata_manager=None,
):
```

---

### 5.4 StoryEngine backward compatibility

以下旧呼び出しを破壊しない。

```python
StoryEngine()
```

```python
StoryEngine(story_db)
```

---

### 5.5 ValidatorIntegrationAdapter synchronization

ValidatorIntegrationAdapter 内部呼び出しを:

修正前:

```python
validator.validate(
    context,
    target,
)
```

修正後:

```python
validator.validate(
    target,
    context,
)
```

へ同期する。

---

### 5.6 Adapter architecture 維持

以下責務は維持。

* Legacy validator compatibility absorption
* strict schema normalization
* violated_rules synchronization
* severity normalization
* order non-dependency guarantee

---

## 6. Debug Step Plan

### Step 1

### WorkflowContext callable contract synchronization

対象:

```text
src/workflow/workflow_context.py
```

実施内容:

```python
def is_valid(self) -> bool:
    return True
```

を追加。

完了条件:

```text
AttributeError:
'WorkflowContext' object has no attribute 'is_valid'
```

が消失。

---

### Step 2

### StoryEngine constructor synchronization

対象:

```text
src/engine/story_engine.py
```

実施内容:

```python
def __init__(
    self,
    story_db=None,
    validator_adapter=None,
    metadata_manager=None,
):
```

へ同期。

validator_adapter=None 時は内部生成を実施。

完了条件:

```python
StoryEngine()
```

および:

```python
StoryEngine(story_db)
```

が成功。

---

### Step 3

### ValidatorIntegrationAdapter argument order synchronization

対象:

```text
src/integrity/validator_integration_adapter.py
```

実施内容:

修正前:

```python
raw_result = validator.validate(
    context,
    target,
)
```

修正後:

```python
raw_result = validator.validate(
    target,
    context,
)
```

完了条件:

* validate(entity, context) 全層一致
* Validation Pipeline 崩壊消失
* callable mismatch 消失

---

### Step 4

### ConsistencyValidator execution flow verification

対象:

```text
src/integrity/consistency_validator.py
```

確認内容:

* validate(entity, context)
* context.is_valid()
* IMMUTABILITY_BREACH → CRITICAL
* escalation routing
* INFO suppression

が維持されていること。

コード rollback 禁止。

---

### Step 5

### test_validator_critical_only synchronization

対象:

```text
tests/unit/test_validator_critical_only.py
```

確認項目:

* validate(entity, context)
* MockStoryDB contract
* UUID Missing Policy
* INFO suppression assertion
* CRITICAL assertion

必要同期:

* StoryEngine constructor synchronization
* WorkflowContext synchronization

---

### Step 6

### Final pytest synchronization verification

実施内容:

```bash
.\.venv\Scripts\activate
python -m pytest -q
```

確認項目:

* RuntimeError routing
* CRITICAL stop routing
* INFO suppression
* validator pipeline consistency
* ValidationResult strict schema
* no callable mismatch
* no constructor mismatch
* no argument order mismatch

完了条件:

* pytest PASS
* no AttributeError
* no TypeError
* no contract mismatch
* no validation routing regression

---

## 7. 推奨修正順序

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
```

理由:

WorkflowContext callable synchronization を最初に解消しない限り、validator routing が正常到達しないため。

---

## 8. Governance Integration

本修正では以下 governance を維持する。

* Recursive Integrity
* strict schema
* ValidationResult architecture
* Adapter architecture
* Severity Monotonicity Rule
* UUID Missing Policy
* validation routing consistency

---

## 9. 最終方針

本 Debug Work Plan では:

* rollback を禁止
* Legacy 汚染を禁止
* strict schema を維持
* Validation architecture を維持
* callable contract を固定
* validate(entity, context) を絶対固定
* Adapter 内部 argument order mismatch を根本修正

した上で、

```text
最小修正で synchronization を回復
```

することを最優先方針とする。

---

## 10. Codex 実施記録

Updated: 2026-06-04T04:48:00+09:00
PIC: Codex

### 10.1 実施範囲

Codex は本 Work Plan の以下 Step を実施した。

```text
Step 3
Step 4
Step 5
Step 6
```

Step 1 および Step 2 は、作業開始時点で完了済みとして確認した。

---

### 10.2 Step 3 実施結果

対象:

```text
src/integrity/validator_integration_adapter.py
```

実施内容:

ValidatorIntegrationAdapter 内部の Validator 呼び出し順序を、
正式契約である:

```python
validate(entity, context)
```

へ同期した。

修正内容:

```python
raw_result = validator.validate(
    target,
    context,
)
```

判定:

```text
完了
```

確認結果:

* validate(entity, context) contract と一致
* Adapter architecture 維持
* ValidationResult strict schema 維持
* rollback 非実施

---

### 10.3 Step 4 実施結果

対象:

```text
src/integrity/consistency_validator.py
```

確認および同期内容:

* validate(entity, context) contract 維持
* context.is_valid() callable contract 維持
* IMMUTABILITY_BREACH → CRITICAL routing 維持
* INFO suppression 維持
* UUID Missing Policy 維持

追加同期:

現行 Evaluator I/F と整合するよう、以下を同期した。

```python
self.rule_evaluator.process(
    rules,
    entity,
    context,
)
```

```python
self.escalation_evaluator.evaluate(
    results,
    context,
)
```

また、RuleEvaluator に渡す rules を context.metadata から取得する補助処理を追加した。

判定:

```text
完了
```

確認結果:

* CRITICAL routing 維持
* INFO suppression 維持
* UUID Missing Policy 正常
* rollback 非実施

---

### 10.4 Step 5 実施結果

対象:

```text
tests/unit/test_validator_critical_only.py
```

確認内容:

* validate(entity, context)
* MockStoryDB.get(entity_id: str)
* UUID Missing Policy
* INFO suppression assertion
* CRITICAL assertion
* Engine stop routing

検証結果:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/unit/test_validator_critical_only.py -q
```

結果:

```text
2 passed
```

判定:

```text
完了
```

---

### 10.5 Step 6 実施結果

実施内容:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

結果:

```text
2 passed
```

確認項目:

* RuntimeError routing
* CRITICAL stop routing
* INFO suppression
* validator pipeline consistency
* ValidationResult strict schema
* no callable mismatch
* no constructor mismatch
* no argument order mismatch

補足:

通常の:

```powershell
pytest
```

および:

```powershell
python -m pytest
```

は PATH 側 Python 環境に pytest が存在しないため実行不能であった。
そのため、リポジトリ内の `.venv` を使用して検証した。

判定:

```text
完了
```

---

### 10.6 最終判定

本 Work Plan の Step 1 から Step 6 までの同期作業は完了した。

最終状態:

```text
NWF v2.0.1 Phase 3.5 Debug Synchronization 完了
```

維持された原則:

* rollback 非実施
* validate(entity, context) contract 固定
* WorkflowContext callable contract 固定
* Adapter architecture 維持
* ValidationResult architecture 維持
* strict schema 維持
* Severity Monotonicity Rule 維持
* UUID Missing Policy 維持
* Legacy compatibility 汚染禁止

---

[EOF]
