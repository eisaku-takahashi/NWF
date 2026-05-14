Source: docs/spec/Data_Spec/NWF_Rule_Data_Binding_Spec_v2.0.1.md
Updated: 2026-04-24T16:47:00+09:00
PIC: Engineer / ChatGPT

# NWF Rule Data Binding Spec v2.0.1

---

## 1. 概要

本仕様は、NWF World Rule DSL が参照可能なデータパス（Data Binding Path）を定義する。

目的：

- DSL評価時の参照対象を明確化する
- 不正アクセス・曖昧参照を排除する
- 決定論・安全性・再現性を保証する
- Spec-Code 一致を担保する

本仕様により、Rule Condition Engine は「許可されたパスのみ」を解決対象とする。

---

## 2. 基本原則

### 2.1 ホワイトリスト方式

- DSLは定義されたパスのみ参照可能
- 未定義パスは常に None を返却
- 例外は発生させない

---

### 2.2 ルートオブジェクト

DSLが参照可能なルートは以下の2つに限定する：

- entity
- context

それ以外のルートはすべて無効とする

---

### 2.3 Null安全

- パス途中で欠損が発生した場合：
  → 即座に None を返却
- Noneは評価時にFalseとして扱う（Comparison / Exists）

---

### 2.4 決定論保証

- 同一入力に対して常に同一値を返す
- 時刻・乱数・外部状態に依存しない

---

## 3. データ構造定義

### 3.1 entity

Entityはルール評価対象のオブジェクトである

#### 許可パス一覧

| パス | 型 | 説明 |
|------|----|------|
| entity.id | string | エンティティID |
| entity.type | string | エンティティ種別 |
| entity.properties | dict | 任意プロパティ格納 |
| entity.properties.* | any | 動的プロパティ |
| entity.state | string | 状態（任意） |
| entity.metadata | dict | メタ情報 |
| entity.metadata.* | any | 拡張情報 |

---

### 3.2 context

WorkflowContextは評価環境を表す

#### 許可パス一覧

| パス | 型 | 説明 |
|------|----|------|
| context.trace_id | string | トレースID（不変） |
| context.execution_id | string | 実行ID |
| context.metadata | dict | メタデータ |
| context.metadata.world_rules | list | ルール定義 |
| context.metadata.* | any | 拡張メタ情報 |
| context.scene_state | dict | シーン状態 |
| context.scene_state.* | any | 動的状態 |
| context.timestamp | string | 実行時刻（ISO 8601 JST） |

---

## 4. パス解決ルール

### 4.1 ドット記法

例：

entity.properties.mass  
context.scene_state.weather.temperature  

---

### 4.2 解決手順

1. ルート識別（entity または context）
2. キー逐次探索
3. 各ステップで以下を適用：

#### dict の場合
- key in dict → 値取得
- 存在しない → None

#### object の場合
- hasattr → getattr
- 存在しない → None

---

### 4.3 優先順位

1. dictキー  
2. 属性（attribute）

---

### 4.4 中断条件

以下の場合、即座に None を返却：

- 途中ノードが None
- キー未存在
- 型不一致アクセス

---

## 5. 禁止事項

以下は禁止する：

- eval の使用
- 動的コード実行
- 任意パスアクセス（ホワイトリスト外）
- 外部I/O参照
- グローバル状態参照

---

## 6. Exists 判定仕様

exists 演算子は以下で評価される：

- パス解決成功
- かつ値が None ではない

それ以外は False

---

## 7. 型ポリシー

| 条件 | 動作 |
|------|------|
| 型一致 | 正常比較 |
| 型不一致 | False（!=のみTrue） |
| None比較 | ==, !=のみ許可 |
| 数値比較 | int / float 許可 |

---

## 8. 拡張ポリシー

### 8.1 将来拡張

以下の領域は将来的に拡張可能：

- context.user_state
- context.system_state
- entity.relationships

追加時は必ず本Specを更新すること

---

### 8.2 後方互換性

- 既存パスの削除は禁止
- 新規追加は非破壊的に行う

---

## 9. Validation Rule

Rule Condition Engine は以下を保証する：

- ホワイトリスト外パス → None → False
- 例外ゼロ
- 副作用ゼロ
- 完全決定論

---

## 10. Cross-Spec Synchronization

本仕様は以下と同期する：

- docs/spec/Core_Spec/NWF_World_Rule_Model_v2.0.1.md
- docs/spec/Core_Spec/NWF_World_Rule_Execution_v2.0.1.md
- src/integrity/rule_condition_engine.py

変更時は全て同時更新すること

---

## 11. まとめ

本仕様により：

- DSLの参照範囲が完全に定義される
- 実装と仕様の乖離が防止される
- Rule Engineの安全性・再現性が保証される

これは NWF Phase 3.5 における

「決定論的ルール実行基盤」

の中核を構成する。

---

## 12. メッセージテンプレート・プレースホルダ仕様（拡張）

### 12.1 追加背景（本改訂の理由）

本仕様は元来「DSL評価時のデータ参照範囲」のみを定義していたが、  
RuleEvaluator 実装仕様において以下が必要となった：

- Action.message における **プレースホルダ展開**
- entity / context を用いた **動的メッセージ生成**
- 決定論・例外ゼロを維持したままの安全な解決

そのため、本セクションを **非破壊的拡張**として追加する。

※既存仕様は削除せず維持する（後方互換性保証）

---

### 12.2 プレースホルダ基本仕様

#### 形式

```

{<data_path>}

```

例：

```

{entity.id}
{entity.properties.name}
{context.scene_state.weather}

```

---

### 12.3 利用可能パス一覧（ホワイトリスト準拠）

プレースホルダで使用可能なパスは、**本Specで定義された Data Binding Path に完全準拠する**。

#### entity系

- {entity.id}
- {entity.type}
- {entity.state}
- {entity.properties.*}
- {entity.metadata.*}

#### context系

- {context.trace_id}
- {context.execution_id}
- {context.metadata.*}
- {context.scene_state.*}
- {context.timestamp}

---

### 12.4 ネストアクセス

ドット記法によりネスト解決可能：

例：

```

{entity.properties.profile.name}
{context.scene_state.weather.temperature}

```

解決ルールは **第4章 パス解決ルールを完全適用**する。

---

### 12.5 解決失敗時の挙動（重要）

従来仕様：
- パス解決失敗 → None

本拡張仕様（message限定）：
- パス解決失敗 → **空文字 "" に置換**

理由：

- メッセージ生成において None 表示は不自然
- 例外禁止ポリシー維持
- 決定論維持

---

### 12.6 None値の扱い

| 状態 | 出力 |
|------|------|
| 正常値 | 文字列化 |
| None | ""（空文字） |

---

### 12.7 型変換ルール

すべての値は以下のルールで文字列化：

- str → そのまま
- int / float → str()
- bool → "true" / "false"
- dict / list → JSON文字列（将来拡張対象）

---

### 12.8 禁止事項（プレースホルダ）

以下は禁止：

- 任意関数呼び出し
- フィルタ（例: | upper）
- 演算（例: +, -, *）
- 外部参照

理由：

- 決定論保証
- DSLの責務分離
- Condition Engineとの一貫性維持

---

### 12.9 仕様削除を行わなかった理由

本仕様において：

- 既存の Data Binding Path 定義
- Null安全仕様
- パス解決ロジック

はすべて **プレースホルダ仕様と完全に整合するため削除不要**

したがって：

- 削除は一切行わず
- 拡張のみで対応

---

### 12.10 Cross-Spec整合性

本拡張は以下仕様と整合：

- NWF_World_Rule_Execution_v2.0.1.md（message生成）
- RuleEvaluator 実装仕様（format_message）
- Condition Engine（同一パス解決ロジック）

---

## 13. 最終結論（改訂後）

本仕様は従来の：

- DSL参照制約定義

に加え、

- **メッセージ生成におけるデータ参照の完全定義**

を包含した。

これにより：

- Condition評価
- Message生成

が **同一のデータ参照モデルで統一**され、

NWF Phase 3.5 の

「完全決定論・副作用ゼロ・Spec-Code一致」

が保証される。

---

[EOF]
