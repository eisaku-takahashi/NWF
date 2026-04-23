"""
Source: src/engine/story_engine.py
Updated: 2026-04-23T03:37:00+09:00  # ★Phase 3.4 Gatekeeper拡張（外部Validation評価導入）
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Engine_Spec/NWF_Story_Engine_Implementation_v2.0.1.md
    - docs/spec/Core_Spec/NWF_World_Rule_Execution_v2.0.1.md
    - docs/spec/Execution_Spec/NWF_Validator_And_Context_Contract_v2.0.1.md
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

    ★ 今回追加修正:
    - CRITICAL検知の最優先化（絶対停止保証）
    - Adapter責務分離の完全適用
    - ValidationResult逐次評価の前にCRITICALスキャン導入

    ★ Phase 3.4 追加（最重要）:
    - Engine停止ロジックの統一（is_blocking使用）
    - CRITICAL判定の単一責務化（ValidationResultへ委譲）

    ★ Phase 3.4 最終拡張（今回）:
    - Validation Pipeline責務分離の明文化（最重要）
        Validator → 「生成のみ」
        Adapter   → 「型変換のみ」
        Auditor   → 「監査のみ（非制御）」
        Engine    → 「最終判断のみ（停止制御）」

    ★ 新規追加（Gatekeeper拡張）:
    - Engine外部Validation評価インターフェースの導入
        → evaluate_validation_results()
        → Pipeline外部入力の評価を可能にする

    【設計原則】
    - Engineは「判断のみ」を行う（制御責務の単一化）
    - 中間層（Adapter/Auditor）は一切の制御を行わない
    - Severityは上位層に伝播される制御信号であり、途中で変更してはならない

    【重要】
    - CRITICALは必ずここで停止する（最終防衛ライン）
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
__all__ = [
    "StoryEngine"
]

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

    ★ 最終仕様:
    - CRITICALは必ず即時停止（最優先）
    - ERRORはエッジ生成スキップ
    - WARNING/INFOはログのみ

    ★ 設計変更（重要）:
    - CRITICAL判定は ValidationResult.is_blocking() に統一
    - Engineは「最終判断責務のみ」を持つ

    ★ Pipeline責務分離（明文化）:
    - Validator: ルール違反の検出とValidationResult生成
    - Adapter: 型保証（Enum変換等）のみ
    - Auditor: 監査ログ生成のみ（非破壊）
    - Engine: 停止判断・実行制御のみ

    → 本クラスは「制御の最終決定点」である
    """

    def __init__(
        self,
        validator_adapter: ValidatorIntegrationAdapter,
        metadata_manager: MetadataManager = None
    ):
        self.validator_adapter = validator_adapter
        self.meta_manager = metadata_manager

        self.graph: Dict[str, Any] = {
            "nodes": [],
            "edges": []
        }

    # ==========================================================
    # ★ ① Engine外部評価インターフェース（新規追加）
    # ==========================================================
    def evaluate_validation_results(
        self,
        validation_results: List[Any]
    ) -> None:
        """
        外部または事前処理で生成されたValidationResultを評価する。

        なぜ必要か：
        - 従来は Engine 内部で生成された結果しか評価できなかった
        - Pipeline外部（テスト / AI / Workflow）からの入力が評価不能だった

        設計意図：
        - Engineを「最終判断ゲートキーパー」に昇格させる
        - Validation Pipelineの終端責務を明確化する

        Args:
            validation_results: ValidationResultのリスト

        Raises:
            RuntimeError: CRITICAL検知時（即時停止）
        """

        # -------------------------------
        # 空配列チェック（契約防御）
        # -------------------------------
        if not validation_results:
            logger.debug("[Engine Evaluation] empty results (no-op)")
            return

        # -------------------------------
        # CRITICAL優先評価
        # -------------------------------
        for result in validation_results:

            logger.debug(
                f"[Engine Evaluation] severity={result.severity}, code={getattr(result, 'error_code', 'N/A')}"
            )

            # -------------------------------
            # ★ 推奨：is_blocking使用
            # -------------------------------
            if hasattr(result, "is_blocking") and result.is_blocking():
                logger.critical(
                    f"[ENGINE STOP] {result.error_code}: {result.message}"
                )
                raise RuntimeError(
                    f"[CRITICAL_BREACH] {result.error_code}: {result.message}"
                )

            # -------------------------------
            # ★ フォールバック（移行期）
            # -------------------------------
            elif result.severity == NWFSeverity.CRITICAL:
                logger.critical(
                    f"[ENGINE STOP] {result.error_code}: {result.message}"
                )
                raise RuntimeError(
                    f"[CRITICAL_BREACH] {result.error_code}: {result.message}"
                )

    # ==========================================================
    # generate_story_graph
    # ==========================================================
    def generate_story_graph(
        self,
        entities: List[Any],
        context: WorkflowContext = None
    ) -> Dict[str, Any]:

        if context is None:
            context = self._create_default_context()

        self.graph["nodes"] = []
        self.graph["edges"] = []

        current_time = datetime.now(JST)

        # -------------------------------
        # ノード生成
        # -------------------------------
        for entity in entities:
            node = {
                "id": entity.id,
                "type": getattr(entity, "type", "unknown"),
                "state": "alive" if entity.is_alive else "dead"
            }
            self.graph["nodes"].append(node)

        # -------------------------------
        # エッジ生成
        # -------------------------------
        for entity in entities:

            related_scenes = getattr(entity, "related_scenes", [])

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
                    "metadata": {
                        "is_alive": entity.is_alive
                    }
                }

                # -------------------------------
                # World Rule
                # -------------------------------
                if not self._apply_world_rules(context, entity, edge):
                    continue

                # -------------------------------
                # Validator 実行（生成責務）
                # -------------------------------
                validation_results = self.validator_adapter.execute(
                    context=context,
                    target=edge
                )

                # -------------------------------
                # 契約違反防御
                # -------------------------------
                if not validation_results:
                    raise RuntimeError("ValidationResult is empty (Contract violation)")

                # ==========================================================
                # ★ ② 修正前（保持：ローカル判定）
                # ==========================================================
                # for result in validation_results:
                #     if result.is_blocking():
                #         raise RuntimeError(...)
                #
                # 問題:
                # - 判定ロジックが分散
                # - DRY違反
                # ==========================================================

                # ==========================================================
                # ★ ② 修正後：外部評価メソッドへ集約（DRY適用）
                # ==========================================================
                self.evaluate_validation_results(validation_results)

                should_add_edge = True

                # -------------------------------
                # 非CRITICAL処理
                # -------------------------------
                for result in validation_results:

                    logger.debug(f"[DEBUG] severity={result.severity}")

                    if result.severity == NWFSeverity.ERROR:
                        logger.error(
                            f"[ERROR] {result.error_code}: {result.message}"
                        )
                        should_add_edge = False
                        break

                    elif result.severity == NWFSeverity.WARNING:
                        logger.warning(
                            f"[WARNING] {result.error_code}: {result.message}"
                        )

                    elif result.severity == NWFSeverity.INFO:
                        logger.info(
                            f"[INFO] {result.message}"
                        )

                if should_add_edge:
                    self.graph["edges"].append(edge)

                if not should_add_edge:
                    continue

        return self.render_timeline()

    # ==========================================================
    # timeline
    # ==========================================================
    def render_timeline(self) -> List[Dict[str, Any]]:

        edges = self.graph.get("edges", [])

        if not edges:
            return []

        sorted_edges = sorted(edges, key=lambda e: e.get("stardate", 0.0))

        timeline = []

        for edge in sorted_edges:
            unit = {
                "timestamp": edge.get("stardate"),
                "actor": edge.get("source"),
                "location": edge.get("target"),
                "action": edge.get("type"),
                "integrity_status": "valid"
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
        edge: Dict[str, Any]
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
                "base_date": datetime.now(JST).isoformat(),
                "time_unit": "stardate",
                "coordinate_system": "default"
            },
            world_rules={
                "allow_ghost_activity": False,
                "allow_time_reversal": False,
                "allow_multi_location": False
            },
            transaction=[],
            current_stardate=0.0
        )


# -------------------------------
# main guard
# -------------------------------
if __name__ == "__main__":
    logger.info("StoryEngine standalone test start")

# [EOF]