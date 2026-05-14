"""
Source: src/integrity/consistency_validator.py
Updated: 2026-05-11T00:15:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Execution_Spec/NWF_Consistency_Validator_Spec_v2.0.1_Phase_3.5.md
    - docs/spec/Execution_Spec/NWF_Validation_System_v2.0.1.md
    - docs/spec/Execution_Spec/NWF_Escalation_Logic_Spec_v2.0.1.md
    - docs/spec/Core_Spec/NWF_Story_Database_v2.0.1.md
    - docs/spec/Core_Spec/NWF_Entity_ID_System_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
Docstring:
    ConsistencyValidator モジュール。

    NWF Phase 3.5 における Validation Orchestrator 実装。
    本クラスは単一ルールを保持する Validator ではなく、
    Validation Pipeline の整合性制御を担う。

    主責務:
    - Validation orchestration
    - Pre-validation
    - Immutability enforcement
    - ValidationResult aggregation
    - Escalation routing
    - Audit logging

    重要仕様:
    - Pure Evaluator Principle 準拠
    - StoryDB I/F のみ利用
    - Immutability violation は即時 CRITICAL
    - violation 存在時は success(INFO) を生成しない
    - validate() 外へ未処理 exception を出さない
      （TypeError のみ再送出許可）
"""

# =========================
# Import
# =========================
from datetime import timezone, timedelta
from typing import Any, List

from src.integrity.validation_result import ValidationResult
from src.integrity.rule_evaluator import RuleEvaluator
from src.integrity.escalation_evaluator import EscalationEvaluator

from src.models.nwf_enums import NWFSeverity

# =========================
# Constants / Config
# =========================

# NWF 時間管理規則:
# - JST 固定
JST = timezone(timedelta(hours=9))

# =========================
# Public Interface
# =========================
__all__ = [
    "ConsistencyValidator",
]

# =========================
# Classes
# =========================
class ConsistencyValidator:
    """
    NWF Phase 3.5 Consistency Validator

    Validation Orchestrator として動作する。

    Args:
        rule_evaluator:
            RuleEvaluator インスタンス

        escalation_evaluator:
            EscalationEvaluator インスタンス

        audit_manager:
            AuditLogManager インスタンス

        story_db:
            StoryDB インスタンス
            必須 I/F:
                get(entity_id: str) -> Optional[NWFObject]

    Notes:
        - validate() は list[ValidationResult] を返す
        - ValidationResult は single-result object
        - aggregate ValidationResult は生成しない
    """

    def __init__(
        self,
        rule_evaluator: RuleEvaluator,
        escalation_evaluator: EscalationEvaluator,
        audit_manager: Any,
        story_db: Any
    ):
        """
        ConsistencyValidator 初期化。

        Args:
            rule_evaluator:
                RuleEvaluator

            escalation_evaluator:
                EscalationEvaluator

            audit_manager:
                AuditLogManager

            story_db:
                StoryDB
        """

        # =========================================================
        # 修正前:
        # self.story_db = story_db
        #
        # self.rule_evaluator = RuleEvaluator()
        # self.escalation_evaluator = EscalationEvaluator()
        #
        # 問題:
        # - Spec の Constructor Contract 不一致
        # - Dependency Injection 非対応
        # - test/mock 差し替え不能
        # =========================================================

        # =========================================================
        # 修正後:
        # Spec の Constructor Contract に完全準拠
        # =========================================================
        self.rule_evaluator = rule_evaluator
        self.escalation_evaluator = escalation_evaluator
        self.audit_manager = audit_manager
        self.story_db = story_db

    # =========================
    # Public Method
    # =========================
    def validate(
        self,
        entity: Any,
        context: Any
    ) -> List[ValidationResult]:
        """
        単一 Entity の整合性検証を行う。

        Args:
            entity:
                検証対象 Entity

            context:
                ValidationContext

        Returns:
            list[ValidationResult]

        Raises:
            TypeError:
                StoryDB I/F 契約違反時
        """

        try:

            # =====================================================
            # Step 1:
            # Context Contract Check
            # =====================================================

            # -----------------------------------------------------
            # 修正前:
            # context.metadata.get(...)
            #
            # 問題:
            # - context is None 時に AttributeError
            # - Spec Step 1 未実装
            # -----------------------------------------------------

            if context is None:
                return [
                    ValidationResult.failure(
                        severity=NWFSeverity.FATAL,
                        message="Validation context is None",
                        target_id="UNKNOWN",
                        scope="SYSTEM_INTEGRITY",
                        rule_id="SYS_CONTEXT_CONTRACT"
                    )
                ]

            # -----------------------------------------------------
            # Spec:
            # context.is_valid() is True
            # -----------------------------------------------------
            if not context.is_valid():
                return [
                    ValidationResult.failure(
                        severity=NWFSeverity.FATAL,
                        message="Validation context is invalid",
                        target_id="UNKNOWN",
                        scope="SYSTEM_INTEGRITY",
                        rule_id="SYS_CONTEXT_CONTRACT"
                    )
                ]

            # =====================================================
            # Step 2:
            # ID Normalization
            # =====================================================

            # -----------------------------------------------------
            # 必須仕様:
            # target_id = str(getattr(entity, "id", ""))
            # -----------------------------------------------------
            target_id: str = str(getattr(entity, "id", ""))

            # -----------------------------------------------------
            # 修正前:
            # target.id を直接使用
            #
            # 問題:
            # - UUID/str 混在で不安定
            # - Spec 8.2 違反
            # -----------------------------------------------------

            # =====================================================
            # Step 3:
            # Basic Integrity
            # =====================================================

            results: List[ValidationResult] = []

            # -----------------------------------------------------
            # metadata 存在確認
            # -----------------------------------------------------
            if not hasattr(entity, "metadata"):
                results.append(
                    ValidationResult.failure(
                        severity=NWFSeverity.ERROR,
                        message="Missing metadata",
                        target_id=target_id,
                        scope="SYSTEM_INTEGRITY",
                        rule_id="SYS_METADATA_CHECK"
                    )
                )

            # -----------------------------------------------------
            # version 存在確認
            # -----------------------------------------------------
            if not hasattr(entity, "version"):
                results.append(
                    ValidationResult.failure(
                        severity=NWFSeverity.ERROR,
                        message="Missing version",
                        target_id=target_id,
                        scope="SYSTEM_INTEGRITY",
                        rule_id="SYS_VERSION_CHECK"
                    )
                )

            # =====================================================
            # Step 4:
            # Immutability Check
            # =====================================================

            # -----------------------------------------------------
            # 必須仕様:
            # previous = self.story_db.get(target_id)
            # -----------------------------------------------------

            previous = None

            try:

                # -------------------------------------------------
                # 修正前:
                # previous = self.story_db.get(target.id)
                #
                # 問題:
                # - ID正規化未適用
                # -------------------------------------------------

                previous = self.story_db.get(target_id)

            except TypeError:
                # -------------------------------------------------
                # Spec 12.2:
                # TypeError のみ再送出許可
                # -------------------------------------------------
                raise

            # -----------------------------------------------------
            # 修正前:
            # except Exception:
            #     previous = None
            #
            # 問題:
            # - Spec 12.3 違反
            # - exception を silent fallback
            # -----------------------------------------------------

            except Exception as exc:
                return [
                    ValidationResult.failure(
                        severity=NWFSeverity.FATAL,
                        message=f"StoryDB access failed: {str(exc)}",
                        target_id=target_id,
                        scope="SYSTEM_INTEGRITY",
                        rule_id="SYS_STORY_DB_ACCESS"
                    )
                ]

            # -----------------------------------------------------
            # UUID comparison debug
            # Required Logging Policy
            # -----------------------------------------------------
            print(
                "[DEBUG] UUID comparison:",
                {
                    "target_id": target_id,
                    "previous_exists": previous is not None,
                }
            )

            # -----------------------------------------------------
            # previous is None:
            # 新規 Entity
            # -----------------------------------------------------
            if previous is not None:

                # =================================================
                # 修正前:
                # UUID未定義を violation 化
                #
                # if not prev_uuid or not curr_uuid:
                #     violations.append("IMMUTABILITY_UUID_MISSING")
                #
                # 問題:
                # - Spec 10.6 違反
                # - UUID Missing は violation にしてはならない
                # =================================================

                previous_uuid = getattr(previous, "uuid", None)
                current_uuid = getattr(entity, "uuid", None)

                # =================================================
                # 必須仕様:
                # str(previous.uuid) != str(entity.uuid)
                # =================================================
                # =================================================
                # UUID Missing Policy
                #
                # Work Plan v20260502 では:
                #
                #     if str(previous.uuid) != str(entity.uuid):
                #
                # の無条件比較例が記載されている。
                #
                # しかし Execution Spec Phase 3.5
                # 「10.6 UUID Missing Policy」により:
                #
                #     previous.uuid is None
                #     entity.uuid is None
                #
                # は violation としてはならない。
                #
                # そのため現在実装では:
                # - UUID 両方存在時のみ比較
                # - None を含むケースは skip
                #
                # を正式仕様として採用する。
                #
                # これは Work Plan の暫定実装例ではなく、
                # Execution Spec の最終仕様を優先した実装である。
                # =================================================                
                if (
                    previous_uuid is not None
                    and current_uuid is not None
                    and str(previous_uuid) != str(current_uuid)
                ):

                    results.append(
                        ValidationResult.failure(
                            severity=NWFSeverity.CRITICAL,
                            message="IMMUTABILITY_BREACH: UUID changed",
                            target_id=target_id,
                            scope="SYSTEM_INTEGRITY",
                            rule_id="SYS_IMMUTABILITY_CHECK"
                        )
                    )

                    # =============================================
                    # Step 7:
                    # Escalation Routing
                    # Immutability violation 時は即時 routing
                    # =============================================

                    # ---------------------------------------------
                    # 修正前:
                    # RuleEvaluator 実行後に immutability
                    #
                    # 問題:
                    # - Spec 10.2 / 10.8 違反
                    # - RuleEvaluator を停止できない
                    # ---------------------------------------------

                    print(
                        "[DEBUG] escalation routing:",
                        {
                            "target_id": target_id,
                            "reason": "IMMUTABILITY_BREACH",
                        }
                    )

                    escalation_results = (
                        self.escalation_evaluator.evaluate_escalation(
                            entity,
                            results
                        )
                    )

                    final_results = [
                        *results,
                        *escalation_results,
                    ]

                    # =============================================
                    # Step 8:
                    # Audit Logging
                    # =============================================
                    self.audit_manager.log_validation(
                        entity=entity,
                        results=final_results,
                        context=context
                    )

                    # =============================================
                    # Step 9:
                    # Deterministic Sort
                    # =============================================
                    final_results = sorted(
                        final_results,
                        key=lambda r: (
                            self._scope_weight(r.scope),
                            getattr(r, "error_code", None) or "SUCCESS",
                            r.target_id
                        )
                    )

                    return final_results

            # =====================================================
            # Step 5:
            # RuleEvaluator Delegation
            # =====================================================

            # -----------------------------------------------------
            # 修正前:
            # self.rule_evaluator.process(...)
            #
            # 問題:
            # - Spec Interface 不一致
            # - evaluate() 必須
            # -----------------------------------------------------

            rule_results = self.rule_evaluator.evaluate(
                entity,
                context
            )

            # =====================================================
            # Step 6:
            # Result Aggregation
            # =====================================================

            results.extend(rule_results)

            # =====================================================
            # INFO Generation Rule
            # =====================================================

            # -----------------------------------------------------
            # 必須仕様:
            # any(not r.is_valid for r in results)
            # -----------------------------------------------------
            has_failure = any(
                not r.is_valid
                for r in results
            )

            # -----------------------------------------------------
            # violation が存在する場合:
            # success を生成しない
            # -----------------------------------------------------
            if not has_failure:

                results.append(
                    ValidationResult.success(
                        severity=NWFSeverity.INFO,
                        message="Validation OK",
                        target_id=target_id,
                        scope="SYSTEM_INTEGRITY",
                        rule_id="SYS_CONSISTENCY_PASS"
                    )
                )

            # =====================================================
            # Step 7:
            # Escalation Routing
            # =====================================================

            has_error_or_critical = any(
                getattr(r, "severity", None) in (
                    NWFSeverity.ERROR,
                    NWFSeverity.CRITICAL,
                    NWFSeverity.FATAL,
                )
                for r in results
            )

            if has_error_or_critical:

                print(
                    "[DEBUG] escalation routing:",
                    {
                        "target_id": target_id,
                        "result_count": len(results),
                    }
                )

                escalation_results = (
                    self.escalation_evaluator.evaluate_escalation(
                        entity,
                        results
                    )
                )

                results.extend(escalation_results)

            # =====================================================
            # Step 8:
            # Audit Logging
            # =====================================================

            self.audit_manager.log_validation(
                entity=entity,
                results=results,
                context=context
            )

            # =====================================================
            # Step 9:
            # Deterministic Sort
            # =====================================================

            # -----------------------------------------------------
            # 修正前:
            # r.code 依存
            #
            # 問題:
            # - ValidationResult 内部実装依存
            # - success 時に未定義となる可能性
            # -----------------------------------------------------

            results = sorted(
                results,
                key=lambda r: (
                    self._scope_weight(r.scope),
                    getattr(r, "error_code", None) or "SUCCESS",
                    r.target_id
                )
            )

            return results

        except TypeError:
            # =====================================================
            # Spec 12.2:
            # TypeError のみ再送出
            # =====================================================
            raise

        except Exception as exc:
            # =====================================================
            # Spec 12.3:
            # その他 exception は FATAL result 化
            # =====================================================

            return [
                ValidationResult.failure(
                    severity=NWFSeverity.FATAL,
                    message=f"Unhandled validation exception: {str(exc)}",
                    target_id=str(getattr(entity, "id", "UNKNOWN")),
                    scope="SYSTEM_INTEGRITY",
                    rule_id="SYS_VALIDATION_EXCEPTION"
                )
            ]

    # =========================
    # Public Method
    # =========================
    def validate_batch(
        self,
        entities: List[Any],
        context: Any
    ) -> List[ValidationResult]:
        """
        複数 Entity を検証する。

        Args:
            entities:
                検証対象 Entity 一覧

            context:
                ValidationContext

        Returns:
            list[ValidationResult]
        """

        batch_results: List[ValidationResult] = []

        for entity in entities:

            entity_results = self.validate(
                entity=entity,
                context=context
            )

            batch_results.extend(entity_results)

        # =========================================================
        # Deterministic Sort
        # =========================================================
        batch_results = sorted(
            batch_results,
            key=lambda r: (
                self._scope_weight(r.scope),
                getattr(r, "error_code", None) or "SUCCESS",
                r.target_id
            )
        )

        return batch_results

    # =========================
    # Utilities
    # =========================
    def _scope_weight(
        self,
        scope: str
    ) -> int:
        """
        scope 用 deterministic sort weight を返す。

        Args:
            scope:
                Validation scope

        Returns:
            int:
                sort weight
        """

        order = {
            "SYSTEM_INTEGRITY": 10,
            "DATA_CONSISTENCY": 20,
            "BUSINESS_LOGIC": 30,
        }

        return order.get(scope, 99)

    # =============================================================
    # Legacy Logic（保持）
    # =============================================================
    # 削除禁止:
    # 過去デバッグ履歴保持のためコメント化して残す
    #
    # 問題:
    # - Phase 3.5 Spec 非準拠
    # - aggregate ValidationResult 前提
    #
    """
    def _legacy_validate(...):
        pass
    """


# =========================
# Main Guard
# =========================
if __name__ == "__main__":
    pass

# [EOF]