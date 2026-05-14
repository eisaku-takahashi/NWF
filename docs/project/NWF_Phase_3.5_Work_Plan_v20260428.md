Source: docs/project/NWF_Phase_3.5_Work_Plan_v20260428.md
Updated: 2026-04-28T20:40:00+09:00
PIC: Engineer / ChatGPT

# NWF Phase 3.5 Work Plan v20260428

---

## 1. 概要

本ドキュメントは  
NWF Phase 3.5 における Integration Test デバッグ以降の最終作業計画を定義する。

本計画は以下を目的とする：

- Spec / Code / Test の完全整合性確立
- 決定論的実行（Deterministic Execution）の保証
- 過去フェーズとの非破壊性（Non-Breaking）確認
- 将来の順序依存バグの再発防止

また、本計画は以下を前提とする：

- Phase 3.5 実装は正しい（Validator Orchestrator化）
- Phase 3.4 仕様は「出力順未定義」である
- 回帰エラーはテストの不備に起因する

---

## 2. 現状整理

### 完了済み

- Rule Action フォーマット定義（Step 8）
- Integration Test 実装（Step 9）
- test_conflict_resolution 修正
- Deterministic 検証（100%一致）
- Spec整合性レビュー（Core / Execution）

### 現在位置

- 回帰テスト確認（Step 6）

### 確定事項

- Breaking Change：NO
- 問題種別：Fragile Test（実装依存）
- リスク：Adapterにおける将来的順序依存

---

## 3. 作業一覧（実行順）

---

### 1. Phase 3.4 Spec差分監査（最終確定）

ファイル:
- docs/spec/Execution_Spec/NWF_Validation_System_v2.0.1.md（既存確認）
- docs/spec/Execution_Spec/NWF_Rule_Engine_Contract_v2.0.1.md（既存確認）

作業内容:

- 以下を明文化確認：

  - Validator出力順は未定義である
  - priorityは評価順専用である
  - 出力順に意味は存在しない

- 不足があれば追記：

  「Validatorの出力順は仕様上意味を持たない」

- ChatGPTで不確実な箇所はGeminiに調査依頼：

  - 「Phase 3.4時点での順序保証有無」
  - 「priorityの責務範囲」

DoD:

- Specに曖昧性ゼロ
- Breaking Changeでないことが仕様上確定

---

### 2. Adapter安全性保証（再発防止）

ファイル:
- src/integrity/validator_integration_adapter.py（既存修正）

作業内容:

- 以下をコードに明示：

```python
# DO NOT rely on order of ValidationResult list
# Always determine priority by severity/code explicitly
```

* 順序依存ロジックの有無を確認：

  * results[0] の使用禁止
  * sorted未指定使用の確認

* 必要に応じて修正：

  * max(severity) ベース選択
  * filter/reduce処理へ変更

* 不明点はGeminiへ調査依頼：

  * Adapterが依存する外部I/F仕様
  * UI/Audit連携の順序依存有無

DoD:

* 順序依存ロジックゼロ
* コメントにより設計意図固定
* 将来の誤用防止

---

### 3. Phase 3.4 テスト修正

ファイル:

* tests/integration_phase_3_4_validator.py（既存修正）
* tests/unit/test_validator_critical_only.py（既存修正）

作業内容:

* インデックス依存の完全排除：

  * results[0] 使用削除

* 修正パターン：

  1. assertEqual → assertCountEqual
  2. 先頭比較 → 包含チェック（any）
  3. 順序比較 → 決定論比較

例:

```python
self.assertTrue(any(r.code == "EXPECTED" for r in results))
```

* 自動変換が困難な場合はGeminiへ依頼：

  * 正規表現ベース変換
  * テスト意図保持変換

DoD:

* 全テストが仕様準拠
* Fragile Test完全排除

---

### 4. 全回帰テスト実行

ファイル:

* 全テスト

作業内容:

* 実行コマンド：

python -m pytest -v

* 確認項目：

  * 全テストPASS
  * 不安定テストゼロ
  * 実行ごとの差分ゼロ

DoD:

* FAIL=0
* Flaky Testなし

---

### 5. Deterministic保証の最終確認

ファイル:

* tests/integration_phase_3_5_world_rules.py

作業内容:

* test_deterministic_execution：

  * 100回一致確認
  * span_id含む完全一致

* ハッシュ比較検証（必要に応じて追加）

DoD:

* 再現性100%
* 非決定要素ゼロ

---

### 6. Validator仕様の最終明文化

ファイル:

* docs/spec/Execution_Spec/NWF_Validation_System_v2.0.1.md（既存修正）

作業内容:

* 以下を明記：

  1. 評価順と出力順の分離
  2. 出力順は決定論のためのみ存在
  3. priorityは出力順に影響しない
  4. 出力順は意味を持たない

* 必要に応じて例を追加

DoD:

* Spec-Code-Test完全一致
* 誤解の余地ゼロ

---

### 7. 最終統合確認（Spec Governance準拠）

ファイル:

* 全Spec

作業内容:

* Cross-Spec Synchronization確認：

  * Core / Execution / Architectureの整合性
  * Validator責務の一貫性

* Recursive Integrityチェック：

  * 論理矛盾の検出

* 不明点はGeminiへ調査依頼：

  * Spec間依存の欠落
  * 非同期更新リスク

DoD:

* Spec整合性100%
* Governance違反ゼロ

---

## 4. Definition of Done

本計画の完了条件：

* Phase 3.4 Spec整合性確認完了
* Adapter順序依存ゼロ
* 全テストPASS
* Deterministic保証成立
* Fragile Test完全排除
* Spec-Code-Test一致
* 再発防止策実装済

---

## 5. 結論

本フェーズの本質は：

「未定義だった順序を排除し、決定論として再定義すること」

である。

これにより：

* Validatorは純粋なOrchestratorとなる
* テストは仕様準拠へ収束する
* システムは再現性を獲得する
* 将来的なバグの再発が防止される

---

## 6. 次フェーズへの接続

Phase 3.6（Temporal）への前提：

* Deterministic Execution 完全保証
* Validator責務分離完了
* Rule Engineの純関数化完了

👉 本計画完了により、Phase 3.6へ安全に移行可能

---

[EOF]