# NWF Development Roadmap v1.0.0

## 1. 概要

NWF Development Roadmap v1.0.0 は、NWF（Novel Writing Framework）を長期連載小説の制作に実用可能な状態まで完成させるための開発工程書である。

本文書は NWF Spec v1.0 および v1.0.1 の仕様を基盤として作成されており、仕様書で定義されたアーキテクチャ、ディレクトリ構造、データ構造、エンジン構成をすべて実装・整備することを目的とする。

本文書では、NWF Spec に基づいて最終的に必要となるプロジェクトのディレクトリ構造を定義し、すでに作成されているフォルダおよびファイルと、今後作成する予定のフォルダおよびファイルの両方を整理する。

さらに、それぞれのフォルダおよびファイルについて以下を明確にする。

- NWF における役割  
- 人間が理解するための説明  
- 仕様書との対応関係  

これにより、NWF v1.0 完成までの開発の順序と優先順位を体系的に整理する。

本ロードマップは、NWF プロジェクト全体の構造を俯瞰するための基盤文書であり、今後のエンジン実装、データ構造設計、ツール開発、小説制作実験など、すべての開発作業の指針として機能する。


## 2. 諸元

Document Path: 
<project_root>/docs/project/v1.0/NWF_Development_Roadmap_v1.0.0.md

文書種別: 
プロジェクト工程書

対象プロジェクト: 
NWF（Novel Writing Framework）

対象バージョン: 
NWF v1.0

基準仕様: 

- NWF Spec v1.0  
- NWF Spec v1.0.0 Updates  
  NWF Spec v1.0.0 と NWF Spec v1.0 は同一バージョンを意味する  
- NWF Spec v1.0.1 Updates  

文書の目的: 
NWF を長期連載小説の制作に実用可能な状態まで完成させるための開発工程を定義する。

文書の役割: 
本工程書は NWF Spec を実装可能なプロジェクト構造へ具体化するための指針を示す文書である。  
NWF の完成に必要なディレクトリ構造、フォルダ構成、ファイル構成、エンジン構成、データ構造を整理し、開発の優先順位と実装範囲を明確にする。

完成の定義: 
NWF v1.0 の完成とは、以下の条件を満たす状態を指す。

- NWF の仕様に基づいた統一されたプロジェクト構造が存在する  
- Thread、Scene、Character、WorldRule などの物語構造をデータとして管理できる  
- それらを処理するエンジン群が実装されている  
- 小説プロジェクトをテンプレートから作成し長期的に管理できる  
- 物語構造の設計から本文執筆までを一つのフレームワーク内で行える  

文書の適用範囲: 
本工程書は NWF の開発および運用に関わる以下の対象に適用される。

- NWF 仕様文書  
- NWF 実行エンジン  
- NWF データ構造  
- NWF 小説プロジェクト  
- NWF 補助ツール  

基準ディレクトリ: 
NWF Project Root

Spec 表記: 
- <project_root>/  
- NWF Project Root  

バージョン管理方式: 
Semantic Versioning を採用する。
仕様書ファイルは以下の形式で管理する。

ファイル名_vMAJOR.MINOR.PATCH.md

例

- NWF_Development_Roadmap_v1.0.0.md  
- NWF_Development_Roadmap_v1.0.1.md  

Git タグ: 
Spec の公開バージョンは Git タグで管理する。

例

spec-v1.0.1

管理対象: 

- 仕様文書  
- エンジン実装  
- データ構造  
- 小説プロジェクト構造  
- 補助ツール  

## 3. NWF Project の主要階層構造

<project_root>/
│
├─ docs/
│  ├─ project/
│  └─ spec/
│     ├─ Index/
│     ├─ System_Architecture/
│     ├─ Core_Spec/
│     ├─ Architecture_Spec/
│     ├─ Engine_Spec/
│     ├─ AI_Interface/
│     ├─ Data_Spec/
│     ├─ Execution_Spec/
│     ├─ AI_Workflow_Spec/
│     └─ Spec_Governance/
│
├─ data/
│  ├─ threads/
│  ├─ scenes/
│  ├─ characters/
│  └─ world_rules/
│
├─ engines/
│  ├─ thread_engine/
│  ├─ scene_engine/
│  ├─ character_engine/
│  ├─ plot_engine/
│  └─ world_rule_engine/
│
├─ novel_projects/
│  └─ project_template/
│     ├─ threads/
│     ├─ scenes/
│     ├─ characters/
│     ├─ world_rules/
│     └─ manuscript/
│
└─ tools/
   └─ validation/

## 4. NWF Project のファイル一覧

- ファイルパスは <project_root>/ の記述がない場合は <project_root>/ からの相対パスとして扱う
- v1.0/などのフォルダは、フォルダ名に表記されたバージョンのファイルをまとめて管理する場合に使用する
- 同一内容のバージョン違いファイルに関しては、最新のバージョンのみを表記する

### 作成済のファイル一覧

1. docs/project/v1.0/ : 
  - NWF_Development_Roadmap_v1.0.0.md（本ファイル）

2. docs/spec/Index/v1.0/ : 
  - NWF_Spec_Index_v1.0.1.md

3. docs/spec/System_Architecture/v1.0/ : 
  - NWF_System_Architecture_v1.0.1.md

4. docs/spec/Core_Spec/v1.0/ : 
  
  - NWF_Core_Architecture_Index_v1.0.1.md
  - NWF_Glossary_v1.0.1.md
  - NWF_Data_Model_v1.0.md
  - NWF_Thread_Graph_Model_v1.0.md
  - NWF_Scene_Model_v1.0.md
  - NWF_Beat_Model_v1.0.md
  - NWF_File_System_v1.0.md
  - NWF_Query_Language_v1.0.md
  - NWF_Execution_Flow_v1.0.md
  - NWF_Narrative_Rendering_v1.0.md

5. docs/spec/Architecture_Spec/v1.0/ : 
  
  - NWF_World_Model_v1.0
  - NWF_Character_Model_v1.0.md
  - NWF_Story_Database_Model_v1.0.md
  - NWF_Emotional_Curve_Model_v1.0.md
  - NWF_Foreshadowing_Model_v1.0.md
  - NWF_Narrative_Consistency_Model_v1.0.md
  - NWF_AI_Authoring_Interface_v1.0.md

6. docs/spec/Engine_Spec/v1.0/ : 
  
  - NWF_Engine_Architecture_v1.0.md
  - NWF_ThreadEngine_v1.0.md
  - NWF_SceneEngine_v1.0.md
  - NWF_BeatEngine_v1.0.md
  - NWF_ForeshadowingEngine_v1.0.md
  - NWF_EmotionalCurveEngine_v1.0.md

7. docs/spec/AI_Interface/v1.0/ : 
  
  - NWF_Prompt_Protocol_v1.0.md
  - NWF_AI_Authoring_Interface_v1.0.md
  - NWF_AI_Analysis_Interface_v1.0.md

8. docs/spec/Data_Spec/v1.0/ : 
  
  - NWF_Data_Spec_Index_v1.0.md
  - NWF_Story_JSON_Structure_v1.0.md
  - NWF_Thread_JSON_Structure_v1.0.md
  - NWF_Scene_JSON_Structure_v1.0.md
  - NWF_Beat_JSON_Structure_v1.0.md
  - NWF_Character_JSON_Structure_v1.0.md
  - NWF_World_JSON_Structure_v1.0.md
  - NWF_Foreshadowing_JSON_Structure_v1.0.md
  - NWF_EmotionalCurve_JSON_Structure_v1.0.md

9. docs/spec/Execution_Spec/v1.0/ : 
  
  - NWF_Execution_Pipeline_v1.0.md
  - NWF_Engine_Order_v1.0.md
  - NWF_Validation_System_v1.0.md
  - NWF_Error_Model_v1.0.md

10. docs/spec/AI_Workflow_Spec/v1.0/ : 
  
  - NWF_AI_Workflow_Index_v1.0.md
  - NWF_AI_Story_Generation_Workflow_v1.0.md
  - NWF_AI_Story_Analysis_Workflow_v1.0.md
  - NWF_AI_Editing_Workflow_v1.0.md
  - NWF_AI_Collaboration_Model_v1.0.md

### 作成予定のファイル一覧


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
END OF DOCUMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━