Source: docs/spec/Execution_Spec/NWF_Integration_Test_Standard_Phase_3.5.md
Updated: 2026-04-27T08:52:00+09:00
PIC: Engineer / ChatGPT

# NWF Integration Test Standard Phase 3.5 v2.0.1

---

## 1. 概要

本ドキュメントは  
NWF Phase 3.5 における統合テストの標準仕様を定義する。

目的：

- Integration Test の入力データおよび期待出力構造を標準化する
- 決定論的検証（Deterministic Validation）の再現性を保証する
- Phase 3.x 系列におけるテスト資産の再利用性を確保する
- Spec-Code 一致をテストレベルで担保する

本仕様は以下を満たす：

- 完全決定論（Deterministic）
- 再現性100%
- テスト間の一貫性保証
- Spec準拠

---

## 2. 適用範囲

本仕様は以下に適用される：

- tests/integration_phase_3_5_world_rules.py
- Phase 3.x における全 Integration Test
- World Rule Execution Pipeline の検証

---

## 3. 標準テスト入力データセット

### 3.1 Entity & Metadata (Input)

以下は標準テスト入力の最小構成である。

```json
{
  "entity": {
    "entity_id": "CHAR-V001",
    "type": "character",
    "stats": {
      "hp": 0,
      "max_hp": 100
    }
  },
  "metadata": {
    "workflow_context": {
      "validation_thresholds": {
        "character": 1
      }
    },
    "traceability": {
      "validation_state": {
        "last_transaction_id": "test-fixed-tx",
        "is_deterministic": true
      }
    }
  }
}
````

### 3.2 World Rule (Sample)

```json
{
  "rule_id": "RULE-HP-CHECK",
  "scope": "character",
  "priority": 10,
  "trigger_logic": {
    "operator": "exists",
    "operands": ["stats.hp"]
  },
  "constraint_conditions": {
    "operator": "<=",
    "operands": ["stats.hp", 0]
  },
  "actions": [
    {
      "severity": "ERROR",
      "code": "C-ERR-001",
      "message": "HP is zero for {target_id}",
      "primary_target": "CHAR-V001"
    }
  ]
}
```

---

## 4. 標準期待出力構造

### 4.1 単一Rule評価

期待される ValidationResult：

* severity: ERROR
* code: C-ERR-001
* target_id: CHAR-V001
* rule_id: RULE-HP-CHECK

---

### 4.2 Escalation発動

条件：

* scope = character
* ERROR数 >= threshold（=1）

期待結果：

1. ERROR（元ルール）
2. CRITICAL（Escalation）

CRITICAL の仕様：

* severity: CRITICAL
* code: SYS-ESC-001
* message: Escalation: {count} errors detected in scope {scope}

---

### 4.3 DSL異常系

条件：

* 不正フィールド参照
* 不正演算子

期待結果：

* condition は False
* action は発火しない
* 必要に応じて ValidationResult(ERROR) を生成

---

### 4.4 Deterministic検証

条件：

* 同一入力を100回評価

期待結果：

* 出力リスト完全一致
* 並び順一致
* span_id 完全一致

---

## 5. 決定論保証仕様

### 5.1 span_id 生成

```
span_id = hash(rule_id + action_index + target_id + transaction_id)
```

テストでは以下を固定：

* transaction_id = "test-fixed-tx"

---

### 5.2 ソート順序

最終出力は以下でソート：

```
(scope, code, target_id)
```

---

### 5.3 比較ルール

ValidationResult の比較対象：

* severity
* code
* message
* target_id
* rule_id
* span_id

除外：

* timestamp（存在のみ検証）

---

## 6. Escalation標準仕様

* 対象：同一 scope
* カウント対象：ERROR以上
* 条件：threshold以上
* 動作：CRITICAL追加（昇格のみ）
* 順序：ERROR群の直後に挿入

---

## 7. DSL境界条件

* 最大深さ：16階層
* 超過時：

  * False を返す
  * DSL_DEPTH_EXCEEDED を記録
* 未定義フィールド：

  * False収束（例外禁止）

---

## 8. 再利用指針

本データセットおよび期待値構造は：

* Phase 3.5 以降の全Integration Testで再利用可能
* Rule追加時も基本構造は変更しない
* テスト拡張は「ケース追加」で行う

---

## 9. まとめ

本仕様により：

* Integration Test の完全決定論が保証される
* Spec-Code-Test の三位一体整合が確立される
* NWF は再現性のある検証基盤を獲得する

本ドキュメントは
Phase 3.x 系列のテスト基準として永続的に使用される。

---

[EOF]