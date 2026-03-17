Source: docs/spec/Spec_Governance/NWF_Spec_Writing_Guidelines_v1.0.0.md
Updated: 2026-03-17T02:10:00+09:00
PIC: Engineer / ChatGPT

# NWF Spec Writing Guidelines v1.0.0

---

## 1. 概要

本ドキュメントは  
Novel Writing Framework（NWF）における  
Specification（Spec）の作成ルールを定義する。

目的

- Spec構造の統一
- ドキュメントの可読性向上
- 長期的なSpec拡張性の確保
- AIによるSpec生成品質の安定

本ルールは以下に適用される。

- Core Spec
- Engine Spec
- Plugin Spec
- System Architecture Spec
- Spec Governance

---

## 2. Specの基本構造

NWF Specは以下の基本構造で作成する。

1 概要  
2 仕様または説明  
3 まとめ  

この構造により

- Specの目的
- 仕様内容
- 要点整理

が明確になる。

必要に応じて追加セクションを定義できる。

---

## 3. Specの粒度

Specは  
**1つの責務を持つドキュメントとして設計する。**

例

NWF_File_System  
ファイル構造のみを定義する

ThreadEngine_Spec  
Thread Engineの仕様のみを定義する

Specが大きくなりすぎる場合は  
複数のSpecに分割する。

---

## 4. Specの分割原則

Specは以下の原則に従って分割する。

### 4.1 単一責任原則

1つのSpecは  
1つの主要テーマのみを扱う。

例

正しい例

NWF_File_System  
NWF_Data_Model  
ThreadEngine_Spec  

誤った例

NWF_System_Design_All

---

### 4.2 階層構造

Specは以下の階層で整理する。

System Architecture  
フレームワーク全体構造

Core Spec  
データ構造・基盤仕様

Engine Spec  
各エンジンの仕様

Plugin Spec  
拡張機能仕様

Spec Governance  
Specルール

---

## 5. Spec命名規則

Specファイル名は以下の形式を使用する。

File_Name_vX.Y.Z.md

例

NWF_File_System_v2.0.0.md  
ThreadEngine_Spec_v1.0.0.md  
NWF_Data_Model_v2.0.0.md

命名ルール

- PascalCase を使用
- 単語はアンダースコアで区切る
- 機能内容が明確になる名前にする

---

## 6. Specカテゴリ

NWF Specは以下のカテゴリに分類される。

System_Architecture  
フレームワーク全体構造

Core_Spec  
基盤データ構造

Engine_Spec  
エンジン仕様

Plugin_Spec  
拡張機能仕様

Spec_Governance  
Spec管理ルール

---

## 7. Specの変更ルール

Spec変更は  
NWF Versioning Rules に従う。

変更の種類

Patch  
軽微修正

Minor  
仕様拡張

Major  
フレームワーク世代変更

---

## 8. AI生成Specのルール

AIがSpecを生成する場合  
以下のルールを守る。

- Metadata Header を必ず含める
- Markdown Format に従う
- EOF Tag を記述する
- Specの責務を明確にする

---

## 9. Spec設計の原則

NWF Specは以下の設計思想を採用する。

- シンプルであること
- 拡張可能であること
- AIと人間の双方が理解できること
- Git履歴が追跡しやすいこと

---

## 10. まとめ

NWF Spec Writing Guidelinesは  
Spec作成の設計ルールを定義する。

本ガイドラインにより

- Spec構造の統一
- 長期的なフレームワーク拡張
- AI生成ドキュメント品質向上

を実現する。

---

[EOF]