Source: docs/spec/Engine_Spec/NWF_QueryEngine_v2.0.0.md
Updated: 2026-03-17T22:20:00+09:00
PIC: Engineer / ChatGPT

# NWF QueryEngine v2.0.0

---

## 1. 概要

Query Engine はNWFデータに対する検索・抽出・分析を行うエンジンである。

---

## 2. クエリの定義

クエリとは条件式に基づくデータ抽出命令である。

---

## 3. Engine の役割

- データ検索
- 条件評価
- 結果出力

---

## 4. データ構造

query は以下を持つ。

- query_id
- target
- condition
- output_format

---

## 5. 評価規則

condition は論理式として評価される。

result = evaluate(condition, dataset)

---

## 6. 変換ロジック

- 対象データ取得
- 条件評価
- フィルタリング
- 出力整形

---

## 7. 制約

- condition はブール式
- target は既存エンジンのみ

---

## 8. 他Engineとの連携

全Engineと連携

---

## 9. 処理フロー

- クエリ受信
- 条件評価
- 結果出力

---

## 10. まとめ

Query Engine はNWFのデータアクセス基盤である。

---

[EOF]