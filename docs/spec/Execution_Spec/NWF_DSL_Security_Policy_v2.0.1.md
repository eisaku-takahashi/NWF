Source: docs/spec/Execution_Spec/NWF_DSL_Security_Policy_v2.0.1.md
Updated: 2026-04-26T19:40:00+09:00
PIC: Engineer / ChatGPT

# NWF DSL Security Policy v2.0.1

---

## 1. 概要

本ドキュメントは、NWF v2.0.1 における World Rule JSON DSL の安全性および決定論的実行を保証するためのセキュリティ・実行ポリシーを定義する。

目的：

- DSL 実行における任意コード実行の完全排除
- 決定論的評価の強制
- 計算量およびリソース使用の制御
- Engine 実装に対する制約の明文化
- Spec-Code 一致の担保

本ポリシーは、Phase 3.5 における RuleConditionEngine / RuleEvaluator の実装制約として適用される。

---

## 2. 適用範囲

本ポリシーは以下に適用される：

- data/schema/dsl_condition_schema.json
- RuleConditionEngine
- RuleEvaluator
- World Rule JSON 定義
- SpecLoader によるロード処理

---

## 3. 禁止事項（Security Restrictions）

DSL の安全性を担保するため、以下の操作を**完全禁止**とする。

### 3.1 動的コード実行の禁止

以下の使用を禁止する：

- eval()
- exec()
- import / require 等のモジュールロード
- 動的関数生成
- 文字列評価による式実行

理由：

- 任意コード実行によるセキュリティリスク排除
- 実行結果の非決定性防止

---

### 3.2 未定義オペレータの実行禁止

- dsl_condition_schema.json に定義されていない operator を評価してはならない
- 未定義 operator は必ず False を返す

---

### 3.3 JSONPath 拡張構文の禁止

以下の記法を禁止する：

- ワイルドカード: `*`
- 再帰検索: `..`
- フィルタ式: `[?()]`

許可される形式：

- ドット記法による絶対パスのみ
  - 例: entity.properties.mass

理由：

- 計算量の予測可能性確保
- 実装の単純化と安全性向上

---

### 3.4 外部状態アクセスの禁止

DSL 評価中に以下へのアクセスを禁止する：

- ファイルシステム
- ネットワーク
- 環境変数
- グローバル状態

DSL は純粋に以下のみを参照する：

- context
- entity
- metadata

---

### 3.5 副作用の禁止

DSL 評価は以下を満たす必要がある：

- 入力データの変更禁止
- グローバル状態変更禁止
- ログ出力等の副作用禁止

---

## 4. 決定論的評価制約（Deterministic Execution Constraints）

DSL は完全決定論的に評価されなければならない。

---

### 4.1 同一入力 → 同一出力保証

以下を満たすこと：

- 同一の context / entity / rule 入力に対し
- 常に同一の評価結果を返す

---

### 4.2 評価順序の固定

評価順序は以下の通り固定する：

1. trigger_logic
2. constraint_conditions（trigger が true の場合のみ）

---

### 4.3 論理演算の優先順位

演算優先順位：

1. NOT
2. AND
3. OR

同一階層：

- operands 配列のインデックス順で評価

---

### 4.4 短絡評価（Short-Circuit）

- AND: False が確定した時点で評価終了
- OR: True が確定した時点で評価終了

---

### 4.5 型比較ルール

- 異種型比較は必ず False
- 例外は発生させない

---

### 4.6 Null 安全性

- 存在しないフィールド参照は False
- 例外は禁止

---

### 4.7 exists 演算子仕様

exists は以下の場合に True：

- フィールドが存在する
- 値が null ではない

以下は True とみなす：

- 空文字 ""
- 空配列 []
- 空オブジェクト {}

---

### 4.8 浮動小数点比較

- 厳密等価比較は非推奨
- 必要に応じて誤差許容（1e-9）を内部処理で吸収

---

### 4.9 Rule 実行順序

- rule_id の ASCII 辞書順でソート
- 必ず固定順序で評価

---

## 5. リソース制約（Resource Constraints）

DSL 実行の安全性および性能保証のため、以下を定義する。

---

### 5.1 最大ネスト深度

- 再帰評価深度は最大 16
- 超過時は False を返す

---

### 5.2 計算量制限

- DSL 評価は O(n) を超えてはならない
- 再帰的爆発を防止する

---

### 5.3 タイムアウトポリシー

- 実装側で評価時間の上限を設定可能
- 超過時は False として処理

---

## 6. Spec Loader における強制バリデーション

DSL はロード時に以下を満たす必要がある：

- JSON Schema 準拠（dsl_condition_schema.json）
- 未定義 operator の不在
- ネスト深度制約の検証

違反時：

- ロード失敗（例外発生可）

---

## 7. Engine 実装制約

RuleConditionEngine は以下を満たす：

- 純関数（Pure Function）
- 副作用ゼロ
- 例外非発生（Fail-safe: False）
- 入力変更禁止

---

## 8. 資産管理およびSpec統合

本ポリシーは以下と連携する：

- docs/spec/Core_Spec/NWF_World_Rule_Model_v2.0.1.md
- docs/spec/Core_Spec/NWF_World_Rule_Execution_v2.0.1.md
- docs/spec/Data_Spec/NWF_Metadata_DSL_Binding_v2.0.1.md
- data/schema/dsl_condition_schema.json

---

### 8.1 既存Specへの影響

以下の仕様は本ポリシーに準拠する：

- DSL Condition 定義
- RuleEvaluator 実行仕様
- Validation Pipeline

---

### 8.2 将来拡張

本ポリシーは以下に対応可能：

- Temporal DSL（Phase 3.6）
- i18n message 解決
- 高度なルール最適化

ただし：

- 決定論性と安全性は常に最優先とする

---

## 9. まとめ

本ポリシーにより：

- DSL は完全に安全な評価モデルとなる
- 任意コード実行リスクは排除される
- Engine は純粋な決定論的評価器となる
- NWF は再現性100%のルール実行基盤を獲得する

---

[EOF]