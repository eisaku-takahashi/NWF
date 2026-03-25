Source: docs/spec/Data_Spec/NWF_StateData_v2.0.1.md
Updated: 2026-03-26T03:37:00+09:00
PIC: Engineer / ChatGPT

# NWF State Data Specification v2.0.1

---

## 1. 概要

NWF_StateData は、Story OS における世界状態を管理するためのデータ仕様である。

v2.0.0 では状態の保存を主目的としていたが、
v2.0.1 では設計思想を拡張し、State を単なる「現在値の保存」ではなく、

**物語世界における全オブジェクトの状態遷移を管理する
全域的状態遷移シミュレーション・データ（Global State Transition Data）**

として再定義する。

StateData は以下の役割を持つ。

- 世界状態の保存
- Scene / Event による状態変化の記録
- 状態間の依存関係の管理
- 因果関係の追跡
- 情報の可視性（誰が知っているか）の管理
- 時系列における状態変化履歴の管理
- Story Engine による状態遷移シミュレーションの基盤

StateData は Story OS における **Memory（世界の状態の現し身）** である。

---

## 2. Core Metadata

State の基本識別情報を定義する。

### 2.1 State ID

各 State を一意に識別する ID。

例:
- STATE_CHAR_HP_001
- STATE_REL_TRUST_A_B
- STATE_WORLD_WEATHER
- STATE_INFO_SECRET_01

### 2.2 Entity ID

この State が属するエンティティ。

Entity Type 例:

- Character
- Relationship
- World
- Information
- Organization
- Location
- Item
- Political
- Economy
- Technology

### 2.3 State Category

State の分類。

主なカテゴリ:

- character_status
- relationship_status
- world_status
- information_status
- political_status
- economic_status
- technological_status
- environmental_status

---

## 3. Value Management

State の値管理を定義する。

### 3.1 Value Type

State が保持する値の型。

- numeric
- boolean
- enum
- string
- vector
- percentage
- level
- probability

### 3.2 Current Value

現在の状態値。

### 3.3 Previous Value

直前の状態値。
Delta（変化量）計算に使用する。

### 3.4 Delta Value

変化量。

Delta = Current Value - Previous Value

---

## 4. Dynamics & Persistence

State の変化しやすさ・持続性・時間変化を定義する。

### 4.1 Stability Score

状態の変化しにくさを示す値。

値が高いほど変化しにくい。
値が低いほど変化しやすい。

例:
- 国家体制 → 高 Stability
- 感情 → 低 Stability

### 4.2 Decay Rate

時間経過による自然減衰率。

例:
- 恐怖
- 怒り
- 噂
- 情報価値
- 経済ブーム
- 戦争緊張度

Decay Rate により、
Scene が発生しなくても世界が変化する。

### 4.3 Persistence Type

状態の持続性。

- permanent
- semi_permanent
- temporary
- instant
- cyclical

---

## 5. Causal Logic

State の因果関係・依存関係を定義する。

### 5.1 Change Trigger

状態変化を引き起こした原因。

リンク可能な要素:

- SceneID
- EventID
- ConflictID
- DecisionID
- SystemEventID
- TimeEventID

### 5.2 Prerequisites

この State が成立するための前提条件。

例:
- 王が死亡 → 王位継承状態が発生
- 信頼度 > 70 → 秘密共有可能
- 戦争状態 = true → 軍事動員状態 = active

### 5.3 Dependent States

この State が変化した際に
再計算が必要な State のリスト。

例:
- 王死亡 → 政治安定度
- 政治安定度 → 経済指数
- 経済指数 → 市民満足度
- 市民満足度 → 反乱発生確率

State は単独ではなく、
**因果ネットワーク上のノード** として扱う。

---

## 6. Observation & Disclosure

状態の観測可能性と情報公開レベルを定義する。

### 6.1 Observer List

その State を知っている存在。

例:
- Character_A
- Character_B
- Organization_X
- Reader
- Narrator
- Hidden

### 6.2 Visibility Level

情報公開レベル。

- hidden
- private
- group
- public
- reader_only
- narrator_only

### 6.3 Narrative Disclosure Level

物語上の開示段階。

- foreshadowing
- hint
- partial_reveal
- reveal
- full_disclosure
- secret
- misinformation

---

## 7. Temporal Integration

時間・実行順序・履歴管理を定義する。

### 7.1 Execution Step

Story Engine 内部での更新順序。

例:
1. Event
2. Conflict
3. Character Action
4. State Update
5. World Update
6. Relationship Update
7. Information Update

### 7.2 Narrative Order

読者に提示される順序。
Execution Order と異なる場合がある。

これは
- 回想
- 伏線
- 情報隠蔽
- ミステリー構造
を実現するために必要。

### 7.3 Update Latency

状態変化が世界に反映されるまでの遅延。

例:
- 噂 → 数日後に広まる
- 政策 → 数ヶ月後に経済へ影響
- 戦争 → 長期的影響

### 7.4 Last Update

最後に更新された Timeline Node。

### 7.5 History Log

状態変化の履歴ログ。

履歴には以下を記録する。

- timestamp
- previous_value
- new_value
- delta
- trigger
- scene_id
- event_id
- conflict_id
- actor_id
- note

---

## 8. Consistency Constraints

State の矛盾を防ぐための制約を定義する。

### 8.1 Logical Constraints

例:

- 死亡状態 = true のキャラクターは行動できない
- 王が存在しないのに王命は出せない
- 戦争状態 = false なら戦闘イベントは発生しない
- 所持していないアイテムは使用できない

### 8.2 Range Constraints

数値の範囲制約。

例:
- 信頼度: 0 – 100
- HP: 0 – MaxHP
- 経済指数: 0 – 1000
- 戦争緊張度: 0 – 100

### 8.3 Dependency Constraints

依存関係に基づく整合性チェック。

例:
- 国家崩壊 → 政府状態 = null
- 王死亡 → 王位 = 空位
- 秘密公開 → 秘密状態 = public

---

## 9. まとめ

NWF_StateData v2.0.1 は、
単なる状態保存データではなく、

**物語世界の全状態を管理し、
Scene / Event / Conflict による状態変化を計算し、
因果関係を連鎖させ、
世界の未来をシミュレーションするための
Story OS の中核データ構造である。**

StateData は以下を統合管理する。

- Character 状態
- Relationship 状態
- World 状態
- Information 状態
- Political 状態
- Economic 状態
- Technology 状態
- Environment 状態
- 因果関係
- 情報可視性
- 時系列履歴
- 状態遷移
- 依存関係
- 世界シミュレーション

これにより NWF v2.0.1 は

**「物語＝状態遷移の連鎖」**

として演算可能になる。

---

[EOF]