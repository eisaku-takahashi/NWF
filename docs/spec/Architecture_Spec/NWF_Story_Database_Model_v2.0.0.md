Source: docs/spec/Architecture_Spec/NWF_Story_Database_Model_v2.0.0.md
Updated: 2026-03-19T03:35:00+09:00
PIC: Engineer / ChatGPT

# NWF Story Database Model v2.0.0

---

## 1. 概要

NWF（Novel Writing Framework）における Story Database Model は、物語を構成するすべての要素を体系的に管理するための中心モデルである。本モデルは、キャラクター、世界設定、ストーリー構造、感情変化、伏線、時間軸、整合性などを統合的に扱い、物語設計、分析、生成のためのデータ基盤を提供する。

v2.0.0 では、v1.0 の基本構造を継承しつつ、以下の拡張を行った。

- Narrative Consistency Model との統合による矛盾検出機能の拡張
- Emotional Curve Model の多層化対応（Threadごとの感情カーブ追跡）
- Foreshadowing Model との連携強化（Thread横断伏線管理）
- AI Authoring Interface との構造的接続強化
- データ形式の明確化（snake_case、単位表記の統一）

---

## 2. 基本構造

Story Database は複数のモデルで構成される。各モデルは相互に連携し、物語全体を統合的に管理する。

### 2.1 Character Model

- 管理対象: 登場人物・知的存在
- 主な情報: キャラクターID、名前、役割、性格、背景、関係性、所属
- 関連性: Thread, Scene, Beat, Emotional Curve, Foreshadowing

### 2.2 World Model

- 管理対象: 物語世界
- 主な情報: 世界名、物理法則、文化、社会制度、地理、歴史
- 関連性: Character 行動制約、Thread イベント制御

### 2.3 Thread Model

- 管理対象: 主要ストーリーライン
- 主な情報: Thread ID、テーマ、概要、関連キャラクター、Scene リスト
- 関連性: Scene, Emotional Curve, Foreshadowing

### 2.4 Scene Model

- 管理対象: 物語の場面
- 主な情報: Scene ID、所属 Thread、場所、登場キャラクター、シーン概要、感情強度、時間情報
- 関連性: Beat, Emotional Curve, Foreshadowing, Narrative Consistency

### 2.5 Beat Model

- 管理対象: Scene 内の最小出来事
- 主な情報: Beat ID、所属 Scene、行動、発言、感情変化、イベント
- 関連性: Character 行動追跡、Emotional Curve 変化、伏線提示

### 2.6 Emotional Curve Model

- 管理対象: 感情の起伏
- 主な情報: 感情強度（数値）、感情種類、変化方向、Thread別感情カーブ
- 関連性: Scene、Beat、Character、Thread

### 2.7 Foreshadowing Model

- 管理対象: 伏線および回収
- 主な情報: 伏線ID、内容、設置 Scene/Beat、回収 Scene/Beat、関連キャラクター、関連 Thread、状態管理（未回収/回収済み/部分回収）
- 関連性: Scene、Beat、Thread、Character

### 2.8 Narrative Consistency Model

- 管理対象: 物語整合性
- 主な情報: キャラクター整合性、世界整合性、因果関係整合性、時間軸整合性、伏線整合性
- 関連性: Scene、Thread、Character、World、Foreshadowing

---

## 3. モデル間の関係

- World は Character の行動範囲と社会的制約を定義  
- Character は Thread, Scene, Beat の中心的存在  
- Thread は複数の Scene を構成  
- Scene は複数の Beat で構成され、Emotional Curve や Foreshadowing と連携  
- Beat は物語の出来事とキャラクター行動を記録  
- Emotional Curve は Scene や Beat の変化に応じて更新  
- Foreshadowing は Beat や Scene に埋め込まれ、回収状況を管理  
- Narrative Consistency は全モデルを監査し整合性を保証  

---

## 4. データ保存形式

- JSON, YAML, Markdown 形式を標準化  
- JSON のキーは snake_case  
- 単位を明記（例: 感情強度 = int, 時間 = 秒, 日付 = ISO 8601 形式）  
- すべての成果物は 1-Click Copy 可能なコードブロック内で管理  
- ファイル末尾に [EOF] タグを記述  

---

## 5. AI連携

Story Database Model は AI による物語生成・分析を支援する。

用途例:

- キャラクター行動生成、関係分析  
- ストーリー構造の分析、感情曲線解析  
- 伏線設置・回収状況確認  
- Narrative Consistency による矛盾検出  
- Thread / Scene / Beat に基づく自動提案  

---

## 6. 設計思想

- 物語構造の体系化と統合管理  
- モデル間の明確な関連付け  
- AI による分析と生成支援の前提設計  
- 再利用可能で拡張性の高いデータモデル  
- 人間と AI の協働創作を支援  

---

## 7. まとめ

Story Database Model v2.0.0 は、NWF における物語データの統合管理基盤である。  
v1.0 からの拡張により、整合性管理、感情曲線、多層伏線、AI連携が強化され、複雑な長編作品やマルチスレッド物語でも安定した構造設計と解析が可能となった。

---

[EOF]