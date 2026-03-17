Source: docs/spec/Engine_Spec/NWF_BeatEngine_v2.0.0.md
Updated: 2026-03-17T20:30:00+09:00
PIC: Engineer / ChatGPT

# NWF BeatEngine v2.0.0

---

## 1. 概要

Beat Engine は NWF（Novel Writing Framework）において、Scene 内のドラマ構造を最小単位で管理するエンジンである。

Beat は物語における最小の状態変化単位であり、キャラクターの行動・反応・認識の変化を表す。

Beat Engine は Scene Engine の内部層として機能し、物語のテンポ・緊張・感情の流れを精密に制御する。

---

## 2. Beat の定義

Beat は「瞬間的な状態変化を伴うドラマ単位」である。

### 2.1 基本要素

Beat は以下の要素を持つ。

- 行動（Action）
- 反応（Reaction）
- 変化（Change）

---

### 2.2 特徴

- Scene 内で連続的に発生する
- State を微小に変化させる
- キャラクターの意思決定や感情に強く依存する
- テンポとリズムを形成する

---

## 3. Beat Engine の役割

Beat Engine は以下の役割を持つ。

- Beat の生成
- Beat の順序制御
- Beat 間の因果関係管理
- Scene 内テンポの制御
- 微細な状態変化の管理

Beat Engine は「ドラマの最小粒度」を扱うエンジンである。

---

## 4. Beat と Scene

- Beat は Scene の内部構造である
- 1つの Scene は複数の Beat によって構成される
- Scene のドラマ性は Beat の連鎖によって決定される

Scene Engine は Beat Engine に対して以下を提供する。

- Scene 構造
- 状態情報（State）
- 登場人物情報

---

## 5. Beat と State

- Beat は State の微小変化を引き起こす
- 複数の Beat が積み重なることで Scene レベルの変化となる
- Beat は状態遷移の最小単位として機能する

---

## 6. Beat 構造

### 6.1 内部構造

Beat は以下の構造を持つ。

- トリガー（Trigger）
- 行動（Action）
- 反応（Reaction）
- 状態変化（State Change）

---

### 6.2 構造特性

- 因果関係を持つ連鎖構造
- 高い局所性（Scene 内で完結）
- 感情変化の直接的表現

---

## 7. Beat 間関係

Beat は以下の関係を持つ。

- 連続関係（Sequence）
- 因果関係（Cause-Effect）
- 強化関係（Escalation）
- 緩和関係（Relief）

---

## 8. 入出力仕様

### 8.1 入力

- Scene 定義
- State 情報
- Character 情報

---

### 8.2 出力

- Beat シーケンス
- State 微小変化ログ
- テンポ分析データ
- 感情変化データ

---

## 9. 処理フロー

Beat Engine は以下の処理を行う。

1. Scene 構造の取得
2. Beat の生成
3. Beat 間関係の構築
4. Beat シーケンスの確定
5. State 微小変化の適用
6. テンポ分析
7. 整合性チェック

---

## 10. 検証（Validation）

Beat Engine は以下を検証する。

- 変化のない Beat の検出
- 因果関係の欠如の検出
- 不自然なテンポの検出
- State との不整合検出

---

## 11. 他 Engine との関係

Beat Engine は以下の Engine と連携する。

- Scene Engine（上位構造）
- State Engine（状態管理）
- Character Engine（行動主体）
- EmotionalCurve Engine（感情曲線）
- Dialogue Engine（対話生成）

---

## 12. AI 連携

AI は Beat Engine の情報を利用して以下を行う。

- ドラマ構造の精密分析
- テンポ改善提案
- 感情演出の最適化
- Scene 内緊張設計の最適化

---

## 13. v1.0 からの変更点

主な変更点

- State Engine との統合強化
- Beat を「状態変化単位」として再定義
- 内部構造（Trigger）の追加
- 感情およびテンポ分析の強化

---

## 14. 設計思想

Beat Engine は以下の思想に基づく。

- 物語を「最小変化の連鎖」として捉える
- ドラマの粒度を最大限に細分化する
- テンポと感情を定量的に扱う
- 上位構造との整合性を維持する

---

## 15. まとめ

Beat Engine v2.0 は、Scene 内のドラマを最小単位で分解・管理し、物語のテンポと感情の流れを精密に制御するエンジンである。

Beat の連鎖により、物語のリアリティと没入感を高水準で実現することが可能となる。

---

[EOF]