# NWF Architecture Redefinition v0.2
Novel Writing Framework 再設計書（公開前提構造）

---

## 1. 目的

NWFを以下の思想で再定義する。

- 特定の小説を作成するためのソフトウェアではなく
- 汎用的な小説制作フレームワークとする
- 制作する作品はエンジン上で動作する「プロジェクト」として扱う

---

## 2. 設計思想

### 2.1 エンジンとプロジェクトの分離

NWFは以下の2層構造を持つ。

- Engine Layer
- Project Layer

#### Engine Layer（汎用）

物語構造を管理・検証・出力するロジック群。

- CLI
- バリデーション
- 状態更新
- スレッド検証
- 構造エクスポート

作品依存の情報は持たない。

---

#### Project Layer（作品依存）

各小説作品ごとのデータ群。

- CanonCore
- WorldMatrix
- PlotArchitecture
- EmotionalCurve
- ThreadEngine
- StoryState
- Manuscript
- Output

作品ごとに独立ディレクトリを持つ。

---

## 3. 新フォルダ構造（理想形）

Novel_Writing_Framework/
│
├── nwf_engine/
│   ├── cli/
│   ├── core/
│   ├── validators/
│   ├── state/
│   └── tools/
│
├── projects/
│   └── virtual_aviation_history_(fluctuation)/
│       ├── CanonCore/
│       ├── WorldMatrix/
│       ├── PlotArchitecture/
│       ├── ThreadEngine/
│       ├── EmotionalCurve/
│       ├── StoryState/
│       ├── Manuscript/
│       └── Output/
│
├── docs/
├── .github/
├── requirements.txt
└── README.md

---

## 4. 命名方針

### 4.1 エンジン命名

- 09_System → nwf_engine
- 内部構造は機能単位で整理する

### 4.2 プロジェクト命名

プロジェクト名は：

virtual_aviation_history_(fluctuation)

とする。

将来：

- virtual_aviation_history_(origins)
- virtual_aviation_history_(collapse)

などの拡張を想定。

---

## 5. バージョン戦略

### Engine Version
SemVerを採用。

例：
v0.2.0 → 構造再定義
v0.3.0 → CLI統合
v1.0.0 → 公開版

### Project Version
各プロジェクトは独立してタグ管理可能。

---

## 6. 今回の変更の意味

この再設計は：

- テンプレート公開前提化
- 複数作品対応化
- 将来pip配布可能化

を目的とする。

---

## 7. 次のステップ

1. 実フォルダ再編
2. importパス修正
3. CLI統合
4. JSON / Markdown出力拡張

---

End of Architecture v0.2
