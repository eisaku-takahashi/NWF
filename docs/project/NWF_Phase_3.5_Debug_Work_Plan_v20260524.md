Source: docs/project/NWF_Phase_3.5_Debug_Work_Plan_v20260524.md
Updated: 2026-05-24T00:53:00+09:00
PIC: Engineer / ChatGPT

# NWF Phase 3.5 Debug Work Plan v20260524

---

## 1. 概要

本ドキュメントは：

```text
tests/unit/test_validator_critical_only.py
```

再検証時に追加で確認された：

* ConsistencyValidator.validate() call synchronization mismatch
* validate(entity, context) 引数順序不一致
* DummyEntity.is_valid callable contract mismatch

について、

* Validation architecture 維持
* strict schema 維持
* Severity Monotonicity 維持
* rollback 非実施
* validator_integration_adapter synchronization 維持
* Legacy compatibility 汚染回避

を前提として実施する
追加 Debug / Synchronization Work Plan である。

本計画は：

* docs/project/NWF_Phase_3.5_Debug_Work_Plan_v20260520.md
* docs/spec/Spec_Governance/NWF_Spec_Standard_v2.0.1.md
* docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
* docs/spec/Execution_Spec/NWF_Validation_System_v2.0.1.md
* docs/spec/Execution_Spec/NWF_Validator_Orchestration_Spec_v2.0.1.md

を Single Source of Truth とする。

---

## 2. 追加確認された障害

---

## 2.1 ConsistencyValidator.validate() call synchronization mismatch

発生箇所：

```text
tests/unit/test_validator_critical_only.py
```

---

### 発生内容

pytest 実行時：

```text
TypeError: 'bool' object is not callable
```

発生箇所：

```python
if not context.is_valid():
```

```text
src/integrity/consistency_validator.py:218
```

---

### 原因分析

現在の：

```python
ConsistencyValidator.validate()
```

の正式 signature：

```python
def validate(
    self,
    entity: Any,
    context: Any
) -> List[ValidationResult]:
```

つまり：

```python
validate(entity, context)
```

順序である。

しかし test code 側では：

```python
results = validator.validate(context, current_entity)
```

として呼び出されている。

その結果：

| validate 引数 | 実際に渡された値        |
| ----------- | --------------- |
| entity      | WorkflowContext |
| context     | DummyEntity     |

となる。

---

### 直接原因

```python
context
```

へ：

```python
DummyEntity
```

が渡されているため：

```python
context.is_valid()
```

実行時、

```python
DummyEntity.is_valid
```

（bool属性）

を callable として実行し：

```text
TypeError: 'bool' object is not callable
```

が発生。

---

### 状態評価

これは：

```text
validate(entity, context)
call synchronization mismatch
```

であり、

```text
Validation architecture failure
```

でも：

```text
UUID Missing Policy failure
```

でも：

```text
IMMUTABILITY_BREACH routing failure
```

でもない。

現在の failure は：

```text
test-side validate call order mismatch
```

に限定される。

---

## 2.2 integration_phase_3_4_validator.py 状態確認

以下 integration tests は：

```text
PASS
```

確認済み：

* adapter_legacy_conversion
* critical_flow
* error_flow
* multiple_validators
* normal_flow
* stardate_precision
* warning_flow

---

### 状態評価

したがって：

```text
validator_integration_adapter.py
```

および：

```text
ValidationResult strict schema synchronization
```

は維持されている。

---

## 3. 基本方針

---

## 3.1 rollback は実施しない

以下を維持：

* strict ValidationResult schema
* Severity Monotonicity
* validation orchestration
* DI architecture
* validator routing

---

## 3.2 validate() signature は変更しない

以下：

```python
validate(entity, context)
```

を正式 contract とする。

validator 側への backward compatibility rollback は実施しない。

---

## 3.3 test synchronization を継続

test code を：

```text
現行 validator contract
```

へ同期する。

---

## 3.4 Entity callable contract を維持

以下仕様：

```python
context.is_valid()
```

は callable contract として維持。

validator 側を：

```python
context.is_valid
```

へ rollback しない。

---

## 4. Debug Work Plan

---

## Step 1. validate() call order synchronization

対象：

```text
tests/unit/test_validator_critical_only.py
```

---

### 修正内容

修正前：

```python
results = validator.validate(context, current_entity)
```

修正後：

```python
results = validator.validate(current_entity, context)
```

---

### 修正対象箇所

以下 2 箇所：

#### 1.

```python
test_immutability_breach_generates_critical()
```

#### 2.

```python
test_uuid_missing_policy_does_not_generate_critical()
```

---

### 理由

正式 validator contract：

```python
validate(entity, context)
```

へ test code を同期するため。

---

### DoD

* TypeError 消滅
* context contract 正常化
* validation pipeline 継続
* UUID comparison logic 到達

---

## Step 2. UUID Missing Policy 再検証

対象：

```text
src/integrity/consistency_validator.py
```

---

### 検証内容

以下条件：

```python
previous_uuid is None
current_uuid is None
```

の場合：

```text
CRITICAL violation 非生成
```

を確認。

---

### 正式仕様

```python
if (
    previous_uuid is not None
    and current_uuid is not None
    and str(previous_uuid) != str(current_uuid)
):
```

---

### DoD

* None 同士比較で violation 非発生
* false positive ゼロ
* UUID Missing Policy 完全準拠

---

## Step 3. IMMUTABILITY_BREACH routing 再検証

対象：

```text
tests/unit/test_validator_critical_only.py
```

---

### 検証内容

UUID変更時：

```text
IMMUTABILITY_BREACH
```

が：

```python
NWFSeverity.CRITICAL
```

へ正常 routing されることを確認。

---

### 検証項目

* CRITICAL routing 正常
* INFO混在なし
* Engine stop routing 維持
* Severity Monotonicity 維持

---

### DoD

* violation generation PASS
* CRITICAL mapping PASS
* Runtime stop PASS
* INFO contamination ゼロ

---

## Step 4. pytest 再実行

実行順：

```powershell
cd D:\NWF

.\.venv\Scripts\activate

python -m pytest -v tests\unit\test_validator_critical_only.py

python -m pytest -v tests\integration_phase_3_4_validator.py

python -m pytest -v
```

---

## 検証項目

* validate() call synchronization 正常化
* TypeError 消滅
* UUID Missing Policy PASS
* IMMUTABILITY_BREACH routing PASS
* INFO混在なし
* strict schema 維持
* integration tests PASS 維持
* import error ゼロ

---

## 5. リスクと対策

| リスク                          | 対策                     |
| ---------------------------- | ---------------------- |
| validate call order mismatch | test synchronization   |
| callable contract mismatch   | context.is_valid() 維持  |
| UUID Policy 誤検知              | None guard 厳守          |
| INFO contamination           | CRITICAL優先停止           |
| backward compatibility 汚染    | validator rollback 非実施 |

---

## 6. Exit Criteria

* tests/unit/test_validator_critical_only.py 全PASS
* integration_phase_3_4_validator.py PASS維持
* validate() TypeError 消滅
* UUID Missing Policy 準拠
* IMMUTABILITY_BREACH routing 正常
* strict schema 維持
* Severity consistency 維持
* rollback 非実施
* Validation architecture 維持

---

## 7. 最終結論

現在確認されている failure は：

```text
Validation architecture 崩壊ではなく、
test-side synchronization mismatch
```

である。

特に：

```text
validator_integration_adapter.py
```

および：

```text
strict schema synchronization
```

は正常維持されている。

本 Phase では：

* rollback を行わず
* validate(entity, context) contract を維持し
* test synchronization を継続し
* UUID Missing Policy を再検証し
* CRITICAL routing を再確認する

方針を正式採用する。

これにより：

```text
Phase 3.5 Validation stabilization
```

を継続する。

---

[EOF]