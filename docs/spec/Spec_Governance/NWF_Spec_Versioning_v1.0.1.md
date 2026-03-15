# NWF Specification Versioning v1.0.1

## 概要

本ドキュメントは NWF Specification のバージョン管理ルールを定義する。

## Version Structure

NWF Spec は以下の3段階バージョンを使用する。

Major.Minor.Patch

## Major Version

Major Version はフレームワークの世代を示す。

例

v1  
v2

## Minor Version

Minor Version は Spec 全体の見直しを伴う変更を示す。

例

v1.0  
v1.1  
v1.2

## Patch Version

Patch Version は個別ファイルの微修正を示す。

例

v1.0.0  
v1.0.1  
v1.0.2

## File Naming Rule

Spec ファイルは以下の形式で命名する。

ファイル名_vX.Y.Z.md

例

NWF_File_System_v1.0.0.md

## v1.0 と v1.0.0 の扱い

NWF Spec では以下のルールを採用する。

ファイル名_v1.0.md は ファイル名_v1.0.0.md と同一のものとみなす。

## Patch Update

微修正の場合は Patch Version を更新する。

例

v1.0.0 → v1.0.1 → v1.0.2

## Minor Update

Spec 全体の見直しが必要な場合は Minor Version を更新する。

例

v1.0 → v1.1

## Git Tag

Spec Version は Git Tag として管理することが推奨される。

例

spec-v1.0  
spec-v1.1

## Version

Version: v1.0.1