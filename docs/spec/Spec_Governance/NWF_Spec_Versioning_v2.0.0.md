Source: docs/spec/Spec_Governance/NWF_Spec_Versioning_v2.0.0.md
Updated: 2026-03-19T01:10:00+09:00
PIC: Engineer / ChatGPT

# NWF Specification Versioning v2.0.0

---

## 1. 概要

本ドキュメントは  
NWFにおけるSpecのバージョン管理ルールを定義する。

目的

- 変更履歴の明確化
- Gitとの整合
- フレームワーク進化の追跡
- Spec間依存関係の管理

---

## 2. バージョン構造

形式

Major.Minor.Patch

例

v1.0.0  
v2.1.3  

---

## 3. Major

フレームワーク世代

互換性が破壊される変更（Breaking Change）

対象

- データ構造の変更
- API仕様の変更
- Engine仕様の非互換変更

例

v1 → v2

---

## 4. Minor

機能追加・構造拡張

後方互換あり

対象

- 新Spec追加
- セクション拡張
- 新機能追加

---

## 5. Patch

軽微修正

対象

- 誤字修正
- 表記修正
- 説明補足
- 非影響な仕様明確化

---

## 6. ファイル命名

File_Name_vX.Y.Z.md

---

## 7. vX.Y と vX.Y.Z

vX.Y は vX.Y.0 と同義

正式運用では vX.Y.Z を使用する

---

## 8. Spec依存関係

Specは相互に依存する場合がある

例

Core Spec → Engine Spec  
Spec Standard → 全Spec  

ルール

- 上位SpecのMajor変更は依存Specに影響する
- 依存関係は明示的に設計する

---

## 9. Git連携

Git Tagで管理する

例

spec-v2.0.0  

目的

- バージョン固定
- リリース管理
- 差分追跡

---

## 10. 更新ルール

Patch  
軽微修正

Minor  
機能追加

Major  
世代変更

---

## 11. JSON・Engineとの整合

Specバージョンは以下と整合する

- JSONデータ構造
- Engine仕様
- Pipeline処理

ルール

- Spec変更は対応するデータ構造と同期する
- 不整合が発生しないよう管理する

---

## 12. まとめ

本ルールにより

- Spec進化の可視化
- 依存関係の管理
- フレームワーク整合性

を実現する。

---

[EOF]