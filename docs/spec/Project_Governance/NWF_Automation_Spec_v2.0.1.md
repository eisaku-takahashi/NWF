Source: docs/spec/Project_Governance/NWF_Automation_Spec_v2.0.1.md
Updated: 2026-04-14T07:05:00+09:00
PIC: Engineer / ChatGPT

# NWF Automation Spec v2.0.1

---

## 1. 概要

本仕様書は、NWF Phase 2.8 における Automation Layer の正式仕様を定義する。  
Automation Layer は、Event駆動による自律実行・整合性維持・リリース・同期・修復を統合し、NWFを「受動的ツール」から「自律型執筆エコシステム」へ進化させる。

本仕様は以下4モジュールの実装指針を提供する。

1. src/automation/event_trigger.py  
2. src/automation/workflow_automation.py  
3. src/automation/auto_repair_engine.py  
4. src/automation/system_orchestrator.py  

---

## 2. アーキテクチャ概要

### 2.1 モデル

Reactive Kernel & Autonomous Shell

- Kernel: Integrity / Validation / State管理
- Shell: Event駆動による自律実行

### 2.2 データフロー

EventTrigger → SystemOrchestrator → WorkflowAutomation → 各Manager  
異常時 → AutoRepairEngine → SystemOrchestrator

---

## 3. 共通設計ルール

### 3.1 時刻管理
- 全てのtimestampは ISO8601 JST (UTC+9)
- 例: 2026-04-14T07:00:00+09:00

### 3.2 エラーコード
- 形式: ERR_<DOMAIN>_<NNN>
- 例: ERR_AUT_001, ERR_INT_002

### 3.3 ログ出力
- audit_log_manager 経由のみ許可
- 直接print禁止

### 3.4 型定義
- Python typing必須
- dataclass使用推奨

---

## 4. Event Model（I/F Contract）

### 4.1 NWFEvent 定義

{
  "event_id": "string",
  "event_type": "string",
  "source": "string",
  "timestamp_jst": "string",
  "payload": "dict"
}

### 4.2 EventType

- FILE_CHANGE
- INTEGRITY_SUCCESS
- INTEGRITY_FAIL
- TEMPORAL_TICK
- RELEASE_COMPLETED
- SYNC_COMPLETED
- ANOMALY_DETECTED

### 4.3 I/F Contract

event_trigger → system_orchestrator

def emit_event(event: NWFEvent) -> None

---

## 5. モジュール仕様

---

## 5.1 event_trigger.py

### 責務
- 外部・内部イベント検知
- NWFEvent生成
- EventBusへ送信

### 入力
- repository_watcher
- sync_scheduler
- anomaly_detector

### 出力
- NWFEvent

### I/F Contract

def detect_file_change(path: str) -> NWFEvent  
def detect_temporal_event() -> NWFEvent  
def detect_system_event() -> NWFEvent  
def emit_event(event: NWFEvent) -> None  

### 制約
- Stateless
- DataState参照のみ許可

---

## 5.2 workflow_automation.py

### 責務
- Eventに基づくパイプライン実行
- 状態遷移制御

### ワークフロー

Auto-Verify  
FILE_CHANGE → integrity_checker.run()

Auto-Release  
INTEGRITY_SUCCESS → release_manager.execute_release()

Auto-Sync  
RELEASE_COMPLETED → github_sync_manager.push()

### 状態

- IDLE
- VERIFYING
- RELEASING
- SYNCING
- WAITING_APPROVAL
- FAILED

### I/F Contract

def handle_event(event: NWFEvent) -> None  
def run_auto_verify(event: NWFEvent) -> bool  
def run_auto_release(event: NWFEvent) -> str  
def run_auto_sync(version: str) -> bool  

依存I/F:

integrity_checker.run() -> bool  
release_manager.execute_release() -> str  
github_sync_manager.push(version: str) -> bool  

---

## 5.3 auto_repair_engine.py

### 責務
- エラー解析
- 修復処理
- ロールバック

### エラー分類

- STRUCTURAL
- CAUSAL
- SYSTEM

### 修復戦略

Minor Fix  
metadata_manager補完

Surgical Rollback  
data_state_manager.restore_entity()

Full Rollback  
deployment_manager.restore_release()

### I/F Contract

def analyze_event(event: NWFEvent) -> str  
def execute_repair(event: NWFEvent) -> bool  
def rollback_entity(entity_id: str) -> bool  
def rollback_release(version: str) -> bool  

依存I/F:

data_state_manager.restore_entity(entity_id: str) -> bool  
deployment_manager.restore_release(version: str) -> bool  

---

## 5.4 system_orchestrator.py

### 責務
- 全体統括
- 排他制御
- イベント分配

### 機能

#### Event Routing
event → workflow または repair

#### Concurrency Control

- RELEASE_LOCK
- REPAIR_LOCK

#### Heartbeat

60秒間隔ログ出力

#### Bootstrap

- spec_loader.load_all()
- repository_watcher.start()

### I/F Contract

def start() -> None  
def route_event(event: NWFEvent) -> None  
def acquire_lock(lock_type: str) -> bool  
def release_lock(lock_type: str) -> None  

---

## 6. モジュール間I/F一覧

### Event Flow

event_trigger.emit_event → system_orchestrator.route_event

### Workflow Flow

system_orchestrator → workflow_automation.handle_event

### Repair Flow

system_orchestrator → auto_repair_engine.execute_repair

### Release Flow

workflow_automation → release_manager.execute_release

### Sync Flow

workflow_automation → github_sync_manager.push

---

## 7. 依存モジュール契約

### integrity_checker.py
run() -> bool

### release_manager.py
execute_release() -> str

### github_sync_manager.py
push(version: str) -> bool

### anomaly_detector.py
detect() -> list

### data_state_manager.py
restore_entity(entity_id: str) -> bool

---

## 8. 排他制御仕様

### Lock定義

- GLOBAL_LOCK
- RELEASE_LOCK
- REPAIR_LOCK

### ルール

- RELEASE中はFILE_CHANGE無視
- REPAIR中はEventTrigger停止

---

## 9. 非同期処理仕様

### Task Queue（新規要素）

- 重い処理はQueueへ
- timeout_sec: 300秒

### 再試行

- 最大3回
- 失敗時 → AutoRepairEngine

---

## 10. HITL統合

### 条件

- 修復3回失敗
- Narrative整合性違反

### I/F

hitl_manager.enqueue_review(task_id: str) -> None

---

## 11. 拡張仕様（Self-Evolution）

### 概要

- audit_log分析
- validationルール最適化

### 将来I/F

def analyze_audit_log() -> dict  
def update_rules() -> None  

---

## 12. まとめ

本仕様により以下が保証される。

- Event駆動完全自動化
- モジュール間I/F完全整合
- 自動修復による恒常性維持
- Release〜Syncの無人化

Phase 2.8 は、NWFの「自律進化基盤」である。

---

[EOF]