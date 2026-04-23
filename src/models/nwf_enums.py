"""
Source: src/models/nwf_enums.py
Updated: 2026-04-20T02:02:00+09:00  # ★更新（Phase 3.4 最終整合）
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Execution_Spec/NWF_Validator_And_Context_Contract_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
Docstring:
    NWF Enum 定義モジュール。

    本モジュールは、NWF v2.0.1 におけるすべての Enum を一元管理する。
    Validator / Engine / Adapter 間のインターフェース整合性（I/F Contract）を保証するための
    Single Source of Truth（SSoT）として機能する。

    設計方針:
    - すべての Enum はこのファイルに集約する（循環参照回避）
    - 文字列ベース Enum を採用（JSONシリアライズ容易性確保）
    - 厳密な型制約により Phase 3.4 の「I/F不一致ゼロ」を実現

    ★ Phase 3.4 修正内容:
    - Spec v2.0.1 の Enum 定義と完全一致を保証
    - 既存コードは削除せず、意図を明示するコメントを追加
    - 将来拡張のための禁止事項・注意点を明文化
"""

# ================================
# import
# ================================
from enum import Enum

# ================================
# 定数 / 設定（現時点ではなし）
# ================================

# ================================
# __all__（公開インターフェース）
# ================================
__all__ = [
    "NWFSeverity",
    "EngineState",
    "NWFActionType",
]

# ================================
# Enum 定義
# ================================

class NWFSeverity(str, Enum):
    """
    バリデーション結果の深刻度を定義する Enum。

    設計理由:
    - Validator の出力を標準化
    - StoryEngine の制御フロー分岐に使用
    - Adapter / IntegrityChecker 間の共通契約

    注意:
    - 値は文字列とし、JSON変換時の互換性を確保

    ★ Phase 3.4 追記:
    - Spec 5.1 と完全一致（INFO / WARNING / ERROR / CRITICAL）
    - Enum値の追加は禁止（Spec Driven Development準拠）
    """

    # 情報提供（処理継続）
    INFO = "INFO"

    # 軽微な問題（処理継続）
    WARNING = "WARNING"

    # シナリオ整合性違反（設定により停止）
    ERROR = "ERROR"

    # システム整合性破壊（即時停止）
    CRITICAL = "CRITICAL"

    def is_blocking(self) -> bool:
        """
        実行を停止すべきかを判定する。

        Returns:
            bool: 停止が必要な場合 True

        ★ 修正ポイント:
        - Spec 5.4（Severity Assignment Rule）に基づく挙動
        - ERROR も停止対象として扱う（Engineで緩和可能）
        """

        # CRITICAL は常に停止
        if self == NWFSeverity.CRITICAL:
            return True

        # ERROR は停止（設定依存だがデフォルトは停止）
        if self == NWFSeverity.ERROR:
            return True

        # WARNING / INFO は非停止
        return False


class EngineState(str, Enum):
    """
    StoryEngine / WorkflowEngine の状態を定義する Enum。

    設計理由:
    - Engine の状態遷移を明確化
    - Validator 実行タイミングの制御
    - デバッグおよび監査ログの可視化

    状態遷移例:
        INIT -> RUNNING -> VALIDATING -> RUNNING -> COMPLETED
        異常時: 任意状態 -> HALTED

    ★ Phase 3.4 追記:
    - Spec 5.3 と完全一致
    - 状態追加は禁止（Spec更新が先）
    """

    # 初期化状態
    INIT = "INIT"

    # 実行中
    RUNNING = "RUNNING"

    # 検証中
    VALIDATING = "VALIDATING"

    # 停止状態（エラー / CRITICAL）
    HALTED = "HALTED"

    # 完了状態
    COMPLETED = "COMPLETED"

    def is_terminal(self) -> bool:
        """
        終端状態かどうかを判定する。

        Returns:
            bool: 終端状態の場合 True

        ★ 修正なし（既存仕様がSpec準拠）
        """
        return self in {EngineState.HALTED, EngineState.COMPLETED}


class NWFActionType(str, Enum):
    """
    エンティティの行動種別を定義する Enum。

    設計理由:
    - StoryEngine の出力フォーマット統一
    - Timeline / Event モデルとの整合性確保
    - Validator による行動検証の基準

    使用箇所:
    - StoryEngine.timeline
    - EventEngine
    - Validator（行動制約チェック）

    ★ Phase 3.4 追記:
    - Spec 5.2 と完全一致
    - 行動タイプ追加はSpec更新が必須
    """

    # その場に留まる
    STAY = "STAY"

    # 移動
    MOVE = "MOVE"

    # 相互作用（会話・操作など）
    INTERACT = "INTERACT"

    # 戦闘
    BATTLE = "BATTLE"

    def is_movement(self) -> bool:
        """
        移動系アクションかどうかを判定する。

        Returns:
            bool: 移動系の場合 True

        ★ 修正なし（既存仕様維持）
        """
        return self == NWFActionType.MOVE


# ================================
# ▼旧コード・将来拡張メモ（削除せず保持）
# ================================

# ※ 将来的に以下のような拡張が検討される可能性があるが、
#   現時点では Spec に存在しないため実装禁止（Spec Driven Development）
#
# class NWFExtendedActionType(str, Enum):
#     TALK = "TALK"
#     TRADE = "TRADE"
#
# ↑ このような拡張は必ず Spec 更新後に実装すること


# ================================
# Main Guard（デバッグ用）
# ================================

if __name__ == "__main__":
    # ★ 動作確認（簡易テスト）
    print(NWFSeverity.INFO)
    print(NWFSeverity.ERROR.is_blocking())
    print(EngineState.COMPLETED.is_terminal())
    print(NWFActionType.MOVE.is_movement())


# ================================
# EOF
# ================================

# [EOF]