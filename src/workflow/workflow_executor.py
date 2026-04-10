"""
Source: src/workflow/workflow_executor.py
Updated: 2026-04-11T06:06:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Project_Governance/NWF_Workflow_Engine_Spec_v2.0.1.md
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
Docstring:
    Workflow Executor モジュール。
    各 Engine の呼び出しを担当し、ExecutionResult を生成する。
    型変換（dict ↔ NWFObject）およびエラーハンドリングを統一的に管理する。
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional

# NWFObject（基底オブジェクト）
from src.models.nwf_object import NWFObject

# JST 定義
JST = timezone(timedelta(hours=9))

__all__ = [
    "WorkflowExecutor"
]


class WorkflowExecutor:
    """
    WorkflowExecutor クラス。

    概要:
        Task 定義に基づき、対象 Engine のメソッドを実行し、
        結果を ExecutionResult 形式で返却する。

    Args:
        None

    Returns:
        None
    """

    def execute(
        self,
        task: Dict[str, Any],
        context: Any
    ) -> Dict[str, Any]:
        """
        タスク実行

        Args:
            task (Dict[str, Any]): タスク定義
                必須キー:
                    - engine: str
                    - method: str
                    - params: Dict[str, Any]
            context (WorkflowContext): 実行コンテキスト

        Returns:
            Dict[str, Any]: ExecutionResult

        Raises:
            Exception: 実行時例外
        """

        transaction_id = context.transaction_id

        try:
            # Engine 名・メソッド名取得
            engine_name: str = task.get("engine")
            method_name: str = task.get("method")
            params: Dict[str, Any] = task.get("params", {})

            # パラメータを Context から解決
            resolved_params = self._resolve_params(params, context)

            # Engine 呼び出し
            result = self._invoke_engine(
                engine_name,
                method_name,
                resolved_params
            )

            # 結果を NWFObject に正規化
            nwf_object = self._to_nwf_object(result)

            return self._build_result(
                status="SUCCESS",
                data=nwf_object,
                transaction_id=transaction_id
            )

        except ValueError as e:
            # Logic Error → SUSPEND
            return self._build_result(
                status="SUSPEND",
                error_code="LOGIC_ERROR",
                message=str(e),
                transaction_id=transaction_id
            )

        except Exception as e:
            # Fatal Error → FAILURE
            return self._build_result(
                status="FAILURE",
                error_code="FATAL_ERROR",
                message=str(e),
                transaction_id=transaction_id
            )

    def _resolve_params(
        self,
        params: Dict[str, Any],
        context: Any
    ) -> Dict[str, Any]:
        """
        Context からパラメータを解決

        Args:
            params (Dict[str, Any]): 元パラメータ
            context (WorkflowContext): コンテキスト

        Returns:
            Dict[str, Any]: 解決済みパラメータ
        """

        resolved = {}

        for key, value in params.items():
            # Context 参照キーの場合
            if isinstance(value, str) and value.startswith("$"):
                context_key = value[1:]
                resolved[key] = context.get(context_key)
            else:
                resolved[key] = value

        return resolved

    def _invoke_engine(
        self,
        engine_name: str,
        method_name: str,
        params: Dict[str, Any]
    ) -> Any:
        """
        Engine 呼び出し

        Args:
            engine_name (str): Engine 名
            method_name (str): メソッド名
            params (Dict[str, Any]): パラメータ

        Returns:
            Any: 実行結果

        Raises:
            ValueError: Engine/Method 不正
        """

        try:
            module = __import__(f"src.core.{engine_name}", fromlist=[engine_name])
            engine = getattr(module, engine_name)()

            method = getattr(engine, method_name)

        except Exception:
            raise ValueError(f"Invalid engine or method: {engine_name}.{method_name}")

        return method(**params)

    def _to_nwf_object(self, data: Any) -> Optional[NWFObject]:
        """
        結果を NWFObject に変換

        Args:
            data (Any): 生データ

        Returns:
            Optional[NWFObject]: 変換後オブジェクト
        """

        if data is None:
            return None

        if isinstance(data, NWFObject):
            return data

        # dict の場合はラップ
        if isinstance(data, dict):
            return NWFObject(data)

        # その他型はそのままラップ
        return NWFObject({"value": data})

    def _build_result(
        self,
        status: str,
        transaction_id: str,
        data: Optional[NWFObject] = None,
        error_code: Optional[str] = None,
        message: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        ExecutionResult 生成

        Args:
            status (str): 状態
            transaction_id (str): トランザクションID
            data (Optional[NWFObject]): データ
            error_code (Optional[str]): エラーコード
            message (Optional[str]): メッセージ

        Returns:
            Dict[str, Any]: ExecutionResult
        """

        return {
            "status": status,
            "data": data,
            "error_code": error_code,
            "message": message,
            "transaction_id": transaction_id,
            "timestamp": datetime.now(JST).isoformat()
        }


# [EOF]