Source: docs/spec/Spec_Governance/NWF_Markdown_Format_v2.0.0.md
Updated: 2026-03-19T01:10:00+09:00
PIC: Engineer / ChatGPT

# NWF Markdown Format v2.0.0

---

## 1. 概要

本ドキュメントは  
NWFにおけるMarkdown記述の標準フォーマットを定義する。

目的

- ドキュメント構造の統一
- 可読性の最大化
- AI生成の安定化

---

## 2. 基本テンプレート

すべてのMarkdownは以下の構造を使用する

Source: docs/spec/<Spec_Category>/<File_Name>.md  
Updated: YYYY-MM-DDTHH:MM:SS+09:00  
PIC: Engineer / ChatGPT  

# Document Title vX.X.X

---

## 1. 概要

説明

---

## 2. Section

説明

---

## 3. まとめ

説明

---

（注）  
EOFタグはテンプレート内には含めず、  
**実際のファイル最終行にのみ記述すること**

---

## 3. 見出しルール

使用階層

# タイトル  
## セクション  
### サブセクション  

---

## 4. セクション構造

基本構造

1 概要  
2 仕様または説明  
3 まとめ  

必要に応じて拡張可能

---

## 5. バージョン表記

タイトルには必ずバージョンを含める

例

NWF_File_System v2.0.0  
ThreadEngine Spec v1.0.0  

---

## 6. まとめ

本フォーマットは

- 統一構造
- 高可読性
- AI適合性

を実現するための標準である。

---

[EOF]