Source: docs/spec/Execution_Spec/NWF_Rule_Engine_Contract_v2.0.1.md
Updated: 2026-04-29T02:02:00+09:00
PIC: Engineer / ChatGPT

# NWF Rule Engine Contract v2.0.1

---

## 1. 概要

本ドキュメントは、NWF Phase 3.5 における RuleEvaluator と RuleConditionEngine 間のインターフェース契約（I/F Contract）を定義する。

目的：

- Evaluator と Condition Engine の責務境界を明確化する
- データ構造・入出力仕様を固定し、実装の自由度による非決定性を排除する
- 純関数・決定論・副作用ゼロの保証をシステムレベルで担保する
- 将来の Phase 3.6（Temporal Evaluator）との整合性を維持する

本契約は以下を保証する：

- 完全決定論（Deterministic Execution）
- 例外非伝播（Fail-safe False）
- データ参照の閉包性（Closed Data Scope）
- 副作用ゼロ（No Side Effects）

---

## 2. インターフェース仕様

### 2.1 Condition Engine

関数シグネチャ：

evaluate(condition: dict, data: dict) -> bool

### 2.2 入力データ構造

data は以下の固定構造を持つ：

{
  "context": WorkflowContext,
  "entity": Entity
}

### 2.3 出力保証

- 戻り値は必ず boolean
- True / False 以外の値は返却禁止

---

## 3. 異常系仕様（Fail-safe）

以下のすべてのケースにおいて、例外を外部に伝播せず False を返す：

- DSL構造不正
- 未定義オペレータ
- フィールド参照エラー
- 型不一致
- Null参照
- 実行時例外（すべて）

これにより、Evaluator は Condition Engine の内部状態に依存しない。

---

## 4. データ参照仕様

### 4.1 Entity

必須フィールド：

- id: str
- properties: dict

オプション：

- location_id: str | None

参照形式：

- entity.id
- entity.properties.<key>

---

### 4.2 WorkflowContext

必須フィールド：

- trace_id: str
- execution_id: str
- scene_id: str

オプション：

- metadata.world_rules: List[Rule]

参照形式：

- context.trace_id
- context.scene_id
- context.metadata.<key>

---

### 4.3 フィールドアクセス仕様

- ドット記法でアクセス
- dict / 属性の両方に対応
- ネスト構造を再帰的に解決

例：

entity.properties.mass  
context.metadata.world_rules  

---

### 4.4 Null安全仕様

- フィールド未存在時：
  → False を返す（例外禁止）

- None 値比較：
  → 常に False

---

## 5. message テンプレート展開仕様

### 5.1 基本仕様

- プレースホルダ形式：
  {entity.id}
  {entity.properties.name}
  {context.scene_id}

### 5.2 解決ルール

- ドット記法によるネスト解決
- dict / 属性の両対応
- 再帰的解決

### 5.3 実装制約

- Python str.format() 使用禁止
- eval 使用禁止
- 安全な置換（正規表現 or 専用パーサー）

### 5.4 エラー時挙動

- 未解決パス：
  → 空文字 "" に置換

- 例外：
  → 発生させない

---

## 6. ValidationResult 契約

### 6.1 データ構造

ValidationResult は以下の immutable dataclass とする：

@dataclass(frozen=True)
class ValidationResult:
    rule_id: str
    severity: str
    scope: str
    code: str
    message: str
    target_id: str
    trace_id: str
    span_id: str
    source: str = "rule_evaluator"

---

### 6.2 等価性保証

__eq__ 実装：

- span_id による完全比較

理由：

- span_id が全構成要素を一意に表現するため

---

### 6.3 span_id 生成仕様

生成式：

sha256(f"{trace_id}:{execution_id}:{rule_id}:{entity.id}".encode()).hexdigest()

仕様：

- アルゴリズム：SHA256
- 出力：64文字Hex
- 完全決定論
- 環境非依存

禁止事項：

- Python hash() 使用禁止

---

## 6.4 【追記】ValidationResultの順序非保証（Phase 3.4仕様明文化）

### 6.4.1 追加背景

Phase 3.4 において、ValidationResult の出力順序に関する明示的仕様が存在しなかったため、
実装依存の順序がテストやAdapterに影響を与える問題が発生した。

本追記は、その未定義領域を明文化し、仕様上の曖昧性を完全に排除するために追加される。

---

### 6.4.2 Phase 3.4時点の仕様（明確化）

ValidationResult のリスト（コレクション）において：

* 要素の**順序は仕様上保証されない**
* 順序は**実装依存であり意味を持たない**
* 特定インデックス（例：results[0]）に意味を持たせてはならない

---

### 6.4.3 明文化ルール（必須）

以下を正式仕様とする：

* ValidationResult は「集合的データ（Collection）」として扱う
* 出力順は**意味を持たない非保証要素**である
* 利用側（Adapter / Test / UI）は順序に依存してはならない

---

### 6.4.4 禁止事項

以下の実装を禁止する：

* results[0] 等のインデックス依存ロジック
* 順序前提の比較
* 暗黙の優先順位解釈

---

### 6.4.5 Phase 3.5との関係（重要）

Phase 3.5では以下が導入される：

* 決定論的ソート（Deterministic Ordering）

ただしこれは：

* **意味順序の導入ではない**
* **未定義順序の安定化（再現性確保）のみを目的とする**

---

### 6.4.6 Breaking Change 判定

本追記は：

* 新規仕様追加ではなく
* 未定義領域の明文化である

したがって：

**Breaking Change ではない**

---

## 6.5 【追記】priorityの責務範囲の明確化（Phase 3.4仕様確定）

### 6.5.1 追加背景

priority の役割が「評価順」と「出力順」で混同される可能性があったため、責務を明確に分離する。

---

### 6.5.2 Phase 3.4仕様（明文化）

priority は以下の用途にのみ使用される：

* RuleEvaluator における評価順制御
* 競合解決時の優先順位決定

---

### 6.5.3 非適用範囲（明確化）

priority は以下には影響しない：

* ValidationResult の出力順
* ValidationResult の並び順
* Deterministic Execution の順序定義

---

### 6.5.4 設計原則

* Evaluator：意味順序を持つ（評価順）
* Validator：意味順序を持たない（出力順）

---

### 6.5.5 禁止事項

* priority を出力順ソートに使用すること
* priority をUI表示順に使用すること
* priority を結果比較に使用すること

---

### 6.5.6 旧解釈の扱い（保持・無効化）

旧来の曖昧な解釈：

* priority により結果順序が暗黙的に決定される

これは以下の理由で無効化：

* 仕様未定義
* 実装依存
* Deterministic性を阻害

ただし：

* 過去実装理解のため削除せず保持する

---

### 6.5.7 Breaking Change 判定

本明文化は：

* 既存仕様の変更ではなく
* 責務の明確化である

したがって：

**Breaking Change ではない**

---

## 7. 純関数制約

### 7.1 禁止事項

- グローバル状態参照
- 時刻取得（datetime.now 等）
- I/O 操作
- ログ出力
- 乱数使用
- キャッシュ保持（Phase 3.5）

---

### 7.2 入力制約

- 入力データは不変として扱う
- 書き換え禁止

---

### 7.3 出力制約

- 新規オブジェクトのみ返却
- ミューテーション禁止

---

## 8. 決定論保証ルール

1. 同一入力 → 同一出力
2. 実行環境非依存
3. 評価順序固定（RuleEvaluator 側で保証）
4. Condition Engine は純粋判定のみ行う

---

## 9. 責務分離

### RuleEvaluator

- ルール選択
- ソート（決定論）
- Condition Engine 呼び出し
- ValidationResult 生成

### Condition Engine

- 条件評価のみ
- データ変換禁止
- 副作用禁止

---

## 10. まとめ

本契約により：

- Evaluator と Condition Engine の境界が明確化される
- すべての評価処理が純関数として成立する
- 非決定性の侵入経路が完全に遮断される
- Phase 3.6 への拡張基盤が確立される

本ドキュメントは Rule Engine 実装における最上位契約とする。

---

[EOF]