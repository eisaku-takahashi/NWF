Source: docs/spec/Architecture_Spec/NWF_Emotional_Curve_Model_v2.0.0.md
Updated: 2026-03-19T06:25:00+09:00
PIC: Engineer / ChatGPT

# NWF Emotional Curve Model v2.0.0

---

## 1. 概要

NWF（Novel Writing Framework）における Emotional Curve Model は、物語内の感情の変化を構造的に表現・管理するモデルである。v2.0.0 では、v1.0 の基本概念を拡張し、Thread、Scene、Beat、Character、Emotional State の相互連動を強化した。

- Thread ごとの感情曲線管理  
- Scene 内の複数 Beat における感情変化追跡  
- Character ごとの感情状態蓄積と解放管理  
- Narrative Consistency Model との連動による感情変化の論理整合性確認  
- AI Authoring Interface との統合による感情分析と物語設計支援

これにより、複雑な物語の感情構造を可視化・分析し、読者体験の設計を高度化できる。

---

## 2. 基本構造

### 2.1 感情強度

- 数値化された感情の強さを管理  
- 低値: 穏やかな感情状態  
- 高値: 緊張や感情的衝突のピーク  
- 単位: arbitrary scale（0〜100 など任意設定可）

### 2.2 感情種類

- 喜び、悲しみ、怒り、恐怖、驚き、期待 など  
- Thread / Scene / Beat ごとに分類管理可能  
- 必要に応じて新しい感情タグを追加可能

### 2.3 Scene と感情

- Scene は感情変化の主要単位  
- Scene ごとに以下を管理:  
  - 総合感情強度  
  - 感情種類別強度  
  - 感情変化の方向（上昇・下降・安定）

### 2.4 Beat と感情

- Beat は Scene 内の最小単位  
- Beat ごとに感情変化を定義  
- キャラクター感情の変化、緊張度、物語の感情転換を管理

### 2.5 Character と感情

- 各キャラクターの感情状態を追跡  
- 感情強度、種類、変化タイミング、蓄積と解放を管理  
- Narrative Consistency Model と連動し、感情の論理整合性を確認

### 2.6 Thread と感情

- Thread ごとに独自の Emotional Curve を持つ  
- 複数 Thread の相互影響を考慮して全体の感情構造を形成

---

## 3. データ管理

- JSON 形式による構造化管理  
- snake_case キー使用  
- Thread / Scene / Beat / Character と紐付け可能  
- 感情強度、種類、変化方向の情報を保持  
- Narrative Consistency Model や Foreshadowing Model との連携情報を保持

---

## 4. AI連携

- 物語の感情構造分析  
- 感情ピーク、緊張度、テンポの自動可視化  
- 感情バランスの改善提案  
- Story / Scene / Thread に基づく自動補助生成  
- Emotional Curve と Narrative Consistency Model の連動による論理チェック

---

## 5. 設計思想

- 物語感情の構造化と可視化  
- 複雑なマルチキャラクター・マルチスレッド作品への対応  
- キャラクター感情の追跡と一貫性確認  
- AI を活用した感情分析と設計支援

---

## 6. まとめ

Emotional Curve Model v2.0.0 は、物語の感情構造を体系的に管理・分析するための NWF モデルである。  
v1.0 からの拡張により、Thread、Scene、Beat、Character 間の連動を強化し、感情変化の論理整合性を維持しながら、AI を活用した物語設計支援が可能となった。

---

[EOF]