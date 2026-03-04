#!/usr/bin/env python3
# ==========================================================
# ThreadEngine v0.1
# NWF仕様準拠 実装版（ID重複優先修正版）
# ----------------------------------------------------------
# 役割：
#   - threads_master.json の構造検証
#   - thread整合性検証
#   - ID重複検出（最優先）
#   - 未回収率計算
#   - strictモード対応
#
# 仕様参照：
#   docs/specification/ThreadEngine_v0.1.md
# ==========================================================

import json
import sys
import argparse
from typing import Dict, List


# ==========================================================
# 定数定義
# ==========================================================

ALLOWED_STATUS = {
    "open",
    "resolved",
    "partially_resolved",
    "abandoned",
    "thematic"
}

UNRESOLVED_STATUS = {
    "open",
    "partially_resolved",
    "abandoned"
}


# ==========================================================
# 例外定義
# ==========================================================

class ThreadValidationError(Exception):
    """ThreadEngine検証エラー基底クラス"""
    pass


class IDDuplicateError(ThreadValidationError):
    """ID重複エラー"""
    pass


# ==========================================================
# ThreadValidator
# ==========================================================

class ThreadValidator:
    """
    threads_master.json 全体を検証するValidator。
    """

    def __init__(self, data: Dict, strict: bool = False):
        self.data = data
        self.strict = strict
        self.thread_ids = set()
        self.duplicate_ids = set()
        self.threads: List[Dict] = []

    # ------------------------------------------------------
    # エントリポイント
    # ------------------------------------------------------

    def validate(self):
        """
        検証メイン処理。
        検証順序：
            1. ルート構造
            2. thread必須項目チェック
            3. ID重複検出（最優先）
            4. strictチェック
            5. 未回収率計算
        """

        # 1. ルート構造チェック
        self._validate_root_structure()

        self.threads = self.data["threads"]

        # 2. thread基本検証（ID収集含む）
        for index, thread in enumerate(self.threads):
            self._validate_thread_basic(thread, index)

        # 3. ID重複チェック（strictより前に実行）
        self._check_duplicate_ids()

        # 4. strictチェック + 未回収数カウント
        unresolved_count = 0

        for index, thread in enumerate(self.threads):
            status = thread["status"]

            if status in UNRESOLVED_STATUS:
                unresolved_count += 1

            if self.strict:
                if status in UNRESOLVED_STATUS:
                    raise ThreadValidationError(
                        f"strictモード: 未回収スレッド検出 ({thread['id']})"
                    )

                if status == "abandoned":
                    raise ThreadValidationError(
                        f"strictモード: abandoned スレッド検出 ({thread['id']})"
                    )

        # 5. 未回収率計算
        total_threads = len(self.threads)
        unresolved_ratio = (
            unresolved_count / total_threads
            if total_threads > 0 else 0
        )

        return {
            "total": total_threads,
            "unresolved": unresolved_count,
            "ratio": unresolved_ratio
        }

    # ------------------------------------------------------
    # ルート構造検証
    # ------------------------------------------------------

    def _validate_root_structure(self):
        if not isinstance(self.data, dict):
            raise ThreadValidationError("ルートは辞書型である必要があります。")

        required_fields = {"project", "version", "threads"}

        for field in required_fields:
            if field not in self.data:
                raise ThreadValidationError(
                    f"ルートに必須フィールド '{field}' がありません。"
                )

        if not isinstance(self.data["threads"], list):
            raise ThreadValidationError("'threads' は配列である必要があります。")

    # ------------------------------------------------------
    # thread基本検証（ID収集＋status検証）
    # ------------------------------------------------------

    def _validate_thread_basic(self, thread: Dict, index: int):

        if not isinstance(thread, dict):
            raise ThreadValidationError(
                f"threads[{index}] は辞書型である必要があります。"
            )

        if "id" not in thread:
            raise ThreadValidationError(
                f"threads[{index}] に 'id' が必要です。"
            )

        if "status" not in thread:
            raise ThreadValidationError(
                f"threads[{index}] に 'status' が必要です。"
            )

        thread_id = thread["id"]
        status = thread["status"]

        # ID重複検出用収集
        if thread_id in self.thread_ids:
            self.duplicate_ids.add(thread_id)
        else:
            self.thread_ids.add(thread_id)

        # status enum検証
        if status not in ALLOWED_STATUS:
            raise ThreadValidationError(
                f"threads[{index}] の status '{status}' は不正です。"
            )

    # ------------------------------------------------------
    # ID重複チェック（最優先）
    # ------------------------------------------------------

    def _check_duplicate_ids(self):
        if self.duplicate_ids:
            ids = ", ".join(sorted(self.duplicate_ids))
            raise IDDuplicateError(
                f"ID重複が検出されました: {ids}"
            )


# ==========================================================
# JSON読み込み
# ==========================================================

def load_json(path: str) -> Dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"JSON読み込みエラー: {e}")
        sys.exit(1)


# ==========================================================
# CLI
# ==========================================================

def main():

    parser = argparse.ArgumentParser(
        description="NWF ThreadEngine v0.1 Validator"
    )

    parser.add_argument(
        "path",
        help="threads_master.json のパス"
    )

    parser.add_argument(
        "--strict",
        action="store_true",
        help="strictモード有効化"
    )

    args = parser.parse_args()

    data = load_json(args.path)

    validator = ThreadValidator(data, strict=args.strict)

    try:
        result = validator.validate()

        total = result["total"]
        unresolved = result["unresolved"]
        ratio = result["ratio"]

        print("Thread検証結果")
        print(f"Total: {total}")
        print(f"Unresolved: {unresolved} / {total} ({ratio:.0%})")

        if unresolved > 0 and not args.strict:
            print("WARNING: 未回収スレッドがあります。")
        else:
            print("OK")

    except ThreadValidationError as e:
        print("ERROR:")
        print(str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()