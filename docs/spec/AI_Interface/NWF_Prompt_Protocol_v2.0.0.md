Source: docs/spec/AI_Interface/NWF_Prompt_Protocol_v2.0.0.md
Updated: 2026-03-18T13:45:00+09:00
PIC: Engineer / ChatGPT

# NWF Prompt Protocol v2.0.0

---

## 1. 概要

NWF（Novel Writing Framework）では AI と物語データを安全かつ一貫した形式でやり取りするために Prompt Protocol を定義する。

Prompt Protocol は AI に対して NWF データをどのように提示し、どのような形式で結果を受け取るかを規定する。

このプロトコルにより AI を物語設計の補助ツールとして体系的に利用することが可能になる。

---

## 2. Prompt Protocol の目的

Prompt Protocol の目的は以下の通りである。

- AI と NWF データの整合性確保  
- AI 解析の再現性の確保  
- AI 出力形式の標準化  
- AI 利用の安全性確保  

---

## 3. 基本構造

NWF Prompt Protocol は以下の構造を持つ。

- Context  
- Instruction  
- Data  
- Output Format  

---

## 4. Context

Context は AI に提供する物語の背景情報である。

主な内容は以下の通り。

- 物語のジャンル  
- 物語のテーマ  
- 物語世界の基本設定  

---

## 5. Instruction

Instruction は AI に対する指示内容である。

例として以下が挙げられる。

- 物語構造の分析  
- 伏線の検出  
- ストーリー展開の提案  

---

## 6. Data

Data は NWF の構造化データである。

主なデータは以下の通り。

- Characters  
- Threads  
- Scenes  
- World Rules  

---

## 7. Output Format

AI の出力は一定の形式で返される。

主な出力形式は以下の通り。

- 分析結果  
- 提案  
- 構造評価  

---

## 8. Prompt 設計方針

Prompt は以下の原則に基づき設計される。

- 明確な指示  
- 構造化されたデータ  
- 再現可能な入力  

---

## 9. AI 利用の安全設計

Prompt Protocol では以下の安全設計を採用する。

- 作者の意図の尊重  
- AI 自動変更の禁止  
- AI 出力の透明性確保  

---

## 10. AI との対話モデル

NWF では AI との対話型プロセスを採用する。

1. 作者がデータを入力  
2. AI が解析  
3. AI が提案  
4. 作者が採用を判断  

---

## 11. まとめ

Prompt Protocol は NWF における AI 利用の標準的な通信方式である。

このプロトコルにより AI と人間の協働による物語制作が可能になる。

---

[EOF]