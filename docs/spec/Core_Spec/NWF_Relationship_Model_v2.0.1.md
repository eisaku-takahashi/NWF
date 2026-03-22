Source: docs/spec/Core_Spec/NWF_Relationship_Model_v2.0.1.md
Updated: 2026-03-22T17:15:00+09:00
PIC: Engineer / ChatGPT

# NWF Relationship Model v2.0.1

---

## 1. 概要

Relationship Model は
NWF におけるすべてのエンティティ間の関係を管理する
ネットワークモデルである。

v2.0.1 では Relationship を単なる参照関係ではなく、
**Dynamic Edge（動的な有向エッジ）**として定義する。

Relationship は以下を表現する：

・キャラクター関係  
・組織関係  
・Thread と Conflict の関係  
・Scene と Event の構造関係  
・対立関係  
・感情関係  
・時間によって変化する関係  
・物語ネットワーク構造  

Relationship Model は
NWF Core Database における
**Relation Layer / Entity Network Layer**
として機能する。

---

## 2. Relationship as Dynamic Edge

Relationship は
有向グラフのエッジとして定義される。

source_entity → target_entity

Relationship は以下の属性を持つ。

| 属性 | 説明 |
|------|------|
| relationship_id | Relationship ID |
| source_entity_id | 起点エンティティ |
| target_entity_id | 対象エンティティ |
| relationship_type | 関係タイプ |
| direction | 方向 |
| weight | 関係の強さ |
| polarity | 正負関係 |
| status | 関係状態 |
| importance | 物語重要度 |

### 2.1 Relationship Polarity

| polarity | 意味 |
|----------|------|
| positive | 友好 |
| negative | 敵対 |
| neutral | 中立 |
| complex | 愛憎など複合 |

### 2.2 Relationship Status

| status | 意味 |
|--------|------|
| active | 有効 |
| inactive | 無効 |
| hidden | 秘密 |
| broken | 破綻 |
| forming | 形成中 |
| changing | 変化中 |

---

## 3. Temporal / Event Linkage

Relationship は時間によって変化する。

Relationship の変化は Event と結びつく。

| 属性 | 説明 |
|------|------|
| start_event_id | 関係成立イベント |
| end_event_id | 関係終了イベント |
| change_event_id | 関係変化イベント |
| start_timestamp | 開始時刻 |
| end_timestamp | 終了時刻 |

これにより関係の履歴を追跡できる。

例：

友人 → 裏切り → 敵  
師弟 → 対立 → 和解  

Relationship History は
物語ドラマの重要要素となる。

---

## 4. Structural vs Narrative Relationship

Relationship は2種類に分類される。

### 4.1 Structural Relationship（構造関係）

システム・構造上の関係

例：

Character → Thread  
Scene → Event  
Thread → Conflict  
Event → State  
Character → Organization  

これはデータ構造上の参照関係である。

### 4.2 Narrative Relationship（物語関係）

ドラマ・感情・対立などの関係

例：

恋愛  
友情  
敵対  
師弟  
裏切り  
尊敬  
恐怖  
支配  
依存  

Narrative Relationship は
Emotional Model や Conflict Model と連動する。

---

## 5. Conflict & Emotion Sync

Relationship は Conflict と Emotion に影響する。

Relationship は以下を参照する：

| 属性 | 説明 |
|------|------|
| related_conflict_id | 関連 Conflict |
| emotion_value | 感情値 |
| tension_value | 緊張値 |
| trust_value | 信頼度 |
| fear_value | 恐怖度 |
| love_value | 愛情度 |
| hate_value | 憎悪度 |

Relationship の変化は
Conflict Intensity や Beat Emotional Delta に影響する。

---

## 6. Relationship JSON Structure

Relationship は以下の JSON 構造で管理される。

{
  "relationship_id": "rel_001",
  "source_entity_id": "character_001",
  "target_entity_id": "character_002",
  "relationship_type": "narrative_relationship",
  "direction": "directed",
  "weight": 0.75,
  "polarity": "negative",
  "status": "active",
  "importance": 0.9,
  "emotion_values": {
    "trust_value": 0.2,
    "fear_value": 0.6,
    "love_value": 0.0,
    "hate_value": 0.8
  },
  "related_conflict_id": "conflict_001",
  "start_event_id": "event_010",
  "end_event_id": null,
  "change_event_id": "event_025",
  "start_timestamp": "2026-01-01T10:00:00+09:00",
  "end_timestamp": null
}

---

## 7. Relationship Graph Structure

Relationship Network はグラフとして扱う。

Graph 定義：

Node = Entity  
Edge = Relationship  

Relationship Graph により以下が可能：

・キャラクター相関図  
・組織関係図  
・対立ネットワーク  
・感情ネットワーク  
・Thread 関係ネットワーク  
・物語構造ネットワーク  

Relationship Graph は
Story Network Engine の基盤となる。

---

## 8. Core Models との関係

Relationship Model は以下のモデルを横断する：

| Model | 関係 |
|------|------|
| Entity ID System | Node 定義 |
| Character Model | 人間関係 |
| Thread Model | Thread 関係 |
| Scene Model | Scene 構造 |
| Event Model | Event 関係 |
| State Model | 状態遷移 |
| Conflict Model | 対立関係 |
| World Rule Model | 世界ルール関係 |

Relationship Model は
**Core Spec 全体を結ぶネットワーク層**である。

---

## 9. Relationship Engine Logic

Relationship Engine は以下を計算する：

1. キャラクター相関図
2. 対立ネットワーク
3. 感情ネットワーク
4. 関係変化イベント
5. Relationship Importance
6. Conflict に影響する関係
7. ストーリー上重要な関係
8. Relationship Graph Centrality
9. Network Clusters
10. Story Relationship Map

Relationship Priority は以下で計算できる：

relationship_priority =
weight × importance × emotion_intensity × conflict_relation

これにより
物語上重要な関係を特定できる。

---

## 10. まとめ

Relationship Model v2.0.1 では
Relationship を

**単なる参照関係ではなく、
時間・感情・対立・構造を持つ動的な有向エッジ**

として定義した。

Relationship Model は

・Entity Network  
・Character Relationship  
・Conflict Network  
・Emotion Network  
・Story Graph  
・Narrative Structure  

を統合する

**NWF Network Core Model**

である。

---

[EOF]