Source: docs/spec/Data_Spec/NWF_Data_Spec_Index_v2.0.0.md
Updated: 2026-03-18T11:45:00+09:00
PIC: Engineer / ChatGPT

# NWF Data Spec Index v2.0.0

---

## 1. 概要

本ドキュメントは Novel Writing Framework（NWF）において使用される
データ構造の仕様を定義する索引（Index）である。

NWFでは物語構造を以下の主要データモデルで管理する。

- Story
- Thread
- Scene
- Beat
- Character
- World
- Foreshadowing
- Emotional Curve
- Conflict
- State
- Timeline
- Narrative
- Query

これらの構造は JSON 形式で保存され、Engine 処理や AI 分析に使用される。

---

## 2. データ設計の目的

NWF のデータ設計の目的は以下である。

- 物語構造の明示化
- AI とのインターフェース統一
- Engine 処理の効率化
- 物語分析の自動化
- 複雑構造の一貫性維持

---

## 3. データ構造の階層

NWF の物語構造は次の階層を持つ。

Story  
Thread  
Scene  
Beat  
Character / Conflict / State / World / Foreshadowing / Emotional Curve / Narrative / Query  

この階層構造により、物語の論理・因果・時間構造を保持する。

---

## 4. データ仕様一覧（v2.0.0）

本 Data Spec では以下の JSON 構造を定義する。

- NWF_CharacterData_v2.0.0.md
- NWF_ConflictData_v2.0.0.md
- NWF_EmotionalCurveData_v2.0.0.md
- NWF_ForeshadowingData_v2.0.0.md
- NWF_NarrativeData_v2.0.0.md
- NWF_QueryData_v2.0.0.md
- NWF_SceneData_v2.0.0.md
- NWF_StateData_v2.0.0.md
- NWF_ThreadData_v2.0.0.md
- NWF_TimelineData_v2.0.0.md

---

## 5. Engineとの関係

各 Engine は以下のデータを参照・利用する。

- ThreadEngine  
  Thread 構造を処理する

- SceneEngine  
  Scene 構造を処理する

- BeatEngine  
  Beat 構造を処理する

- CharacterEngine  
  キャラクター状態を処理する

- ConflictEngine  
  対立構造を処理する

- ForeshadowingEngine  
  伏線データを解析する

- EmotionalCurveEngine  
  感情曲線を解析する

- StateEngine  
  物語の状態遷移を管理する

- TimelineEngine  
  時間構造を統合管理する

- NarrativeEngine  
  物語進行と構造を分析する

- QueryEngine  
  データ問い合わせ・検索を処理する

---

## 6. 拡張性

NWF のデータ構造は以下を前提として設計されている。

- AI 生成による拡張
- Story Database 化
- 分析アルゴリズム追加
- 大規模作品対応
- 複雑構造の一貫性保持

---

## 7. バージョン

Version: v2.0.0

---

[EOF]