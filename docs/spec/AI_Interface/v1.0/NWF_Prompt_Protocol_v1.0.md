# NWF Prompt Protocol v1.0

## 概要

NWF（Novel Writing Framework）では AI と物語データを安全かつ一貫した形式でやり取りするために Prompt Protocol を定義する。

Prompt Protocol は AI に対して NWF データをどのように提示し、どのような形式で結果を受け取るかを規定する。

このプロトコルにより AI を物語設計の補助ツールとして体系的に利用することが可能になる。


## Prompt Protocol の目的

Prompt Protocol の目的は以下である。

AI と NWF データの整合性確保  
AI 解析の再現性の確保  
AI 出力形式の標準化  
AI 利用の安全性確保  


## 基本構造

NWF Prompt Protocol は以下の構造を持つ。

Context  
Instruction  
Data  
Output Format  


## Context

Context は AI に提供する物語の背景情報である。

主な内容

物語のジャンル  
物語のテーマ  
物語世界の基本設定  


## Instruction

Instruction は AI に対する指示内容である。

例

物語構造の分析  
伏線の検出  
ストーリー展開の提案  


## Data

Data は NWF の構造化データである。

主なデータ

Characters  
Threads  
Scenes  
World Rules  


## Output Format

AI の出力は一定の形式で返される。

主な出力形式

分析結果  
提案  
構造評価  


## Prompt 設計方針

Prompt は以下の原則に基づいて設計される。

明確な指示  
構造化されたデータ  
再現可能な入力  


## AI 利用の安全設計

Prompt Protocol では以下の安全設計を採用する。

作者の意図の尊重  
AI 自動変更の禁止  
AI 出力の透明性確保  


## AI との対話モデル

NWF では AI との対話型プロセスを採用する。

作者がデータを入力  
AI が解析  
AI が提案  
作者が採用を判断  


## まとめ

Prompt Protocol は NWF における AI 利用の標準的な通信方式である。

このプロトコルにより AI と人間の協働による物語制作が可能になる。