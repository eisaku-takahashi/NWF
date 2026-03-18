Source: docs/spec/Spec_Governance/NWF_Spec_Writing_Guidelines_v2.0.0.md
Updated: 2026-03-19T00:55:00+09:00
PIC: Engineer / ChatGPT

# NWF Spec Writing Guidelines v2.0.0

---

## 1. 概要

本ドキュメントは  
NWFにおけるSpec作成ルールを定義する。

目的

- 構造統一
- 可読性向上
- 拡張性確保
- AI生成品質安定

---

## 2. 基本構造

Specは以下で構成する

1 概要  
2 仕様  
3 まとめ  

---

## 3. 粒度

1Spec = 1責務

大規模な場合は分割する

---

## 4. 分割原則

### 単一責任

1テーマのみ扱う

### 階層構造

System Architecture  
Core Spec  
Engine Spec  
Plugin Spec  
Spec Governance  

---

## 5. 命名規則

形式

File_Name_vX.Y.Z.md

ルール

- PascalCase
- アンダースコア区切り
- 明確な命名

---

## 6. カテゴリ

System_Architecture  
Core_Spec  
Engine_Spec  
Plugin_Spec  
Spec_Governance  

---

## 7. 変更ルール

Versioningに従う

Patch  
Minor  
Major  

---

## 8. AI生成ルール

- Metadata必須
- Markdown形式遵守
- EOF必須
- 責務明確化

---

## 9. 設計原則

- シンプル
- 拡張可能
- 人間とAI双方に可読
- Git追跡容易

---

## 10. まとめ

本ガイドラインは

- Spec品質の統一
- 長期運用の安定
- AI生成の最適化

を実現する。

---

[EOF]