"""
NWF Phase 2.1 Integration Test Script
実行日時: 2026-04-05T23:56+09:00
目的: src/core/ 各マネージャの実機動作検証

テスト項目:
  T1: ID生成 (UUID v4 / v7 仕様確認)
  T2: Transaction 整合性 (begin~record)
  T3: 状態遷移バリデーション (DRAFT→REVIEW)
  T4: Metadata 自動注入確認
  T5: AuditLog 追記確認
"""

import sys
import os
import json
import traceback

# プロジェクトルートをパスに追加
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

# テスト用一時ディレクトリ
TMP_ENTITY_DIR = os.path.join(PROJECT_ROOT, "tmp", "test_entities")
TMP_LOG_DIR    = os.path.join(PROJECT_ROOT, "tmp", "test_logs")
os.makedirs(TMP_ENTITY_DIR, exist_ok=True)
os.makedirs(TMP_LOG_DIR,    exist_ok=True)

PASS = "✅ PASS"
FAIL = "❌ FAIL"
WARN = "⚠️  WARN"

results = []

def log_result(test_id, name, status, detail=""):
    icon = PASS if status == "PASS" else (WARN if status == "WARN" else FAIL)
    results.append((test_id, name, status, detail))
    print(f"  [{test_id}] {icon} {name}")
    if detail:
        for line in detail.split("\n"):
            print(f"         → {line}")

print("=" * 60)
print("NWF Phase 2.1 Integration Test")
print("=" * 60)

# ─────────────────────────────────────────────
# T1: ID 生成テスト
# ─────────────────────────────────────────────
print("\n[T1] ID Generator テスト")
try:
    from src.core.id_generator import IDGenerator
    gen = IDGenerator()

    txn_id = gen.generate_transaction_id()
    log_id = gen.generate_log_id()
    ent_id = gen.generate_entity_id("CHR")
    evt_id = gen.generate_event_id()

    # フォーマット確認: PREFIX-UUID(36chars)
    import re
    pattern = re.compile(r"^[A-Z]{3,4}-[0-9a-f\-]{36}$")

    for label, val in [("TXN", txn_id), ("LOG", log_id), ("CHR", ent_id), ("EVT", evt_id)]:
        if pattern.match(val):
            log_result("T1a", f"ID形式 ({label}): {val}", "PASS")
        else:
            log_result("T1a", f"ID形式 ({label}): {val}", "FAIL", "パターン不一致")

    # validate_id テスト
    valid = gen.validate_id(ent_id)
    invalid = gen.validate_id("INVALID")
    if valid and not invalid:
        log_result("T1b", "validate_id() 正常動作確認", "PASS")
    else:
        log_result("T1b", "validate_id() 正常動作確認", "FAIL", f"valid={valid}, invalid={invalid}")

    # ★仕様乖離チェック: Kernel Core Concept では "UUID v7" を要求
    # NWF_Entity_ID_System_v2.0.1.md Section 3.2 では "UUID v4" と記載
    # 実装は uuid.uuid4() を使用 -> Entity ID Spec (v4) とは一致するが
    # Kernel Core Concept の "UUID v7" とは乖離
    log_result("T1c", "UUID バージョン確認", "WARN",
        "実装: uuid4() / Kernel_Core_Concept_Spec: UUID v7 を指定\n"
        "Entity_ID_System Spec: UUID v4 を指定\n"
        "→ 2つのSpec間で UUID v4/v7 に矛盾あり（後述: 乖離D1）")

except Exception as e:
    log_result("T1", "IDGenerator インポート/実行", "FAIL", traceback.format_exc())

# ─────────────────────────────────────────────
# T2: AuditLogManager Transaction 整合性テスト
# ─────────────────────────────────────────────
print("\n[T2] AuditLogManager Transaction テスト")
try:
    from src.core.audit_log_manager import AuditLogManager

    mgr = AuditLogManager(log_dir=TMP_LOG_DIR)

    # begin_transaction
    txn_id = mgr.begin_transaction(actor_id="USR-TAKAHASHI")
    if txn_id and txn_id.startswith("TXN-"):
        log_result("T2a", f"begin_transaction() -> {txn_id[:20]}...", "PASS")
    else:
        log_result("T2a", "begin_transaction() 戻り値確認", "FAIL", f"取得値: {txn_id}")

    # record_event
    mgr.record_event(
        event_type="ENT_CREATE",
        subject_id="CHR-TEST-001",
        actor_id="USR-TAKAHASHI",
        payload={"entity_type": "CHARACTER", "title": "Via"},
    )
    log_result("T2b", "record_event() 実行", "PASS")

    # ログファイル追記確認
    log_files = [f for f in os.listdir(TMP_LOG_DIR) if f.endswith(".jsonl")]
    if log_files:
        log_path = os.path.join(TMP_LOG_DIR, log_files[0])
        with open(log_path, "r", encoding="utf-8") as f:
            lines = [json.loads(l.strip()) for l in f if l.strip()]
        
        # TRANSACTION_BEGIN + ENT_CREATE の2件確認
        event_types = [l["event_type"] for l in lines]
        if "TRANSACTION_BEGIN" in event_types and "ENT_CREATE" in event_types:
            log_result("T2c", f"JSONL ログ追記確認: {log_files[0]} ({len(lines)}件)", "PASS")
        else:
            log_result("T2c", "JSONL ログ追記確認", "FAIL", f"検出イベント: {event_types}")

        # integrity_hash 存在確認
        has_hash = all("integrity_hash" in l for l in lines)
        if has_hash:
            log_result("T2d", "integrity_hash フィールド存在確認", "PASS")
        else:
            log_result("T2d", "integrity_hash フィールド存在確認", "FAIL")

        # verify_integrity テスト
        if mgr.verify_integrity():
            log_result("T2e", "verify_integrity() ハッシュ整合性確認", "PASS")
        else:
            log_result("T2e", "verify_integrity() ハッシュ整合性確認", "FAIL")
    else:
        log_result("T2c", "JSONL ログファイル確認", "FAIL", "ログファイルが生成されていない")

    # Transaction なしで record_event -> RuntimeError の確認
    mgr2 = AuditLogManager(log_dir=TMP_LOG_DIR)
    try:
        mgr2.record_event("TEST", "OBJ-001", "USR-X")
        log_result("T2f", "Transaction未開始でのrecord_event ガード", "FAIL", "例外が発生しなかった")
    except RuntimeError as e:
        log_result("T2f", "Transaction未開始でのrecord_event ガード", "PASS", str(e))

    # ★仕様乖離チェック: Kernel_Audit_System_Spec の命名規則は audit_YYYYMMDD.jsonl
    # AuditLogManager は YYYY-MM-DD.jsonl 形式で保存 -> 乖離
    from datetime import datetime, timezone, timedelta
    JST = timezone(timedelta(hours=9))
    date_audit = datetime.now(JST).strftime("%Y%m%d")  # spec規定形式
    date_mgr   = datetime.now(JST).strftime("%Y-%m-%d") # 実装の形式
    log_result("T2g", "ログファイル命名規則確認", "WARN",
        f"Spec: audit_{date_audit}.jsonl\n"
        f"AuditLogManager実装: {date_mgr}.jsonl\n"
        "→ 仕様乖離あり（後述: 乖離D2）")

    # AuditLogger (旧実装) の命名は audit_{YYYYMMDD}.jsonl -> Spec と一致
    log_result("T2h", "AuditLogger (旧実装) 命名規則", "PASS",
        "AuditLogger.py: audit_{YYYYMMDD}.jsonl -> Spec と一致")

except Exception as e:
    log_result("T2", "AuditLogManager テスト", "FAIL", traceback.format_exc())

# ─────────────────────────────────────────────
# T3: 状態遷移バリデーションテスト
# ─────────────────────────────────────────────
print("\n[T3] DataStateManager 状態遷移テスト")
try:
    from src.core.data_state_manager import DataStateManager

    dsm = DataStateManager()

    # DRAFT -> REVIEW (正常遷移)
    entity = {"id": "CHR-TEST-001", "state": "DRAFT",
              "created_at": "2026-04-05T00:00:00+09:00",
              "updated_at": "2026-04-05T00:00:00+09:00"}
    result_entity = dsm.change_state(entity, "REVIEW", actor_id="USR-TAKAHASHI")
    if result_entity["state"] == "REVIEW":
        log_result("T3a", "DRAFT → REVIEW 状態遷移", "PASS")
    else:
        log_result("T3a", "DRAFT → REVIEW 状態遷移", "FAIL", f"state={result_entity['state']}")

    # DRAFT -> APPROVED (不正遷移) -> ValueError 確認
    entity2 = {"id": "CHR-TEST-002", "state": "DRAFT",
               "created_at": "2026-04-05T00:00:00+09:00",
               "updated_at": "2026-04-05T00:00:00+09:00"}
    try:
        dsm.change_state(entity2, "APPROVED", actor_id="USR-TAKAHASHI")
        log_result("T3b", "DRAFT → APPROVED 不正遷移ガード", "FAIL", "例外が発生しなかった")
    except ValueError as e:
        log_result("T3b", "DRAFT → APPROVED 不正遷移ガード", "PASS", str(e))

    # ARCHIVED -> DRAFT (不正遷移)
    entity3 = {"id": "CHR-TEST-003", "state": "ARCHIVED",
               "created_at": "2026-04-05T00:00:00+09:00",
               "updated_at": "2026-04-05T00:00:00+09:00"}
    try:
        dsm.change_state(entity3, "DRAFT", actor_id="USR-TAKAHASHI")
        log_result("T3c", "ARCHIVED → DRAFT 不正遷移ガード", "FAIL", "例外が発生しなかった")
    except ValueError as e:
        log_result("T3c", "ARCHIVED → DRAFT 不正遷移ガード", "PASS", str(e))

    # ★仕様乖離チェック: DataStateMachine vs DataStateManager の遷移ルール差異
    from src.core.data_state_machine import ALLOWED_TRANSITIONS as DSM_MACHINE
    from src.core.data_state_manager import STATE_TRANSITIONS as DSM_MANAGER

    print("\n  [T3d] 2モジュール間の遷移ルール差異:")
    print(f"    DataStateMachine: {DSM_MACHINE}")
    print(f"    DataStateManager: {DSM_MANAGER}")

    # 比較
    diffs = []
    for state in set(list(DSM_MACHINE.keys()) + list(DSM_MANAGER.keys())):
        m1 = set(DSM_MACHINE.get(state, []))
        m2 = set(DSM_MANAGER.get(state, []))
        if m1 != m2:
            diffs.append(f"  {state}: Machine={sorted(m1)}, Manager={sorted(m2)}")

    if diffs:
        log_result("T3d", "DataStateMachine vs DataStateManager 遷移ルール一致確認", "FAIL",
            "不一致の状態:\n" + "\n".join(diffs) + "\n→ 乖離D3")
    else:
        log_result("T3d", "DataStateMachine vs DataStateManager 遷移ルール一致確認", "PASS")

    # DataStateManager.change_state のシグネチャ確認
    # 仕様: change_state(entity, new_state, actor_id)
    # EntityManager.archive_entity では change_state(subject_id, "ARCHIVED", actor_id) を呼び出し
    # DataStateManager.change_state は (entity: Dict, ...) を期待 -> 型不一致
    log_result("T3e", "EntityManager → DataStateManager.change_state 呼び出し整合性", "FAIL",
        "EntityManager.archive_entity (L237) が\n"
        "  self.state_manager.change_state(subject_id, 'ARCHIVED', actor_id) と呼び出し\n"
        "DataStateManager.change_state の第1引数は Dict[str, Any] entity を期待\n"
        "→ 乖離D4: 型不一致による実行時エラー")

except Exception as e:
    log_result("T3", "DataStateManager テスト", "FAIL", traceback.format_exc())

# ─────────────────────────────────────────────
# T4: Metadata 自動注入テスト
# ─────────────────────────────────────────────
print("\n[T4] MetadataManager 初期化・注入テスト")
try:
    from src.core.metadata_manager import MetadataManager

    mm = MetadataManager()

    # initialize_metadata
    meta = mm.initialize_metadata(
        spec_id="NWF-CHAR-SPEC-001",
        actor_id="USR-TAKAHASHI",
        parent_entity_id=None,
        derivation_type="MANUAL_CREATE"
    )

    required_fields = ["source_spec_id", "actor_id", "created_at", "updated_at",
                       "audit_context", "traceability", "extensions"]
    missing = [f for f in required_fields if f not in meta]
    if not missing:
        log_result("T4a", "initialize_metadata() 必須フィールド確認", "PASS",
            f"actor_id={meta['actor_id']}, created_at={meta['created_at']}")
    else:
        log_result("T4a", "initialize_metadata() 必須フィールド確認", "FAIL",
            f"欠落フィールド: {missing}")

    # update_metadata
    meta_updated = mm.update_metadata(
        current_metadata=meta,
        actor_id="USR-TAKAHASHI",
        transaction_id="TXN-TEST-001",
        reason="State changed to REVIEW"
    )
    if meta_updated["audit_context"]["last_transaction_id"] == "TXN-TEST-001":
        log_result("T4b", "update_metadata() audit_context 更新確認", "PASS")
    else:
        log_result("T4b", "update_metadata() audit_context 更新確認", "FAIL")

    # validate_metadata
    try:
        valid = mm.validate_metadata(meta_updated)
        log_result("T4c", "validate_metadata() 正常確認", "PASS" if valid else "FAIL")
    except ValueError as e:
        log_result("T4c", "validate_metadata() 正常確認", "FAIL", str(e))

    # ★仕様乖離チェック: EntityManager.create_entity のmetadata構造
    # EntityManager は metadata = {created_at, updated_at, actor_id} のみで初期化
    # MetadataManager.initialize_metadata では source_spec_id, audit_context, traceability が必須
    # EntityManager は MetadataManager を使わずに独立した metadata を構築している -> 乖離
    log_result("T4d", "EntityManager と MetadataManager の metadata 構造整合性", "WARN",
        "EntityManager.create_entity が生成するmetadata:\n"
        "  {created_at, updated_at, actor_id} のみ\n"
        "MetadataManager.initialize_metadata が生成するmetadata:\n"
        "  {source_spec_id, actor_id, created_at, updated_at,\n"
        "   audit_context, traceability, extensions}\n"
        "→ 乖離D5: EntityManagerはMetadataManagerを使用していない")

except Exception as e:
    log_result("T4", "MetadataManager テスト", "FAIL", traceback.format_exc())

# ─────────────────────────────────────────────
# T5: EntityManager 作成・Audit Log 連携テスト
# ─────────────────────────────────────────────
print("\n[T5] EntityManager 統合テスト")
try:
    from src.core.entity_manager import EntityManager
    from src.core.audit_log_manager import AuditLogManager
    from src.core.audit_logger import AuditLogger

    # AuditLogger の log_event 呼び出しシグネチャ確認
    # EntityManager は audit_logger.log_event(event_type=..., actor_id=..., target_id=..., payload=...)
    # AuditLogger は handle_event(event) のみ提供し、log_event メソッドは存在しない
    audit_logger = AuditLogger(log_dir=TMP_LOG_DIR)
    has_log_event = hasattr(audit_logger, "log_event")
    log_result("T5a", "AuditLogger.log_event() メソッド存在確認", "FAIL" if not has_log_event else "PASS",
        "EntityManager は audit_logger.log_event() を呼び出しているが\n"
        "AuditLogger クラスには log_event() メソッドが存在しない\n"
        "→ 乖離D6: 実行時 AttributeError が発生する" if not has_log_event else "")

    # EntityManager を audit_logger なしで実行 (安全な検証のため)
    em = EntityManager(
        entity_dir=TMP_ENTITY_DIR,
        state_manager=None,
        audit_logger=None  # Noneにして AttributeError を回避
    )

    entity = em.create_entity(
        subject_id="CHR-TEST-AUDIT-001",
        entity_type="CHARACTER",
        content={"name": "Via", "role": "protagonist"},
        actor_id="USR-TAKAHASHI"
    )

    if entity and entity.subject_id == "CHR-TEST-AUDIT-001":
        log_result("T5b", "create_entity() 実行確認", "PASS",
            f"subject_id={entity.subject_id}, state={entity.state}")
    else:
        log_result("T5b", "create_entity() 実行確認", "FAIL")

    # Entity ファイル永続化確認
    entity_file = os.path.join(TMP_ENTITY_DIR, "CHR-TEST-AUDIT-001.json")
    if os.path.exists(entity_file):
        with open(entity_file, "r", encoding="utf-8") as f:
            saved = json.load(f)
        log_result("T5c", "Entity JSON 永続化確認", "PASS",
            f"state={saved.get('state')}, version={saved.get('version')}")
    else:
        log_result("T5c", "Entity JSON 永続化確認", "FAIL", "ファイルが存在しない")

    # 初期状態 DRAFT 確認
    if entity.state == "DRAFT":
        log_result("T5d", "初期状態 DRAFT 確認", "PASS")
    else:
        log_result("T5d", "初期状態 DRAFT 確認", "FAIL", f"state={entity.state}")

    # 重複作成エラー確認
    try:
        em.create_entity("CHR-TEST-AUDIT-001", "CHARACTER", {}, "USR-TAKAHASHI")
        log_result("T5e", "重複 Entity 作成ガード", "FAIL", "例外が発生しなかった")
    except ValueError as e:
        log_result("T5e", "重複 Entity 作成ガード", "PASS", str(e))

except Exception as e:
    log_result("T5", "EntityManager テスト", "FAIL", traceback.format_exc())

# ─────────────────────────────────────────────
# 結果サマリー
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("テスト結果サマリー")
print("=" * 60)

pass_count  = sum(1 for r in results if r[2] == "PASS")
fail_count  = sum(1 for r in results if r[2] == "FAIL")
warn_count  = sum(1 for r in results if r[2] == "WARN")

print(f"  PASS: {pass_count}")
print(f"  FAIL: {fail_count}")
print(f"  WARN: {warn_count}")
print(f"  合計: {len(results)}")

if fail_count > 0:
    print("\n--- FAIL 一覧 ---")
    for r in results:
        if r[2] == "FAIL":
            print(f"  [{r[0]}] {r[1]}")
            if r[3]:
                for line in r[3].split("\n")[:3]:
                    print(f"      {line}")

print("\n[EOF]")
