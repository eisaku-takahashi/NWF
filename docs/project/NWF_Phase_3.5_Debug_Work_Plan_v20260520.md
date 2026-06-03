Source: docs/project/NWF_Phase_3.5_Debug_Work_Plan_v20260520.md
Updated: 2026-05-20T02:15:00+09:00
PIC: Engineer / ChatGPT

# NWF Phase 3.5 Debug Work Plan v20260520

---

## 1. 概要

本ドキュメントは、
Phase 3.5 Step 6 pytest 再実行時に確認された：

- StoryEngine constructor interface mismatch
- ConsistencyValidator entity contract mismatch
- DummyEntity test contract 不足
- UUID Missing Policy 検証未到達

について、

- Validation architecture 維持
- strict schema 維持
- DI architecture 維持
- Severity Monotonicity 維持
- rollback 非実施
- Legacy compatibility 維持

を前提として実施する
追加 Synchronization / Debug Work Plan である。

本計画は：

- docs/spec/Spec_Governance/NWF_Spec_Standard_v2.0.1.md
- docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
- docs/project/NWF_Phase_3.5_Debug_Work_Plan_v20260519.md
- docs/spec/Execution_Spec/NWF_Validation_System_v2.0.1.md
- docs/spec/Execution_Spec/NWF_Validator_Orchestration_Spec_v2.0.1.md

を Single Source of Truth とする。

---

## 2. 現在確認済みの障害

---

## 2.1 StoryEngine constructor interface mismatch

発生箇所：

```text
tests/unit/test_validator_critical_only.py
```

発生内容：

```python
engine = StoryEngine(adapter=None)
```

pytest 実行時：

```text
TypeError:
StoryEngine.__init__()
got an unexpected keyword argument 'adapter'
```

が発生。

---

### 原因

現在の：

```python
StoryEngine.__init__()
```

は：

```python
adapter
```

引数を受け取らない仕様へ同期済み。

しかし test code 側が：

```python
adapter=None
```

を渡している。

---

### 状態評価

これは：

```text
StoryEngine API synchronization mismatch
```

であり、

```text
Validation architecture 崩壊
```

ではない。

---

## 2.2 ConsistencyValidator entity contract mismatch

発生箇所：

```text
tests/unit/test_validator_critical_only.py
```

および：

```text
src/integrity/consistency_validator.py
```

---

### 発生内容

pytest DEBUGログ：

```text
Unhandled validation exception:
'DummyEntity' object has no attribute 'is_valid'
```

---

### 発生結果

ConsistencyValidator が：

```python
SYS_VALIDATION_EXCEPTION
```

を：

```python
NWFSeverity.CRITICAL
```

として返却。

その結果：

```text
UUID Missing Policy
```

検証前に validation pipeline が停止。

---

### 原因

test 用：

```python
DummyEntity
```

に：

```python
is_valid
```

属性が存在しない。

しかし：

```python
ConsistencyValidator.validate()
```

内部で：

```python
target.is_valid
```

参照が実施されている。

---

### 状態評価

これは：

```text
Entity Contract synchronization mismatch
```

であり、

```text
UUID Missing Policy failure
```

そのものではない。

UUID比較ロジック到達前に：

```text
entity contract exception
```

が発生している。

---

## 2.3 UUID Missing Policy 検証未完了

現在：

```text
previous_uuid is None
current_uuid is None
```

ケースは：

```text
ConsistencyValidator exception
```

によって中断されている。

そのため：

```text
UUID Missing Policy 実装自体の正否は未確定
```

状態である。

---

## 3. 現在の状態評価

以下は正常完了済み：

* ValidationResult strict schema synchronization
* violated_rules includes rule_id synchronization
* Severity synchronization
* Legacy adapter synchronization
* integration_phase_3_4_validator.py 全PASS

したがって：

```text
validator_integration_adapter.py の
strict schema synchronization は成功
```

している。

現在の failure は：

```text
test synchronization
```

および：

```text
entity contract synchronization
```

に限定される。

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
Severity Monotonicity
```

および：

```text
Validation architecture
```

---

## 4.2 StoryEngine backward compatibility は原則復元しない

以下の復元：

```python
def __init__(..., adapter=None)
```

は原則実施しない。

理由：

```text
不要DI互換の復活リスク
```

が存在するため。

---

## 4.3 test synchronization を優先

test code を：

```text
現行 API / contract
```

へ同期する。

---

## 4.4 Entity contract を明示化

test 用 Entity は：

```python
is_valid
```

属性を保持する。

---

## 5. Debug Work Plan

---

## Step 1. StoryEngine test synchronization

対象：

```text
tests/unit/test_validator_critical_only.py
```

---

### 修正内容

修正前：

```python
engine = StoryEngine(adapter=None)
```

修正後：

```python
engine = StoryEngine()
```

---

### 理由

現在の：

```python
StoryEngine.__init__()
```

仕様へ同期するため。

---

### DoD

* TypeError 消滅
* StoryEngine import 正常
* DI architecture 維持

---

## Step 2. DummyEntity contract synchronization

対象：

```text
tests/unit/test_validator_critical_only.py
```

---

### 修正内容

DummyEntity に：

```python
self.is_valid = True
```

を追加。

または：

```python
@property
def is_valid(self):
    return True
```

を追加。

---

### 理由

ConsistencyValidator の：

```python
target.is_valid
```

参照 contract へ同期するため。

---

### DoD

* SYS_VALIDATION_EXCEPTION 消滅
* validation pipeline 継続
* UUID comparison logic 到達可能化

---

## Step 3. UUID Missing Policy 再検証

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
CRITICAL を生成しない
```

ことを再確認。

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
* CRITICAL 誤発火ゼロ
* UUID Missing Policy 完全準拠

---

## Step 4. immutability breach routing 再検証

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

へ正常昇格することを確認。

---

### DoD

* CRITICAL routing 正常
* INFO混在なし
* Engine stop routing 維持

---

## Step 5. pytest 再実行

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

* StoryEngine TypeError 消滅
* SYS_VALIDATION_EXCEPTION 消滅
* UUID Missing Policy 正常化
* CRITICAL routing 維持
* INFO混在なし
* strict schema 維持
* integration tests PASS 維持
* pytest import error ゼロ

---

## 6. リスクと対策

| リスク                       | 対策                         |
| ------------------------- | -------------------------- |
| test code の旧 API 依存       | test synchronization       |
| DummyEntity contract 不足   | is_valid 属性追加              |
| UUID Policy 誤検知           | None guard 厳守              |
| INFO混在                    | violation優先停止              |
| backward compatibility 汚染 | StoryEngine 側 rollback 非実施 |

---

## 7. Exit Criteria

* pytest 全PASS
* StoryEngine TypeError 消滅
* SYS_VALIDATION_EXCEPTION 消滅
* UUID Missing Policy 準拠
* strict schema 維持
* Severity consistency 維持
* rollback 非実施
* Validation architecture 維持

---

## 8. 最終結論

現在の failure は：

```text
Validation strict architecture の崩壊ではなく、
test / contract synchronization mismatch
```

である。

特に：

```text
validator_integration_adapter.py
```

の strict schema synchronization は：

```text
正常完了
```

していることを確認。

本 Phase では：

* rollback を行わず
* test code を現行 API へ同期し
* entity contract を明示化し
* UUID Missing Policy を再検証し
* Validation architecture を維持する

方針を正式採用する。

これにより：

```text
Phase 3.5 Validation stabilization
```

を継続する。

---

[EOF]