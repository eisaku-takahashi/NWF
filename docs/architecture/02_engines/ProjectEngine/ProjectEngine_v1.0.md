# ProjectEngine v1.0

---

# 1. 概要

ProjectEngineは、NWFプロジェクトを作成・初期化するためのエンジンである。

目的:

* 新規プロジェクトのディレクトリ構造作成
* 初期設定ファイル作成
* 初期ThreadEngineデータ生成（threads_master.json は別エンジンで担当）
* プロジェクトテンプレートの展開

---

# 2. Engineの役割

| 機能                           | 説明                                                           |
| ---------------------------- | ------------------------------------------------------------ |
| Project Creation             | 新規プロジェクトフォルダ作成                                               |
| Template Copying             | テンプレートファイルを展開                                                |
| Configuration Initialization | project_config.json 等の初期化                                    |
| Directory Setup              | Manuscript / Output / PlotArchitecture / StoryState 等のフォルダ作成 |
| Hooks                        | threads_master.json 初期化用のHook呼び出し                            |

---

# 3. プロジェクト構造

新規作成されるプロジェクトの例:

```
MyProject/
  project_config.json
  Manuscript/
  Output/
    compiled_versions/
    export/
  PlotArchitecture/
    GrandDesign.json
    Arc_01/
      arc_design.json
      scene_list.json
  StoryState/
    current_state.json
    archive/
  ThreadEngine/
    threads_master.json (生成は別エンジン)
  WorldMatrix/
    factions.json
    geography.json
    history.json
    power_balance.json
```

---

# 4. CLI/関数

## 4.1 create_project()

```
create_project(project_name: str, template: str = 'minimal') -> ProjectObject
```

* project_name: プロジェクト名
* template: 展開するテンプレート名（デフォルト minimal）
* 戻り値: ProjectObject（プロジェクトディレクトリ情報を保持）

処理:

1. ディレクトリ作成
2. テンプレートコピー
3. project_config.json 作成
4. 初期フォルダ作成
5. threads_master.json 生成Hook呼び出し

---

## 4.2 initialize_hooks()

```
initialize_hooks(project: ProjectObject)
```

* ThreadEngine への初期化コール
* 他将来拡張フックもここで呼び出す

---

# 5. ファイル/フォルダ命名ルール

* プロジェクト名: PascalCase
* Arcフォルダ: Arc_01, Arc_02 ...
* Chapterファイル: Chapter_01.md, Chapter_02.md ...
* Outputディレクトリ: compiled_versions, export
* StoryState: current_state.json, archive/

---

# 6. 拡張性

* threads_master.json 初期化ロジックをHookで分離
* 将来、テンプレート種類追加可能
* 他Engineとの連携をHookで追加可能

---

# 7. Version

```
ProjectEngine v1.0
NWF Engine Architecture
```
