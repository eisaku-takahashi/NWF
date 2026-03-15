# NWF Data Spec v1.0

## 1. 概要

本ドキュメントは Novel Writing Framework（NWF）において使用される
データ構造の仕様を定義する。

NWFでは物語構造を以下の主要データモデルで管理する。

- Story
- Thread
- Scene
- Beat
- Character
- World
- Foreshadowing
- Emotional Curve

これらの構造はJSON形式で保存される。

---

## 2. データ設計の目的

NWFのデータ設計の目的は以下である。

- 物語構造の明示化
- AIとのインターフェース統一
- Engine処理の効率化
- 物語分析の自動化

---

## 3. データ構造の階層

NWFの物語構造は次の階層を持つ。

Story  
Thread  
Scene  
Beat

この構造は物語の論理構造を保持する。

---

## 4. データ仕様一覧

本Data Specでは以下のJSON構造を定義する。

- Story JSON Structure
- Thread JSON Structure
- Scene JSON Structure
- Beat JSON Structure
- Character JSON Structure
- World JSON Structure
- Foreshadowing JSON Structure
- EmotionalCurve JSON Structure

---

## 5. Engineとの関係

各Engineは以下のデータを参照する。

ThreadEngine  
Thread構造を処理する

SceneEngine  
Scene構造を処理する

BeatEngine  
Beat構造を処理する

ForeshadowingEngine  
伏線データを解析する

EmotionalCurveEngine  
感情曲線を解析する

---

## 6. 拡張性

NWFのデータ構造は以下を前提として設計されている。

- AI生成の拡張
- Story Database化
- 分析アルゴリズム追加
- 大規模作品対応

---

## 7. バージョン

Version: v1.0