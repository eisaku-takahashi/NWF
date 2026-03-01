# NWF Development Guidelines
Novel Writing Framework – 開発・運用ポリシー

---

## 0. Philosophy（設計思想）

NWF（Novel Writing Framework）は単なる執筆ツールではない。  
それは「物語OS（Narrative Operating System）」である。

本ドキュメントは以下を定義する：

- システムの進化方法
- 小説の進化方法
- 両者を混同しないための原則

<!--
SYSTEM_OVERVIEW は「NWFとは何か」を説明する。
DEVELOPMENT_GUIDELINES は「NWFをどう進化させるか」を定義する。
-->

---

# 1. Versioning Strategy（バージョン戦略）

## 1.1 二層進化モデル（Dual Evolution Model）

NWFは以下の二層構造で進化する：

1. System Layer（Framework / Engine）
2. Manuscript Layer（創作物）

この2つは同じ方法でバージョン管理してはならない。

---

## 1.2 System Versioning（Gitタグ専用）

Gitタグは **NWFの構造バージョン専用** とする。

形式：

    nwf-vMAJOR.MINOR.PATCH

例：

    nwf-v0.1.0
    nwf-v0.2.0
    nwf-v1.0.0

セマンティックバージョニング規則：

- MAJOR：構造破壊的変更
- MINOR：機能追加
- PATCH：軽微な修正・リファクタ

小説進行でタグを切ってはならない。

<!--
タグを物語進行に使うと履歴の可読性が崩壊する。
-->

---

## 1.3 Manuscript Versioning（小説の管理）

小説の進化は以下で管理する：

- 通常コミット
- 08_Output/ に固定版を保存

例：

    08_Output/
        Arc01_v1.0.md
        Arc01_v1.1.md

タグは使用しない。

---

# 2. Commit Message Convention（コミット規則）

履歴の可読性は必須条件。

形式：

    type(scope): description

例：

    feat(system): emotion validation機能追加
    fix(plot): Arc01 シーン遷移修正
    docs: SYSTEM_OVERVIEW更新
    manuscript: Chapter03 草稿追加
    refactor(system): state updater再設計

---

## 2.1 使用可能な type

- feat        → 新機能追加
- fix         → 修正
- refactor    → 構造改善
- docs        → ドキュメント変更
- manuscript  → 本文更新
- chore       → メンテナンス

<!--
将来自動CHANGELOG生成を想定。
-->

---

# 3. Branch Strategy（将来公開を想定）

現在：個人開発のため単一ブランチで可。

将来公開時：

    main      → 安定版
    dev       → 開発中
    feature/* → 実験機能

小説用ブランチ例：

    arc01-dev
    arc02-dev

---

# 4. フォルダ責務厳守原則

トップレベルフォルダの責務を混在させない。

禁止例：

- CanonCoreにPythonスクリプトを置く
- Systemに本文を書く
- OutputとManuscriptを混ぜる

構造の秩序は長編一貫性の土台である。

---

# 5. export_structureツール方針

export_structure.py は：

- .venv を除外
- .git を除外
- 再現性を保つ
- Systemツールとして扱う

将来的には：

    09_System/tools/

へ移動しCLI化する。

---

# 6. 公開テンプレート化ポリシー

公開前に必ず：

- 個人原稿を削除
- CanonCoreをテンプレート化
- パス情報や秘密情報を除去
- READMEを外部向けに修正

将来理想構造：

    NWF-Core（テンプレート）
    Project-X（作品）

---

# 7. 設計整合性原則（Design Integrity Principle）

NWFは以下を目的とする：

- 長編一貫性
- 感情曲線の保持
- 構造追跡可能性

追跡可能性を損なう変更は禁止。

---

# 8. Future-Proofing（将来拡張原則）

構造思想が変化した場合、
本ドキュメントを同一コミットで更新すること。

<!--
設計思想のサイレント変更を防ぐ。
-->

---

End of Guidelines.