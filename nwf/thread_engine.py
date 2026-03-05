#!/usr/bin/env python3
# ==========================================================
# ThreadEngine v0.2
# NWF仕様準拠 実装版（JSON出力対応）
# ----------------------------------------------------------
# 追加機能：
#   - --json オプション
#   - 構造化出力対応
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
    pass


class IDDuplicateError(ThreadValidationError):
    pass


# ==========================================================
# ThreadValidator
# ==========================================================

class ThreadValidator:

    def __init__(self, data: Dict, strict: bool = False):
        self.data = data
        self.strict = strict
        self.thread_ids = set()
        self.duplicate_ids = set()
        self.threads: List[Dict] = []

    # ------------------------------------------------------

    def validate(self):

        self._validate_root_structure()
        self.threads = self.data["threads"]

        for index, thread in enumerate(self.threads):
            self._validate_thread_basic(thread, index)

        self._check_duplicate_ids()

        unresolved_count = 0

        for thread in self.threads:
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

        if thread_id in self.thread_ids:
            self.duplicate_ids.add(thread_id)
        else:
            self.thread_ids.add(thread_id)

        if status not in ALLOWED_STATUS:
            raise ThreadValidationError(
                f"threads[{index}] の status '{status}' は不正です。"
            )

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
        raise ThreadValidationError(f"JSON読み込みエラー: {e}")


# ==========================================================
# CLI
# ==========================================================

def main():

    parser = argparse.ArgumentParser(
        description="NWF ThreadEngine v0.2 Validator"
    )

    parser.add_argument("path", help="threads_master.json のパス")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json", action="store_true")

    args = parser.parse_args()

    try:
        data = load_json(args.path)
        validator = ThreadValidator(data, strict=args.strict)
        result = validator.validate()

        if args.json:
            output = {
                "status": "ok",
                "total": result["total"],
                "unresolved": result["unresolved"],
                "ratio": result["ratio"],
                "strict": args.strict
            }
            print(json.dumps(output, ensure_ascii=False))
        else:
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

        sys.exit(0)

    except ThreadValidationError as e:

        if args.json:
            error_output = {
                "status": "error",
                "error_type": e.__class__.__name__,
                "message": str(e)
            }
            print(json.dumps(error_output, ensure_ascii=False))
        else:
            print("ERROR:")
            print(str(e))

        sys.exit(1)


if __name__ == "__main__":
    main()