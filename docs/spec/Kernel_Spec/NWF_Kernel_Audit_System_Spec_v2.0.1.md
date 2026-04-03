Source: docs/spec/Kernel_Spec/NWF_Kernel_Audit_System_Spec_v2.0.1.md
Updated: 2026-04-03T20:48:00+09:00
PIC: Engineer / ChatGPT

# NWF Kernel Audit System Spec v2.0.1

---

## 1. 概要

本仕様は、NWF v2.0.1 における Kernel Layer の最下層基盤である Audit System を定義する。

Audit System は単なるログ機構ではなく、NWF OS におけるすべての事象を記録する「不変の記憶（Immutable Memory）」として機能する。

本システムは以下を保証する。

- 完全なトレーサビリティ
- 状態遷移の監査可能性
- AI / Workflow の意思決定の可観測性
- フォレンジック対応（事後検証）
- Spec Driven System の証拠基盤

---

## 2. 適用範囲

本仕様は以下に適用される。

- Kernel Layer（Event / State / Object）
- Core System
- Data Control System
- Execution Engine
- AI Interface
- Workflow Engine
- 外部入力・API
- ファイル操作

---

## 3. 基本原則（Kernel Constraints）

### 3.1 Append-Only

ログは追記専用とする。

- 更新禁止
- 削除禁止
- 上書き禁止

---

### 3.2 Immutable

ログは不変である。

- 改ざん不可
- 永続保存

---

### 3.3 JST固定

すべての時刻は JST で統一する。

形式：

YYYY-MM-DDTHH:MM:SS+09:00

---

### 3.4 JSONL形式

ログは JSON Lines 形式で保存する。

- 1行 = 1イベント
- UTF-8

---

## 4. Audit Event データ構造

### 4.1 必須フィールド

| フィールド | 型 | 説明 |
|------------|----|------|
| event_id | string | UUID |
| timestamp | string | JST ISO8601 |
| event_type | string | イベント種別 |
| actor | string | 実行主体 |
| object_id | string | 対象ID |
| spec_id | string | Spec ID |
| action | string | 実行内容 |
| status_before | string | 変更前 |
| status_after | string | 変更後 |
| transaction_id | string | トランザクションID |

---

### 4.2 Actor 定義

actor は以下の形式を許容する。

- user:12345
- system:loader
- system:event_manager
- ai:chatgpt
- workflow:engine

---

### 4.3 任意フィールド

| フィールド | 型 | 説明 |
|------------|----|------|
| context | dict | 実行文脈 |
| payload | dict | 入出力 |
| error | string | エラー |
| metadata | dict | 拡張 |

---

## 5. Transaction 管理

### 5.1 Transaction ID

- 処理単位ごとに付与
- 同一処理のイベントを紐付け

---

### 5.2 Context 伝播

transaction_id は以下により伝播される。

- contextvars によりスレッド・非同期間で保持
- Logger 内部で自動付与

---

### 5.3 Context Manager

Audit Logger は以下の形式をサポートする。

例：

with transaction("OBJECT_UPDATE"):
    処理

このスコープ内のすべてのログに同一 transaction_id が付与される。

---

## 6. Event Type

- SYSTEM_START
- OBJECT_CREATED
- STATE_TRANSITION
- DATA_UPDATED
- EVENT_EMITTED
- AI_EXECUTION
- WORKFLOW_EXECUTION
- FILE_OPERATION
- ERROR
- EXCEPTION

---

## 7. Event Manager 連携

- Event 発行時に自動記録
- 非同期イベントも対象
- Event 自体も監査対象

---

## 8. State Machine 連携

- 遷移前後を記録
- 検証結果を記録
- 不正遷移も記録

---

## 9. AI / Workflow 連携

以下を記録する。

- 入力
- 出力
- 使用Spec
- 判断根拠

---

## 10. ファイル管理

### 10.1 保存形式

JSONL

---

### 10.2 命名規則

audit_YYYYMMDD.jsonl

---

### 10.3 ログローテーション

- 日付変更時に自動切替
- 実行時に日付チェック
- ファイルハンドル再生成

---

## 11. 初期化順序

Audit System は最優先で初期化される。

理由：

- 他モジュールのエラーを記録するため
- Loader より先に起動

---

## 12. セキュリティ

- 改ざん防止（将来：ハッシュチェーン）
- アクセス制御
- マスキング対応

---

## 13. 拡張性

- ハッシュ連鎖
- 分散ログ
- 外部監査API
- リアルタイム監視

---

## 14. 実装対応

対応ファイル：

src/core/audit_logger.py

クラス：

KernelAuditLogger

---

## 15. まとめ

本システムは、

「すべてを記録し、決して忘れない」

という原則に基づく。

これにより NWF は

- 完全な透明性
- AI判断の説明可能性
- データの真正性

を保証する。

---

[EOF]