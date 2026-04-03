Source: docs/spec/Core_Spec/NWF_Data_Model_v2.0.1.md
Updated: 2026-04-04T00:39:00+09:00
PIC: Engineer / ChatGPT

# NWF Data Model v2.0.1

---

## 1. 概要（更新）

本ドキュメントは  
NWF v2.0.1 における **Story Data Model の標準構造** を定義する。

本バージョンでは、以下を新たに導入・強化する。

- Graph指向データモデル
- Entity関係の明確化
- 多対多関係の正式定義
- Timeline独立管理
- **Kernel Audit System との統合（重要追加）**

---

## 2. 問題点と不足Entityの特定

### 2.1 不足していたEntity（解決済）

Event  
State  
Relationship  
Timeline  
World  

### 2.2 階層構造の問題（解決済）

旧構造：

WorldRule → Character → Thread → Scene → Beat

問題：

- Scene / Event / Beat の関係が曖昧
- 状態変化が構造に含まれていない

### 2.3 データモデルの問題（解決済）

- 多対多関係の欠如
- Timelineの未独立化
- State管理不在

→ v2.0.1 では Graphモデルで解決

---

## 3. 新データ構造（Graph指向モデル）

Story
 ├── World
 │    └── WorldRule
 │
 ├── Characters
 │    ├── Character
 │    ├── State
 │    └── Relationship
 │
 ├── Threads
 │    └── Thread
 │         └── Scene
 │              └── Event
 │                   └── Beat
 │
 ├── Timeline
 │    └── Scene / Event Timeline
 │
 └── Links
      ├── character_scene_links
      ├── character_event_links
      ├── thread_scene_links
      └── relationship_links

---

## 4. 構造定義

### 4.1 構造軸（Narrative Structure Axis）

Thread → Scene → Event → Beat

### 4.2 動態要素（Dynamic Elements）

Character  
State  
Relationship  
Timeline  

---

## 5. Entity関係マトリックス

World
- world_rule_ids

WorldRule
- world_id

Character
- world_id
- state_ids
- relationship_ids
- thread_ids
- scene_ids
- event_ids
- audit_context

Thread
- related_character_ids
- scene_ids

Scene
- thread_ids
- location
- participant_character_ids
- event_ids
- timeline_id

Event
- scene_id
- involved_character_ids
- beat_ids
- state_change_ids
- timeline_id

Beat
- event_id

State
- character_id
- related_event_id

Relationship
- character_id_1
- character_id_2

Timeline
- scene_ids
- event_ids

---

## 6. Audit System 統合（新規追加）

NWF v2.0.1 では、すべての Entity は  
**Kernel Audit System と因果関係を持つ必要がある。**

### 6.1 Audit Context 定義

各 Entity は以下のフィールドを持つことを推奨する。

audit_context:
- last_transaction_id
- created_at_jst
- updated_at_jst
- created_by
- updated_by

### 6.2 Transaction ID

- すべてのデータ変更は transaction_id を持つ
- transaction_id は Audit Log と完全に一致する
- UUID形式を推奨

### 6.3 Actor 定義

actor フィールドは以下の形式を許容する：

system:loader  
system:engine  
user:12345  
ai:gpt  

### 6.4 Audit連携ルール

- Entity生成 → CREATEイベント記録
- Entity更新 → UPDATEイベント記録
- Entity削除 → DELETEイベント記録
- State変化 → STATE_TRANSITIONイベント記録
- Validation失敗 → ERRORイベント記録

---

## 7. Story Database 実装ガイドライン

### 7.1 Database Model

Document-Graph Hybrid Model

### 7.2 JSON保存単位

worlds.json  
world_rules.json  
characters.json  
relationships.json  
states.json  
threads.json  
scenes.json  
events.json  
beats.json  
timeline.json  
links.json  

### 7.3 Link Table

character_scene_links  
character_event_links  
thread_scene_links  
relationship_links  

---

## 8. ID参照原則

- EntityはIDで参照する
- 子は親IDを持つ
- 多対多はLinkテーブル
- 循環参照は禁止
- 構造軸に従う

---

## 9. Data Model 設計原則

- Graph指向
- ID参照ベース
- Document DB互換
- Git管理適合
- AI解析適合
- 拡張性
- Audit対応（重要）

---

## 10. まとめ

NWF Data Model v2.0.1 は以下を実現する。

- 完全なGraph構造
- 多対多関係管理
- Timeline管理
- 状態管理の明確化
- **Audit Systemとの完全統合**

これにより NWF は

- データの完全追跡
- 状態変化の証拠保存
- AI生成の説明責任
- システムの一貫性保証

を実現する。

---

[EOF]