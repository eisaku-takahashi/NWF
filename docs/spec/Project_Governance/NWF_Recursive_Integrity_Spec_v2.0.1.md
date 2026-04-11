Source: docs/spec/Project_Governance/NWF_Recursive_Integrity_Spec_v2.0.1.md
Updated: 2026-04-12T00:43:00+09:00
PIC: Engineer / ChatGPT

# NWF Recursive Integrity Specification v2.0.1

---

## 1. 概要

本仕様書は、NWF v2.0.1 における **Recursive Integrity（再帰的整合性）システム** の定義である。

本システムは以下を目的とする：

- 出力データの自己検証（Self Validation）
- 矛盾検知（Contradiction Detection）
- 自動修復（Self-Healing）
- 因果律の維持（Causality Enforcement）
- AI生成物の信頼性担保

本仕様は Phase 2.5 の以下モジュールに適用される：

- src/integrity/integrity_checker.py
- src/integrity/consistency_validator.py
- src/integrity/recursive_auditor.py
- src/integrity/anomaly_detector.py

---

## 2. 核心思想

### 2.1 Spec Driven Recursive Validation

すべての検証は Spec を唯一の正とする。

検証は以下の3層で構成される：

1. Structural Integrity（構造）
2. Causal Integrity（因果律）
3. Narrative Integrity（物語整合性）

---

### 2.2 因果律優先順位

矛盾発生時の正当性優先順位：

1. World Rule Model
2. Story Database
3. HITL Input
4. AI Output

---

## 3. データフロー

WorkflowExecutor → Integrity Checker → Consistency Validator → Recursive Auditor → Anomaly Detector

---

## 4. モジュール構成

### 4.1 Integrity Checker

責務：

- NWFObject の検証
- JSON Schema 検証
- entity_id 検証
- timestamp 検証

入力：

- ExecutionResult

出力：

- ValidationResult

---

### 4.2 Consistency Validator

責務：

- 状態遷移検証
- transaction_id 整合性
- World Rule 検証

入力：

- WorkflowContext
- ValidationResult

出力：

- ConsistencyResult

---

### 4.3 Recursive Auditor

責務：

- 階層構造検証
- Timeline整合性
- Foreshadowing検証

入力：

- ConsistencyResult
- Story Data

出力：

- AuditReport

---

### 4.4 Anomaly Detector

責務：

- ハルシネーション検知
- 異常検出
- SUSPEND判定

入力：

- AuditReport

出力：

- FinalIntegrityResult

---

## 5. インターフェース定義（I/F Contract）

### 5.1 ExecutionResult（WorkflowExecutor 出力）

必須フィールド：

- status: str
- data: Optional[NWFObject]
- error_code: Optional[str]
- message: Optional[str]
- transaction_id: str
- timestamp: datetime

---

### 5.2 ValidationResult

- is_valid: bool
- errors: List[str]
- warnings: List[str]
- transaction_id: str
- timestamp: datetime

---

### 5.3 ConsistencyResult

- is_consistent: bool
- violations: List[str]
- transaction_id: str
- timestamp: datetime

---

### 5.4 AuditReport

- is_valid: bool
- issues: List[str]
- depth_checked: int
- transaction_id: str
- timestamp: datetime

---

### 5.5 FinalIntegrityResult

- status: SUCCESS | FAILURE | SUSPEND
- anomalies: List[str]
- requires_hitl: bool
- transaction_id: str
- timestamp: datetime

---

## 6. Workflow モジュールとの整合性

### 6.1 WorkflowExecutor との接続

- ExecutionResult を必ず入力とする
- 状態遷移は変更禁止

---

### 6.2 WorkflowStateMachine との整合

- Integrity 系は状態変更不可
- SUSPEND 判定のみ返却

---

### 6.3 WorkflowContext との整合

- transaction_id 必須
- context_data は read-only

---

## 7. 検証レベル

### Level 1（構造）

- 型チェック
- schemaチェック
- 必須フィールド

---

### Level 2（論理）

- 状態遷移
- 時系列整合性
- entity整合性

---

### Level 3（ナラティブ）

- 伏線
- 感情曲線
- 世界観整合性

---

## 8. SUSPEND 条件

以下の場合に SUSPEND：

- schema違反
- 因果律違反
- AI信頼度低下
- 修復不能エラー

---

## 9. 自己修復プロトコル

処理：

1. 矛盾検知
2. 優先順位評価
3. 低優先データ破棄
4. 再生成要求

---

## 10. 制約

- Spec未定義処理は禁止
- Engine直接操作禁止
- transaction_id 必須
- Audit必須

---

## 11. ログ / 監査

記録内容：

- validation結果
- consistency結果
- anomaly検知
- SUSPEND判定

---

## 12. 依存関係

- src/workflow/*
- src/models/nwf_object.py
- entity_schema.json
- metadata_schema.json
- AuditLogManager
- HITLManager

---

## 13. 拡張性

将来的拡張：

- 自動修復AI
- 重み付き整合性スコア
- リアルタイム監査

---

## 14. まとめ

本仕様は以下を保証する：

- 因果律維持
- 自己検証
- 自己修復
- AI信頼性担保
- 長期運用可能な整合性基盤

---

[EOF]