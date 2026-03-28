Source: docs/spec/Spec_Governance/NWF_Spec_Review_Process_v2.0.1.md
Updated: 2026-03-29T01:22:00+09:00
PIC: Engineer / ChatGPT

# NWF Spec Review Process v2.0.1

---

## 1. 概要

本スペックは、NWF v2.0.1 における仕様書レビューおよび承認フローを規定する。  
AI による自動検証（Recursive Integrity）と人間（Architect）による最終判断を統合し、全 9 カテゴリの Spec 間の矛盾を排除、Story OS の設計品質を永続的に担保することを目的とする。

---

## 2. Section

### 2.1 AI Automated Review (自動検証フェーズ)
- **Recursive Integrity Check**: `NWF_Spec_Standard` に基づき、Markdown/JSON 構造、snake_case 命名、単位系を自動チェック。
- **Cross-Spec Impact Analysis**: 更新 Spec が他 Spec に与える論理的影響を抽出。
- **Reference Validation**: 不存在ファイルパスや旧バージョン参照の検知。

### 2.2 Human-in-the-Loop Approval (人間承認フェーズ)
- **Architect Role**: 最終承認権限。芸術的・論理的整合性を判断。
- **Approval Level**:
  - **Patch**: AI 自動承認（事後報告）。
  - **Minor**: Architect 承認必須。
  - **Major**: 全ステークホルダー合意と Architect 承認。
- **Rollback Protocol**: 検証失敗時や承認後不具合発見時に、`NWF_Spec_Version_Control` と連携し安全に前バージョンへ復元。

### 2.3 監査ログと透明性
- **Decision History**: 承認・却下理由を記録し、仕様進化過程を追跡可能とする。

### 2.4 レビュー全体フロー
1. 修正提案の提出
2. AI による自動検証
3. HITL Gate を通した Architect 承認
4. 修正反映と承認ログ記録
5. 必要に応じてロールバック対応

### 2.5 チェックリスト例
- Markdown 文法チェック
- JSON / データ構造の整合性
- 依存 Spec 参照の妥当性
- Cross-Spec Impact の明示
- 単位、ID、バージョン表記の適正

### 2.6 Integration with Spec Governance
- クロス Spec 依存関係の追跡
- Recursive Integrity 検証の自動化
- バージョン管理（Patch/Minor/Major）の承認プロセス統合

---

## 3. まとめ

NWF v2.0.1 のレビュー・承認プロセスは、AI による自動検証と人間による最終承認を統合することで、仕様書の不整合を構造的に排除し、Story OS の設計品質と信頼性を持続的に担保する。  
すべての Spec 更新は、自動チェック、HITL 承認、監査ログの保存を経て、バージョン管理下で安全に運用される。

---

[EOF]