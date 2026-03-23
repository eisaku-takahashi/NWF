Source: docs/spec/Architecture_Spec/NWF_World_Model_v2.0.1.md
Updated: 2026-03-23T19:05:00+09:00
PIC: Engineer / ChatGPT

# NWF World Model v2.0.1

---

## 1. 概要

NWF（Novel Writing Framework）における World Model は、物語世界の構造、法則、社会、歴史、経済、組織などを統合的に管理するモデルであり、Story OS におけるシミュレーション基盤として機能する。

World Model は System Architecture v2.0.1 において **World & Actor Layer** に属し、Foundation Layer（Story Database）と Narrative Logic Layer（Thread / Scene）の中間に位置する。このモデルは、キャラクターの行動制約、イベント発生条件、社会構造、歴史背景などを規定し、物語生成・物語解析・整合性チェックの基盤となる。

v2.0.1 では以下の点が強化された。

- Multi-Graph Data Architecture との完全統合
- Geography Layer の追加
- Organization / Faction Model の追加
- Socio-Economic Layer の追加
- WorldRule を Constraint System として再定義
- Timeline Model との統合（History → Timeline Event）
- AI Authoring Interface との連携強化
- Simulation 前提条件モデルとしての再定義

---

## 2. 階層構造と Geography Layer

World Model は階層構造で管理される。

World > Geography > Location

### 2.1 World

物語世界全体を定義する最上位要素。

主な情報:
- world_id
- world_name
- genre
- technology_level
- civilization_level
- basic_laws
- description

World は Character、Thread、Scene のすべての前提条件となる。

---

### 2.2 Geography

Geography は Location の上位概念であり、国家、地形、交通網、地域構造などのマクロ地理構造を管理する。

主な情報:
- geography_id
- continent
- country
- region
- terrain
- climate
- transportation_network
- political_structure

Geography は Location、Organization、Economy に強く影響する。

---

### 2.3 Location

Location は Scene の舞台となる具体的な場所を管理する。

主な情報:
- location_id
- location_name
- geography_id
- environment
- population
- culture_id
- controlling_organization_id
- economic_features

Location は Scene 設定、イベント発生条件、キャラクター行動制約に影響する。

---

## 3. WorldRule と Constraint System

### 3.1 WorldRule 概要

WorldRule は世界の法則、倫理、社会制度、技術制約、魔法体系などを定義する。

v2.0.1 では WorldRule を単なる設定ではなく、
**Constraint System（論理制約エンジン）** として再定義する。

WorldRule は Execution Flow における Logic Synthesis フェーズで参照され、
以下を制御する。

- Character 行動可能性
- Event 発生可能性
- 技術・魔法の使用可否
- 社会制度による制約
- 倫理・法律による制約
- 物語整合性チェック

---

### 3.2 WorldRule の分類

WorldRule は以下のサブモデルで構成される。

1. Physical Rules
   - 物理法則
   - 重力
   - エネルギー保存
   - 生物制約

2. Technology System
   - 技術レベル
   - 技術ツリー
   - エネルギー体系
   - 武器・通信・医療技術

3. Magic / Supernatural System
   - 魔法体系
   - 超能力
   - 神・精霊・異世界法則
   - 使用条件・代償・制限

4. Social / Legal Rules
   - 法律
   - 政治制度
   - 身分制度
   - 倫理観

5. Economic Rules
   - 通貨
   - 税
   - 資源
   - 市場構造

これらは constraint_document として Story Database に保存される。

---

## 4. 社会・文化・組織・経済システム

World Model v2.0.1 では社会構造を以下のレイヤで管理する。

### 4.1 Culture

文化・価値観・宗教・言語・社会慣習を管理する。

主な情報:
- culture_id
- religion
- language
- values
- social_customs
- taboo
- education
- art

Culture は Character の価値観・行動原理・対立構造に影響する。

---

### 4.2 Organization / Faction

Organization は国家、軍、宗教団体、企業、ギルド、秘密結社などの組織体を管理する。

Organization は Character（個人）と World（環境）を繋ぐ中間層として機能する。

主な情報:
- organization_id
- organization_name
- type
- hierarchy
- ideology
- resources
- controlled_locations
- allies
- enemies

Organization は Thread（戦争、政治、犯罪、陰謀など）の発生源となる。

---

### 4.3 Socio-Economic Layer

経済・資源・貿易・格差などの社会経済構造を管理する。

主な情報:
- currency
- resources
- trade_routes
- economic_class
- wealth_distribution
- industry
- food_supply
- energy_supply

経済は Thread におけるコンフリクトの主要因となる。

---

## 5. Historical Timeline

History は v2.0.1 では独立した履歴文章ではなく、
**Timeline Model の Story Time（ST）軸における過去 Event 集合** として管理される。

History は以下として保存される。

- historical_event
- war
- revolution
- discovery
- disaster
- dynasty_change
- migration
- technological_invention

これらは Timeline Graph 上の Event Node として管理される。

History は以下に影響する。

- Character 背景
- Organization 関係
- Culture 形成
- Geography 境界
- Thread コンフリクト
- WorldRule 変化

---

## 6. モデル間依存関係

World Model は以下のモデルと相互参照関係を持つ。

### 6.1 Character Model
- Character の能力制約
- 社会的立場
- 所属 Organization
- 行動可能 Location
- 価値観（Culture）

### 6.2 Thread / Scene Model
- イベント発生条件
- シーン環境
- 参加可能キャラクター
- 組織間対立
- 経済・政治・戦争

### 6.3 Story Database Model
World Model は Multi-Graph Data Architecture 上で以下のノードとして管理される。

- world_node
- geography_node
- location_node
- culture_node
- organization_node
- economy_node
- rule_node
- historical_event_node

WorldRule は constraint_document として保存される。

---

## 7. AI & Simulation Support

World Model は AI Authoring Interface において、
**物語生成時の前提条件（Context Buffer）** として使用される。

AI は以下の情報を World Model から読み込む。

- 世界の技術レベル
- 魔法・物理法則
- 社会制度
- 組織構造
- 経済状況
- 地理
- 歴史
- 文化
- 禁止事項（WorldRule）

AI の主な利用目的:

- 世界設定に矛盾しない描写生成
- キャラクター行動妥当性チェック
- イベント発生可能性評価
- 世界設定の矛盾検出
- 新しい Thread / Scene 提案
- Simulation ベース物語生成

World Model は Story OS における
**Simulation Environment Definition Model**
として機能する。

---

## 8. まとめ

World Model v2.0.1 は、NWF における物語世界の統合管理モデルであり、
Story OS のシミュレーション基盤として以下を管理する。

- 世界構造（World / Geography / Location）
- 法則・制約（WorldRule / Constraint System）
- 文化・社会
- 組織・国家・勢力
- 経済・資源
- 歴史（Timeline Event）
- キャラクター行動制約
- イベント発生条件
- AI 生成前提条件

これにより、NWF は単なるプロット管理システムではなく、
**物語世界シミュレーション OS** として機能する。

World Model は Character Model、Thread / Scene Model、
Story Database Model、Timeline Model、AI Authoring Interface を結びつける
中心的な基盤モデルである。

---

[EOF]