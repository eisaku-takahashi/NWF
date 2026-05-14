Source: docs/project/NWF_Phase_3.5_Debug_Work_Plan_v20260502.md
Updated: 2026-05-13T00:38:00+09:00
PIC: Engineer / ChatGPT

# NWF Phase 3.5 Debug Work Plan v20260502（v2 完全実装版）

---

## 1. 概要

本ドキュメントは、Phase 3.5 における Validator Immutability違反テスト障害の修正および関連するアーキテクチャ整合性の確保を目的とした**完全実装可能なデバッグ作業計画**である。

目的：

- テスト失敗の根本原因（I/F不整合）の解消
- Spec準拠のアーキテクチャ維持
- 再発防止のためのI/Fおよびデータ整合性の強化
- 実装ブレの排除（曖昧性ゼロ化）

---

## 2. 前提条件（確定仕様）

- `story_db` は必ず `get(entity_id: str) -> Optional[Entity]` を持つ
- Validatorは `story_db.get()` のみを使用する（内部構造に依存しない）
- Entity IDは全て `str` に正規化される
- Immutability違反は **即時CRITICAL**
- violationが1件でも存在する場合：
  - Validation OK（INFO）は生成しない

---

## 3. Debug Work Plan（実行順序）

---

### 1. MockStoryDBのI/F準拠化  
**ファイル**:  
tests/unit/test_validator_critical_only.py（既存修正）

**作業内容**:
- `MockStoryDB` に `get(entity_id: str)` を実装
- 内部辞書アクセスを完全にI/F経由に統一
- IDは必ず `str` として扱う

**実装**:
```

class MockStoryDB:
def **init**(self, data: dict):
self._data = data

```
def get(self, entity_id: str):
    return self._data.get(str(entity_id))
```

```

**DoD**:
- `previous is None` が意図しない形で発生しない
- Validatorが正常に旧Entityを取得できる

---

### 2. ValidationResult I/Fの確定（必須タスク）  
**ファイル**:  
~~src/models/validation_result.py（既存確認 or 修正）~~
src/integrity/validation_result.py（既存確認 or 修正）

**作業内容**:
- 以下を必ず確認・確定する：
  - `ValidationResult.failure()` の有無
  - コンストラクタの引数
  - `severity`, `scope`, `rule_id`, `target_id` の設定方法

**DoD**:
- Work Plan内の生成コードと実装が100%一致
- 不明なAPIを使用していない

---

### 3. ConsistencyValidatorのID参照安定化  
**ファイル**:  
src/integrity/consistency_validator.py（既存修正）

**作業内容**:
- ID取得時に必ず `str` 化
- DB呼び出しはI/Fのみに依存

**実装**:
```

target_id = str(getattr(target, "id", ""))
previous = self.story_db.get(target_id)

```

**DoD**:
- UUID/str混在でも取得失敗しない
- Mock依存コードが完全に排除されている

---

### 4. Immutability違反ロジックの完全実装（確定仕様）  
**ファイル**:  
src/integrity/consistency_validator.py（既存修正）

**作業内容（厳密定義）**:

```

1. previous が None の場合：
   → 新規生成とみなしチェックをスキップ

2. previous.uuid と current.uuid を比較

3. 不一致の場合：
   → CRITICAL violation を1件生成

```

**実装（必須仕様）**:
```

if previous is not None:
if str(previous.uuid) != str(target.uuid):
results.append(
ValidationResult.failure(
severity=NWFSeverity.CRITICAL,
message="IMMUTABILITY_BREACH: UUID changed",
target_id=target_id,
scope="SYSTEM_INTEGRITY",
rule_id="SYS_IMMUTABILITY_CHECK"
)
)

```

**追加仕様**:
```

* violationが1件でもある場合：
  → Validation OK（INFO）は生成しない

```

**DoD**:
- UUID変更時に必ずCRITICALが生成される
- INFO結果が混在しない

**Execution Spec 優先に関する補足（後続確定仕様）**:

本 Work Plan 内の実装例：

```python
if str(previous.uuid) != str(target.uuid):
```

は Debug Work Plan 作成時点での暫定実装例である。

後続の正式仕様：

* `docs/spec/Execution_Spec/NWF_Consistency_Validator_Spec_v2.0.1_Phase_3.5.md`

において、

```text
10.6 UUID Missing Policy
```

が追加され、

* `previous.uuid is None`
* `entity.uuid is None`

は violation として扱わないことが正式確定された。

そのため最終実装では：

```python
if (
    previous_uuid is not None
    and current_uuid is not None
    and str(previous_uuid) != str(current_uuid)
):
```

を採用する。

したがって：

```text
UUID変更時に必ずCRITICALが生成される
```

の DoD は、

```text
「UUID が双方定義済みであり、
かつ値が変更された場合」
```

を意味する。

---

### 5. ValidationResult属性仕様の統一  
**ファイル**:  
src/integrity/consistency_validator.py（既存修正）

**作業内容**:
- 以下を必須属性として設定
  - `severity = CRITICAL`
  - `scope = "SYSTEM_INTEGRITY"`
  - `rule_id = "SYS_IMMUTABILITY_CHECK"`

**DoD**:
- すべての構造違反が同一フォーマットで出力される
- Pipeline処理において安定動作する

---

### 6. Entity ID正規化仕様の明文化  
**ファイル**:  
docs/spec/Core_Spec/NWF_Entity_ID_System_v2.0.1.md（既存修正）

**作業内容**:
- Entity IDは常に `str` とすることを明記
- UUIDオブジェクトは内部でカプセル化

**DoD**:
- ID型の揺れが完全排除される

---

### 7. StoryDB I/F仕様の明文化  
**ファイル**:  
docs/spec/Core_Spec/NWF_Story_Database_v2.0.1.md（既存修正）

**作業内容**:
- 以下を明文化：
  - `get(entity_id: str) -> Optional[Entity]`
  - 非存在時は `None` を返す

**DoD**:
- 全DB実装が統一I/Fに準拠

---

### 8. Specとコードの同期検証（追加必須）  
**ファイル**:  

docs/project/NWF_Phase_3.5_Debug_Work_Plan_v20260502.md（既存）  
docs/spec/Execution_Spec/NWF_Consistency_Validator_Spec_v2.0.1_Phase_3.5.md（既存）  
docs/spec/Execution_Spec/NWF_Validation_System_v2.0.1.md（既存）  
docs/spec/Execution_Spec/NWF_Validator_Orchestration_Spec_v2.0.1.md（既存）  
docs/spec/Execution_Spec/NWF_Mock_Design_Guideline_v2.0.1.md（既存）  
docs/spec/Core_Spec/NWF_Entity_ID_System_v2.0.1.md（既存）  
docs/spec/Core_Spec/NWF_Story_Database_v2.0.1.md（既存）  

src/integrity/consistency_validator.py（既存）  
src/integrity/validation_result.py（既存）  
src/models/nwf_object.py（既存）  
src/engine/story_engine.py（既存）  
src/integrity/__init__.py（新規）  
src/models/__init__.py（新規）  

tests/unit/test_validator_critical_only.py（既存）  
tests/integration_phase_3_4_validator.py（既存）  
tests/mocks/mock_story_db.py（新規）  

**作業内容**:

#### 8.1 Validator実装とExecution Specの同期確認

以下のSpecを正（Single Source of Truth）として使用する：

- docs/spec/Execution_Spec/NWF_Consistency_Validator_Spec_v2.0.1_Phase_3.5.md
- docs/spec/Execution_Spec/NWF_Validation_System_v2.0.1.md
- docs/spec/Execution_Spec/NWF_Validator_Orchestration_Spec_v2.0.1.md

以下を確認する：

- `ConsistencyValidator` が `story_db.get()` のみを使用している
- DB内部構造へ直接アクセスしていない
- `target_id` が必ず `str` 化されている
- UUID比較が正式仕様：

```python
if (
    previous_uuid is not None
    and current_uuid is not None
    and str(previous_uuid) != str(current_uuid)
):
```

に一致している

- violation存在時に INFO を生成していない
- `ValidationResult.failure()` の使用方法がSpecと一致している
- `severity`
- `scope`
- `rule_id`
- `target_id`

の設定がSpec準拠である

#### 8.2 Mock実装とStoryDB Interface仕様の同期確認

以下のSpecを正として使用する：

- docs/spec/Execution_Spec/NWF_Mock_Design_Guideline_v2.0.1.md
- docs/spec/Core_Spec/NWF_Story_Database_v2.0.1.md

以下を確認する：

- `MockStoryDB` が `get(entity_id: str)` を実装している
- 非存在Entity時に `None` を返している
- IDを `str` に正規化している
- Mockが内部dictへ直接アクセスさせていない
- Mock実装が本番StoryDB I/F契約と一致している

確認対象：

- tests/unit/test_validator_critical_only.py
- tests/mocks/mock_story_db.py

#### 8.3 Entity ID型仕様の同期確認

以下のSpecを正として使用する：

- docs/spec/Core_Spec/NWF_Entity_ID_System_v2.0.1.md

以下を確認する：

- Entity ID が外部I/F上すべて `str`
- UUID object が外部へ露出していない
- Validator / Engine / Mock 間で ID型揺れが存在しない
- `story_db.get()` 呼び出し時に常に `str` が渡される

確認対象：

- src/models/nwf_object.py
- src/integrity/consistency_validator.py
- src/integrity/validation_result.py
- src/engine/story_engine.py
- tests/unit/test_validator_critical_only.py
- tests/integration_phase_3_4_validator.py

#### 8.4 Import / Package整合性確認

以下を確認する：

- `src/integrity/__init__.py`
- `src/models/__init__.py`

が存在し、Python package import が安定している

以下を確認する：

- import path の循環参照が存在しない
- pytest 実行時に import error が発生しない
- Validator / Engine / Models 間 import が統一されている

#### 8.5 StoryDB Interface統一確認

以下を確認する：

- 全StoryDB実装が：

```python
get(entity_id: str) -> Optional[Entity]
```

に準拠している

- 非存在時 `None`
- 外部I/F上のID型は `str`
- Validator が StoryDB 実装差異に依存していない

確認対象：

- docs/spec/Core_Spec/NWF_Story_Database_v2.0.1.md
- tests/mocks/mock_story_db.py
- tests/unit/test_validator_critical_only.py
- src/integrity/consistency_validator.py
- src/integrity/validation_result.py

**DoD**:

- Specと実装の乖離がゼロ
- Validator実装がExecution Specと100%一致
- Mock実装がStoryDB I/F仕様と100%一致
- Entity ID型揺れが完全排除されている
- UUID比較仕様が正式仕様に一致
- INFO混在禁止仕様が完全実装されている
- StoryDB I/Fが全実装で統一されている
- pytest実行時に import error が発生しない
- Validator / Engine / Mock / Spec 間で論理矛盾が存在しない
- Single Source of Truth が全Specで統一されている

---

### 9. pytestによる検証実行  
**作業内容**:

```

python -m pytest -v

```

**検証項目（明文化）**:
- len(results) > 0
- CRITICALが存在する
- INFOが混在しない
- Engine.evaluate に渡した場合に停止する

**DoD**:
- 全テストPASS
- 副作用なし

---

### 10. Debugログの最終整理  
**ファイル**:  
src/integrity/consistency_validator.py（既存修正）

**作業内容**:
- UUID比較ログの確認
- 不要ログ削除 or DEBUG制御

**DoD**:
- 本番コードの可読性維持
- デバッグ情報の適切管理

---

## 4. リスクと対策

| リスク | 対策 |
|------|------|
| I/F不整合 | Spec明文化 + Mock修正 |
| ID型混在 | Entityレベルで正規化 |
| 実装ブレ | 本Planで仕様固定 |
| テスト不安定 | OK生成ルール明文化 |

---

## 5. 完了条件（Phase 3.5 Exit Criteria）

- pytest 全テストPASS
- Immutability違反がCRITICALとして確実に検出される
- INFO結果が混在しない
- Engineで停止が確認される
- story_db I/Fが全実装で統一
- Specと実装の乖離がゼロ

---

## 6. まとめ

本計画は、

- I/F契約の強制
- Validatorの純粋性維持
- 実装曖昧性の完全排除

を目的とした**実行可能な最終形（v2）**である。

これにより Phase 3.5 は  
「バグ修正」ではなく「構造の確定」として完了する。

---

[EOF]