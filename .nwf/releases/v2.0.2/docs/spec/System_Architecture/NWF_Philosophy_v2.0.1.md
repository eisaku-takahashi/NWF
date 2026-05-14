Source: NWF/docs/spec/System_Architecture/NWF_Philosophy_v2.0.1.md
Updated: 2026-04-06T01:30:00+09:00
PIC: Engineer / ChatGPT

# NWF_Philosophy v2.0.1

---

## 1. 概要

本ドキュメントは、Narrative Workflow Framework（NWF）の設計思想（Philosophy）を定義する最上位概念仕様である。  
NWF は単なる物語生成ツールではなく、**物語の因果律・存在証明・履歴を物理的に管理するシステム**として設計される。

本 Philosophy は、すべての Core Spec、System Architecture、Implementation、Schema の上位概念として位置付けられる。

---

## 2. NWF の本質的設計思想 (Core Philosophy)

### 2.1 なぜ NWF は存在するのか

従来の物語生成システムは確率的な文章生成を前提としており、設定矛盾、時間軸崩壊、存在しない事象の生成などの問題を根本的に解決できなかった。

NWF は物語を以下のように再定義するために存在する。

**「物語とは、状態とトランザクションの連鎖によって構成される決定論的なデータ遷移である。」**

つまり、物語は文章ではなく、**状態遷移の結果として表現されるログの集合**である。

---

### 2.2 NWF が保証するもの

NWF はシステムレベルで次の 3 つを保証する。

1. 因果の一貫性 (Causal Consistency)  
   すべての状態変化は、直前の状態と正当なトランザクションからのみ発生する。

2. 存在の証明 (Proof of Existence)  
   Audit Log に記録されていない事象は、その世界では「存在しない」とみなす。

3. 記述の正典性 (Canonical Specification)  
   実装よりも Spec（仕様書）が絶対的な正典であり、実装は Spec に従属する。

---

### 2.3 従来の物語生成との違い

| 項目 | 従来の物語生成 | NWF |
|------|----------------|-----|
| 制御対象 | 自然言語テキスト | 構造化データ |
| 整合性維持 | 人間・プロンプト | Kernel バリデーション |
| 時間管理 | 線形時間 | タイムラインモデル |
| AI の役割 | 執筆者 | 実行エンジン |
| 物語の本体 | 文章 | 状態遷移ログ |

---

## 3. アーキテクチャ原則 (Architectural Principles)

### 3.1 Spec-Driven Architecture

NWF は Spec Driven Architecture を採用する。

原則:
- 仕様が最上位
- 実装は仕様の影
- 仕様が更新されない実装変更はバグ

関係:
Philosophy → Spec → Architecture → Implementation → Data

---

### 3.2 Causality System

NWF におけるデータの現在値は本質ではない。  
本質は「どのような因果でその状態になったか」である。

原則:
Current State = Initial State + Σ(Transactions)

すべての変更は Audit Log を通過しなければならない。

---

### 3.3 Immutability / Append Only

NWF のログは追記専用であり、過去のデータは変更・削除できない。

誤ったデータは削除ではなく、
**修正トランザクション**
によってのみ変更される。

原則:
- Past cannot be changed
- Only future interpretation can change

---

### 3.4 Narrative Operating System

NWF はライブラリではなく OS である。

構造:

Layer:
- Kernel
- Engine
- Application
- Interface

役割:
- Kernel: 整合性・因果律・ログ管理
- Engine: プロット計算・感情曲線・イベント生成
- Application: 物語制作ツール
- Interface: 人間・AI 操作インターフェース

---

### 3.5 Traceability

すべての Entity と Transaction は一意の ID を持ち、完全追跡可能でなければならない。

ID 要件:
- 時系列順序を持つ
- 衝突しない
- 分散生成可能

NWF では UUID v7 の採用を標準とする。

---

## 4. 設計哲学の階層構造 (Hierarchy)

NWF の設計は次の階層構造を持つ。

### 4.1 Philosophy（思想）
物語は因果律の演算結果である。  
データはログの射影である。

### 4.2 Principles（原則）
- Kernel Centric
- Spec First
- Append Only
- Full Traceability

### 4.3 Constraints（制約）
- No Log, No Change
- Schema Strict Validation
- All Changes Are Transactions
- State Is Derived From Log

### 4.4 Implementation Mapping
各思想は実装に対応する。

| Concept | Implementation |
|--------|---------------|
| Causality | audit_log_manager |
| Entity | nwf_object |
| State Transition | data_state_machine |
| Version | version_manager |
| Timeline | timeline_manager |

---

## 5. 暗黙ルール (Implicit Rules)

NWF 設計から導出される暗黙ルールを明文化する。

1. 作者であってもログなしに世界を変更できない
2. バージョン管理はバックアップではなく世界線分岐である
3. 整合性は物語の面白さより優先される
4. 現在の状態はログから再構築可能でなければならない
5. すべてのイベントはトランザクションとして記録される

---

## 6. 現状仕様の矛盾と是正方針

### 6.1 UUID バージョン問題
Spec と Implementation で UUID v4 と v7 が混在している。

方針:
UUID v7 に統一する。

理由:
- 時系列ソート可能
- ログシステムと相性が良い
- 分散環境対応

---

### 6.2 ID 命名問題
Spec:
subject_id

Implementation:
id

方針:
Spec 用語を正典とし、
**subject_id に統一する**

---

## 7. まとめ

NWF の哲学を一文で表すと次のようになる。

**「物語とは文章ではなく、因果律によって記録される状態遷移ログである。」**

そして NWF は、

**「物語の因果律を物理的に強制する Narrative Operating System」**

として定義される。

この Philosophy は、NWF のすべての仕様・実装・データ構造の最上位原則として扱われる。

---

[EOF]