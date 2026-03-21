Source: docs/spec/Architecture_Spec/NWF_World_Model_v2.0.0.md
Updated: 2026-03-19T03:40:00+09:00
PIC: Engineer / ChatGPT

# NWF World Model v2.0.0

---

## 1. 概要

NWF（Novel Writing Framework）における World Model は、物語世界の構造とルールを体系的に管理するモデルである。v2.0.0 では v1.0 の基本概念を継承しつつ、以下の拡張を行った。

- 世界ルールと物語整合性管理の統合  
- 複数作品間での世界設定再利用の効率化  
- AI Authoring Interface との連携強化  
- 世界設定の階層化管理（World / Location / Culture / History / WorldRule）  
- Character Model と Thread / Scene モデルとの制約関係明確化

このモデルにより、物語の一貫性を維持しつつ、キャラクター行動、ストーリー進行、イベント発生条件を統合管理できる。

---

## 2. 基本構造

### 2.1 World

- 管理対象: 物語世界全体  
- 主な情報: 世界名、概要、ジャンル、技術レベル、文明レベル、基本法則  
- 関連性: Character 能力・行動範囲制約、Thread イベント制御

### 2.2 WorldRule

- 管理対象: 世界の基本ルール  
- 主な情報: 物理法則、魔法システム、技術制約、社会制度、倫理観  
- 関連性: Character 行動の制約、物語整合性確認、Scene イベント制御

### 2.3 Location

- 管理対象: 物語に登場する場所  
- 主な情報: 場所名、地理情報、環境条件、所属国家、文化的特徴  
- 関連性: Scene 設定、Thread イベント発生条件

### 2.4 Culture

- 管理対象: 世界の文化要素  
- 主な情報: 宗教、言語、価値観、社会慣習  
- 関連性: Character 価値観・行動、Scene / Thread の社会的制約

### 2.5 History

- 管理対象: 世界の歴史的背景  
- 主な情報: 過去の戦争、文明成立、王朝変遷、重大事件  
- 関連性: Timeline Consistency、Character 背景、Story イベント制御

---

## 3. World と他モデルの連携

- Character Model: 世界のルールがキャラクター能力、行動範囲、社会的立場を制約  
- Thread / Scene Model: 世界設定がイベント発生条件、シーン環境、登場キャラクター制約に影響  
- Narrative Consistency Model: 世界ルールの整合性確認に利用  
- AI Authoring Interface: 世界設定の解析、物語生成提案の基礎データとして活用

---

## 4. データ管理と階層構造

- World Model は階層構造で管理  
  - World → Location → Culture / History  
  - WorldRule はすべての階層で参照可能  
- 各要素は一意の ID を持ち、Thread / Scene / Character から参照可能  
- データ形式は JSON, YAML, Markdown で統一  
- JSON キーは snake_case、単位表記を明確化

---

## 5. AI連携

World Model は AI による物語分析・生成に利用される。

用途例:

- キャラクター行動制約の自動チェック  
- Scene / Thread におけるイベント妥当性確認  
- 世界設定の矛盾検出  
- 他作品設定との再利用提案  
- 世界観を反映したストーリー生成補助

---

## 6. 設計思想

- 世界設定の構造化と階層化  
- 物語整合性の維持  
- 複数作品間での設定再利用可能性  
- AI による物語解析・生成支援  
- キャラクター・Scene・Thread との制約関係の明確化

---

## 7. まとめ

World Model v2.0.0 は、NWF における物語世界の統合管理基盤である。  
v1.0 からの改良により、世界設定の階層化、整合性管理、AI連携が強化され、複雑な物語やマルチスレッド作品でも安定した世界構築と解析が可能となった。

---

[EOF]