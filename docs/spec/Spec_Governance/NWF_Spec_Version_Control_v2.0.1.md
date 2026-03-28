Source: docs/spec/Spec_Governance/NWF_Spec_Version_Control_v2.0.1.md
Updated: 2026-03-29T01:39:00+09:00
PIC: Engineer / ChatGPT

# NWF Spec Version Control v2.0.1

---

## 1. 概要

本仕様書は、NWF v2.0.1 における全仕様書の版数管理、ライフサイクル、および Git/GitHub 運用ルールを標準化することを目的とする。  
Semantic Versioning (SemVer) を軸に、AI による自動レビューと人間（Architect）による承認を組み合わせ、仕様変更の安全性と追跡可能性を担保する。

---

## 2. Semantic Versioning Rules

- **Major (X.0.0)**: 基本哲学、データ構造、実行パイプラインの非互換変更。Architect 承認必須。
- **Minor (0.X.0)**: 新機能追加や仕様拡張。AI 自動レビュー後に Architect 承認。
- **Patch (0.0.X)**: 誤字修正、表現明確化、Markdown調整。AI 自動承認および事後通知。

---

## 3. Branching & Repository Model

- 各 Spec は独立リポジトリまたはサブディレクトリで管理。
- `main` ブランチ: 安定版リリース
- `develop` ブランチ: 開発・検証
- Feature/Hotfix ブランチは SemVer に従い命名 (`feature/v2.0.1-minor`, `hotfix/v2.0.1-patch`)

---

## 4. Commit & PR Standards

- **Commit Message Format**: `[Action] File_Name: Description`
  - 例: `[Update] Data_Spec: Added hydrogen_fuel_cell schema`
- **Pull Request (PR) Policy**: Cross-Spec Impact を含む場合は関連ファイルの同時更新を義務化
- **AI Trigger**: PR 作成時に自動レビューを実行し、形式・依存関係・JSON 構造を検証

---

## 5. Impact Analysis & Cross-Sync

- バージョン更新に伴う他 Spec への影響を自動抽出
- 依存関係マップを作成し、影響範囲を文書化
- 必要に応じて Cross-Spec 同期更新を実施

---

## 6. Release & Tagging Policy

- **Stable Release Tag**: `v2.0.1-stable` など
- **Experimental Tag**: 開発中バージョンに `-experimental` を付与
- 安定版のみ Pull Request マージ後に main ブランチへ反映

---

## 7. Rollback Procedures

- **Automatic Revert Condition**: Integrity Check 失敗時または人間による不備検出時に即時ロールバック
- **Rollback Steps**:
  1. 対象コミットを revert
  2. PR に再提出
  3. Decision Log に理由を記録
- バージョン間依存関係を考慮した安全な復元プロセスを保証

---

## 8. Audit & Traceability

- 各ファイルヘッダーの `Updated` フィールドと Git コミット履歴を同期
- 変更理由（Why）を Decision Log として保存
- すべてのバージョン変更履歴を参照可能にする

---

## 9. Integration with Spec_Governance

- NWF_Spec_Review_Process と連携し、人間承認および自動検証のフローと統合
- Cross-Spec 同期・影響分析と組み合わせ、仕様変更の安全性を担保
- 仕様統治基盤（Spec_Governance）全体での整合性維持に貢献

---

[EOF]