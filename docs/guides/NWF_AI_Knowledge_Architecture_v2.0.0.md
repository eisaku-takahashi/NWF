Source: docs/guides/NWF_AI_Knowledge_Architecture_v2.0.0.md
Updated: 2026-03-15T21:20:00+09:00
PIC: Engineer / ChatGPT

# NWF AI Knowledge Architecture v2.0.0
Novel Writing Framework (NWF)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 概要
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

本ドキュメントは  
NWF (Novel Writing Framework) v2.0 における  
AI連携を前提とした知識管理アーキテクチャを定義する。

NWFは以下の特徴を持つ創作フレームワークである。

・小説構造のデータ化  
・Thread / Scene / Character / WorldRule による物語管理  
・JSONベースのデータ構造  
・複数AIによる協調開発  
・Gitによる仕様管理  

NWF v2.0 では  
AIと人間の協調作業を前提とした  
「AI Knowledge Architecture」を導入する。

本アーキテクチャは

AI  
開発環境  
知識ベース  
バックアップ

の四層構造によって運用される。


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. AI運用体制
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NWF v2.0 は  
複数AIによる「三頭政治（Tri-Model System）」で運用される。

構成は以下である。

Director  
Gemini

Engineer  
ChatGPT

Writer  
Claude

各AIの役割は以下の通り。


Director（Gemini）

・プロジェクト全体設計  
・物語構造ディレクション  
・仕様意思決定  


Engineer（ChatGPT）

・技術設計  
・フレームワーク構築  
・データ構造設計  
・整合性検証  


Writer（Claude）

・文章生成  
・物語表現  
・シーン執筆  


この三者により  
創作と技術設計を分離した高度な制作体制を構築する。


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. 開発環境
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NWF v2.0 のローカル開発環境は  
**Antigravity** を使用する。

Antigravity は  
NWFプロジェクトのローカル管理環境として使用される。

主な用途は以下である。

・ローカルGit管理  
・リポジトリ操作  
・ファイル編集  
・プロジェクト管理  


開発作業の基本フローは以下である。

1  
Antigravity上でローカル開発

2  
Gitによる変更管理

3  
GitHubへの同期

4  
AIによる仕様生成および検証

この構造により  
人間の開発環境とAIの知識処理を分離する。


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. 知識管理レイヤー
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NWF v2.0 の知識管理は  
以下の四層構造で構成される。


Layer 1  
Local Development Layer

Antigravity


役割

・ローカル開発  
・Git操作  
・実装管理  


Layer 2  
Repository Layer

GitHub


役割

・ソースコード管理  
・仕様管理  
・バージョン管理  


Layer 3  
AI Knowledge Layer

NotebookLM


役割

・仕様ドキュメント蓄積  
・AI参照用ナレッジベース  
・設計資料管理  


Layer 4  
Backup Layer

Google Drive


役割

・長期バックアップ  
・プロジェクト保管  
・災害対策  


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5. AI連携データフロー
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NWF v2.0 のAI連携は  
以下のデータフローで運用される。


1  
ローカル開発

Antigravity


2  
仕様作成

AI（ChatGPT / Gemini / Claude）


3  
仕様保存

docs/spec  
docs/guides


4  
Git管理

Git / GitHub


5  
知識同期

NotebookLM


6  
バックアップ

Google Drive


このフローにより

開発  
仕様  
知識  
バックアップ

を分離管理する。


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
6. NWF Knowledge Asset
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NWFの知識資産は以下のカテゴリに分類される。


Spec Documents

仕様書


Engine Documents

エンジン設計


Project Documents

小説プロジェクト資料


Story Data

JSON形式の物語データ


Research Documents

世界設定資料


これらはすべて  
docs ディレクトリを中心に管理される。


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
7. AI対応ドキュメント設計
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NWF v2.0 のドキュメントは  
AIによる解析を前提として設計される。

基本ルールは以下である。


1  
Markdown形式


2  
明確なセクション構造


3  
機械可読な命名規則


4  
Spec Version 管理


これにより  
AIによる構造解析と知識再利用を可能にする。


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
8. セキュリティと冗長性
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NWF v2.0 は  
三重バックアップ体制を採用する。


Primary

Local Repository


Secondary

GitHub Repository


Tertiary

Google Drive Backup


この構造により  
以下のリスクを回避する。

・ローカル障害  
・クラウド障害  
・データ破損  


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
9. 将来拡張
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NWF AI Knowledge Architecture は  
将来的に以下の拡張を想定する。


AI Agent Integration

AIエージェントによる自動解析


Automated Story Analysis

物語構造の自動分析


World Simulation

世界設定の論理シミュレーション


Collaborative AI Writing

AI共同執筆環境


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
10. まとめ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NWF v2.0 のAI知識管理構造は  
以下の四層で構成される。


Local Development

Antigravity


Repository

GitHub


AI Knowledge

NotebookLM


Backup

Google Drive


この構造により

AI  
開発環境  
知識管理  
バックアップ

を統合した  
高度な創作フレームワークを実現する。


[EOF]