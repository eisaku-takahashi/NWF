Source: docs/spec/Spec_Governance/NWF_Spec_Governance_Index_v2.0.1.md
Updated: 2026-03-29T00:23:00+09:00
PIC: Engineer / ChatGPT

# NWF Spec Governance Index v2.0.1

---

## 1. 概要

本ドキュメントは  
NWF v2.0.1 (Story OS) における全仕様書の統治・整合性・進化を管理する **マスタ索引** です。  
目的は以下の通りです。

- 全 Spec ファイルの統合的管理
- 仕様間依存関係の明示化と整合性維持
- AI と人間が協働して仕様の品質を保証
- 次世代 (v2.0.2 以降) への進化指針の提供

---

## 2. Spec 階層構造

NWF v2.0.1 は以下の 9 カテゴリで構成されています。

1. **Core Spec**  
2. **System Architecture Spec**  
3. **Architecture Spec**  
4. **Data Spec**  
5. **Engine Spec**  
6. **Execution Spec**  
7. **AI Interface Spec**  
8. **AI Workflow Spec**  
9. **Spec Governance**

各カテゴリは相互依存関係を持ち、更新時には Cross-Spec Synchronization が適用されます。

---

## 3. マスタファイル一覧 (v2.0.1)

| ファイル名 | カテゴリ | 概要 | 最終更新日 |
|------------|---------|------|------------|
| NWF_Spec_Standard_v2.0.1.md | Spec Governance | 全 Spec 共通の記述規約、用語定義、Markdown フォーマット | 2026-03-29 |
| NWF_Spec_Review_Process_v2.0.1.md | Spec Governance | AI 自動レビュー + HITL 承認フロー | 2026-03-29 |
| NWF_Spec_Version_Control_v2.0.1.md | Spec Governance | セマンティック・バージョニング、ロールバック規約 | 2026-03-29 |
| NWF_Spec_Integrity_Check_v2.0.1.md | Spec Governance | 仕様間の不整合・論理矛盾の検知手法 | 2026-03-29 |

---

## 4. Cross-Spec Dependency Map

- **Core / Architecture** → 全 Spec の根本規律を提供
- **Data / Engine** → 実行層の論理制約を担保
- **Execution / AI Workflow** → 動的運用手順の遵守
- **Spec Governance** → 版数管理・レビュー・整合性チェック

更新時は影響範囲を AI が分析し、必要に応じて Human-in-the-Loop により最終承認が行われます。

---

## 5. 統治プロトコル

1. **バージョン管理**  
   - Major / Minor / Patch に基づき変更履歴を管理
2. **レビュー**  
   - AI による自動チェック + 人間（Architect）による承認
3. **整合性チェック**  
   - Recursive Integrity により Spec 間矛盾を検出

---

## 6. AI 支援による保守

- 更新影響分析の自動化
- 不整合レポート生成
- 次世代 Spec への半自動反映

---

## 7. 人間の最終決定権限

- Architect ロールは、AI 提案に対する承認・修正・却下の最終権限を保持
- HITL プロセスにより仕様の品質と信頼性を保証

---

## 8. 変更履歴 (v2.0.0 → v2.0.1)

- Markdown フォーマット標準化
- Spec Standard の統一ルール化
- バージョン管理とレビュー手順の明確化
- 仕様整合性チェック (Recursive Integrity) の導入
- HITL 承認プロセスによる統治強化

---

[EOF]