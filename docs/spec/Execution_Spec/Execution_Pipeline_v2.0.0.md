Source: docs/spec/Execution_Spec/Execution_Pipeline_v2.0.0.md
Updated: 2026-03-18T23:45:00+09:00
PIC: Engineer / ChatGPT

# NWF Execution Pipeline v2.0.0

---

## 1. 概要

Execution Pipeline は NWF におけるエンジン処理の実行フローを定義する。

本仕様は、複数の Engine が連携して物語構造の生成・解析・変換を行うための標準的な処理順序およびデータ依存関係を規定する。

---

## 2. 目的

Execution Pipeline の目的は以下である。

- Engine 処理順序の標準化  
- データ依存関係の明確化  
- AI 処理の統合  
- 構造解析の自動化  
- 再現可能な処理フローの確立  

---

## 3. 基本処理フロー

NWF の基本処理は以下の順序で実行される。

1. Story Data Load  
2. Thread Structure Processing  
3. Scene Structure Processing  
4. Beat Structure Processing  
5. Foreshadowing Analysis  
6. Emotional Curve Analysis  
7. Narrative Rendering  

本フローは Engine Order に従って実行される。

---

## 4. データフロー

各処理段階における入出力および依存関係は以下の通りである。

- Story Data Load  
  入力: story.json  
  出力: 全体コンテキスト  

- Thread Structure Processing  
  入力: thread.json  
  出力: thread 構造解析  

- Scene Structure Processing  
  入力: scene.json  
  依存: thread 構造  
  出力: scene 構造解析  

- Beat Structure Processing  
  入力: beat.json  
  依存: scene 構造  
  出力: beat 構造解析  

- Foreshadowing Analysis  
  入力: foreshadowing.json  
  依存: scene 構造, beat 構造  
  出力: 伏線整合性  

- Emotional Curve Analysis  
  入力: emotional_curve.json  
  依存: scene 構造, beat 構造  
  出力: 感情曲線評価  

- Narrative Rendering  
  入力: 全データ  
  出力: 文章生成結果  

---

## 5. 入力データ

Execution Pipeline は以下のデータを入力として使用する。

- story.json  
- thread.json  
- scene.json  
- beat.json  
- character.json  
- world.json  
- foreshadowing.json  
- emotional_curve.json  

---

## 6. 出力データ

Execution Pipeline は以下の情報を生成する。

- 構造解析結果  
- 伏線整合性レポート  
- 感情曲線評価  
- narrative テキスト  

---

## 7. AI連携

AI Interface は Pipeline の各段階に接続可能である。

AI は以下の処理に使用される。

- scene / beat 生成  
- プロット分析  
- キャラクター分析  
- narrative 生成  

各処理は独立して AI 呼び出し可能とする。

---

## 8. 実行原則

Execution Pipeline は以下の原則に従う。

- Engine Order に基づく順序実行  
- データ依存関係に基づく処理  
- 段階的処理（Stepwise Execution）  
- 再実行可能性（Reproducibility）  
- モジュール分離  

---

## 9. 拡張性

本 Pipeline は以下の拡張を想定する。

- 新 Engine の追加  
- 分析アルゴリズムの追加  
- AI モデルの差し替え  
- 並列処理対応  

---

## 10. まとめ

Execution Pipeline は NWF における実行フローの中核であり、Engine Order と連携して動作する。

本仕様により、依存関係を満たした一貫性のある物語処理が実現される。

---

[EOF]