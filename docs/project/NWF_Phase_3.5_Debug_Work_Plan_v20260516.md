Source: docs/project/NWF_Phase_3.5_Debug_Work_Plan_v20260516.md
Updated: 2026-05-16T15:31:00+09:00
PIC: Engineer / ChatGPT

# NWF Phase 3.5 Debug Work Plan v20260516

---

## 1. 概要

本ドキュメントは、Phase 3.5 において発生した Validator / ValidationResult 系 pytest 失敗について、

- Spec準拠性維持
- DIアーキテクチャ維持
- ValidationResult厳格化維持
- StoryDB I/F統一
- テストコードの新I/F追従

を目的として実施する、正式デバッグ・同期作業計画である。

本計画は：

- docs/project/NWF_Phase_3.5_Debug_Work_Plan_v20260502.md
- docs/spec/Execution_Spec/NWF_Consistency_Validator_Spec_v2.0.1_Phase_3.5.md
- docs/spec/Execution_Spec/NWF_Validation_System_v2.0.1.md
- docs/spec/Execution_Spec/NWF_Validator_Orchestration_Spec_v2.0.1.md
- docs/spec/Spec_Governance/NWF_Spec_Standard_v2.0.1.md

を Single Source of Truth として構成される。

---

## 2. 現在確認済みの障害

---

### 2.1 ConsistencyValidator DI必須化によるUnit Test崩壊

発生ログ：

```text
TypeError:
ConsistencyValidator.__init__()
missing 3 required positional arguments:
'rule_evaluator',
'escalation_evaluator',
'and audit_manager'
````

原因：

```python
validator = ConsistencyValidator(
    story_db=story_db
)
```

に対し、

```python
ConsistencyValidator.__init__()
```

が DI必須化されている。

これは：

* Validator純粋化
* Spec準拠DI化

が実装側へ浸透した結果である。

---

### 2.2 ValidationResult rule_id 必須化によるIntegration Test崩壊

発生ログ：

```text
ValueError: rule_id is required
```

原因：

```python
ValidationResult(...)
```

生成時に：

```python
rule_id=""
```

となっている。

これは：

```text
ValidationResult strict schema enforcement
```

が実装済みであることを意味する。

---

### 2.3 validator_integration_adapter の Legacy変換不足

発生箇所：

```text
src/integrity/validator_integration_adapter.py
```

問題：

Legacy dict → ValidationResult 変換時に：

* rule_id
* scope
* target_id

が未補完。

そのため：

```python
ValidationResult(...)
```

生成時に整合性エラーとなる。

---

## 3. 現在の状態評価（重要）

現在の失敗は：

```text
実装がSpecへ近づいた結果、
旧テストコードが新I/Fへ追従できていない
```

状態である。

これは：

* ValidationResult strict化
* Validator DI化
* StoryDB Interface統一

が成功方向へ進んでいることを意味する。

従って：

```text
実装 rollback は行わない
```

を原則とする。

---

## 4. 修正方針（正式決定）

---

## 4.1 方針A（採用）

ConsistencyValidator は：

```python
Optional Dependency Injection
```

を許可する。

実装：

```python
def __init__(
    self,
    story_db,
    rule_evaluator=None,
    escalation_evaluator=None,
    audit_manager=None,
):
```

---

### 採用理由

* Unit Test軽量化
* Mock容易化
* Validator純粋性維持
* StoryDB I/F独立性維持
* Spec整合性維持
* 循環依存回避

---

### 非採用方針

以下は採用しない：

```text
Test側で巨大DIツリーを毎回構築する
```

理由：

* Unit Testが実装詳細へ過剰依存する
* Validator単体検証性が低下する
* Mock設計が崩壊する

---

## 4.2 ValidationResult strict schema は維持

以下は維持する：

```text
rule_id 必須
scope 必須
target_id 必須
```

つまり：

```text
ValidationResult strict化は rollback しない
```

---

## 4.3 Legacy Adapter側で互換吸収

互換責務は：

```text
validator_integration_adapter.py
```

側が持つ。

ValidationResult 本体では吸収しない。

---

## 5. Debug Work Plan（実行順）

---

### 1. ConsistencyValidator Optional DI化

対象：

```text
src/integrity/consistency_validator.py
```

作業内容：

```python
def __init__(
    self,
    story_db,
    rule_evaluator=None,
    escalation_evaluator=None,
    audit_manager=None,
):
```

へ変更。

---

### DoD

* Unit Test が lightweight に実行可能
* Validator純粋性維持
* DI設計維持
* pytest import 崩壊なし

---

### 2. ValidationResult生成コードの全修正

対象：

```text
tests/integration_phase_3_4_validator.py
tests/unit/test_validator_critical_only.py
src/integrity/validator_integration_adapter.py
```

作業内容：

全 ValidationResult 生成へ：

```python
rule_id="TEST_RULE"
scope="TEST_SCOPE"
target_id="TEST_TARGET"
```

を付与。

---

### 修正例

修正前：

```python
ValidationResult(
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
    message="test"
)
```

---

### DoD

* rule_id required error 消滅
* strict schema 維持
* 全 ValidationResult が Spec準拠

---

### 3. validator_integration_adapter Legacy互換修正

対象：

```text
src/integrity/validator_integration_adapter.py
```

作業内容：

Legacy dict 変換時に：

```python
rule_id=raw_result.get("rule_id", "LEGACY_RULE")
scope=raw_result.get("scope", "LEGACY")
target_id=raw_result.get("target_id", "")
```

を補完。

---

### DoD

* Legacy validator が ValidationResult strict schema へ適合
* Adapter が互換責務を保持
* ValidationResult 本体が汚染されない

---

### 4. MockStoryDB I/F同期確認

対象：

```text
tests/unit/test_validator_critical_only.py
tests/mocks/mock_story_db.py
```

確認内容：

```python
get(entity_id: str) -> Optional[Entity]
```

準拠。

---

### 必須仕様

```python
def get(self, entity_id: str):
    return self._data.get(str(entity_id))
```

---

### DoD

* StoryDB I/F統一
* ID型揺れ排除
* Mockが本番I/F契約へ一致

---

### 5. UUID Missing Policy同期確認

対象：

```text
src/integrity/consistency_validator.py
```

正式仕様：

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

* UUID Missing Policy完全準拠
* None比較誤検知ゼロ
* CRITICAL誤発火なし

---

### 6. INFO混在禁止仕様確認

正式仕様：

```text
violation が1件でも存在する場合：
Validation OK（INFO）は生成しない
```

対象：

```text
src/integrity/consistency_validator.py
```

---

### DoD

* CRITICAL時に INFO混在なし
* Severity Monotonicity維持
* Engine停止条件が安定

---

### 7. ValidationResult属性統一確認

対象：

```text
src/integrity/consistency_validator.py
src/integrity/validation_result.py
```

必須属性：

```python
severity=NWFSeverity.CRITICAL
scope="SYSTEM_INTEGRITY"
rule_id="SYS_IMMUTABILITY_CHECK"
target_id=target_id
```

---

### DoD

* Validation Pipeline 安定化
* Structure violation format統一
* Severity routing 安定化

---

### 8. Package / Import整合性確認

対象：

```text
src/integrity/__init__.py
src/models/__init__.py
```

確認内容：

* package import 安定
* pytest import error 無し
* 循環参照無し

---

### DoD

* pytest import 崩壊ゼロ
* package path 安定
* Validator/Models/Engine import 統一

---

### 9. pytest実行

実行順：

```powershell
cd D:\NWF

.\.venv\Scripts\activate

python -m pytest -v tests\unit\test_validator_critical_only.py

python -m pytest -v tests\integration_phase_3_4_validator.py

python -m pytest -v
```

---

### 検証項目

* len(results) > 0
* CRITICAL存在
* INFO混在なし
* Engine停止確認
* rule_id error 消滅
* import error 消滅

---

### DoD

* 全対象PASS
* 副作用なし
* Validation strict schema 維持
* DI architecture 維持

---

## 6. 現時点で修正対象外とする項目

以下は本Phase対象外：

* IDGenerator
* AuditLogManager
* MetadataManager
* EntityManager
* tmp/nwf_integration_test.py

理由：

```text
Phase 3.5 Exit Criteria と無関係
```

であるため。

---

## 7. リスクと対策

| リスク                     | 対策                    |
| ----------------------- | --------------------- |
| strict schema による旧コード崩壊 | Adapter互換層で吸収         |
| DI導入によるUnit Test複雑化     | Optional DI採用         |
| StoryDB実装差異             | I/F固定化                |
| UUID None比較誤検知          | UUID Missing Policy厳守 |
| INFO混在                  | violation優先停止         |

---

## 8. Phase 3.5 Exit Criteria

* pytest 全PASS
* ValidationResult strict schema維持
* rule_id required error 解消
* ConsistencyValidator DI整合化
* StoryDB I/F統一
* UUID Missing Policy完全準拠
* INFO混在禁止完全実装
* Engine停止確認
* Import/package 崩壊ゼロ
* Specと実装の乖離ゼロ

---

## 9. 最終結論

現在の崩壊は：

```text
Spec v2.0.1 が実装へ浸透した結果
```

であり、

```text
アーキテクチャ刷新が正常方向に進行している
```

ことを意味する。

従って本Phaseでは：

* rollback を行わず
* strict schema を維持し
* DI architecture を維持し
* 旧テストを新I/Fへ同期させる

方針を正式採用する。

これにより：

```text
Phase 3.5 は
「バグ修正」ではなく
「Validator Architecture確定」
として完了する。
```

---

[EOF]