Source: docs/spec/Spec_Governance/NWF_Spec_Standard_v2.0.0.md
Updated: 2026-03-19T00:55:00+09:00
PIC: Engineer / ChatGPT

# NWF Spec Standard v2.0.0

---

## 1. 概要

本ドキュメントは  
Novel Writing Framework（NWF）における  
**仕様書およびデータファイル作成の標準規格**を定義する。

目的

- ドキュメント構造の完全統一
- AI生成物の品質安定
- Git差分の可読性向上
- 長期運用に耐える仕様基盤の確立

本規格は以下に適用される。

- Markdown
- JSON
- Text
- AI生成成果物

---

## 2. Metadata Header

すべてのドキュメントは  
**必ずメタデータヘッダーから開始する。**

形式

1行目 Source  
2行目 Updated  
3行目 PIC  

定義

Source  
NWFルートからの相対パス

Updated  
ISO 8601形式（JST）

PIC  
担当者または役割

---

## 3. 1-Click Copy Rule

すべての成果物は  
**1クリックで完全コピー可能な形式で出力する。**

ルール

- 成果物全体を1つのコードブロックにまとめる
- コードブロック内でバッククォートを使用しない
- 表示崩れを防ぐ構造にする

---

## 4. EOF Tag

すべての成果物は  
**最終行にEOFタグを記述する。**

形式

[EOF]

目的

- ファイル終端の明確化
- 完全性チェック
- Git差分の安定化

---

## 5. Data Format Rules

### 5.1 キー命名

snake_case を使用する

例

thread_id  
scene_index  

---

### 5.2 単位明記

数値には単位を含める

例

duration_seconds  
distance_km  

---

## 6. 適用範囲

本規格は以下に適用される

- Core Spec
- Engine Spec
- Plugin Spec
- System Architecture
- Spec Governance
- JSONデータ
- AI生成物

---

## 7. まとめ

本規格は

- 構造統一
- データ規約
- 出力形式

を定義し

**NWFの拡張性・保守性・再現性を保証する。**

---

[EOF]