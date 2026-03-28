Source: docs/spec/AI_Workflow_Spec/NWF_AI_Collaboration_Model_v2.0.1.md
Updated: 2026-03-28T19:15:00+09:00
PIC: Engineer / ChatGPT

# NWF AI Collaboration Model v2.0.1

---

## 1. 概要

本ドキュメントは、NWF v2.0.1（Story OS）における  
**Human（人間）・AI Agents（AIエージェント群）・System Engines（システムエンジン）**  
の三者協調構造を定義する。

本モデルは単一AIによる制作ではなく、役割分担された複数のAIエージェントと論理エンジン、
そして最終意思決定者としての人間が協調して作品制作を行う
**Digital Creative Team（デジタル創作チーム）** の組織構造と運用規律を定義することを目的とする。

---

## 2. The Creative Trinity（創作三位一体モデル）

NWF Story OS は以下の三者によって構成される。

### 2.1 Human（The Decision Maker）
人間は意思決定者であり、最終責任者である。

役割：
- アイデアの発案
- 各制作フェーズの承認
- 方向性の決定
- 作家性・テーマの最終決定
- 最終成果物の承認

AIやEngineは人間の意思を補助・拡張する存在であり、
最終判断は常にHumanが行う。

---

### 2.2 AI Agents（The Creative Intelligence）
AIエージェントは創作知能として機能し、
それぞれ専門的な役割（Role）を持つ。

AIはEngineの論理結果を基に、
物語・文章・構造・分析などの創作作業を行う。

AI Agents は直接データ整合性を保証するのではなく、
**論理的事実を物語表現へ変換する役割** を持つ。

---

### 2.3 System Engines（The Logical Backbone）
System Engine は論理基盤であり、
AIではなく計算・検証・整合性管理を担当する。

役割：
- Timeline 計算
- World Rule 整合性
- Character State 管理
- Event 因果関係管理
- 感情曲線計算
- Thread 構造管理
- データ整合性チェック

Engine は **物語を作らない**。  
Engine は **論理的に正しい状態（State / Fact）を計算する**。

---

## 3. AI Agent Organization Chart

NWF v2.0.1 では以下のエージェントロールを定義する。

### 3.1 Planner
役割：
- プロット構造設計
- Thread構造設計
- 章構成
- イベントの因果関係設計
- ストーリー全体の構造設計

---

### 3.2 Narrative Strategist
役割：
- 視点（POV）設計
- 情報開示順序設計
- 語りのトーン設計
- 読者体験設計
- テーマの表現方法設計

---

### 3.3 Writer（Authoring Agent）
役割：
- 地の文の執筆
- セリフ作成
- シーン描写
- 心理描写
- 文章の具体化

Writer は Engine が確定した事実を基に文章を生成する。

---

### 3.4 Critic（Analysis Agent）
役割：
- プロットの矛盾検出
- キャラクター行動の不整合検出
- テーマとの乖離検出
- 感情曲線の問題点分析
- 伏線構造の分析
- 物語品質評価

---

### 3.5 Validator
役割：
- World Rule 整合性チェック
- Timeline 整合性チェック
- Character State 整合性チェック
- Event 因果関係検証
- データ矛盾検出

Validator は物語ではなく **論理整合性** を検証する。

---

### 3.6 Director（Orchestrator）
役割：
- 各AI Agentの出力統合
- Writer / Critic / Planner のバランス調整
- 制作パイプライン管理
- 最終アウトプット統合
- Humanへの提出物作成

Director は AI 制作チームの指揮官に相当する。

---

## 4. Agent-Engine Interaction Model

AI Agent と System Engine の関係を定義する。

基本原則：

1. Engine は論理的事実を計算する
2. AI Agent はその事実を物語表現へ変換する
3. AI Agent は Engine を直接変更しない
4. Engine の出力は制約条件として扱う

データの流れ：

Engine Output（State / Fact）
→ AI Interface
→ AI Agent
→ Narrative / Text / Analysis
→ Director
→ Human Approval

つまり、

**Engine = Logic**  
**AI Agent = Narrative**  
**Human = Decision**

という役割分担になる。

---

## 5. Human-in-the-Loop Protocol

NWF v2.0.1 では人間による承認ゲートを定義する。

主な承認フェーズ：

1. Idea Approval
2. World Setting Approval
3. Character Approval
4. Plot Structure Approval
5. Draft Approval
6. Revision Approval
7. Final Approval

すべての重要フェーズで Human の承認を必須とする。

これにより、
AIによる暴走やテーマ逸脱を防止し、
作品の最終責任を人間が保持する。

---

## 6. Collaboration Pipeline

AIエージェント間の制作フローを定義する。

基本的な制作パイプライン：

1. Human → Idea 提出
2. Planner → プロット構造設計
3. Narrative Strategist → 視点・語り設計
4. Engine → Timeline / State 計算
5. Writer → シーン執筆
6. Validator → 整合性チェック
7. Critic → 物語分析・批評
8. Director → 修正統合
9. Human → 承認
10. Final Output

この流れにより、
物語制作は単一AIではなく、
**役割分担されたAIチームによる制作**となる。

---

## 7. Conflict Resolution

AIエージェント間で意見が対立した場合の規則を定義する。

例：
- Writer：ドラマ性を優先
- Validator：整合性違反を指摘
- Critic：テーマ逸脱を指摘

調停優先順位：

1. System Engine（論理整合性）
2. Validator（設定整合性）
3. Critic（物語品質）
4. Planner（構造）
5. Writer（表現）
6. Director（総合判断）
7. Human（最終決定）

最終決定権は常に Human が持つ。

---

## 8. Maintenance & Scaling

AIエージェントロールの追加・拡張に関する規則。

拡張可能な例：
- Dialogue Specialist
- Emotion Designer
- Worldbuilding Specialist
- Foreshadowing Designer
- Pacing Controller
- Theme Analyst

新しい Agent を追加する場合は以下を定義すること：

- Role Name
- Responsibility
- Input Data
- Output Data
- Related Engine
- Pipeline Position

これにより NWF は将来的に
**拡張可能なAI制作組織**としてスケールする。

---

## 9. まとめ

NWF AI Collaboration Model は、

- Human（意思決定）
- AI Agents（創作知能）
- System Engines（論理基盤）

の三者によって構成される。

System Engine が論理を保証し、
AI Agent が物語を創作し、
Human が最終意思決定を行う。

この構造により NWF Story OS は
単一AIツールではなく、

**人間 + 複数AI + 論理エンジンによる創作オペレーティングシステム**

として機能する。

---

[EOF]