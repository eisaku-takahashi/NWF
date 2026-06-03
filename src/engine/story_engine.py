"""
Source: src/engine/story_engine.py
Updated: 2026-06-03T09:38:00+09:00  # ★Phase 3.5 Debug Synchronization Step 2 対応
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Engine_Spec/NWF_Story_Engine_Implementation_v2.0.1.md
    - docs/spec/Core_Spec/NWF_World_Rule_Execution_v2.0.1.md
    - docs/spec/Execution_Spec/NWF_Validator_And_Context_Contract_v2.0.1.md
    - docs/project/NWF_Phase_3.5_Debug_Work_Plan_v20260525.md
    - src/core/metadata_manager.py
    - src/integrity/validator_integration_adapter.py
    - src/workflow/workflow_context.py
    - src/models/nwf_enums.py
Docstring:
    Story Engine モジュール。

    Phase 3.4 最終修正:
    - ValidationResult 空配列検知（①）
    - ERROR / CRITICAL の例外制御強化（⑥⑦）
    - silent failure 完全排除

    Phase 3.5 Debug Synchronization Step 2:
    - StoryEngine constructor synchronization
    - backward compatibility 維持
    - StoryEngine()
    - StoryEngine(story_db)
      の両方をサポート
"""

# -------------------------------
# imports
# -------------------------------
from typing import List, Dict, Any
from datetime import datetime, timezone, timedelta
import logging

from src.core.metadata_manager import MetadataManager
from src.integrity.validator_integration_adapter import ValidatorIntegrationAdapter
from src.workflow.workflow_context import WorkflowContext
from src.models.nwf_enums import NWFSeverity

# -------------------------------
# __all__
# -------------------------------
__all__ = ["StoryEngine"]

# -------------------------------
# constants
# -------------------------------
JST = timezone(timedelta(hours=9))

# -------------------------------
# logger
# -------------------------------
logger = logging.getLogger(__name__)


# -------------------------------
# main class
# -------------------------------
class StoryEngine:
    """
    StoryEngine

    Phase 3.4:
    - Adapter経由Validator統合
    - ValidationResult List対応
    - ERROR / CRITICAL 制御のSpec完全準拠

    Phase 3.5 Debug Synchronization:
    - StoryEngine constructor synchronization
    - backward compatibility 維持
    """

    def __init__(
        self,
        story_db=None,
        validator_adapter=None,
        metadata_manager=None,
    ):
        """
        StoryEngine 初期化。

        Phase 3.5 Debug Step 2:
        - StoryEngine()
        - StoryEngine(story_db)

        の後方互換性を維持する。

        Args:
            story_db:
                StoryDB インスタンス

            validator_adapter:
                ValidatorIntegrationAdapter

            metadata_manager:
                MetadataManager
        """

        # -----------------------------------------------------
        # Backward Compatibility
        # -----------------------------------------------------
        self.story_db = story_db
        self.meta_manager = metadata_manager

        # -----------------------------------------------------
        # validator_adapter 同期
        # -----------------------------------------------------
        if validator_adapter is None:
            # 循環参照防止のため遅延インポート
            from src.integrity.consistency_validator import (
                ConsistencyValidator,
            )

            from src.integrity.validator_integration_adapter import (
                ValidatorIntegrationAdapter,
            )

            self.validator_adapter = ValidatorIntegrationAdapter(
                validator=ConsistencyValidator(story_db=self.story_db)
            )

        else:
            self.validator_adapter = validator_adapter

        self.graph: Dict[str, Any] = {"nodes": [], "edges": []}

    # ==========================================================
    # Engine外部評価インターフェース
    # ==========================================================
    def evaluate_validation_results(self, validation_results: List[Any]) -> None:
        """
        ValidationResult を評価する。

        Args:
            validation_results:
                ValidationResult のリスト

        Raises:
            RuntimeError:
                CRITICAL 検知時
        """

        if not validation_results:
            logger.debug("[Engine Evaluation] empty results (no-op)")
            return

        for result in validation_results:
            logger.debug(
                f"[Engine Evaluation] severity={result.severity}, "
                f"code={getattr(result, 'error_code', 'N/A')}"
            )

            if hasattr(result, "is_blocking") and result.is_blocking():
                logger.critical(f"[ENGINE STOP] {result.error_code}: {result.message}")

                raise RuntimeError(
                    f"[CRITICAL_BREACH] {result.error_code}: {result.message}"
                )

            elif result.severity == NWFSeverity.CRITICAL:
                logger.critical(f"[ENGINE STOP] {result.error_code}: {result.message}")

                raise RuntimeError(
                    f"[CRITICAL_BREACH] {result.error_code}: {result.message}"
                )

    # ==========================================================
    # generate_story_graph
    # ==========================================================
    def generate_story_graph(
        self, entities: List[Any], context: WorkflowContext = None
    ) -> Dict[str, Any]:

        if context is None:
            context = self._create_default_context()

        self.graph["nodes"] = []
        self.graph["edges"] = []

        current_time = datetime.now(JST)

        for entity in entities:
            node = {
                "id": entity.id,
                "type": getattr(
                    entity,
                    "type",
                    "unknown",
                ),
                "state": ("alive" if entity.is_alive else "dead"),
            }

            self.graph["nodes"].append(node)

        for entity in entities:
            related_scenes = getattr(
                entity,
                "related_scenes",
                [],
            )

            for scene_id in related_scenes:
                if self.meta_manager:
                    stardate = self.meta_manager.convert_to_stardate(current_time)
                else:
                    stardate = context.current_stardate

                edge = {
                    "source": entity.id,
                    "target": scene_id,
                    "type": "LOCATION_STAY",
                    "weight": 1.0,
                    "stardate": stardate,
                    "metadata": {"is_alive": entity.is_alive},
                }

                if not self._apply_world_rules(
                    context,
                    entity,
                    edge,
                ):
                    continue

                validation_results = self.validator_adapter.execute(
                    context=context,
                    target=edge,
                )

                if not validation_results:
                    raise RuntimeError("ValidationResult is empty (Contract violation)")

                self.evaluate_validation_results(validation_results)

                should_add_edge = True

                for result in validation_results:
                    logger.debug(f"[DEBUG] severity={result.severity}")

                    if result.severity == NWFSeverity.ERROR:
                        logger.error(f"[ERROR] {result.error_code}: {result.message}")

                        should_add_edge = False
                        break

                    elif result.severity == NWFSeverity.WARNING:
                        logger.warning(
                            f"[WARNING] {result.error_code}: {result.message}"
                        )

                    elif result.severity == NWFSeverity.INFO:
                        logger.info(f"[INFO] {result.message}")

                if should_add_edge:
                    self.graph["edges"].append(edge)

                if not should_add_edge:
                    continue

        return self.render_timeline()

    # ==========================================================
    # timeline
    # ==========================================================
    def render_timeline(self) -> List[Dict[str, Any]]:

        edges = self.graph.get(
            "edges",
            [],
        )

        if not edges:
            return []

        sorted_edges = sorted(
            edges,
            key=lambda e: e.get(
                "stardate",
                0.0,
            ),
        )

        timeline = []

        for edge in sorted_edges:
            unit = {
                "timestamp": edge.get("stardate"),
                "actor": edge.get("source"),
                "location": edge.get("target"),
                "action": edge.get("type"),
                "integrity_status": "valid",
            }

            timeline.append(unit)

        return timeline

    # ==========================================================
    # world rule
    # ==========================================================
    def _apply_world_rules(
        self,
        context: WorkflowContext,
        entity: Any,
        edge: Dict[str, Any],
    ) -> bool:

        allow_ghost = context.get_world_rule("allow_ghost_activity")

        if not entity.is_alive and not allow_ghost:
            return False

        return True

    # ==========================================================
    # default context
    # ==========================================================
    def _create_default_context(self) -> WorkflowContext:

        return WorkflowContext(
            metadata={
                "base_date": (datetime.now(JST).isoformat()),
                "time_unit": "stardate",
                "coordinate_system": "default",
            },
            world_rules={
                "allow_ghost_activity": False,
                "allow_time_reversal": False,
                "allow_multi_location": False,
            },
            transaction=[],
            current_stardate=0.0,
        )


# -------------------------------
# main guard
# -------------------------------
if __name__ == "__main__":
    logger.info("StoryEngine standalone test start")

# [EOF]
