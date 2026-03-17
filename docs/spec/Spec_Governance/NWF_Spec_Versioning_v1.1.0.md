Source: docs/spec/Spec_Governance/NWF_Spec_Versioning_v1.1.0.md
Updated: 2026-03-17T01:30:00+09:00
PIC: Engineer / ChatGPT

# NWF Specification Versioning v1.1.0

---

## 1. 概要

本ドキュメントは  
Novel Writing Framework（NWF）における  
Specification（Spec）のバージョン管理ルールを定義する。

目的

- Spec変更履歴の明確化
- Git管理との整合
- フレームワーク進化の追跡

本ルールは以下に適用される。

- Core Spec
- System Architecture Spec
- Engine Spec
- Plugin Spec
- Spec Governance

---

## 2. Version Structure

NWF Specは以下の3段階バージョン構造を採用する。

Major.Minor.Patch

例

v1.0.0  
v1.2.3  
v2.0.0

本構造は Semantic Versioning の考え方をベースとしている。

---

## 3. Major Version

Major Version は  
**フレームワーク世代**を示す。

互換性が大きく変わる場合に更新される。

例

v1  
v2

例

NWF v1 → 初期アーキテクチャ  
NWF v2 → 新アーキテクチャ

---

## 4. Minor Version

Minor Version は  
**Spec全体の構造変更または機能拡張**を示す。

後方互換が維持される場合が多い。

例

v1.0  
v1.1  
v1.2

例

Spec章構造変更  
新Spec追加  
Engine拡張

---

## 5. Patch Version

Patch Version は  
**軽微な修正**を示す。

例

v1.0.0  
v1.0.1  
v1.0.2

対象

- 誤字修正
- 表記修正
- 小さな説明追加
- 軽微な仕様補足

例

v1.0.0 → v1.0.1 → v1.0.2

---

## 6. File Naming Rule

NWF Specファイルは  
以下の命名規則を使用する。

File_Name_vX.Y.Z.md

例

NWF_File_System_v1.0.0.md  
ThreadEngine_Spec_v1.2.0.md  
NWF_System_Architecture_v2.0.0.md

---

## 7. v1.0 と v1.0.0 の扱い

NWF Specでは以下のルールを採用する。

ファイル名_v1.0.md は  
ファイル名_v1.0.0.md と  
**同一のものとみなす。**

理由

- ドキュメント可読性向上
- バージョン表記の簡略化

推奨

正式Specでは  
vX.Y.Z 表記を使用する。

---

## 8. Git Tag

Spec Versionは  
Git Tagとして管理することが推奨される。

例

spec-v1.0  
spec-v1.1  
spec-v2.0

目的

- Spec履歴の追跡
- フレームワーク世代管理
- リリース管理

---

## 9. Version Update Guidelines

### Patch Update

軽微な修正の場合

例

v1.0.0 → v1.0.1

---

### Minor Update

Spec構造変更または拡張

例

v1.0 → v1.1

---

### Major Update

フレームワーク世代変更

例

v1 → v2

---

## 10. まとめ

NWF Specification Versioningは  
Spec進化を管理するための  
統一バージョンルールを定義する。

本ルールにより

- Spec履歴の明確化
- Git管理との整合
- NWF長期発展

を実現する。

---

Version: v1.1.0

---

[EOF]