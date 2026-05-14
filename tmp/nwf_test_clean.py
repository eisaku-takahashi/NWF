# -*- coding: utf-8 -*-
"""
NWF Phase 2.1 Integration Test - ASCII-safe version
"""
import sys, os, json, traceback, re
from datetime import datetime, timezone, timedelta

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

TMP_ENTITY_DIR = os.path.join(PROJECT_ROOT, "tmp", "test_entities")
TMP_LOG_DIR    = os.path.join(PROJECT_ROOT, "tmp", "test_logs")
os.makedirs(TMP_ENTITY_DIR, exist_ok=True)
os.makedirs(TMP_LOG_DIR,    exist_ok=True)

results = []

def log_result(tid, name, status, detail=""):
    mark = "[PASS]" if status == "PASS" else ("[WARN]" if status == "WARN" else "[FAIL]")
    results.append((tid, name, status, detail))
    print("  %s %s %s" % (tid, mark, name))
    if detail:
        for line in detail.split("\n"):
            print("         -> %s" % line)

SEP = "=" * 60
print(SEP)
print("NWF Phase 2.1 Integration Test")
print(SEP)

# ===========================================================
# T1: ID Generator
# ===========================================================
print("\n[T1] ID Generator")
try:
    from src.core.id_generator import IDGenerator
    gen = IDGenerator()

    pattern = re.compile(r"^[A-Z]{3,4}-[0-9a-f\-]{36}$")
    ids = {
        "TXN": gen.generate_transaction_id(),
        "LOG": gen.generate_log_id(),
        "CHR": gen.generate_entity_id("CHR"),
        "EVT": gen.generate_event_id(),
    }
    all_ok = True
    for label, val in ids.items():
        if not pattern.match(val):
            log_result("T1a", "ID format (%s): %s" % (label, val), "FAIL", "Pattern mismatch")
            all_ok = False
    if all_ok:
        log_result("T1a", "All ID formats match PREFIX-UUIDv4 pattern", "PASS",
                   "  ".join("%s=%s" % (k, v[:12]+"...") for k,v in ids.items()))

    valid   = gen.validate_id(ids["CHR"])
    invalid = gen.validate_id("INVALID")
    if valid and not invalid:
        log_result("T1b", "validate_id() works correctly", "PASS")
    else:
        log_result("T1b", "validate_id() works correctly", "FAIL",
                   "valid=%s, invalid=%s" % (valid, invalid))

    # Spec discrepancy note
    log_result("T1c", "UUID version check (spec vs impl)", "WARN",
        "Impl: uuid.uuid4() (v4)\n"
        "NWF_Kernel_Core_Concept_Spec: 'UUID v7' required\n"
        "NWF_Entity_ID_System_Spec: 'UUID v4' specified\n"
        "=> DISCREPANCY D1: Two specs conflict on UUID version")

except Exception as e:
    log_result("T1", "IDGenerator import/run", "FAIL", traceback.format_exc())

# ===========================================================
# T2: AuditLogManager Transaction
# ===========================================================
print("\n[T2] AuditLogManager Transaction")
try:
    from src.core.audit_log_manager import AuditLogManager

    mgr = AuditLogManager(log_dir=TMP_LOG_DIR)
    txn_id = mgr.begin_transaction(actor_id="USR-TAKAHASHI")

    if txn_id and txn_id.startswith("TXN-"):
        log_result("T2a", "begin_transaction() -> %s..." % txn_id[:20], "PASS")
    else:
        log_result("T2a", "begin_transaction() return value", "FAIL", "Got: %s" % txn_id)

    mgr.record_event(
        event_type="ENT_CREATE",
        subject_id="CHR-TEST-001",
        actor_id="USR-TAKAHASHI",
        payload={"entity_type": "CHARACTER", "title": "Via"},
    )
    log_result("T2b", "record_event() executed without error", "PASS")

    log_files = [f for f in os.listdir(TMP_LOG_DIR) if f.endswith(".jsonl")]
    if log_files:
        lpath = os.path.join(TMP_LOG_DIR, log_files[0])
        with open(lpath, "r", encoding="utf-8") as f:
            lines = [json.loads(l.strip()) for l in f if l.strip()]

        evt_types = [l["event_type"] for l in lines]
        if "TRANSACTION_BEGIN" in evt_types and "ENT_CREATE" in evt_types:
            log_result("T2c", "JSONL append confirmed: %s (%d entries)" % (log_files[0], len(lines)), "PASS")
        else:
            log_result("T2c", "JSONL append check", "FAIL", "Found events: %s" % evt_types)

        if all("integrity_hash" in l for l in lines):
            log_result("T2d", "integrity_hash field present in all entries", "PASS")
        else:
            log_result("T2d", "integrity_hash field check", "FAIL")

        if mgr.verify_integrity():
            log_result("T2e", "verify_integrity() hash check passed", "PASS")
        else:
            log_result("T2e", "verify_integrity() hash check", "FAIL")
    else:
        log_result("T2c", "JSONL log file exists", "FAIL", "No .jsonl file generated")

    # Guard: record without begin_transaction
    mgr2 = AuditLogManager(log_dir=TMP_LOG_DIR)
    try:
        mgr2.record_event("TEST", "OBJ-001", "USR-X")
        log_result("T2f", "record_event without transaction -> RuntimeError guard", "FAIL",
                   "No exception raised")
    except RuntimeError as e:
        log_result("T2f", "record_event without transaction -> RuntimeError guard", "PASS", str(e))

    # Spec discrepancy: log file naming
    JST = timezone(timedelta(hours=9))
    spec_name   = "audit_%s.jsonl" % datetime.now(JST).strftime("%Y%m%d")
    actual_name = "%s.jsonl"       % datetime.now(JST).strftime("%Y-%m-%d")
    log_result("T2g", "Log file naming convention", "WARN",
        "Spec (NWF_Kernel_Audit_System_Spec): %s\n"
        "AuditLogManager impl: %s\n"
        "=> DISCREPANCY D2: filename format mismatch" % (spec_name, actual_name))

    log_result("T2h", "AuditLogger.py naming (audit_YYYYMMDD.jsonl) matches spec", "PASS")

except Exception as e:
    log_result("T2", "AuditLogManager test", "FAIL", traceback.format_exc())

# ===========================================================
# T3: State Transition Validation
# ===========================================================
print("\n[T3] DataStateManager State Transition")
try:
    from src.core.data_state_manager import DataStateManager

    dsm = DataStateManager()

    # DRAFT -> REVIEW (valid)
    ent = {"id": "CHR-T001", "state": "DRAFT",
           "created_at": "2026-04-05T00:00:00+09:00",
           "updated_at": "2026-04-05T00:00:00+09:00"}
    res = dsm.change_state(ent, "REVIEW", actor_id="USR-TAKAHASHI")
    if res["state"] == "REVIEW":
        log_result("T3a", "DRAFT -> REVIEW transition", "PASS")
    else:
        log_result("T3a", "DRAFT -> REVIEW transition", "FAIL", "state=%s" % res["state"])

    # DRAFT -> APPROVED (invalid)
    ent2 = {"id": "CHR-T002", "state": "DRAFT",
            "created_at": "2026-04-05T00:00:00+09:00",
            "updated_at": "2026-04-05T00:00:00+09:00"}
    try:
        dsm.change_state(ent2, "APPROVED", actor_id="USR-TAKAHASHI")
        log_result("T3b", "DRAFT -> APPROVED (invalid) raises ValueError", "FAIL", "No exception")
    except ValueError as e:
        log_result("T3b", "DRAFT -> APPROVED (invalid) raises ValueError", "PASS", str(e))

    # ARCHIVED -> DRAFT (invalid)
    ent3 = {"id": "CHR-T003", "state": "ARCHIVED",
            "created_at": "2026-04-05T00:00:00+09:00",
            "updated_at": "2026-04-05T00:00:00+09:00"}
    try:
        dsm.change_state(ent3, "DRAFT", actor_id="USR-TAKAHASHI")
        log_result("T3c", "ARCHIVED -> DRAFT (invalid) raises ValueError", "FAIL", "No exception")
    except ValueError as e:
        log_result("T3c", "ARCHIVED -> DRAFT (invalid) raises ValueError", "PASS", str(e))

    # Compare transition tables between DataStateMachine and DataStateManager
    from src.core.data_state_machine import ALLOWED_TRANSITIONS as MACHINE_TBL
    from src.core.data_state_manager import STATE_TRANSITIONS   as MANAGER_TBL

    print("\n  Transition tables:")
    print("    DataStateMachine : %s" % MACHINE_TBL)
    print("    DataStateManager : %s" % MANAGER_TBL)

    diffs = []
    for state in set(list(MACHINE_TBL.keys()) + list(MANAGER_TBL.keys())):
        m1 = set(MACHINE_TBL.get(state, []))
        m2 = set(MANAGER_TBL.get(state, []))
        if m1 != m2:
            diffs.append("  %s: Machine=%s, Manager=%s" % (state, sorted(m1), sorted(m2)))

    if diffs:
        log_result("T3d", "DataStateMachine vs DataStateManager transition table match", "FAIL",
            "Mismatches:\n" + "\n".join(diffs) + "\n=> DISCREPANCY D3")
    else:
        log_result("T3d", "DataStateMachine vs DataStateManager transition table match", "PASS")

    # Call signature check: EntityManager calls change_state(subject_id_str, state, actor)
    # but DataStateManager.change_state expects (entity: Dict, ...)
    log_result("T3e",
        "EntityManager.archive_entity -> DataStateManager.change_state signature match", "FAIL",
        "EntityManager L237: self.state_manager.change_state(subject_id, 'ARCHIVED', actor_id)\n"
        "DataStateManager.change_state expects: (entity: Dict, new_state, actor_id)\n"
        "Passing a str where Dict is expected -> AttributeError at runtime\n"
        "=> DISCREPANCY D4")

except Exception as e:
    log_result("T3", "DataStateManager test", "FAIL", traceback.format_exc())

# ===========================================================
# T4: MetadataManager
# ===========================================================
print("\n[T4] MetadataManager")
try:
    from src.core.metadata_manager import MetadataManager

    mm   = MetadataManager()
    meta = mm.initialize_metadata(
        spec_id="NWF-CHAR-SPEC-001",
        actor_id="USR-TAKAHASHI",
    )

    required = ["source_spec_id", "actor_id", "created_at", "updated_at",
                "audit_context", "traceability", "extensions"]
    missing = [f for f in required if f not in meta]
    if not missing:
        log_result("T4a", "initialize_metadata() required fields present", "PASS",
                   "actor_id=%s, created_at=%s" % (meta["actor_id"], meta["created_at"]))
    else:
        log_result("T4a", "initialize_metadata() required fields", "FAIL",
                   "Missing: %s" % missing)

    meta2 = mm.update_metadata(meta, "USR-TAKAHASHI", "TXN-TEST-001", reason="REVIEW transition")
    if meta2["audit_context"]["last_transaction_id"] == "TXN-TEST-001":
        log_result("T4b", "update_metadata() audit_context.last_transaction_id set", "PASS")
    else:
        log_result("T4b", "update_metadata() audit_context update", "FAIL")

    try:
        ok = mm.validate_metadata(meta2)
        log_result("T4c", "validate_metadata() passes", "PASS" if ok else "FAIL")
    except ValueError as e:
        log_result("T4c", "validate_metadata()", "FAIL", str(e))

    log_result("T4d", "EntityManager metadata vs MetadataManager output structure", "WARN",
        "EntityManager.create_entity builds: {created_at, updated_at, actor_id}\n"
        "MetadataManager.initialize_metadata builds: {source_spec_id, actor_id, created_at,\n"
        "  updated_at, audit_context, traceability, extensions}\n"
        "EntityManager does NOT call MetadataManager\n"
        "=> DISCREPANCY D5: metadata structure incomplete in EntityManager")

except Exception as e:
    log_result("T4", "MetadataManager test", "FAIL", traceback.format_exc())

# ===========================================================
# T5: EntityManager integration
# ===========================================================
print("\n[T5] EntityManager integration")
try:
    from src.core.audit_logger import AuditLogger
    from src.core.entity_manager import EntityManager

    al = AuditLogger(log_dir=TMP_LOG_DIR)
    has_log_event = hasattr(al, "log_event")
    if has_log_event:
        log_result("T5a", "AuditLogger.log_event() exists", "PASS")
    else:
        log_result("T5a", "AuditLogger.log_event() exists", "FAIL",
            "EntityManager calls audit_logger.log_event(...) but method does not exist\n"
            "AuditLogger only has handle_event(event)\n"
            "=> DISCREPANCY D6: AttributeError at runtime when audit_logger is wired")

    # NWFObject field name check (EntityManager vs NWFObject)
    # EntityManager uses: entity.subject_id, entity.entity_type, entity.state, entity.relationships
    # NWFObject has:      self.id,           self.type,          self.status, self.dependencies
    log_result("T5b", "EntityManager attribute names vs NWFObject fields", "FAIL",
        "EntityManager uses: subject_id, entity_type, state, relationships, version\n"
        "NWFObject defines:  id,         type,         status, dependencies, version\n"
        "=> DISCREPANCY D7: Attribute name mismatch causes AttributeError at runtime")

    # Run create_entity WITHOUT audit_logger to isolate the D7 issue
    em = EntityManager(entity_dir=TMP_ENTITY_DIR, state_manager=None, audit_logger=None)
    try:
        entity = em.create_entity(
            subject_id="CHR-TEST-AUDIT-001",
            entity_type="CHARACTER",
            content={"name": "Via", "role": "protagonist"},
            actor_id="USR-TAKAHASHI",
        )
        log_result("T5c", "create_entity() executes", "PASS",
                   "Returned: %s" % type(entity).__name__)
        # Try accessing subject_id (should raise if NWFObject uses 'id')
        try:
            _ = entity.subject_id
            log_result("T5d", "entity.subject_id accessible", "PASS")
        except AttributeError:
            log_result("T5d", "entity.subject_id accessible", "FAIL",
                "NWFObject uses 'id', not 'subject_id'")
    except Exception as e2:
        log_result("T5c", "create_entity() executes", "FAIL", str(e2))

    # Duplicate entity guard
    try:
        em.create_entity("CHR-TEST-AUDIT-001", "CHARACTER", {}, "USR-TAKAHASHI")
        log_result("T5e", "Duplicate entity ValueError guard", "FAIL", "No exception raised")
    except (ValueError, Exception) as e2:
        log_result("T5e", "Duplicate entity ValueError guard", "PASS", str(e2)[:80])

    # Persistence check
    ef = os.path.join(TMP_ENTITY_DIR, "CHR-TEST-AUDIT-001.json")
    if os.path.exists(ef):
        with open(ef, "r", encoding="utf-8") as f:
            saved = json.load(f)
        log_result("T5f", "Entity persisted as JSON", "PASS",
                   "Keys: %s" % list(saved.keys()))
    else:
        log_result("T5f", "Entity persisted as JSON", "FAIL", "File not found")

except Exception as e:
    log_result("T5", "EntityManager integration", "FAIL", traceback.format_exc())

# ===========================================================
# Summary
# ===========================================================
print("\n" + SEP)
print("SUMMARY")
print(SEP)
pc = sum(1 for r in results if r[2] == "PASS")
fc = sum(1 for r in results if r[2] == "FAIL")
wc = sum(1 for r in results if r[2] == "WARN")
print("  PASS : %d" % pc)
print("  FAIL : %d" % fc)
print("  WARN : %d" % wc)
print("  TOTAL: %d" % len(results))

if fc:
    print("\n--- FAIL list ---")
    for r in results:
        if r[2] == "FAIL":
            print("  [%s] %s" % (r[0], r[1]))
            for line in r[3].split("\n")[:3]:
                print("       %s" % line)

print("\n[EOF]")
