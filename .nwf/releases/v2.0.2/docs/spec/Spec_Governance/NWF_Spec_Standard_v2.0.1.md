Source: docs/spec/Spec_Governance/NWF_Spec_Standard_v2.0.1.md
Updated: 2026-03-29T00:45:00+09:00
PIC: Engineer / ChatGPT

# NWF Spec Standard v2.0.1

---

## 1. 概要

本ドキュメントは  
NWF v2.0.1 における全仕様書の記述規約、データフォーマット、およびドキュメント構造の標準を定義する。

目的

- AI と人間（Architect）が共通言語で仕様を理解・記述・検証できるようにする
- Spec_Governance における自動整合性チェック（Recursive Integrity）の基盤を提供
- 仕様書間の依存関係および同期手順を明示化
- 長期運用に耐える拡張性と保守性を確保

---

## 2. Metadata & 1-Click Copy

### 2.1 Metadata Header

すべての Spec ファイルは冒頭に以下を必須とする

- Source: ファイルパス（NWF ルートからの相対パス）
- Updated: ISO 8601 形式の作成日時（JST）
- PIC: 担当者／役割（例: Engineer / ChatGPT）

### 2.2 1-Click Copy 構造

- ドキュメント全体はコードブロック内に記述する
- バッククォートは使用せず、表示崩れを防止
- 部分コードやテンプレートは必要に応じて別記号で代替

### 2.3 EOF タグ

- ファイル最終行に [EOF] を必ず付与
- 不完全な生成・転送や差分チェックを容易にする

---

## 3. ドキュメント構造

1. 概要（Overview）
2. Document Structure
   - ファイル命名規則
   - Metadata Header 構成
   - セクション階層
3. Writing Guidelines
   - 用語集参照
   - 記述トーン
   - 禁止表現
4. Data Formatting Rules
   - JSON / ID体系
   - 単位明記（例: sec, km, pts）
   - バージョン表記（Semantic Versioning）
5. Diagram & Visual Standards
   - Mermaid や [Image of X] タグの使用基準
6. Cross-Spec Sync Protocol
   - 他仕様書との参照と同期記述のテンプレート
7. Human-in-the-Loop Notation
   - 承認ゲートや人間介入ポイントの明示
8. Automated Validation Rules
   - NWF_Spec_Integrity_Check が使用する検証構文
9. Template
   - v2.0.1 準拠 Markdown テンプレート例

---

## 4. Data & Technical Notation

- JSON キーは snake_case を使用
- 数値には単位を明記（例: duration_sec, distance_km, integrity_pts）
- Spec 間依存関係を Cross-Spec Synchronization セクションに記述
- 仕様の重要度や検証厳密度をランク付けする Integrity Level を規定

---

## 5. Governance Integration

- Recursive Integrity により、仕様書自体の論理矛盾を検知
- HITL（Human-in-the-Loop）による承認プロセスを明記
- 仕様変更時は、Architect が最終承認を行う

---

## 6. Cross-Spec Synchronization

- Core / Architecture: 全 Spec の根幹規律
- Data / Engine: 実行層の論理制約
- Execution / AI Workflow: 動的運用手順
- Spec Governance: 仕様全体の品質・整合性管理

---

## 7. Template Example

```text
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

[EOF]
```

---

## 8. まとめ

本規格は

- 仕様書間の整合性を保証
- AI と人間が共通言語で記述・理解可能
- v2.0.1 以降の Story OS 仕様進化の基盤

を提供する。

---

[EOF]