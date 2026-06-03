"""
Source: src/integrity/consistency_validator.py
Updated: 2026-06-04T03:56:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Execution_Spec/NWF_Consistency_Validator_Spec_v2.0.1_Phase_3.5.md
    - docs/spec/Execution_Spec/NWF_Validation_System_v2.0.1.md
    - docs/spec/Execution_Spec/NWF_Escalation_Logic_Spec_v2.0.1.md
    - docs/spec/Core_Spec/NWF_Story_Database_v2.0.1.md
    - docs/spec/Core_Spec/NWF_Entity_ID_System_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
    - docs/project/NWF_Phase_3.5_Debug_Work_Plan_v20260516.md
    - docs/project/NWF_Phase_3.5_Debug_Work_Plan_v20260519.md
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

    Phase 3.5 Debug Work Plan v20260519 対応:
    - Severity Enum synchronization
    - UUID Missing Policy 同期
    - INFO混在禁止
    - ValidationResult strict schema 維持
    - Optional Dependency Injection
"""

# =========================
# Import
# =========================
from datetime import timedelta
from datetime import timezone
from typing import Any
from typing import List
from typing import Optional

from src.integrity.escalation_evaluator import EscalationEvaluator
from src.integrity.rule_evaluator import RuleEvaluator
from src.integrity.validation_result import ValidationResult
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
        story_db:
            StoryDB インスタンス
            必須 I/F:
                get(entity_id: str) -> Optional[NWFObject]

        rule_evaluator:
            RuleEvaluator インスタンス

        escalation_evaluator:
            EscalationEvaluator インスタンス

        audit_manager:
            AuditLogManager インスタンス

    Notes:
        - validate() は list[ValidationResult] を返す
        - ValidationResult は single-result object
        - aggregate ValidationResult は生成しない
    """

    def __init__(
        self,
        story_db: Any,
        rule_evaluator: Optional[RuleEvaluator] = None,
        escalation_evaluator: Optional[EscalationEvaluator] = None,
        audit_manager: Optional[Any] = None,
    ):
        """
        ConsistencyValidator 初期化。

        Args:
            story_db:
                StoryDB

            rule_evaluator:
                RuleEvaluator

            escalation_evaluator:
                EscalationEvaluator

            audit_manager:
                AuditLogManager
        """

        # =========================================================
        # Optional Dependency Injection
        #
        # 目的:
        # - Unit Test軽量化
        # - Mock容易化
        # - Validator純粋性維持
        # - DI architecture 維持
        # =========================================================

        self.story_db = story_db

        # =========================================================
        # Optional DI:
        # 未指定時は標準実装を使用
        # =========================================================
        self.rule_evaluator = (
            rule_evaluator
            if rule_evaluator is not None
            else RuleEvaluator()
        )

        self.escalation_evaluator = (
            escalation_evaluator
            if escalation_evaluator is not None
            else EscalationEvaluator()
        )

        # =========================================================
        # audit_manager:
        #
        # Optional DI 対応。
        #
        # validate() 内では hasattr により安全呼び出し。
        # =========================================================
        self.audit_manager = audit_manager

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

            if context is None:

                return [
                    ValidationResult.failure(
                        severity=NWFSeverity.CRITICAL,
                        message="Validation context is None",
                        target_id="UNKNOWN",
                        scope="SYSTEM_INTEGRITY",
                        rule_id="SYS_CONTEXT_CONTRACT",
                        violated_rules=[
                            "SYS_CONTEXT_CONTRACT"
                        ]
                    )
                ]

            # =====================================================
            # Spec:
            # context.is_valid() is True
            # =====================================================
            if not context.is_valid():

                return [
                    ValidationResult.failure(
                        severity=NWFSeverity.CRITICAL,
                        message="Validation context is invalid",
                        target_id="UNKNOWN",
                        scope="SYSTEM_INTEGRITY",
                        rule_id="SYS_CONTEXT_CONTRACT",
                        violated_rules=[
                            "SYS_CONTEXT_CONTRACT"
                        ]
                    )
                ]

            # =====================================================
            # Step 2:
            # ID Normalization
            # =====================================================

            # =====================================================
            # 必須仕様:
            # target_id = str(getattr(entity, "id", ""))
            # =====================================================
            target_id: str = str(
                getattr(entity, "id", "")
            )

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
                        rule_id="SYS_METADATA_CHECK",
                        violated_rules=[
                            "SYS_METADATA_CHECK"
                        ]
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
                        rule_id="SYS_VERSION_CHECK",
                        violated_rules=[
                            "SYS_VERSION_CHECK"
                        ]
                    )
                )

            # =====================================================
            # Step 4:
            # Immutability Check
            # =====================================================

            previous = None

            try:

                # =================================================
                # StoryDB Interface 正式仕様:
                #
                # get(entity_id: str) -> Optional[Entity]
                #
                # 必ず str ID を渡す
                # =================================================
                previous = self.story_db.get(target_id)

            except TypeError:

                # =================================================
                # Spec:
                # TypeError のみ再送出
                # =================================================
                raise

            except Exception as exc:

                # =================================================
                # StoryDB異常は CRITICAL result 化
                # =================================================
                return [
                    ValidationResult.failure(
                        severity=NWFSeverity.CRITICAL,
                        message=(
                            "StoryDB access failed: "
                            f"{str(exc)}"
                        ),
                        target_id=target_id,
                        scope="SYSTEM_INTEGRITY",
                        rule_id="SYS_STORY_DB_ACCESS",
                        violated_rules=[
                            "SYS_STORY_DB_ACCESS"
                        ]
                    )
                ]

            # =====================================================
            # UUID comparison debug
            # Required Logging Policy
            # =====================================================
            print(
                "[DEBUG] UUID comparison:",
                {
                    "target_id": target_id,
                    "previous_exists": (
                        previous is not None
                    ),
                }
            )

            # =====================================================
            # previous is None:
            # 新規 Entity
            # =====================================================
            if previous is not None:

                previous_uuid = getattr(
                    previous,
                    "uuid",
                    None
                )

                current_uuid = getattr(
                    entity,
                    "uuid",
                    None
                )

                # =================================================
                # UUID Missing Policy 正式仕様
                #
                # None比較誤検知を防止する。
                # =================================================
                if (
                    previous_uuid is not None
                    and current_uuid is not None
                    and str(previous_uuid)
                    != str(current_uuid)
                ):

                    results.append(
                        ValidationResult.failure(
                            severity=NWFSeverity.CRITICAL,
                            message=(
                                "IMMUTABILITY_BREACH: "
                                "UUID changed"
                            ),
                            target_id=target_id,
                            scope="SYSTEM_INTEGRITY",
                            rule_id="SYS_IMMUTABILITY_CHECK",
                            violated_rules=[
                                "SYS_IMMUTABILITY_CHECK"
                            ]
                        )
                    )

                    # =============================================
                    # Step 7:
                    # Escalation Routing
                    #
                    # Immutability violation は
                    # 即時 escalation routing
                    # =============================================
                    print(
                        "[DEBUG] escalation routing:",
                        {
                            "target_id": target_id,
                            "reason": (
                                "IMMUTABILITY_BREACH"
                            ),
                        }
                    )

                    final_results = (
                        self.escalation_evaluator
                        .evaluate(
                            results,
                            context
                        )
                    )

                    # =============================================
                    # Step 8:
                    # Audit Logging
                    # =============================================
                    if (
                        self.audit_manager is not None
                        and hasattr(
                            self.audit_manager,
                            "log_validation"
                        )
                    ):

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
                            self._scope_weight(
                                r.scope
                            ),
                            getattr(
                                r,
                                "error_code",
                                None
                            )
                            or "SUCCESS",
                            r.target_id
                        )
                    )

                    return final_results

            # =====================================================
            # Step 5:
            # RuleEvaluator Delegation
            # =====================================================

            rules = self._extract_rules(
                context
            )

            rule_results = self.rule_evaluator.process(
                rules,
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
            #
            # violation が1件でも存在する場合:
            # success(INFO) を生成しない
            # =====================================================

            has_failure = any(
                not r.is_valid
                for r in results
            )

            # =====================================================
            # violation が存在しない場合のみ INFO生成
            # =====================================================
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

                results = (
                    self.escalation_evaluator
                    .evaluate(
                        results,
                        context
                    )
                )

            # =====================================================
            # Step 8:
            # Audit Logging
            # =====================================================

            if (
                self.audit_manager is not None
                and hasattr(
                    self.audit_manager,
                    "log_validation"
                )
            ):

                self.audit_manager.log_validation(
                    entity=entity,
                    results=results,
                    context=context
                )

            # =====================================================
            # Step 9:
            # Deterministic Sort
            # =====================================================

            results = sorted(
                results,
                key=lambda r: (
                    self._scope_weight(r.scope),
                    getattr(
                        r,
                        "error_code",
                        None
                    )
                    or "SUCCESS",
                    r.target_id
                )
            )

            return results

        except TypeError:

            # =====================================================
            # Spec:
            # TypeError のみ再送出
            # =====================================================
            raise

        except Exception as exc:

            # =====================================================
            # その他 exception は
            # CRITICAL result 化
            # =====================================================

            return [
                ValidationResult.failure(
                    severity=NWFSeverity.CRITICAL,
                    message=(
                        "Unhandled validation exception: "
                        f"{str(exc)}"
                    ),
                    target_id=str(
                        getattr(
                            entity,
                            "id",
                            "UNKNOWN"
                        )
                    ),
                    scope="SYSTEM_INTEGRITY",
                    rule_id="SYS_VALIDATION_EXCEPTION",
                    violated_rules=[
                        "SYS_VALIDATION_EXCEPTION"
                    ]
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

        batch_results: List[
            ValidationResult
        ] = []

        for entity in entities:

            entity_results = self.validate(
                entity=entity,
                context=context
            )

            batch_results.extend(
                entity_results
            )

        # =========================================================
        # Deterministic Sort
        # =========================================================
        batch_results = sorted(
            batch_results,
            key=lambda r: (
                self._scope_weight(r.scope),
                getattr(
                    r,
                    "error_code",
                    None
                )
                or "SUCCESS",
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

    def _extract_rules(
        self,
        context: Any
    ) -> List[Any]:
        """
        Context から RuleEvaluator 用 rules を取得する。

        Args:
            context:
                WorkflowContext

        Returns:
            list:
                RuleEvaluator に渡す rule 一覧
        """

        metadata = getattr(
            context,
            "metadata",
            {},
        )

        rules = metadata.get(
            "rules",
            [],
        )

        if isinstance(
            rules,
            list,
        ):
            return rules

        return []

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
