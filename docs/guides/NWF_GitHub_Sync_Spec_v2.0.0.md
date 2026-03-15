Source: docs/guides/NWF_GitHub_Sync_Spec_v2.0.0.md
Updated: 2026-03-15T21:28:00+09:00
PIC: Engineer / ChatGPT

# NWF GitHub Synchronization & Information Sharing Spec v2.0.0

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 概要
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

本仕様は  
NWF (Novel Writing Framework) v2.0 における  
GitHub同期およびAI間情報共有の運用ルールを定義する。

本仕様の目的は以下である。

・人間による同期ミスの防止  
・古いファイルへの誤上書きの防止  
・Director(Gemini) と Engineer(ChatGPT) の間での仕様整合性確保  
・AIが解析可能なGit運用の確立  

本仕様は  
NWFのAI開発体制（Director / Engineer / Writer）における  
公式同期プロトコルとして使用される。


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. Source of Truth (SoT)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NWF v2.0 では  
以下の階層で「正しい情報」を定義する。


Primary Source of Truth

GitHub main ブランチ


定義

GitHub の main ブランチに存在する内容を  
NWFプロジェクトの唯一の公式仕様とする。


理由

・中央リポジトリとしての一貫性  
・履歴管理  
・AI参照の統一  


階層構造は以下の通り。


Level 1

GitHub main

Absolute Source of Truth


Level 2

Local Repository (Antigravity)

Working Copy


Level 3

NotebookLM

Knowledge Mirror


つまり

GitHub main  
のみが

「正しい状態」

である。


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. ブランチ運用
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NWF v2.0 の基本ブランチ構造は以下とする。


main

安定仕様


develop

統合開発


feature/*

個別開発


例

feature/thread_engine  
feature/spec_update  
feature/scene_logic


運用ルール

1

新規作業は必ず  
featureブランチで開始


2

feature → develop


3

develop → main


4

main は常に安定状態


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. Commit Message Standard
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NWFでは  
AI解析を前提としたコミットメッセージ形式を採用する。


基本構造

[TYPE/SCOPE] Summary


例

[DOC/SPEC] Update WorldRule Logic v2.0.0

[ENGINE/THREAD] Add conflict validation system

[DATA/STORY] Update story_state.json

[FIX/SCHEMA] Correct thread_id format

[TOOLS/DEV] Add JSON validation script


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5. Commit Type 定義
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TYPE は以下から選択する。


DOC

ドキュメント更新


SPEC

仕様更新


ENGINE

エンジン更新


DATA

JSONデータ更新


FIX

バグ修正


REFACTOR

構造改善


TOOLS

開発ツール


TEST

テスト関連


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
6. Synchronization Flow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NWFの基本同期フローは以下である。


Local Development

Antigravity


↓

Git Commit


↓

Git Push


↓

GitHub Repository


↓

NotebookLM Sync


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
7. Local → GitHub 同期手順
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Antigravityでの作業後は  
以下の手順で同期する。


Step 1

ローカル変更確認

git status


Step 2

変更内容確認

git diff


Step 3

コミット

git commit


Step 4

Push

git push


Step 5

GitHub確認

・ファイル更新確認  
・コミット履歴確認


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
8. GitHub → NotebookLM 同期
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Director(Gemini)の知識基盤は  
NotebookLMで管理される。

同期手順は以下。


1

GitHubの最新仕様を確認


2

更新されたSpecファイルを抽出


3

NotebookLMへアップロード


4

Knowledge Base 更新


これにより

Director は常に

最新仕様

を参照可能となる。


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
9. AI-Driven Validation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Engineer(ChatGPT) は  
以下の検証を行う。


Validation 1

Metadata Header


確認項目

Source  
Updated  
PIC


Validation 2

ファイルパス整合性


例

docs/spec  
docs/guides  
docs/references


Validation 3

Spec Version


確認項目

version形式

major.minor.patch


Validation 4

JSON Schema


確認項目

snake_case  
unit明記


Validation 5

重複ファイル


同一Specの複数存在を検知


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
10. Engineer Sync Checklist
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Engineerは以下を確認する。


1

現在のファイルは

GitHub main

と一致しているか


2

Metadata Header の Source が

正しいパスか


3

Spec Version が

既存仕様と矛盾していないか


4

同名ファイルが

docs/spec 内に存在しないか


5

commit message が

NWF標準に従っているか


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
11. 自動不整合検出ロジック
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Engineerは以下を検出する。


Rule 1

Source path mismatch


Rule 2

Spec version conflict


Rule 3

duplicate filename


Rule 4

metadata missing


Rule 5

invalid json key format


これにより

AIが仕様破損を検知する。


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
12. Human Error Prevention
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NWF Git運用では  
以下のヒューマンエラーを防止する。


同期漏れ


古い仕様編集


誤ファイル更新


誤パス保存


誤バージョン更新


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
13. まとめ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NWF GitHub同期仕様の核心は以下である。


Source of Truth

GitHub main


Development

Antigravity Local


Knowledge Base

NotebookLM


Backup

Google Drive


そして

Engineer(ChatGPT)

は

仕様整合性検証AI

として機能する。


この仕組みにより

AIと人間が

常に同一仕様

を共有できる。


[EOF]