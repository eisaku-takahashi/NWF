Source: docs/spec/Execution_Spec/NWF_Escalation_Logic_Spec_v2.0.1.md
Updated: 2026-04-25T07:15:00+09:00
PIC: Engineer / ChatGPT

# NWF Escalation Logic Spec v2.0.1

---

## 1. 概要

本仕様は、NWF v2.0.1 における Error Escalation（エラー昇格）ロジックを定義する。

本ロジックは、個別に検出された ERROR を統計的に評価し、
閾値を超過した場合に CRITICAL を生成することで、
システム全体の整合性崩壊を早期検知することを目的とする。

本仕様は以下の原則に従う：

- Pure Function（副作用なし）
- Deterministic（完全決定論）
- Monotonicity（昇格のみ）
- Non-destructive（非破壊）

---

## 2. 適用範囲

本ロジックは以下の Execution Pipeline において適用される：

- Validator（最終フェーズ）
- Analysis Engine（補助的評価）

処理順序：

1. RuleEvaluator
2. TemporalEvaluator（任意）
3. EscalationEvaluator（本仕様）

---

## 3. 入出力定義

### 3.1 関数シグネチャ

evaluate(results: List[ValidationResult], context: WorkflowContext) -> List[ValidationResult]

---

### 3.2 入力仕様

| フィールド | 説明 |
|----------|------|
| results | ValidationResult のリスト |
| context | WorkflowContext |

---

### 3.3 出力仕様

- 入力リストを変更せず、新規リストを返却する
- 元の ValidationResult を完全保持する
- 必要に応じて CRITICAL を追加する

---

## 4. カウントルール

### 4.1 対象

- severity == "ERROR" のみカウント対象
- CRITICAL は母数に含めない

---

### 4.2 集計単位

以下のペア単位でカウントする：

(scope, target_id)

---

### 4.3 重複扱い

- rule_id が同一でも個別にカウントする
- 集約は禁止

---

## 5. Threshold（閾値）仕様

### 5.1 取得方法

context.metadata.get("validation_thresholds", DEFAULT_THRESHOLDS)

---

### 5.2 デフォルト値

| scope | threshold |
|------|----------|
| scene | 5 |
| character | 3 |
| regional | 10 |
| global | 20 |

---

### 5.3 未知scope

未知の scope は global を適用する

---

## 6. CRITICAL生成ルール

閾値を超過した場合、新規 ValidationResult を生成する

---

### 6.1 生成条件

count >= threshold

---

### 6.2 フィールド仕様

| フィールド | 値 |
|----------|----|
| rule_id | "ESCALATION_" + scope.upper() + "_" + target_id |
| severity | CRITICAL |
| code | E999_THRESHOLD_EXCEEDED |
| message | "Threshold exceeded for {scope}:{target_id}. (Current: {count}, Limit: {threshold})" |
| target_id | 元対象 |
| span_id | sha256("escalation:{target_id}:{execution_id}") |
| source | escalation_evaluator |

---

## 7. 順序保証（Deterministic Ordering）

### 7.1 入力順序

- 入力リストはそのまま保持する

---

### 7.2 CRITICAL追加順序

- rule_id 順でソートして追加する

---

### 7.3 最終出力

result = original_results + sorted(new_criticals)

---

## 8. Monotonicity保証

### 8.1 許可

- ERROR → CRITICAL（追加のみ）

---

### 8.2 禁止

- ERROR の削除
- ERROR の書き換え
- CRITICAL のダウングレード

---

## 9. 非破壊性（Immutability）

- 入力 ValidationResult は変更しない
- 新規リストを生成する
- ValidationResult は immutable 前提

---

## 10. エッジケース

| ケース | 動作 |
|------|------|
| 空入力 | 空リスト返却 |
| threshold = 0 | 即 CRITICAL |
| ERROR = 0 | CRITICAL生成なし |

---

## 11. 擬似コード

```python
def evaluate(results, context):
    error_counts = Counter()

    for r in results:
        if r.severity == "ERROR":
            error_counts[(r.scope, r.target_id)] += 1

    thresholds = context.metadata.get("validation_thresholds", DEFAULT_THRESHOLDS)

    new_criticals = []

    for (scope, target_id) in sorted(error_counts.keys()):
        count = error_counts[(scope, target_id)]
        limit = thresholds.get(scope, DEFAULT_THRESHOLDS.get(scope, DEFAULT_THRESHOLDS["global"]))

        if count >= limit:
            new_criticals.append(
                create_critical(scope, target_id, count, limit, context)
            )

    return list(results) + sorted(new_criticals, key=lambda x: x.rule_id)
```

---

## 12. Logging要件

### 12.1 必須ログ

以下を出力する：

* scope
* target_id
* error_count
* threshold
* generated_critical_count

---

### 12.2 目的

* デバッグ
* 監査
* CRITICAL発生原因の追跡

---

## 13. 既存仕様との関係

本仕様は以下と整合する：

* NWF_Error_Model_v2.0.1
* Severity Monotonicity Rule
* ValidationResult Immutable原則

---

### 13.1 削除された設計

* ERROR累積無視
* 局所判定のみ

---

### 13.2 追加された設計

* Thresholdモデル
* 統計的CRITICAL生成
* 完全決定論順序

---

## 14. 制約事項

* target_id は正規化されている前提
* scope は定義済みであることが望ましい
* location resolution は未対応（Phase 3.6）

---

## 15. 将来拡張

### 15.1 Phase 3.6

* location resolution layer
* dynamic threshold
* temporal escalation

---

### 15.2 Phase 4以降

* probabilistic escalation
* anomaly detection
* adaptive threshold

---

## 16. 結論

本仕様により：

* ERROR の累積が可視化される
* CRITICAL が決定論的に生成される
* Validation Pipeline が非破壊構造となる
* 整合性崩壊の早期検知が可能となる

Escalation Logic は、NWF における整合性監視の最終防衛ラインである。

---

[EOF]