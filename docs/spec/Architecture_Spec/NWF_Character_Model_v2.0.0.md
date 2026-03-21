Source: docs/spec/Architecture_Spec/NWF_Character_Model_v2.0.0.md
Updated: 2026-03-19T06:15:00+09:00
PIC: Engineer / ChatGPT

# NWF Character Model v2.0.0

---

## 1. 概要

NWF（Novel Writing Framework）における Character Model は、物語に登場するキャラクターを構造化して管理するためのモデルである。v2.0.0 では v1.0 の基本概念を継承しつつ、以下の拡張を行った。

- Character / CharacterRole / CharacterTrait / CharacterBackground / CharacterRelationship の統合管理  
- World Model と連携した行動制約および社会的立場の自動管理  
- Thread / Scene モデルとの統合により、キャラクターの行動可能範囲とイベント参加条件を明確化  
- Emotional Curve Model との直接連携による感情変化の追跡  
- Narrative Consistency Model との連動による設定整合性チェック

このモデルにより、キャラクター情報を体系的に管理し、物語全体の一貫性と連携性を強化する。

---

## 2. 基本構造

### 2.1 Character

- 管理対象: 物語に登場する人物または知的存在  
- 主な情報: キャラクターID、名前、概要、所属、年齢、性別、種族、職業  
- 関連性: World Model による能力・行動制約、Thread / Scene におけるイベント参加条件

### 2.2 CharacterRole

- 管理対象: キャラクターが物語内で担う役割  
- 主な情報: 主人公、対立者、助言者、仲間、敵対者  
- 備考: 一人のキャラクターが複数役割を持つことも可能  
- 関連性: Thread / Scene の進行制御、Story の因果関係

### 2.3 CharacterTrait

- 管理対象: キャラクターの性格・能力・価値観・弱点・信念  
- 関連性: 行動決定、Emotional Curve 変化、Narrative Consistency の整合性確認

### 2.4 CharacterBackground

- 管理対象: キャラクターの出生、育成環境、過去の出来事、人生の転機、動機  
- 関連性: 行動原理、Story / Scene イベントへの影響、Timeline Consistency

### 2.5 CharacterRelationship

- 管理対象: キャラクター間の関係性  
- 主な情報: 家族、友人、師弟、敵対、恋愛  
- 関連性: Story ドラマ生成、Scene 行動制御、Foreshadowing の関連付け

---

## 3. Character と他モデルの連携

- World Model: 社会的立場・文化的価値観・行動制約の参照  
- Thread / Scene Model: イベント参加条件、行動可能範囲の制御  
- Emotional Curve Model: 感情変化の追跡、ピーク・落差の反映  
- Narrative Consistency Model: キャラクター設定整合性の自動確認  
- AI Authoring Interface: キャラクター生成補助、関係性分析、行動提案

---

## 4. データ管理

- 各キャラクターは一意の character_id を持つ  
- Role / Trait / Background / Relationship は JSON 配列で階層管理  
- Thread / Scene との関連情報を保持し、行動制約やイベント参加条件をリアルタイム参照可能  
- JSON キーは snake_case、単位や形式を明示

---

## 5. AI連携

Character Model は AI による物語生成および分析に利用される。

用途例:

- キャラクター行動の自動生成および整合性チェック  
- キャラクター間関係分析によるストーリー提案  
- Emotional Curve 変化に基づく感情的クライマックス検出  
- 未整合設定の警告および修正提案

---

## 6. 設計思想

- キャラクター情報の体系化と階層管理  
- 行動・関係性・感情変化の統合管理  
- World / Thread / Scene との制約関係明確化  
- AI による分析・生成支援の最大化  
- Narrative Consistency との連動による設定整合性確保

---

## 7. まとめ

Character Model v2.0.0 は、NWF におけるキャラクター管理の統合基盤である。  
v1.0 からの改良により、キャラクターの役割・属性・背景・関係性を階層的に管理でき、世界設定・ストーリーライン・シーンとの連動が強化され、より一貫性のある物語設計と AI 支援が可能となった。

---

[EOF]