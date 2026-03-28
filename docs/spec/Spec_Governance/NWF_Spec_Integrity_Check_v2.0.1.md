Source: docs/spec/Spec_Governance/NWF_Spec_Integrity_Check_v2.0.1.md
Updated: 2026-03-29T02:48:00+09:00
PIC: Engineer / ChatGPT

# NWF Spec Integrity Check v2.0.1

---

## 1. 概要

本ドキュメントは、NWF v2.0.1 における全仕様書の整合性、参照不備、規格不適合を検知するプロトコルを定義します。
Recursive Integrity エンジンにより、AI 自動検証と人間（Architect）による最終承認を組み合わせ、仕様書間の論理矛盾を排除し、常に信頼性の高い設計基盤を維持することを目的とします。

---

## 2. Recursive Integrity Model

1. **仕様書間の再帰的検証**  
   - 各 Spec は、他 Spec の変更影響を自動解析し、更新の整合性を評価。
2. **階層的整合性**  
   - Core → Data → Engine → Execution → AI → Workflow → Governance の順に依存関係を解析。
3. **Integrity Score**  
   - 各 Spec に 0-100 pts で整合性スコアを算出。低スコア時は自動アラート。

---

## 3. Automated Scan Rules

- Metadata Consistency: `Source`, `Updated`, `PIC` 欄の存在と ISO 8601 形式確認。
- EOF Tag: ファイル末尾に `[EOF]` が存在するか。
- Notation Compliance: JSON キーは snake_case、数値には単位付与。
- 1-Click Copy: コードブロックで全文が保護されているか。

---

## 4. Logical Consistency Rules

- Broken Link Detection: 存在しないファイルパスや v2.0.0 参照を抽出。
- Dependency Paradox: Data Spec 変更が Engine/Execution に矛盾を生じさせないか。
- Cross-Spec Sync: 各 Spec の「影響範囲記述」が更新状況と一致するか。

---

## 5. Integrity Score for Specs

- スコア算出式: 
  - `metadata_score (20%) + structure_score (30%) + cross_spec_score (30%) + HITL_score (20%)`
- スコア分類:
  - 90-100 pts: Excellent
  - 70-89 pts: Good
  - 50-69 pts: Warning
  - <50 pts: Critical

---

## 6. HITL Validation Protocol

- Major/Minor 更新における Human Approval Gate 設置確認。
- 権限レベル（Observer〜Architect）の正確なマッピング。
- HITL 指摘事項は Decision Log に記録。

---

## 7. Decision Log & Audit Trace

- 各 Spec 更新時の判断理由と承認状況を記録。
- 不整合発見時は Rollback プロトコルに従い、Git/GitHub 上で安全に復元。
- Audit Log は Spec_Review_Process とリンク。

---

## 8. Automated Reporting Template

- 整合性診断レポート構造:
  - File Name
  - Integrity Score
  - Issue List (Metadata / Structure / Cross-Spec / HITL)
  - Recommended Action
  - Approval Status

---

## 9. Integration with Spec_Review_Process

- Integrity Check の結果は NWF_Spec_Review_Process に自動反映。
- 修正提案 → AI 自動スキャン → HITL 承認 → ログ記録 → 反映 のフローを確立。

---

[EOF]