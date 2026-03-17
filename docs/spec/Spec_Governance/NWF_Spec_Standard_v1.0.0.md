Source: docs/spec/Spec_Governance/NWF_Spec_Standard_v1.0.0.md
Updated: 2026-03-17T01:00:00+09:00
PIC: Engineer / ChatGPT

# NWF Spec Standard v1.0.0

---

## 1. 概要

本ドキュメントは  
Novel Writing Framework（NWF）における  
**仕様書・データファイル作成の標準規格**を定義する。

この規格は以下の目的で作成される。

- NWFドキュメント構造の統一
- AI生成物の品質安定
- Gitによる変更追跡の容易化
- エンジニア間の仕様理解の統一

本規格は

- Markdown
- JSON
- Text

などのNWF成果物すべてに適用される。

---

## 2. Metadata Header

すべてのNWFドキュメントは  
**必ずメタデータヘッダーから開始する。**

形式は以下とする。

1行目：Source  
2行目：Updated  
3行目：PIC

例

Source: docs/spec/Core_Spec/NWF_File_System_v2.0.0.md  
Updated: 2026-03-16T01:35:00+09:00  
PIC: Engineer / ChatGPT

項目定義

Source  
ファイルのNWFルートからの相対パス

Updated  
ISO 8601形式の更新日時（JST）

PIC  
Person In Charge  
担当者または役割

例

Engineer / ChatGPT

---

## 3. 1-Click Copy Rule

NWFで生成される成果物は  
**1クリックコピー可能な形式で出力する。**

ルール

1  
成果物全体を1つのコードブロックにまとめる

2  
ユーザーは右上のCopyボタンで全文をコピーできる

3  
表示崩れを防ぐため  
コードブロック内部ではバッククォートを使用しない

4  
Markdown内でコード例が必要な場合は  
代替表現を使用する

---

## 4. EOF Tag

すべてのNWF成果物は  
**最終行に EOFタグを記述する。**

形式

[EOF]

目的

- ファイル終端の明確化
- AI生成物の完全性確認
- Git差分確認の容易化

---

## 5. Data Format Rules

JSONデータには以下のルールを適用する。

### 5.1 Key Naming

キーは snake_case を使用する。

例

thread_id  
scene_index  
character_name

---

### 5.2 Unit Annotation

数値には可能な限り単位を明記する。

例

duration_seconds  
distance_km  
time_minutes

---

## 6. 適用範囲

本規格は以下に適用される。

- NWF Spec
- Engine Spec
- Plugin Spec
- JSONデータ
- AI生成成果物

---

## 7. まとめ

NWF Spec Standardは

- メタデータ管理
- コピー互換性
- データ規約

を統一することで

**NWFの長期的な拡張性と保守性を確保する。**

---

[EOF]