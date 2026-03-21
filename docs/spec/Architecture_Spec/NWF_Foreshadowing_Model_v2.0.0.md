Source: docs/spec/Architecture_Spec/NWF_Foreshadowing_Model_v2.0.0.md
Updated: 2026-03-19T06:28:00+09:00
PIC: Engineer / ChatGPT

# NWF Foreshadowing Model v2.0.0

---

## 1. 概要

NWF（Novel Writing Framework）における Foreshadowing Model は、物語の伏線とその回収を体系的に管理するモデルである。v2.0.0 では、Thread、Scene、Beat、Character との連動を強化し、伏線の状態管理や未回収チェックをより精密に行えるようになった。

- Thread ごとの伏線管理  
- Scene 内の伏線設置・回収管理  
- Beat 単位での伏線表現  
- キャラクター行動との関連付け  
- Narrative Consistency Model との連動による未回収伏線警告  
- AI Authoring Interface による伏線分析支援

このモデルにより、物語の構造的完成度と整合性を高めることができる。

---

## 2. 基本構造

### 2.1 伏線ID

- 伏線を一意に識別する識別子  
- 設置と回収の関係を明確化する

### 2.2 伏線内容

- 物体、発言、出来事、描写など、未来の物語に影響する要素  
- 必要に応じて複数タグで分類可能

### 2.3 設置位置

- Scene / Beat / キャラクター発言 / 描写 など  
- Thread に紐付けて管理

### 2.4 回収位置

- Scene / Beat における回収イベント  
- 回収者キャラクター、回収時の意味や効果を管理

### 2.5 関連キャラクター

- 伏線提示者  
- 伏線回収者  
- 伏線に関わる行動や会話を紐付け

### 2.6 状態管理

- 未回収  
- 部分回収  
- 回収済み  
- 状態変化の履歴を保持し、物語整合性チェックに利用

---

## 3. Scene と Foreshadowing

- Scene は伏線設置・回収の主要単位  
- Scene ごとに設置済み・回収予定の伏線情報を管理  
- 伏線の影響範囲や関連 Thread も保持

---

## 4. Beat と Foreshadowing

- Beat は Scene 内の最小単位  
- 伏線提示・強調・回収の細かい表現を管理  
- キャラクター行動との直接的関連付けが可能

---

## 5. Thread と Foreshadowing

- Thread ごとに複数の伏線を管理  
- 複数 Thread を横断する伏線も対応  
- Thread 間の伏線連動により物語全体の統合性を維持

---

## 6. AI連携

- 未回収伏線の警告  
- 回収漏れチェック  
- Thread / Scene / Beat 単位での伏線分析  
- AI Authoring Interface 経由での自動提案・補助生成  
- Narrative Consistency Model との統合による物語整合性の維持

---

## 7. 設計思想

- 伏線構造の明確化  
- 物語整合性の維持  
- 複雑な Thread / Scene 構造への対応  
- AI による分析・設計支援

---

## 8. まとめ

Foreshadowing Model v2.0.0 は、物語の伏線と回収を体系的に管理する NWF モデルである。  
v1.0 からの拡張により、Thread、Scene、Beat、Character の連動を強化し、未回収伏線の管理や物語整合性チェックが可能となった。AI を活用することで、伏線設計の効率化と物語完成度の向上を実現する。

---

[EOF]