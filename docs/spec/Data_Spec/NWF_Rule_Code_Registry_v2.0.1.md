Source: docs/spec/Data_Spec/NWF_Rule_Code_Registry_v2.0.1.md
Updated: 2026-04-26T20:08:00+09:00
PIC: Engineer / ChatGPT

# NWF Rule Code Registry v2.0.1

---

## 1. 概要

本ドキュメントは  
NWF v2.0.1 における World Rule の `code` フィールドを体系的に管理するためのレジストリ仕様を定義する。

目的：

- Rule Action における `code` の一意性と可読性を保証する
- スコープ・カテゴリ別のエラー分類を標準化する
- ValidationResult の機械処理および分析処理を容易にする
- Spec-Code 一致および決定論的運用を支援する

本レジストリは以下を保証する：

- 命名規則の厳格適用
- カテゴリ体系の明確化
- 拡張時の後方互換性維持
- 重複コードの禁止

---

## 2. Code 命名規則

### 2.1 基本フォーマット

すべての `code` は以下の形式を必須とする：

[SCOPE_INITIAL]-[CATEGORY_ID]-[SEQUENCE]

例：

- G-GEN-001
- C-STA-002
- W-RUL-010

---

### 2.2 各構成要素

#### ■ SCOPE_INITIAL（スコープ識別子）

| 値 | 意味 |
|----|------|
| G | Global |
| C | Character |
| W | World |
| S | Scene |
| R | Relationship |
| T | Temporal（Phase 3.6以降） |

---

#### ■ CATEGORY_ID（カテゴリ識別子）

3文字の英大文字で定義する。

| カテゴリ | ID | 説明 |
|----------|----|------|
| General | GEN | 汎用エラー |
| State | STA | 状態不整合 |
| Rule | RUL | ルール違反 |
| Constraint | CON | 制約違反 |
| Data | DAT | データ不正 |
| Integrity | INT | 整合性違反 |
| Logic | LOG | 論理エラー |

---

#### ■ SEQUENCE（連番）

- 3桁のゼロ埋め数値（001〜999）
- 同一 (SCOPE + CATEGORY) 内で一意
- 昇順で割り当て
- 再利用禁止（削除後も欠番維持）

---

## 3. コード定義ルール

### 3.1 一意性

- 全コードはグローバルに一意であること
- 重複は禁止

---

### 3.2 不変性

- 一度定義された code は変更不可
- 意味変更も禁止（新規コードを発行する）

---

### 3.3 可読性

- コードから意味カテゴリが推測可能であること
- Message と整合すること

---

### 3.4 拡張性

- 新カテゴリ追加時は CATEGORY_ID を追加
- 既存カテゴリの再定義は禁止

---

## 4. 登録済みコード一覧

### 4.1 Global（G）

#### General（GEN）

| Code | 説明 |
|------|------|
| G-GEN-001 | 汎用バリデーションエラー |
| G-GEN-002 | 未定義フィールド参照 |
| G-GEN-003 | Null値検出 |

---

#### Integrity（INT）

| Code | 説明 |
|------|------|
| G-INT-001 | 全体整合性違反 |
| G-INT-002 | データ不整合 |

---

### 4.2 Character（C）

#### State（STA）

| Code | 説明 |
|------|------|
| C-STA-001 | HP不正値 |
| C-STA-002 | ステータス範囲外 |
| C-STA-003 | 必須属性欠落 |

---

#### Rule（RUL）

| Code | 説明 |
|------|------|
| C-RUL-001 | キャラクタールール違反 |
| C-RUL-002 | 行動制約違反 |

---

### 4.3 World（W）

#### Rule（RUL）

| Code | 説明 |
|------|------|
| W-RUL-001 | ワールドルール違反 |
| W-RUL-002 | 物理制約違反 |

---

#### Constraint（CON）

| Code | 説明 |
|------|------|
| W-CON-001 | 環境制約違反 |
| W-CON-002 | リソース制約違反 |

---

### 4.4 Scene（S）

#### Logic（LOG）

| Code | 説明 |
|------|------|
| S-LOG-001 | シーン論理矛盾 |
| S-LOG-002 | 時系列不整合 |

---

### 4.5 Relationship（R）

#### Integrity（INT）

| Code | 説明 |
|------|------|
| R-INT-001 | 関係整合性違反 |
| R-INT-002 | 双方向不一致 |

---

## 5. Escalation との関係

- `ERROR` レベルの code は EscalationEvaluator により集計対象となる
- threshold 超過時に以下のコードが追加される：

| Code | 説明 |
|------|------|
| G-INT-999 | ERROR過多によるCRITICAL昇格 |

---

## 6. 運用ルール

### 6.1 新規コード追加手順

1. 対象スコープ・カテゴリを決定
2. 未使用の SEQUENCE を割り当て
3. 本レジストリへ追記
4. Spec 更新（World Rule Model）
5. Architect 承認（HITL）

---

### 6.2 廃止ポリシー

- コードは削除しない
- Deprecated フラグを付与（将来拡張）
- 互換性維持を優先

---

### 6.3 バリデーション

- CI にて code の重複チェックを実施
- JSON Schema によりフォーマット検証
- 未登録 code の使用は禁止

---

## 7. Cross-Spec Synchronization

本レジストリは以下の Spec と同期される：

- Core_Spec:
  - NWF_World_Rule_Model_v2.0.1.md
- Execution_Spec:
  - NWF_Error_Model_v2.0.1.md
  - NWF_Escalation_Logic_Spec_v2.0.1.md
- Data_Spec:
  - NWF_Metadata_DSL_Binding_v2.0.1.md

---

## 8. まとめ

本レジストリにより：

- Rule Action の code が完全に標準化される
- ValidationResult の解析・集計が容易になる
- Escalation および Error Model と整合する
- NWF 全体の決定論的実行とトレーサビリティが強化される

---

[EOF]