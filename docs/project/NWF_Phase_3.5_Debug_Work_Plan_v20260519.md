Source: docs/project/NWF_Phase_3.5_Debug_Work_Plan_v20260519.md
Updated: 2026-05-19T01:10:00+09:00
PIC: Engineer / ChatGPT

# NWF Phase 3.5 Debug Work Plan v20260519

---

## 1. 概要

本ドキュメントは、
Phase 3.5 pytest 実行時に確認された：

- ConsistencyValidator severity 不整合
- ValidationResult strict schema 違反
- Legacy Adapter violated_rules 不足
- Integration Test の旧 schema 依存

について、

- Spec準拠性維持
- Validation strictness 維持
- DI architecture 維持
- Severity Monotonicity 維持
- Legacy compatibility 維持
- rollback 非実施

を前提として実施する
正式 Debug / Synchronization Work Plan である。

本計画は：

- docs/spec/Spec_Governance/NWF_Spec_Standard_v2.0.1.md
- docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
- docs/project/NWF_Phase_3.5_Debug_Work_Plan_v20260516.md
- docs/spec/Execution_Spec/NWF_Validation_System_v2.0.1.md
- docs/spec/Execution_Spec/NWF_Validator_Orchestration_Spec_v2.0.1.md

を Single Source of Truth とする。

---

## 2. 現在確認済みの障害

---

## 2.1 NWFSeverity.FATAL 不存在問題

発生箇所：

```text
src/integrity/consistency_validator.py
```

発生内容：

```python
severity=NWFSeverity.FATAL
```

pytest 実行時：

```text
AttributeError: FATAL
```

が発生。

---

### 原因

NWFSeverity Enum に：

```python
FATAL
```

が定義されていない。

しかし：

```python
ConsistencyValidator
```

側で：

```python
NWFSeverity.FATAL
```

を参照している。

---

### 状態評価

これは：

```text
Severity Enum synchronization mismatch
```

であり、

```text
Validation architecture 崩壊
```

ではない。

---

## 2.2 ValidationResult strict schema violation

発生箇所：

```text
tests/integration_phase_3_4_validator.py
```

および：

```text
src/integrity/validator_integration_adapter.py
```

---

### 発生内容 A

```text
ValueError:
violated_rules must not be empty when invalid
```

---

### 原因

以下条件：

```python
is_valid=False
```

にもかかわらず：

```python
violated_rules=[]
```

または未指定。

---

### 発生内容 B

```text
ValueError:
violated_rules must include rule_id
```

---

### 原因

以下 strict schema：

```python
if self.rule_id not in self.violated_rules:
```

へ違反。

---

## 2.3 Legacy Adapter strict schema 未同期

発生箇所：

```text
src/integrity/validator_integration_adapter.py
```

---

### 問題

Legacy dict →

```python
ValidationResult
```

変換時に：

```python
violated_rules
```

が補完されていない。

---

## 3. 現在の状態評価

現在の failure は：

```text
Validation strict化が正常に浸透し、
旧 test / legacy adapter が
新 schema に追従できていない状態
```

である。

これは：

* ValidationResult strict化
* Severity Monotonicity 強化
* Validation Pipeline 厳格化
* Adapter責務分離

が正常方向へ進行していることを意味する。

---

## 4. 基本方針

---

## 4.1 rollback は行わない

以下は維持する：

```text
ValidationResult strict schema
```

および：

```text
DI architecture
```

および：

```text
Severity Monotonicity
```

---

## 4.2 strict schema は維持

以下は mandatory とする：

```python
rule_id
scope
target_id
violated_rules
```

---

## 4.3 Legacy互換責務は Adapter 側が保持

ValidationResult 本体では吸収しない。

互換責務は：

```text
validator_integration_adapter.py
```

が持つ。

---

## 4.4 Severity は CRITICAL へ統一

正式 severity は：

```python
NWFSeverity.CRITICAL
```

とする。

---

## 5. Debug Work Plan

---

## Step 1. Severity Enum 同期修正

対象：

```text
src/integrity/consistency_validator.py
```

---

### 修正内容

修正前：

```python
severity=NWFSeverity.FATAL
```

修正後：

```python
severity=NWFSeverity.CRITICAL
```

---

### 理由

* Work Plan v20260516 準拠
* Spec synchronization
* Severity Enum consistency
* CRITICAL routing 統一

---

### DoD

* AttributeError 消滅
* pytest import 崩壊なし
* CRITICAL routing 維持

---

## Step 2. ValidationResult strict schema 同期

対象：

```text
tests/integration_phase_3_4_validator.py
```

---

### 修正内容

ERROR / CRITICAL 系 ValidationResult 作成時：

修正前：

```python
ValidationResult(
    rule_id="TEST_RULE",
    scope="TEST_SCOPE",
    target_id="TEST_TARGET",
    severity=NWFSeverity.ERROR,
    error_code="TEST_CODE",
    message="test"
)
```

修正後：

```python
ValidationResult(
    rule_id="TEST_RULE",
    scope="TEST_SCOPE",
    target_id="TEST_TARGET",
    severity=NWFSeverity.ERROR,
    error_code="TEST_CODE",
    message="test",
    violated_rules=["TEST_RULE"]
)
```

---

### 理由

strict schema：

```python
violated_rules must not be empty when invalid
```

へ準拠。

---

### DoD

* strict schema violation 解消
* rollback 不要
* invalid state consistency 維持

---

## Step 3. violated_rules includes rule_id 同期

対象：

```text
src/integrity/validator_integration_adapter.py
```

---

### 修正内容

Legacy dict conversion 時：

修正前：

```python
ValidationResult(
    rule_id=rule_id,
    ...
)
```

修正後：

```python
ValidationResult(
    rule_id=rule_id,
    violated_rules=[rule_id],
    ...
)
```

---

### 理由

strict schema：

```python
violated_rules must include rule_id
```

へ準拠。

---

### DoD

* Legacy adapter compatibility 維持
* strict schema violation 解消
* ValidationResult 本体汚染なし

---

## Step 4. UUID Missing Policy 再確認

対象：

```text
src/integrity/consistency_validator.py
```

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

### 禁止事項

以下は禁止：

```python
str(None) != str(None)
```

比較。

---

### DoD

* UUID Missing Policy 完全準拠
* None 誤検知ゼロ
* CRITICAL 誤発火なし

---

## Step 5. INFO混在禁止確認

対象：

```text
src/integrity/consistency_validator.py
```

---

### 正式仕様

```text
violation が存在する場合、
INFO ValidationResult は生成しない
```

---

### DoD

* Severity Monotonicity 維持
* Engine stop routing 安定
* CRITICAL/ERROR時 INFO混在ゼロ

---

## Step 6. pytest 再実行

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

* AttributeError 消滅
* violated_rules error 消滅
* rule_id strict schema 維持
* Legacy conversion 正常化
* CRITICAL routing 維持
* INFO混在なし
* pytest import error ゼロ

---

## DoD

* 全対象PASS
* rollback 不要
* strict schema 維持
* Validation architecture 維持
* Severity consistency 維持

---

## 6. 修正対象外

以下は本 Phase 対象外：

* IDGenerator
* MetadataManager
* EntityManager
* AuditLogManager
* tmp/
* experimental/

理由：

```text
Phase 3.5 Exit Criteria と無関係
```

---

## 7. リスクと対策

| リスク                        | 対策                     |
| -------------------------- | ---------------------- |
| strict schema による旧 test 崩壊 | test synchronization   |
| Severity Enum mismatch     | CRITICAL 統一            |
| Legacy validator 不整合       | Adapter互換吸収            |
| UUID None 誤検知              | UUID Missing Policy 厳守 |
| INFO混在                     | violation優先停止          |

---

## 8. Exit Criteria

* pytest 全PASS
* AttributeError 消滅
* violated_rules error 消滅
* strict schema 維持
* Severity consistency 完全同期
* Legacy compatibility 維持
* rollback 非実施
* Validation architecture 維持
* Import/package 崩壊ゼロ

---

## 9. 最終結論

現在の failure は：

```text
Validation strict architecture が
正常に浸透した結果発生した
同期不整合
```

であり、

```text
設計崩壊ではない
```

ことを確認。

本 Phase では：

* rollback を行わず
* strict schema を維持し
* Legacy adapter を同期し
* test code を新 schema へ追従させ
* Severity consistency を統一する

方針を正式採用する。

これにより：

```text
Phase 3.5 は
Validation Architecture stabilization
として完了する。
```

---

[EOF]