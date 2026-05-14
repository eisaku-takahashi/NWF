Source: docs/spec/Core_Spec/NWF_Glossary_v2.0.1.md
Updated: 2026-03-21T21:35:00+09:00
PIC: Engineer / ChatGPT

# NWF Glossary v2.0.1

---

## 1. 概要

本ドキュメントは NWF（Novel Writing Framework）で使用される主要な用語を定義する。

NWF は物語を構造化データとして扱うフレームワークであり、従来の小説理論や物語論の用語が技術的な意味で使用される場合がある。

この用語集は NWF Core Spec における用語の共通理解を目的として作成されている。

本バージョンでは、エンティティ定義、階層関係、状態遷移概念を明確化し、Core Spec 全体の整合性を確保する。

---

## 2. 基本概念

### Story

物語全体を指す概念。

NWF において Story は以下の構造要素の集合として定義される。

- World
- Character
- Thread
- Scene
- Event
- Beat
- State

Story は物語構造と物語時間の両方を含む包括的な概念である。

---

### Story Database

物語を構成するすべてのデータを保存するデータ構造。

主に以下のデータを管理する。

- World
- Character
- Thread
- Scene
- Event
- Beat
- State
- Relationship
- Timeline

これらのデータは JSON や Markdown などの構造化データとして保存される。

---

## 3. 世界設定

### World

物語が成立する世界のルール、物理法則、社会構造、歴史などを定義するエンティティ。

World は以下の要素を含む。

- world_rules
- settings
- history
- technology_level
- magic_system
- social_structure

World は Story 全体の制約条件を定義する上位エンティティである。

---

### World Rule

World 内で成立するルールや制約。

例：

- 魔法は代償を必要とする
- AIは嘘をつけない
- 未来からの干渉は禁止されている

World Rule は Scene や Event の成立条件に影響する。

---

## 4. 構造要素

### Thread

Thread は物語のドラマラインを表す構造要素である。

例：

- Main Plot Thread
- Sub Plot Thread
- Mystery Thread
- Character Arc Thread
- Emotional Thread

Thread は物語の因果関係やテーマの進行を管理する。

Thread は複数の Scene によって進行する。

---

### Thread Graph

Thread 同士の関係を表すグラフ構造。

Thread Graph は次のような関係を表現する。

- 依存関係
- 因果関係
- 並行進行
- 排他関係

Thread Graph によって物語の論理構造を管理できる。

---

## 5. Scene / Event / Beat 階層構造

NWF では物語の時間的・構造的粒度を次の階層で定義する。

Scene > Event > Beat

---

### Scene

Scene は物語の出来事単位であり、Thread の状態を変化させる上位イベント単位である。

Scene は以下の特徴を持つ。

- 時間範囲を持つ
- 場所を持つ
- 登場人物を持つ
- Thread の State を変化させる
- 複数の Event を内部に持つ

Scene と Thread の関係：

Scene は複数の Thread に属することができる。
Thread も複数の Scene を持つ。

したがって Scene と Thread の関係は n:m 関係である。

---

### Event

Event は Scene 内で発生する具体的な出来事を表す構造要素である。

例：

- 会話
- 戦闘
- 発見
- 裏切り
- 秘密の暴露
- 出会い
- 別れ

Event は Thread や Character の State を変化させる最小の論理イベント単位である。

Event は複数の Beat を内部に持つ。

---

### Beat

Beat は Event 内部の最小ドラマ単位である。

Beat は次のような要素を表す。

- 情報提示
- 感情変化
- 行動
- 反応
- 対立の瞬間
- 決断の瞬間

Beat は物語のテンポ、感情曲線、演出を構成する最小単位である。

階層まとめ：

- Scene：出来事のまとまり
- Event：具体的な出来事
- Beat：感情・演出・瞬間

---

## 6. 時間構造

### Timeline

物語内の時間構造を管理するデータ構造。

Timeline は以下を管理する。

- Scene の時系列順序
- Event の時系列
- 同時進行イベント
- 回想
- 未来イベント
- 分岐時間

Timeline によって物語の時間的整合性を管理する。

---

## 7. キャラクター関連

### Character

物語に登場する人物または主体。

Character は以下の属性を持つ。

必須属性：
- name
- goal
- motivation

任意属性：
- personality
- background
- relationships
- beliefs
- internal_conflict

Character は Thread、Scene、Event に関与する。

---

### Character Arc

キャラクターの内面的変化の構造。

Character Arc は次のような要素を通じて表現される。

- 信念
- 成長
- 価値観の変化
- 目標の変化
- 自己認識の変化

Character Arc は Thread および State 変化によって表現される。

---

## 8. Relationship

### Relationship

Character 同士の関係を表すデータ。

例：

- 友人
- 敵
- 家族
- 恋人
- 師弟
- 同僚

Relationship は Story の社会構造や感情構造を表現する。

---

## 9. State 概念

### State

State は Character、Thread、World などのエンティティが特定の時点で持つ状態を表す。

例：

Character State：
- alive
- injured
- arrested
- in_love
- betrayed

Thread State：
- not_started
- in_progress
- stalled
- resolved
- failed

World State：
- war
- peace
- collapse
- revolution

State は Scene や Event によって変化する。

---

### State Transition

State が別の State に変化することを State Transition と呼ぶ。

State Transition は主に Event によって発生する。

Event → State Transition → Thread Progress / Character Arc

この構造により物語の因果関係を管理する。

---

## 10. エンジン関連

### Thread Engine

Thread 構造、Thread Graph、Thread State を管理するエンジン。

---

### Scene Engine

Scene、Event、Timeline の整合性と順序を管理するエンジン。

Scene Engine は以下を担当する。

- Scene 順序管理
- Timeline 整合性
- Thread と Scene の同期
- Scene 構造検証

---

### Narrative Rendering

Scene、Event、Beat などの構造データを自然言語の文章へ変換する処理。

出力例：

- 小説
- 脚本
- ナレーション
- あらすじ

Narrative Rendering は NWF における最終的な文章生成プロセスである。

---

## 11. NWF設計思想

### Story as Data

物語を構造化データとして扱う設計思想。

この思想により物語の分析、生成、再利用が可能になる。

---

### Narrative Simulation

Character、Thread、Scene、Event、State の相互作用によって物語が動的に進行する概念。

これは Execution Engine によって実行されるシミュレーション概念である。

---

### Story OS

物語制作を支援する統合的なシステムという考え方。

NWF は Story OS の実装を目指すフレームワークとして設計されている。

---

## 12. まとめ

本用語集は NWF Core Spec における主要概念を整理し、共通理解を提供するためのものである。

本バージョンでは以下を明確化した。

- World / Event / State の定義追加
- Scene > Event > Beat の階層定義
- Scene と Thread の n:m 関係
- State と Event による状態遷移モデル
- Timeline による時間管理

この Glossary は NWF Core Spec 全体の基礎概念定義として使用される。

---

[EOF]