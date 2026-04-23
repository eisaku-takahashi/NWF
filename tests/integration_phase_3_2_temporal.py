"""
Source: tests/integration_phase_3_2_temporal.py
Updated: 2026-04-21T14:17:00+09:00  # ★Phase 3.4 対応修正
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - src/core/metadata_manager.py
    - src/models/nwf_enums.py
Docstring:
    Phase 3.2 Temporal Management テスト（Phase 3.4 対応版）。

    本修正では以下を実施：
    - ValidationResult中心設計へ移行
    - success フィールド依存の排除
    - Severity検証の追加（CRITICAL保証）
    - 旧仕様コードはコメントとして保持し、差分を明示
"""

# =========================================================
# import
# =========================================================
import unittest
from datetime import datetime, timezone, timedelta

from src.core.metadata_manager import MetadataManager
from src.models.nwf_enums import NWFSeverity  # ★Phase 3.4対応で追加


# =========================================================
# Test Class
# =========================================================
class TestPhase32TemporalManagement(unittest.TestCase):

    def setUp(self):
        """
        テスト前初期化
        """
        self.meta_manager = MetadataManager()
        self.jst = timezone(timedelta(hours=9))

    # -----------------------------------------------------
    # JST → Stardate
    # -----------------------------------------------------
    def test_01_jst_to_stardate_mapping(self):
        """【時間同期】現実時間から作中時間へのマッピング検証"""
        print("\n[Test 01] Checking JST to Stardate mapping...")
        now_jst = datetime.now(self.jst)
        stardate = self.meta_manager.convert_to_stardate(now_jst)

        self.assertIsNotNone(stardate)
        self.assertTrue(isinstance(stardate, (float, int, str)))

        print(f" -> SUCCESS: JST[{now_jst}] mapped to Stardate[{stardate}]")

    # -----------------------------------------------------
    # Temporal Paradox
    # -----------------------------------------------------
    def test_02_temporal_paradox_prevention(self):
        """
        【逆転検知】過去へのイベント挿入を拒絶できるか
        ★Phase 3.4 対応：
        - ValidationResultベース検証へ変更
        - Severity（CRITICAL）検証追加
        """
        print("\n[Test 02] Checking Temporal Paradox Guard...")

        # --- 基準点（アンカー）の設定 ---
        anchor_event = {"id": "EVT-001", "stardate": 1000.0}
        self.meta_manager.register_anchor(anchor_event)

        # --- 矛盾データ ---
        paradox_event = {"id": "EVT-002", "stardate": 999.0}

        # --- 検証実行 ---
        result = self.meta_manager.validate_temporal_consistency(paradox_event)

        # =========================================================
        # ▼ 修正前（旧仕様）----------------------------------------
        # =========================================================
        # self.assertFalse(result.success)
        # ↑ 問題：
        # - success は非標準フィールド
        # - Phase 3.4 では ValidationResult に統一されたため廃止

        # =========================================================
        # ▼ 修正後（Phase 3.4）------------------------------------
        # =========================================================

        # is_valid を使用（ValidationResult標準）
        self.assertFalse(result.is_valid)

        # ★最重要：時間逆行は CRITICAL
        self.assertEqual(result.severity, NWFSeverity.CRITICAL)

        # error_code は継続使用（問題なし）
        self.assertEqual(result.error_code, "TEMPORAL_CAUSALITY_VIOLATION")

        print(f" -> SUCCESS: Temporal paradox detected: {result.message}")

    # -----------------------------------------------------
    # Timeline Continuity
    # -----------------------------------------------------
    def test_03_timeline_continuity(self):
        """【連続性】タイムラインの順序整合性"""
        print("\n[Test 03] Checking Timeline Continuity...")

        events = [
            {"id": "E1", "stardate": 100.0},
            {"id": "E2", "stardate": 105.0},
            {"id": "E3", "stardate": 110.0}
        ]

        is_linear = self.meta_manager.check_timeline_linearity(events)

        self.assertTrue(is_linear)

        print(" -> SUCCESS: Timeline linearity confirmed.")


# =========================================================
# Main Guard
# =========================================================
if __name__ == "__main__":
    unittest.main()

# [EOF]