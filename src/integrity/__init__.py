"""
Source: src/integrity/__init__.py
Updated: 2026-05-15T20:15:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
    - docs/project/NWF_Phase_3.5_Debug_Work_Plan_v20260502.md
    - docs/spec/Execution_Spec/NWF_Consistency_Validator_Spec_v2.0.1_Phase_3.5.md
    - src/integrity/consistency_validator.py
    - src/integrity/validation_result.py
Docstring:
    Integrity パッケージの公開 I/F を定義する。

    本パッケージは Validation Orchestration と
    Validation Result の公開インターフェースを提供する。

    外部モジュールは本パッケージ経由で
    ConsistencyValidator / ValidationResult /
    NWFSeverity にアクセスすることを標準とする。
"""

from .consistency_validator import ConsistencyValidator
from .validation_result import NWFSeverity
from .validation_result import ValidationResult

__all__ = [
    "ConsistencyValidator",
    "ValidationResult",
    "NWFSeverity",
]

# [EOF]