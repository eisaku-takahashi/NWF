Source: docs/spec/Kernel_Spec/NWF_Temporal_Management_v2.0.1.md
Updated: 2026-04-06T11:23:00+09:00
PIC: Engineer / ChatGPT

# NWF Temporal Management v2.0.1

---

## 1. 概要

NWF Temporal Management は、NWF Kernel における時間管理・バージョン管理・スナップショット管理・世界線管理を統合的に扱う基盤システムである。

NWF における時間管理は単なるタイムスタンプ管理ではなく、以下を目的とする。

- 因果律の保証
- Event / Scene / Story の時間順序管理
- Version / Snapshot による状態履歴管理
- Branch / World Line による世界線分岐管理
- Rollback / Replay / Time Travel の実現
- Engine Execution Pipeline の時間的一貫性保証
- Audit Log の順序保証
- Concurrency Control との統合

Temporal Management は Kernel の最重要機能の一つであり、Audit System、Version Manager、Timeline Engine、Execution Pipeline と密接に連携する。

---

## 2. NWF における時間の種類

NWF では複数の時間概念を区別して管理する。

### 2.1 Narrative Time（物語時間）
物語内の時間軸。  
Scene、Event、Beat、Timeline がこの時間軸上に配置される。

例:
- Day 1
- Year 1205
- Episode Timeline

Timeline Engine が管理する。

### 2.2 Logical Time（論理時間）
Event や Beat の因果関係上の順序を表す時間。  
Narrative Time と一致するとは限らない。

例:
- Foreshadowing → Reveal
- Cause → Effect
- Setup → Payoff

Story Engine / Event Engine が利用する。

### 2.3 Transaction Time（トランザクション時間）
Kernel が Audit Log に書き込みを行った物理時間。  
全ての変更は Transaction Time によって順序付けされる。

UUID v7 により時間順序が保証される。

### 2.4 Version Time（バージョン時間）
Snapshot / Version の履歴上の時間。  
どの Version からどの Version が派生したかという系統時間。

Version Manager が管理する。

### 2.5 Branch Time（世界線時間）
Branch / World Line の分岐タイミングを示す時間。  
ある Version から分岐した別世界線を表す。

---

## 3. Temporal Management System 構成

Kernel 内の Temporal Management は以下のコンポーネントで構成される。

### 3.1 Temporal Manager
Temporal 管理全体を統括する Kernel コンポーネント。

責務:
- Timeline 管理
- Version / Snapshot 管理
- Branch 管理
- Temporal Query
- Temporal Consistency 検証
- Time Travel / Rollback / Replay 制御

### 3.2 Timeline Manager
物語時間（Narrative Time）を管理する。

管理対象:
- Timeline
- Scene Time
- Event Time
- Episode / Chapter 時間
- Parallel Timeline

Timeline Engine と連携する。

### 3.3 Version Manager
データのバージョン履歴を管理する。

管理対象:
- Version ID
- Parent Version
- Snapshot ID
- Branch ID
- Transaction ID

Audit Log と密接に連携する。

### 3.4 Snapshot Manager
特定 Version 時点の Entity 状態のスナップショットを管理する。

Snapshot の特徴:
- Immutable（不変）
- Read Only
- Engine 実行時の基準状態
- Rollback / Replay の基準点

### 3.5 Branch Manager
世界線（Branch / World Line）を管理する。

管理内容:
- Branch ID
- Parent Branch
- Base Version
- Merge History
- Parallel World Line

Git の branch 概念に近い。

---

## 4. Temporal Data Flow

Engine 実行時の時間データフローは以下の通り。

1. Engine が Version Manager に Version を指定して Snapshot を取得
2. Snapshot を元に Execution Context を生成
3. Engine が Logical Time / Narrative Time を進めながら演算
4. 結果を Transaction として Kernel に送信
5. Kernel が Audit Log に Transaction を記録
6. 新しい Version が生成される
7. 必要に応じて Snapshot を作成
8. Timeline / Version / Branch 情報が更新される

この流れにより、全ての変更は時間順序と因果関係を保持したまま保存される。

---

## 5. Temporal Consistency Model

NWF は以下の整合性モデルを採用する。

### 5.1 Causal Consistency（因果整合性）
原因より結果が先に発生することは禁止される。

例:
- Foreshadowing は Reveal より前
- Event Cause は Effect より前

### 5.2 Transaction Ordering
Audit Log の Transaction は必ず時間順に並ぶ。

UUID v7 により順序が保証される。

### 5.3 Snapshot Isolation
Engine 実行中は Snapshot を使用し、他 Transaction の影響を受けない。

### 5.4 Branch Consistency
Branch は必ず Parent Version から派生する。

---

## 6. Time Travel / Rollback / Replay

Temporal Management は以下の機能を提供する。

### 6.1 Rollback
指定 Snapshot または Version に状態を戻す。

### 6.2 Replay
Audit Log を最初から再実行し、状態を再構築する。

### 6.3 Time Travel Branch
過去の Version から新しい Branch を作成し、別の物語展開を生成する。

---

## 7. 他 Kernel システムとの関係

### 7.1 Audit System
Temporal Management は Audit Log の Transaction Time に依存する。

### 7.2 Concurrency Control
同時書き込み時の順序と整合性を Temporal と Concurrency が共同で保証する。

### 7.3 Engine Execution Pipeline
Engine は必ず Snapshot を基準に実行され、Commit 時に新 Version が生成される。

### 7.4 Entity Manager
Entity の状態履歴は Version / Snapshot によって管理される。

### 7.5 Metadata Manager
Spec Version と Data Version の対応関係を管理する。

---

## 8. まとめ

NWF Temporal Management は以下を統合管理する Kernel 中核システムである。

- Timeline（物語時間）
- Logical Time（因果時間）
- Transaction Time（Audit Log 時間）
- Version / Snapshot（状態履歴）
- Branch / World Line（世界線）
- Rollback / Replay / Time Travel
- Temporal Consistency
- Engine Execution Pipeline の時間的一貫性

Temporal Management は NWF Kernel における
「因果律」「履歴」「世界線」を統合する基盤であり、
Audit System、Version Manager、Concurrency Control と並ぶ
最重要 Kernel コンポーネントである。

---

[EOF]