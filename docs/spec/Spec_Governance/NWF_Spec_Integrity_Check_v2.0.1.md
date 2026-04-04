Source: docs/spec/Spec_Governance/NWF_Spec_Integrity_Check_v2.0.1.md
Updated: 2026-04-04T15:09:00+09:00
PIC: Engineer / ChatGPT

# NWF Spec Integrity Check v2.0.1

---

## 1. 概要

本ドキュメントは、NWF v2.0.1 における全仕様書の整合性、参照不備、規格不適合を検知するプロトコルを定義します。
Recursive Integrity エンジンにより、AI 自動検証と人間（Architect）による最終承認を組み合わせ、仕様書間の論理矛盾を排除し、常に信頼性の高い設計基盤を維持することを目的とします。

また、本 Integrity Check は NWF_Kernel_Audit_System と連携し、仕様書の変更・検証・承認のすべてのプロセスを監査ログとして記録し、仕様変更の説明責任（Accountability）およびトレーサビリティを確保します。

---

## 2. Recursive Integrity Model

1. 仕様書間の再帰的検証  
   - 各 Spec は、他 Spec の変更影響を自動解析し、更新の整合性を評価。

2. 階層的整合性  
   - Kernel → Core → Data → Engine → Execution → AI → Workflow → Governance の順に依存関係を解析。
   - 特に Kernel Layer（Audit / Logging / Transaction）は全レイヤーの Root of Trust として扱う。

3. Integrity Score  
   - 各 Spec に 0-100 pts で整合性スコアを算出。低スコア時は自動アラート。

4. Audit Traceability  
   - すべての Integrity Check 実行は transaction_id を持ち、Audit Log に記録される。
   - 各 Spec は last_audit_transaction_id を保持し、最後に整合性確認されたトランザクションを追跡可能とする。

---

## 3. Automated Scan Rules

Integrity Engine は以下の自動スキャンを実施する。

- Metadata Consistency  
  - Source, Updated, PIC 欄の存在確認
  - Updated は ISO 8601 (JST) 形式であること

- EOF Tag  
  - ファイル末尾に [EOF] が存在するか

- Notation Compliance  
  - JSON キーは snake_case
  - 数値データには単位が明記されていること

- 1-Click Copy  
  - 成果物全体が単一コードブロックで保護されているか

- Version Consistency  
  - 参照している Spec のバージョンが v2.0.1 と一致しているか
  - 旧バージョン参照が残っていないかを検出

すべてのスキャン結果は Audit Logger に送信され、scan_result イベントとして記録される。

---

## 4. Logical Consistency Rules

- Broken Link Detection  
  - 存在しないファイルパスや古いバージョン参照を抽出

- Dependency Paradox  
  - Data Spec 変更が Engine / Execution / AI に矛盾を生じさせないかを検証

- Cross-Spec Sync  
  - 各 Spec の「影響範囲記述」が更新状況と一致するかを確認

- Kernel Compliance Check  
  - すべての Spec が Audit System / Transaction / Logging の仕様に準拠しているか確認

- Audit Reference Integrity  
  - Spec 内で参照される transaction_id, event_id, entity_id の形式が ID System Spec と一致するか検証

これらの論理チェック結果もすべて監査ログへ記録される。

---

## 5. Integrity Score for Specs

Integrity Score は以下の要素から算出する。

- metadata_score (20%)
- structure_score (20%)
- cross_spec_score (25%)
- audit_compliance_score (20%)
- hitl_score (15%)

スコア分類:

- 90-100 pts: Excellent
- 70-89 pts: Good
- 50-69 pts: Warning
- <50 pts: Critical

Critical 判定の場合、Spec は Release Block 状態となり、Architect 承認なしでは適用不可とする。

Integrity Score 計算イベントは audit_event_type = "integrity_score_calculated" として記録する。

---

## 6. HITL Validation Protocol

Human-In-The-Loop による検証プロトコルを以下に定義する。

- Major / Minor 更新における Human Approval Gate 設置確認
- 権限レベル（Observer〜Architect）の正確なマッピング確認
- HITL 指摘事項は Decision Log に記録
- 承認 / 却下 / 差し戻し のアクションはすべて Audit Log に actor 情報付きで記録

HITL アクションログ例:

- event_type: spec_approval
- actor: user:architect_id
- target_spec: spec_file_path
- decision: approved / rejected / revision_required
- comment: approval_reason

---

## 7. Decision Log & Audit Trace

本セクションでは Spec 更新における意思決定履歴と監査ログの関係を定義する。

- 各 Spec 更新時の判断理由と承認状況を Decision Log に記録
- Decision Log は Audit Log の transaction_id と必ず紐付ける
- 不整合発見時は Rollback プロトコルに従い Git/GitHub 上で安全に復元
- Git Commit Hash を Audit Log に記録し、Spec バージョンと実行履歴を完全に紐付ける

これにより以下のトレーサビリティを実現する。

Spec Version → Commit Hash → Transaction ID → Audit Log → Decision Log → Actor

---

## 8. Automated Reporting Template

整合性診断レポート構造を以下に定義する。

- file_name
- spec_version
- integrity_score
- audit_compliance_score
- issue_list
  - metadata
  - structure
  - cross_spec
  - audit
  - hitl
- recommended_action
- approval_status
- last_audit_transaction_id

このレポートは integrity_report_generated イベントとして Audit Log に保存される。

---

## 9. Integration with Spec_Review_Process

Integrity Check の結果は NWF_Spec_Review_Process に自動反映される。

標準フロー:

1. Spec 修正提案
2. AI 自動 Integrity Scan
3. Audit Log 記録
4. Integrity Score 算出
5. HITL 承認プロセス
6. Decision Log 記録
7. Git Commit / Version 更新
8. Master Index 更新
9. Audit Log に最終確定イベント記録

この一連の流れにより、NWF 仕様書管理は完全な監査対応型ガバナンスプロセスとして運用される。

---

## 10. Dynamic Integrity Monitoring

本 Integrity System は静的チェックだけでなく、監査ログを用いた動的整合性チェックを実施する。

- 実行ログと Spec 定義の不一致検出
- 未定義イベントの検出
- 不正 actor による操作の検出
- Spec に存在しないデータ構造の使用検出

これにより以下を保証する。

- Spec と Implementation の乖離検出
- 不正操作の検出
- システム運用の透明性
- 完全な説明責任

Dynamic Integrity Monitoring の結果は periodic_integrity_audit イベントとして定期的に記録される。

---

## 11. Summary

NWF Spec Integrity Check は以下を目的とする。

- 仕様書間の論理整合性維持
- バージョン整合性管理
- Human-In-The-Loop 承認管理
- Audit System との完全連携
- Spec と実装の動的整合性検証
- システム全体の説明責任とトレーサビリティ確保

本仕様は NWF Governance Layer における整合性管理の中核を担う。

---

[EOF]