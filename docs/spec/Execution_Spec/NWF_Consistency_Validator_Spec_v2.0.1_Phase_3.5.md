Source: docs/spec/Execution_Spec/NWF_Consistency_Validator_Spec_v2.0.1_Phase_3.5.md
Updated: 2026-05-13T15:05:00+09:00
PIC: Engineer / ChatGPT

# NWF Consistency Validator Spec v2.0.1 Phase 3.5

---

## 1. 概要 (Overview)

本仕様書は、
NWF (Narrative World Framework) v2.0.1 Phase 3.5 における

- src/integrity/consistency_validator.py

の実装仕様を定義する。

対象クラス：

python
ConsistencyValidator

本クラスは単一ルールを評価する Validator ではなく、

- Validation Pipeline の整合性制御
- Immutability 保証
- ValidationResult の統合
- Escalation Routing
- Audit Logging

を司る「Validation Orchestrator」である。

本仕様は以下を目的とする：

- 実装曖昧性の排除
- Spec とコードの乖離ゼロ化
- Mock / 実装 / テスト間のI/F統一
- AI実装時の手戻り防止
- Recursive Integrity 準拠

本仕様書のみを参照することで、
ChatGPT 等の AI Assistant は

- src/integrity/consistency_validator.py

を再現可能でなければならない。

---

## 2. Scope (適用範囲)

本仕様は以下に適用される：

- src/integrity/consistency_validator.py
- Validation orchestration
- Immutability validation
- ValidationResult aggregation
- Escalation routing
- Audit logging

本仕様は以下を直接定義しない：

- RuleEvaluator 内部ロジック
- EscalationEvaluator 内部ロジック
- StoryDB 実装詳細
- Workflow Engine 実装

---

## 3. Cross-Spec Synchronization

本仕様は以下の仕様書と同期される。

### Core / Data

- docs/spec/Core_Spec/NWF_Entity_ID_System_v2.0.1.md
- docs/spec/Core_Spec/NWF_Story_Database_v2.0.1.md

### Execution / Validation

- docs/spec/Execution_Spec/NWF_Validation_System_v2.0.1.md
- docs/spec/Execution_Spec/NWF_Execution_Pipeline_v2.0.1.md
- docs/spec/Execution_Spec/NWF_Escalation_Logic_Spec_v2.0.1.md
- docs/spec/Execution_Spec/NWF_Validator_Orchestration_Spec_v2.0.1.md
- docs/spec/Execution_Spec/NWF_Mock_Design_Guideline_v2.0.1.md

### Governance

- docs/spec/Spec_Governance/NWF_Spec_Standard_v2.0.1.md

### Work Plan

- docs/project/NWF_Phase_3.5_Debug_Work_Plan_v20260502.md

本仕様と上位仕様が矛盾した場合：

1. Work Plan
2. Execution Spec
3. Core Spec
4. Governance Spec

の順で優先する。

### 追記理由

Work Plan Section 8「Specとコードの同期検証（追加必須）」において：

- NWF_Validator_Orchestration_Spec_v2.0.1.md
- NWF_Mock_Design_Guideline_v2.0.1.md

が Single Source of Truth の検証対象として追加定義された。

そのため Cross-Spec Synchronization に正式追加した。

修正前：
- 上記2 Spec への同期記述なし

修正後：
- Execution / Validation セクションへ正式追加

---

## 4. Roles & Responsibilities

ConsistencyValidator の責務を以下に定義する。

### 4.1 Validation Orchestration

各 Validator / Evaluator を
正しい順序で呼び出す。

ConsistencyValidator 自身は
複雑な業務ルールを保持してはならない。

---

### 4.2 Pre-validation

以下を検証する：

- entity.id 正規性
- metadata 存在
- context 正常性
- ValidationContext 契約

### 追記（Spec同期明確化）

Work Plan Section 8.1 において：

- target_id が必ず str 化されている
- ValidationContext 契約違反時に exception を外部送出しない

ことが追加検証対象として定義された。

そのため Pre-validation の責務として：

- Entity ID の str 正規化
- ValidationContext 契約失敗時の failure result 化

を明示的責務として扱う。

修正前：
- ValidationContext 契約の責務のみ記載
- str 正規化責務が暗黙

修正後：
- str 正規化責務を Validation 前提責務として明示

---

### 4.3 Immutability Enforcement

Phase 3.5 最重要責務。

過去確定済み Entity の
不正変更を検出する。

Immutability violation は：

- 即時 CRITICAL
- 後続 validation 停止
- escalation 対象

として扱う。

---

### 4.4 ValidationResult Aggregation

複数 Validator の結果を
決定論的に統合する。

Aggregation の対象は：

python
list[ValidationResult]

である。

ValidationResult 自体は
aggregate object ではない。

---

### 4.5 Escalation Routing

重大 violation 発生時：

python
self.escalation_evaluator.evaluate_escalation(...)

を呼び出す。

---

### 4.6 Audit Logging

最終 ValidationResult を
AuditLogManager に記録する。

---

## 5. Architectural Principles

---

### 5.1 Pure Evaluator Principle

ConsistencyValidator は
Pure Evaluator として振る舞う。

validate() 内で：

- entity 修正
- state mutation
- automatic repair

を行ってはならない。

---

### 5.2 No Internal DB Structure Dependency

Validator は
StoryDB 内部構造に依存してはならない。

禁止：

python
story_db._data
story_db.entities
story_db.storage

許可：

python
story_db.get(entity_id)

のみ。

### 追記（Mock同期仕様）

Work Plan Section 8.2 / 8.5 により：

- MockStoryDB
- 本番 StoryDB
- Validator

の I/F 統一が正式要件となった。

そのため：

- Mock 実装であっても内部辞書アクセスを Validator に露出してはならない
- Validator は Mock / 本番 DB 差異を認識してはならない

を追加原則として扱う。

修正前：
- 本番 StoryDB のみを対象とした記述

修正後：
- Mock 実装も含む統一 I/F 原則へ拡張

---

### 5.3 Spec Strictness Principle

本仕様未記載の
防御的追加実装は禁止とする。

特に：

- 暗黙 fallback
- silent auto-repair
- extra validation
- hidden normalization

は禁止。

理由：

Spec と実装の乖離防止。

---

### 5.4 Deterministic Result Principle

ValidationResult の順序は
決定論的でなければならない。

sort 時：

- 未定義属性依存禁止
- hash/random 依存禁止

---

## 6. Interface Contract

---

### 6.1 Constructor

python
class ConsistencyValidator:

    def __init__(
        self,
        rule_evaluator: RuleEvaluator,
        escalation_evaluator: EscalationEvaluator,
        audit_manager: AuditLogManager,
        story_db: StoryDB
    ):
        pass

---

### 6.2 validate()

python
def validate(
    self,
    entity: NWFObject,
    context: ValidationContext
) -> list[ValidationResult]:

単一 entity の整合性検証を行う。

戻り値は：

- list[ValidationResult]

であり、

- aggregate ValidationResult object

ではない。

1 violation = 1 ValidationResult object

とする。

---

### 6.3 validate_batch()

python
def validate_batch(
    self,
    entities: list[NWFObject],
    context: ValidationContext
) -> list[ValidationResult]:

複数 entity を検証する。

---

## 7. StoryDB Interface Contract

StoryDB は以下を必須とする。

python
def get(entity_id: str) -> Optional[NWFObject]:
    pass

### Requirements

- entity_id は str
- 非存在時は None
- TypeError は契約違反

---

## 8. Entity ID Specification

---

### 8.1 ID Type

Entity ID は常に：

python
str

で扱う。

UUID object を直接扱ってはならない。

---

### 8.2 Mandatory Normalization

以下を必須とする。

python
target_id = str(getattr(entity, "id", ""))

---

### 8.3 Forbidden

禁止：

python
entity.id.hex
uuid.UUID(entity.id)

---

## 9. ValidationResult Specification

---

## 9.1 Responsibility Definition

ValidationResult は：

- aggregate result object

ではなく、

- single validation event object

である。

つまり：

- 1 success
- 1 warning
- 1 violation

ごとに独立した object を生成する。

---

## 9.2 Required Fields

ValidationResult は最低限以下を持つ。

python
severity
message
target_id
scope
rule_id
is_valid

---

## 9.3 Forbidden Structure

以下は禁止：

python
ValidationResult.errors
ValidationResult.warnings
ValidationResult.results

理由：

ValidationResult は
single-result object であり、
aggregate container ではないため。

---

## 9.4 Failure Factory

以下を必須とする。

python
ValidationResult.failure(...)

これは：

- 単一 failure object

を生成する factory method である。

---

## 9.5 Success Factory

以下を許可する。

python
ValidationResult.success(...)

これは：

- 単一 success object

を生成する factory method である。

---

## 9.6 INFO Generation Rule

重要仕様：

violation が 1 件でも存在する場合：

python
ValidationResult.success()

を生成してはならない。

---

## 9.7 Failure Detection Rule

failure 判定は：

python
any(not r.is_valid for r in results)

を正式仕様とする。

---

## 9.8 Standardized Attributes

Immutability violation は
必ず以下を使用する。

python
severity = NWFSeverity.CRITICAL
scope = "SYSTEM_INTEGRITY"
rule_id = "SYS_IMMUTABILITY_CHECK"

---

## 10. Immutability Specification

---

## 10.1 Purpose

Immutability Check は：

- 過去確定 state 保護
- timeline integrity 保護
- Entity replacement 検知

を目的とする。

---

## 10.2 Execution Timing

Immutability Check は：

- RuleEvaluator より前
- escalation より前

に実行する。

---

## 10.3 Required Logic

以下を厳密仕様とする。

python
target_id = str(getattr(entity, "id", ""))

previous = self.story_db.get(target_id)

---

## 10.4 previous is None

python
if previous is None:

の場合：

- 新規 Entity とみなす
- violation を生成しない
- validation 継続

---

## 10.5 UUID Comparison Rule

Immutability 判定は：

python
str(previous.uuid) != str(entity.uuid)

のみを使用する。

### 修正（正式仕様同期）

Work Plan v20260502 Section 4 において：

```python
if str(previous.uuid) != str(target.uuid):
```

は暫定実装例であり、

Execution Spec 10.6 UUID Missing Policy を優先することが正式確定した。

そのため最終仕様は以下とする。

修正前：

python
str(previous.uuid) != str(entity.uuid)

修正後：

python
if (
previous.uuid is not None
and entity.uuid is not None
and str(previous.uuid) != str(entity.uuid)
):

理由：

* previous.uuid is None
* entity.uuid is None

を violation としない正式仕様との整合性確保のため。

### 仕様固定

Immutability 判定ロジックは：

* UUID 双方定義済み
* かつ値不一致

の場合のみ violation とする。

追加 validation の導入は禁止。

---

## 10.6 UUID Missing Policy

以下は violation としない：

python
previous.uuid is None
entity.uuid is None

理由：

Phase 3.5 Work Plan において
正式仕様化されていないため。

Spec 未記載 validation の追加は禁止。

### 追記（Execution Spec 優先固定）

Work Plan v20260502 Section 4 において：

```python
if str(previous.uuid) != str(target.uuid):
```

は暫定実装例であり、

本 Section 10.6 を優先することが正式に明文化された。

そのため：

```python
if (
    previous.uuid is not None
    and entity.uuid is not None
    and str(previous.uuid) != str(entity.uuid)
):
```

のみを正式仕様とする。

修正前：

* UUID Missing Policy と比較式の関係が暗黙

修正後：

* 比較式との優先関係を明示

---

## 10.7 Immutability Violation Result

UUID 不一致時：

python
ValidationResult.failure(
    severity=NWFSeverity.CRITICAL,
    message="IMMUTABILITY_BREACH: UUID changed",
    target_id=target_id,
    scope="SYSTEM_INTEGRITY",
    rule_id="SYS_IMMUTABILITY_CHECK"
)

を生成する。

---

## 10.8 Post-Violation Behavior

Immutability violation 発生時：

- 後続 RuleEvaluator をスキップ
- escalation routing へ進む

---

## 11. Execution Flow

validate() は
以下順序を厳守する。

---

### Step 1 Context Contract Check

検証：

python
context is not None
context.is_valid() is True

失敗時：

- FATAL result 返却
- exception を raise しない

### 追記

Work Plan Section 8.1 に基づき：

- ValidationContext 契約失敗は ValidationResult.failure(...)
  へ変換される必要がある
- validate() 外への未処理 exception を禁止する

ことを Execution Flow に統合した。

---

### Step 2 ID Normalization

python
target_id = str(getattr(entity, "id", ""))

### 追記

Work Plan Section 8.3 により：

- story_db.get() 呼び出し時に常に str を渡す
- Validator / Engine / Mock 間で ID型揺れを禁止する

ことが正式固定された。

---

### Step 3 Basic Integrity

確認：

- metadata
- version

---

### Step 4 Immutability Check

UUID comparison 実施。

### 修正

修正前：
- UUID comparison の詳細条件が暗黙

修正後：
- 以下を正式仕様として固定

python
if (
    previous.uuid is not None
    and entity.uuid is not None
    and str(previous.uuid) != str(entity.uuid)
):

### 追加仕様

violation 発生時：

- RuleEvaluator を実行しない
- ValidationResult.success() を生成しない
- escalation routing へ即時遷移する

これは：

- INFO混在禁止
- Engine stops on CRITICAL

の Work Plan DoD に基づく。

---

### Step 5 RuleEvaluator Delegation

python
self.rule_evaluator.evaluate(entity, context)

RuleEvaluator は：

- list[ValidationResult]

を返すものとする。

### 追記

Work Plan Section 8.1 に基づき：

- RuleEvaluator は aggregate object を返してはならない
- list[ValidationResult] のみ許可

を Execution Flow として固定した。

---

### Step 6 Result Aggregation

ValidationResult を：

python
list[ValidationResult]

として統合する。

---

### Step 7 Escalation Routing

Error / Critical 存在時：

python
self.escalation_evaluator.evaluate_escalation(
    entity,
    results
)

EscalationEvaluator は：

python
list[ValidationResult]

を受け取る。

### 追記

Work Plan Section 8.1 に基づき：

failure 判定は：

python
any(not r.is_valid for r in results)

を使用する。

未定義属性による暗黙判定は禁止。

---

### Step 8 Audit Logging

python
self.audit_manager.log_validation(...)

### 追記

Work Plan Section 10 に基づき：

- UUID comparison debug
- escalation routing

は logging 必須対象とする。

ただし：

- excessive debug spam
- nondeterministic logging

は禁止。

---

### Step 9 Return

python
list[ValidationResult]

を返却する。

---

## 12. Exception Handling Policy

---

### 12.1 No Unhandled Exception

validate() 外へ
未処理 exception を出してはならない。

### 追記

Work Plan Section 8.1 に基づき：

ValidationContext 契約失敗や validation failure は：

python
ValidationResult.failure(...)

へ変換する。

exception を validation control flow として使用してはならない。

---

### 12.2 TypeError Policy

以下のみ再送出を許可：

python
TypeError

理由：

I/F契約違反。

### 追記

Work Plan Section 8.5 に基づき：

- StoryDB I/F 契約違反
- ValidationResult I/F 契約違反
- RuleEvaluator I/F 契約違反

は TypeError 再送出対象に含まれる。

---

### 12.3 Other Exceptions

その他 exception は：

python
ValidationResult.failure(
    severity=NWFSeverity.FATAL,
    ...
)

へ変換する。

### 追記

修正前：
- FATAL conversion の範囲が抽象的

修正後：
- validate() 外への未処理 exception 流出禁止を明示
- failure result 化を mandatory behavior として固定

---

## 13. Sorting & Determinism

ValidationResult sort は：

python
getattr(r, "error_code", None) or "SUCCESS"

等、
未定義属性安全性を持つこと。

sort 対象は：

python
list[ValidationResult]

内の各 object とする。

### 追記（Determinism固定）

Work Plan Section 8 DoD により：

- Validator / Engine / Mock / Spec 間で論理矛盾が存在しない
- Single Source of Truth が統一されている

ことが Exit Criteria に追加された。

そのため：

- hash/random ベース sort
- 実行順依存 sort
- dict iteration order 依存

は禁止とする。

修正前：
- 未定義属性安全性のみ記載

修正後：
- 非決定論的 sort 実装を明示禁止

---

## 14. Logging Policy

---

### Required

- UUID comparison debug
- escalation routing

---

### Forbidden

- excessive debug spam
- nondeterministic logging

---

## 15. Testing Requirements

pytest にて以下を確認する。

---

### Required Assertions

python
len(results) > 0

python
CRITICAL exists

python
INFO not mixed

python
Engine stops on CRITICAL

### 追記（Work Plan同期）

Work Plan Section 9 および Section 8 DoD に基づき、
以下を追加必須検証項目とする。

追加：

python
story_db.get() only usage

python
target_id is always str

python
MockStoryDB implements get(entity_id: str)

python
Nonexistent entity returns None

python
UUID None does not create violation

python
RuleEvaluator skipped on immutability breach

python
No aggregate ValidationResult object exists

python
pytest import error does not occur

### 追記理由

Work Plan v20260502 において：

- StoryDB I/F統一
- Mock同期
- UUID Missing Policy
- Import/package整合性
- aggregate/single-result 混在排除

が正式 DoD に追加されたため。

---

## 16. Exit Criteria

Phase 3.5 完了条件：

- pytest PASS
- Immutability violation CRITICAL化
- INFO 混在なし
- StoryDB I/F 統一
- Spec / 実装乖離ゼロ

### 追記（Work Plan完全同期）

Work Plan Section 8 / 9 / 5 に基づき、
以下を追加する。

追加：

- UUID Missing Policy が正式仕様と一致
- story_db.get(entity_id: str) が全実装で統一
- MockStoryDB が本番 I/F と一致
- Validator が DB内部構造へ依存していない
- ValidationResult が single-result object として統一
- aggregate ValidationResult object が存在しない
- pytest import error が発生しない
- Validator / Engine / Mock / Spec 間で論理矛盾が存在しない
- Single Source of Truth が全Specで統一されている

修正前：
- 高レベル Exit Criteria のみ

修正後：
- Work Plan DoD と完全同期した詳細 Exit Criteria を追加

---

## 17. まとめ

本仕様は：

- ConsistencyValidator の責務固定
- ValidationResult I/F 固定
- ValidationResult の単一責務化
- aggregate/single-result 混在排除
- Immutability 判定固定
- StoryDB I/F 固定
- 実装曖昧性排除

を目的とする。

これにより
Phase 3.5 は：

「暫定修正」

ではなく

「構造仕様の固定」

として完了する。

---

[EOF]