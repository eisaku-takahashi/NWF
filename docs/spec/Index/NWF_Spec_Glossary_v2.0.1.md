Source: docs/spec/Index/NWF_Spec_Glossary_v2.0.1.md
Updated: 2026-03-29T06:14:00+09:00
PIC: Engineer / ChatGPT

# NWF Spec Glossary v2.0.1

---

## 1. Introduction

本ドキュメントは NWF (Narrative Workflow Framework / Story OS) における全仕様書共通の用語定義を管理するグロッサリである。  
本 Glossary は AI と人間の間で用語解釈の差異（Semantic Drift）を防止し、Spec、Data、Engine、Workflow、Governance の全領域における意味的整合性を維持することを目的とする。

本 Glossary は以下の役割を持つ。

- 全 Spec 共通語彙の統一定義
- 用語の一意性保証（1 用語 = 1 定義）
- Cross-Spec 用語整合性維持
- AI Prompt / Workflow における語彙基準
- Recursive Integrity Check における語彙整合性判定基準

用語は以下の 5 カテゴリに分類する。

- Concepts
- Data
- Engine
- AI / Workflow
- Governance

---

## 2. Core Vocabulary

### Story OS
NWF 全体を指す概念。  
世界設定、データ構造、物理制約、物語ロジック、AI Workflow、Spec Governance が相互作用しながら物語世界を生成・維持・進化させる統合システム。

### Recursive Integrity
仕様書、データ、生成物、Workflow が相互に整合性を検証し合い、システム全体の論理的一貫性を再帰的に維持・修復するプロセス。

### Integrity Score
仕様書または生成データの整合性・完全性・一貫性を数値化した指標。  
0 から 100 のスコアで表され、Spec Review、Data Validation、Story Consistency Check に使用される。

### Human-in-the-Loop (HITL)
AI による生成・更新・判断プロセスにおいて、人間（Architect / Engineer / Reviewer）が最終判断または承認を行う制御方式。

### Approval Gate
Spec 更新、Version Release、Story Milestone 確定などの重要イベントにおいて、PIC による承認を必須とする論理的関門。

---

## 3. Category-specific Terms

### 3.1 Concepts

World  
物語が展開される世界全体の設定、地理、政治、文化、技術水準を含む概念。

Timeline  
世界内で発生する出来事を時間順に整理した歴史構造。

Entity  
世界内に存在する実体。Character、Organization、Country、Aircraft などを含む。

Character  
物語に登場する人物または人格を持つ存在。

Event  
Timeline 上で発生する出来事、戦争、事故、政治イベントなど。

State  
ある時点における Entity または World の状態。

Relationship  
Entity 間の関係性（同盟、敵対、所属など）。

Story  
World、Timeline、Character、Event を基に構成される物語構造。

Story Arc  
物語全体または章単位の構造的なストーリーの流れ。

---

### 3.2 Data

Data Schema  
JSON データ構造の形式定義。

JSON Schema  
JSON データの構造、型、必須項目を定義する仕様。

snake_case  
JSON キー名およびデータフィールド名に使用する命名規則。

Unit Specification  
数値データに対して単位（kg、km、year など）を必ず明記する規則。

Data Integrity  
データの完全性、一貫性、整合性が維持されている状態。

Data Validation  
データが Schema および Spec に適合しているか検証する処理。

Master Data  
World、Country、Aircraft など基盤となるデータセット。

Derived Data  
Simulation や Engine により生成されたデータ。

---

### 3.3 Engine

Engine  
Data を入力として処理し、Simulation、Validation、Calculation を行うロジックモジュール。

Simulation Engine  
物理、戦闘、経済、技術進化などをシミュレーションするエンジン。

Validation Engine  
データやストーリーの整合性を検証するエンジン。

Rule Engine  
定義されたルールに基づいて判定や処理を行うエンジン。

Execution Pipeline  
Data が Engine を通過して Output が生成される一方向の処理フロー。

Output  
Engine または Execution によって生成された結果データまたはレポート。

---

### 3.4 AI / Workflow

AI Interface  
AI と NWF システムの間でデータ、プロンプト、結果をやり取りするインターフェース仕様。

Prompt Template  
AI に対して一定の形式で指示を出すためのテンプレート化されたプロンプト。

Workflow  
AI と Human の作業手順、レビュー、承認を含む運用プロセス。

Pipeline  
Data や処理が Engine を通過する機械的な一方向処理フロー。

AI Role  
AI に割り当てられた役割（Writer、Reviewer、Engineer、Analyst など）。

Draft  
AI または Human によって作成された初稿。

Review  
Draft を評価し修正点を抽出するプロセス。

Rewrite  
Review 結果に基づいて Draft を修正する作業。

Story Production Pipeline  
World 設定から最終原稿までの物語制作工程全体。

---

### 3.5 Governance

Spec  
個別の技術仕様書または定義書。

Standard  
全 Spec が従う共通規格または記述ルール。

Spec Governance  
Spec の作成、レビュー、承認、バージョン管理を行う統治プロセス。

Semantic Versioning  
Major、Minor、Patch によって仕様変更レベルを管理するバージョン管理方式。

Version Control  
Git 等を用いた変更履歴管理。

Decision Log  
重要な設計判断、仕様変更理由、承認記録を残すログ。

Audit  
Spec、Data、Workflow が規格に従っているか検証する監査プロセス。

Backup  
Spec、Data、Story、Log を安全に保存するプロセス。

Archive  
過去バージョンの Spec、Data、Story を保存する領域。

---

## 4. Naming Conventions

NWF における命名規則を以下に定義する。

- JSON キーは snake_case を使用する
- 単位を伴う数値は必ず unit を明記する
- Spec 名は PascalCase + Version
- ファイル名は Spec_Name_vX.X.X.md
- 略語は初出時に必ず正式名称を記述する
- 同一概念に複数名称を使用しない
- Workflow と Pipeline を混同しない
- Spec と Standard を区別する

---

## 5. Semantic Drift Control

意味の混同を防ぐため、以下を厳密に区別する。

Workflow  
AI と Human の作業手順、レビュー、承認を含む運用プロセス。

Pipeline  
Data が Engine を通過して処理される機械的な処理フロー。

Spec  
個別仕様書。

Standard  
全 Spec 共通の規格。

Data  
保存・管理される構造化情報。

Story  
World、Timeline、Character、Event を基にした物語構造。

Engine  
Data を処理するロジック。

Execution  
Engine を実行する処理プロセス。

Governance  
Spec、Version、Decision、Approval を管理する統治プロセス。

---

## 6. Integrity Validation Rules

Glossary に基づく整合性検証の基本ルールを定義する。

- 同一用語は常に同一の意味で使用すること
- 新規用語は Glossary に追加してから Spec に使用すること
- 同義語の新規作成を禁止する
- Spec 間で用語定義が矛盾してはならない
- Workflow と Pipeline を混同してはならない
- Spec と Standard を混同してはならない
- Engine と Execution を混同してはならない
- Story と Data を混同してはならない

Glossary は Recursive Integrity Check において語彙整合性検証の基準として使用される。

---

## 7. まとめ

NWF_Spec_Glossary_v2.0.1 は以下を目的として作成された。

- NWF 共通語彙の統一定義
- Semantic Drift の防止
- AI と Human の共通言語の確立
- Cross-Spec 用語整合性維持
- Recursive Integrity Check の語彙基準

Glossary は Spec、Data、Engine、Workflow、Governance を横断する  
**NWF の意味体系（Semantic Layer）** として機能する。

---

[EOF]