Source: logs/audit/NWF_data_state_log_v2.0.1.md
Updated: 2026-04-05T03:45:00+09:00
PIC: Engineer / ChatGPT

# NWF Data State Log v2.0.1

---

## 1. 概要

本ドキュメントは、NWF v2.0.1 における Data Control System の監査ログ仕様を定義する。

本ログは、Entity の生成・更新・状態遷移・メタデータ操作・ワークフロー実行など、
すべての「因果的イベント」を時系列で記録することで、以下を実現する。

- 完全な監査可能性（Auditability）
- 状態遷移の追跡（Traceability）
- データ整合性の検証（Consistency Validation）
- 障害発生時のリプレイ復元（Replay Recovery）

---

## 2. ログの基本原則

### 2.1 Append-Only 原則

本ログは追記専用とし、以下を禁止する。

- 既存ログの書き換え
- ログ行の削除
- 並び順の変更

理由：
因果関係の改ざんを防止し、監査証跡の完全性を保証するため。

---

### 2.2 Sync-on-Write 原則

各 Transaction の完了時に、ログは必ずファイルへ同期書き込みされる。

理由：
システム障害時でも、直前の状態まで復元可能とするため。

---

### 2.3 一貫した時間管理

すべての Timestamp は JST 固定とする。

形式：
YYYY-MM-DDTHH:MM:SS+09:00

---

## 3. ログイベント定義

| イベント種別 | コード | 説明 |
|--------------|--------|------|
| Transaction | TXN_START | トランザクション開始 |
| Transaction | TXN_END | トランザクション終了 |
| Entity | ENT_CREATE | Entity 作成 |
| Entity | ENT_UPDATE | Entity 更新 |
| Entity | ENT_DELETE | Entity 削除 |
| State | ST_TRANSITION | 状態遷移 |
| Metadata | META_INJECT | メタデータ付与 |
| Metadata | META_UPDATE | メタデータ更新 |
| Version | VER_BUMP | バージョン更新 |
| Version | VER_TAG | バージョンタグ付与 |
| Workflow | WKF_EXEC | ワークフロー実行 |
| Workflow | WKF_STEP | ワークフローステップ |
| Spec | SPEC_VALIDATE | 仕様検証 |
| Security | AUTH_FAIL | 認可エラー |

---

## 4. ログフィールド仕様

| フィールド名 | 説明 |
|--------------|------|
| timestamp | JST ISO 8601 時刻 |
| log_id | LOG- プレフィックス付き UUIDv7 |
| txn_id | TXN- プレフィックス付き UUIDv7 |
| event_type | イベントコード |
| actor_id | 操作主体（USR / AI / SYS） |
| target_id | 対象 Entity / Spec ID |
| state_pre | 遷移前状態（任意） |
| state_post | 遷移後状態（任意） |
| payload_summary | JSON 形式の変更概要 |
| workflow_id | 関連ワークフロー ID（任意） |

---

## 5. ログフォーマット

本ログは Markdown Table 形式で記録する。

| Timestamp | Log ID | TXN ID | Event | Actor | Target | Summary |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |

---

## 6. ログ記録例

| 2026-04-05T03:21:00+09:00 | LOG-018e9a12-xxxx | TXN-018e9a12-xxxx | ENT_CREATE | AI-GEMINI | CHR-018e9a12-xxxx | {"type": "CHARACTER", "title": "Via"} |
| 2026-04-05T03:21:05+09:00 | LOG-018e9a13-xxxx | TXN-018e9a12-xxxx | ST_TRANSITION | USR-TAKAHASHI | CHR-018e9a12-xxxx | {"from": "DRAFT", "to": "REVIEW"} |

---

## 7. システム連携

### 7.1 DataStateManager

- 状態遷移（ST_TRANSITION）を記録
- 状態の整合性を保証

---

### 7.2 EntityManager

- ENT_CREATE / ENT_UPDATE / ENT_DELETE を発行
- Entity ライフサイクルの管理

---

### 7.3 MetadataManager

- META_INJECT / META_UPDATE を発行
- metadata の整合性を保証

---

### 7.4 VersionManager

- VER_BUMP / VER_TAG を発行
- バージョン管理の追跡

---

### 7.5 AuditLogManager

- 本ログへの書き込みを担当
- Transaction 単位での整合性保証

---

## 8. トランザクションモデル

すべての操作は Transaction ID に紐づく。

例：

TXN_START  
→ ENT_CREATE  
→ META_INJECT  
→ ST_TRANSITION  
→ VER_BUMP  
→ TXN_END  

理由：
操作単位での因果関係を完全に追跡するため。

---

## 9. 将来拡張（Kernel Audit System）

本ログは将来的に以下と連携する。

- ハッシュチェーン生成
- 改ざん検知
- 分散監査

設計思想：
ログを「改ざん不能な履歴」として扱う。

---

## 10. 設計哲学

NWF において、

「データはログの結果である」

すべての Entity は、このログに記録された因果の結果として存在する。

このログは、

- AI の意思決定
- 人間の操作
- システムの処理

を統一的に記録する「世界の履歴」である。

---

## 11. まとめ

本ログは以下を保証する。

- 完全な監査性
- 状態遷移の透明性
- データの再現可能性
- AI・人間協働の信頼性

NWF v2.0.1 において、本ログは Data Control System の中核を担う。

---

[EOF]