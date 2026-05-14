Source: docs/spec/Spec_Governance/NWF_Python_Implementation_Rules_v2.0.1.md
Updated: 2026-04-02T01:41:00+09:00
PIC: Engineer / ChatGPT

# NWF Python Implementation Rules v2.0.1

---

## 1. 概要

本ドキュメントは、NWF Phase 2 における Python 実装の標準規格を定義するものである。  
NWF v2.0.1 におけるすべての Python 実装ファイルは、本規格に厳密に従う必要がある。

本規格の目的は以下である。

- コード構造の統一
- 監査・追跡可能な実装
- Story OS / NWF Engine の長期保守性確保
- AI・人間双方による共同開発の標準化
- Spec Driven Development の実現

---

## 2. 適用範囲

本 Implementation Rules は以下に適用される。

- NWF Engine
- Story OS
- Data Control System
- Audit System
- State Machine
- AI Interface
- Workflow Engine
- Core Objects
- Utilities
- Logging System
- Execution System
- その他 NWF v2.0.1 に属するすべての Python ファイル

---

## 3. Python ファイル標準メタデータ

すべての Python ファイルは、ファイル冒頭に docstring 形式でメタデータを記述しなければならない。

### 3.1 メタデータヘッダー形式

必ず以下の順序で記述すること。

Source: ファイルパス  
Updated: ISO 8601 形式 JST  
PIC: Engineer / ChatGPT  
Version: NWF v2.0.1  
Dependencies: 依存 Spec ファイル一覧  
Docstring: ファイル概要説明  

### 3.2 例

Source: src/core/audit_logger.py  
Updated: 2026-04-01T18:32:00+09:00  
PIC: Engineer / ChatGPT  
Version: NWF v2.0.1  
Dependencies:
    - docs/spec/Core_Spec/Audit_System.md
    - docs/spec/Data_Spec/Data_Model.md
Docstring:
    Audit Logger モジュール。
    NWF システム内のすべてのイベント・状態遷移・データ更新を監査ログとして記録する。

---

## 4. Time Policy（時間管理規則）

NWF システムでは、すべての時間は JST 固定とする。

### 4.1 タイムゾーン定義

timezone(timedelta(hours=9)) を必ず使用すること。

### 4.2 タイムスタンプ形式

ISO 8601 形式を使用する。

YYYY-MM-DDTHH:MM:SS+09:00

例:
2026-04-01T18:52:00+09:00

### 4.3 使用例

datetime.now(JST).isoformat()

---

## 5. Encapsulation / 公開インターフェース規則

各 Python モジュールでは __all__ を使用して公開インターフェースを明示すること。

例:

__all__ = [
    "AuditLogger",
    "DataStateMachine",
    "NWFObject"
]

これにより、外部モジュールからアクセス可能なクラス・関数を制御する。

---

## 6. コーディング規約

### 6.1 命名規則

| 対象 | 命名規則 |
|------|-----------|
| 変数 | snake_case |
| 関数 | snake_case |
| クラス | PascalCase |
| 定数 | UPPER_CASE |
| ファイル名 | snake_case |
| JSONキー | snake_case |

---

### 6.2 Docstring 規則

すべてのクラス・関数には Docstring を記述すること。

Docstring には以下を含める。

- 概要
- Args
- Returns
- Raises（必要な場合）
- 使用例（重要な場合）

---

### 6.3 コメント規則

コメントは日本語で記述すること。

以下を必ず説明する。

- なぜこの処理が必要か
- 状態遷移の理由
- データ構造の意味
- 例外処理の理由

---

## 7. ログ / 監査 / 状態管理

NWF システムでは以下を必須とする。

### 7.1 必須ログ対象

- システム起動
- オブジェクト生成
- 状態遷移
- データ更新
- エラー
- 例外
- 外部入力
- AI 実行
- Workflow 実行
- ファイル操作

### 7.2 ログレベル

| Level | 用途 |
|------|------|
| DEBUG | 開発用詳細ログ |
| INFO | 通常イベント |
| WARNING | 異常の可能性 |
| ERROR | エラー |
| CRITICAL | システム停止レベル |

---

## 8. ファイル構造標準

Python ファイルの基本構造は以下とする。

1. Docstring Metadata
2. import
3. 定数 / 設定
4. __all__
5. Utility Functions
6. Classes
7. Main Guard
8. EOF

---

## 9. 1-Click Copy 規則

成果物として Python ファイルを出力する場合、

- ファイル全体を 1つのコードブロックに入れる
- コードブロックは python を指定
- コードブロック内でバッククォートを使用しない
- ファイル最終行に必ず EOF を記述

Python の場合の EOF 表記:

# [EOF]

---

## 10. Spec Driven Development 規則

NWF の Python 実装は Spec Driven Development に従う。

### 10.1 実装前に必ず確認する Spec

- Core Spec
- Data Spec
- Architecture Spec
- Engine Spec
- Execution Spec
- AI Interface Spec
- Workflow Spec
- Governance Spec

Spec に存在しない機能は実装してはならない。  
Spec を先に更新し、その後実装する。

---

## 11. バージョン管理規則

NWF Python 実装は NWF Spec Version と同期する。

| Spec Version | Python Implementation |
|--------------|----------------------|
| v2.0.1 | v2.0.1 |
| v2.1.0 | v2.1.0 |

Implementation Rules も Spec Version に合わせる。

---

## 12. まとめ

NWF Python Implementation Rules v2.0.1 の目的は以下である。

- 実装の完全標準化
- AI と人間の共同開発ルール統一
- 監査可能なシステム構築
- Story OS / NWF Engine の長期運用
- Spec Driven Development の徹底
- コード品質の長期維持
- フェーズ開発の安定化

本規格は NWF v2.0.1 のすべての Python 実装に対して強制適用される。

---

[EOF]