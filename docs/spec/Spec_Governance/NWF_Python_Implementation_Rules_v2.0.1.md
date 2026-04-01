Source: docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
Updated: 2026-04-01T21:58:00+09:00
PIC: Engineer / ChatGPT

# NWF Python Implementation Rules v2.0.1

---

## 1. 概要

本ドキュメントは、NWF v2.0.1 における Python 実装の標準規格を定義するものである。  
NWF の Spec 群（Core, Data, Engine, Architecture 等）で定義された「What（何を作るか）」に対し、本 Implementation Rules は「How（どのように Python で実装するか）」を定義する。

本規格は NWF Phase 2 – Implementation において作成されるすべての Python ファイルに適用される。

対象範囲：
- src/ 以下のすべての Python モジュール
- audit_logger.py
- data_state_machine.py
- nwf_object.py
- engine / workflow / system / models / loader / utils モジュール
- tests/ 以下のテストコード

---

## 2. 適用範囲（Scope）

本 Implementation Rules は以下を対象とする。

1. Python コーディング規約
2. メタデータヘッダー規格
3. ディレクトリ構造規格
4. ログおよび監査ログ規格
5. 例外・エラーハンドリング規格
6. NWF Object 実装規格
7. State Machine 実装規格
8. 命名規則
9. タイムスタンプ規格
10. バージョン管理規格
11. モジュール依存関係規格
12. JSON / ファイルフォーマット規格
13. テスト規格
14. セキュリティおよび整合性規格

---

## 3. Directory Structure（ディレクトリ構造規格）

NWF の物理ディレクトリ構造は OS レイヤー構造に対応する。

標準ディレクトリ構造：

NWF/
    src/
        engine/
        workflow/
        system/
        loader/
        models/
        utils/
    data/
        schema/
    logs/
        audit/
    docs/
        spec/
    tests/

各ディレクトリの役割：

src/engine/  
状態遷移、整合性チェックなどのコアロジック。

src/workflow/  
ワークフロー制御、HITL ゲートなどの処理フロー。

src/system/  
監査ログ、外部同期、システムインフラ関連。

src/loader/  
Spec や設定ファイルの読み込み。

src/models/  
NWF Object などデータ構造定義。

src/utils/  
共通ユーティリティ。

data/schema/  
JSON Schema ファイル保存場所。

logs/audit/  
監査ログ（JSONL）保存場所。

tests/  
Unit Test / Integration Test。

---

## 4. Python Coding Standard

Python 実装は以下の規格に従う。

- PEP 8 準拠
- PEP 257 Docstring 準拠
- 型ヒント必須（typing）
- 変数・関数名は snake_case
- クラス名は PascalCase
- 定数は UPPER_CASE
- print() 使用禁止（logging を使用）
- Any の使用は最小限
- すべての関数に戻り値型を明記
- Optional 型は明示する
- None を返す関数も -> None を記述

---

## 5. Metadata Header & Docstring Rules

すべての Python ファイルの冒頭に必ず docstring 形式でメタデータヘッダーを記述する。

必須項目：

Source: src/<module>/<file>.py
Updated: ISO 8601 JST
PIC: Engineer / ChatGPT
Version: NWF v2.0.1
Dependencies:
Docstring:

Updated の形式：
YYYY-MM-DDTHH:MM:SS+09:00

タイムスタンプは JST 固定とする。

Python 実装では必ず以下を使用する：

timezone(timedelta(hours=9))

---

## 6. Naming Rules（命名規則）

命名規則は以下の通り。

File Name:
snake_case
例：nwf_object.py

Class Name:
PascalCase
例：NWFObject

Function / Variable:
snake_case

ID:
Prefix_ID_Number
例：
SPEC_CORE_001
CHAR_HERO_001
OBJ_STORY_001

Spec File:
NWF_<Category>_<Name>_vX.X.X.md

---

## 7. Timestamp & Time Policy

タイムスタンプは以下の規格に従う。

標準形式：
ISO 8601

例：
2026-04-01T21:30:00+09:00

タイムゾーン：
JST (UTC+09:00) 固定

Python 実装では以下を使用する：

timezone(timedelta(hours=9))

ログ・監査ログ・データの created_at / updated_at はすべてこの形式を使用する。

---

## 8. Logging & Audit Log Rules

ログは通常ログと監査ログを分離する。

ログレベル：
DEBUG
INFO
WARNING
ERROR
CRITICAL

監査ログ仕様：

形式：
JSONL（1行1JSON）

ポリシー：
Append Only（追記専用）
既存ログの編集・削除は禁止。

監査ログ必須フィールド：

timestamp
event_type
user
object_id
old_state
new_state
version
message

保存場所：
logs/audit/

---

## 9. Exception & Error Handling Rules

エラー処理ポリシー：

- Fail Fast（エラー発生時は即停止）
- 例外は raise する
- print は使用禁止
- logging.error に記録
- 不正な状態遷移は例外
- 整合性エラーは例外
- 外部保存失敗時はロールバック

例外階層：

NWFError
    NWFValidationError
    NWFStateTransitionError
    NWFAuditError
    NWFSchemaError
    NWFIntegrityError
    NWFExecutionError

---

## 10. Data Object Implementation Rules

NWF Object は以下のフィールドを持つ。

id
type
title
content
status
version
dependencies
created_at
updated_at
created_by
approved_by
approved_at
metadata

JSON Schema と完全一致する必要がある。

Approved 後は metadata 以外の変更は禁止。
変更が必要な場合は version を更新する。

---

## 11. State Machine Implementation Rules

状態遷移は以下の状態を持つ。

DRAFT
REVIEW
APPROVED
RELEASED
ARCHIVED

遷移ルール：

draft → review
review → approved
review → draft
approved → released
released → archived

Approved への遷移には以下が必須：
approved_by
approved_at
HITL Gate 通過

不正遷移は例外を発生させる。

---

## 12. Versioning Rules

バージョン管理は Semantic Versioning を使用する。

MAJOR.MINOR.PATCH

Spec Version
Object Version
Engine Version
Workflow Version

すべて SemVer に従う。

---

## 13. Module Dependency Rules（依存関係規格）

モジュール依存はレイヤー構造に従う。

Layer 構造：

system
engine
workflow
application

依存ルール：

上位レイヤー → 下位レイヤー OK
下位レイヤー → 上位レイヤー NG

例：

workflow → engine OK
engine → workflow NG
engine → system OK
system → engine NG

循環参照は禁止。

---

## 14. File Encoding / JSON Rules

ファイルエンコーディング：
UTF-8

JSON 規格：
- キーは snake_case
- 単位を明記
- ISO8601 timestamp
- UTF-8
- 改行は LF

JSONL：
1行1JSON
Append Only

---

## 15. Testing Rules

tests/ ディレクトリに Unit Test を作成する。

テスト規約：

tests/test_<module>.py

pytest 使用
State Machine
NWF Object
Audit Logger
Schema Validation
Workflow Engine

主要モジュールは必ずテストを書く。

---

## 16. Security & Integrity Rules

整合性ポリシー：

- Audit Log は改ざん不可
- Approved データは変更不可
- Version で履歴管理
- Schema Validation 必須
- State Machine を必ず通す
- 直接 JSON を編集しない
- Engine 経由でのみ変更

---

## 17. EOF / Formatting Rules

Python / Markdown / JSON / Text ファイルの最終行には必ず EOF タグを記述する。

Python:
# [EOF]

Markdown / Text:
[EOF]

すべての成果物は 1 つのコードブロックで出力する。

---

## 18. まとめ

本 Implementation Rules は、NWF v2.0.1 の Python 実装における統一規格であり、  
すべてのモジュール・エンジン・データ管理・監査ログ・状態遷移処理は本規格に従って実装される。

Spec = What（何を作るか）
Implementation Rules = How（どう実装するか）
Code = Implementation（実装）

この三層構造により、NWF System の一貫性・再現性・監査性・拡張性を保証する。

[EOF]