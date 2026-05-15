"""
Source: src/models/__init__.py
Updated: 2026-05-15T21:51:00+09:00
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
    - docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
    - docs/project/NWF_Phase_3.5_Debug_Work_Plan_v20260502.md
    - docs/spec/Core_Spec/NWF_Entity_ID_System_v2.0.1.md
    - docs/spec/Execution_Spec/NWF_Validation_System_v2.0.1.md
Docstring:
    Models パッケージの公開 I/F を定義する。

    本モジュールは NWF v2.0.1 における
    Models 層の公開インターフェースを統一管理する。

    外部モジュールは本 __init__.py 経由で
    Models オブジェクトへアクセスする。

    Spec Driven Development に従い、
    package 内部構造を外部へ露出しない。
"""

from .nwf_object import NWFObject

__all__ = [
    "NWFObject",
]

# [EOF]