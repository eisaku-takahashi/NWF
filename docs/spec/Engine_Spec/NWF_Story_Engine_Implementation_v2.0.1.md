Source: docs/spec/Engine_Spec/NWF_Story_Engine_Implementation_v2.0.1.md
Updated: 2026-04-16T11:37:00+09:00
PIC: Engineer / ChatGPT

# NWF Story Engine 実装設計仕様書 v2.0.1

---

## 1. 概要

本仕様書は、Phase 3.3「Engine Skeleton」における src/engine/story_engine.py の実装仕様を定義する。

Story Engine は以下を担う：

- Entity → Story Graph 変換
- Stardate ベース Timeline 生成
- 論理整合性（ConsistencyValidator）および時間整合性（MetadataManager）の統合検証

また、本仕様書は Spec Driven Development に基づき、既存モジュールとのインターフェース完全一致（I/F Contract）を保証することを目的とする。

---

## 2. 依存関係（Dependencies）

### 2.1 Python モジュール

- src/core/entity_manager.py
- src/core/metadata_manager.py
- src/integrity/consistency_validator.py
- src/integrity/integrity_checker.py
- src/workflow/workflow_context.py

### 2.2 Spec

- NWF_Data_Model_v2.0.1.md
- NWF_Timeline_Model_v2.0.1.md
- NWF_Relationship_Model_v2.0.1.md
- NWF_Narrative_Consistency_Model_v2.0.1.md
- NWF_Temporal_Management_v2.0.1.md
- NWF_World_Rule_Execution_v2.0.1.md（追加）

※修正理由：
World Rule による動的制約が Story Engine の動作に直接影響するため依存関係に追加

---

## 3. インターフェース定義（I/F Contract）

### 3.1 WorkflowContext（既存）

アクセス方法（Private準拠）：

- context._transaction_id : str
- context._metadata : Dict[str, Any]
- context._local_vars : Dict[str, Any]

※禁止：
- context.transaction_id
- context.metadata
- context.global_vars

※追加仕様（重要）：
- context._metadata["world_rules"] : Dict[str, Any]

修正理由：
World Rule Execution により、行動可否判定が context metadata に依存するため

---

### 3.2 EntityManager

想定インターフェース：

- get_all_entities() -> Dict[str, Any]

戻り値：

{
    "entity_id": entity_object
}

entity_object 必須属性：

- id
- type
- relationships (List[Dict])
- metadata（任意）

変更なし

---

### 3.3 MetadataManager

使用メソッド：

- convert_to_stardate(datetime) -> float
- check_timeline_linearity(events) -> bool

変更なし

---

### 3.4 ConsistencyValidator

使用方法：

validator = ConsistencyValidator()
result = validator.validate(context, validation_result)

戻り値：

- result.is_consistent : bool
- result.violations : List[str]

修正点：

旧：
- 死亡状態による固定的な行動禁止

新：
- World Rule に基づく動的判定へ変更

修正理由：
Narrative Relativity 原則に基づき、因果律は世界設定に依存するため

---

### 3.5 ValidationResult（integrity_checker）

使用：

- prev_result.is_valid : bool

変更なし

---

## 4. データ構造定義

### 4.1 StoryGraph

{
    "nodes": List[Node],
    "edges": List[Edge]
}

変更なし

---

### 4.2 Node

{
    "id": str,
    "type": str,
    "state": Optional[str]
}

変更なし

---

### 4.3 Edge

{
    "source": str,
    "target": str,
    "type": str,
    "weight": float,
    "stardate": float
}

変更なし

---

### 4.4 NarrativeUnit

{
    "timestamp": str,
    "actor": str,
    "location": str,
    "action": str,
    "integrity_status": str
}

変更なし

---

## 5. 処理フロー

### 5.1 generate_story_graph()

#### Input

- entities: Dict[str, Entity]

#### Process

1. Entity を Node に変換
2. relationships を Edge に変換
3. MetadataManager により Stardate を付与
4. ConsistencyValidator による検証

追加処理：

5. World Rule の取得

world_rules = context._metadata.get("world_rules", {})

6. World Rule に基づくエッジ生成制御

修正理由：
グラフ構築段階で既に「存在し得ない関係」を除外する必要があるため

#### Output

- StoryGraph

---

### 5.2 render_timeline()

#### Input

- StoryGraph

#### Process

1. Edge を Stardate 昇順ソート
2. NarrativeUnit に変換
3. MetadataManager による時間整合性チェック

追加処理：

4. World Rule に基づくナラティブフィルタリング

修正理由：
同一グラフでも世界設定により描写可能な物語が変化するため

#### Output

- List[NarrativeUnit]

---

## 6. 整合性統合（Guard Rails）

### 6.1 Temporal Integrity

旧：
- Stardate の逆転禁止

新：
- Stardate の逆転は World Rule により制御

例：
allow_time_reversal = true の場合許可

修正理由：
時間逆行系作品に対応するため

---

### 6.2 Causal Integrity

旧：
- 死亡キャラの行動禁止

新：
- 死亡キャラの行動可否は World Rule に依存

例：
allow_ghost_activity = true → 行動可能

修正理由：
ファンタジー・ホラー・SF 等の表現自由度確保

---

### 6.3 エラー時動作

- 即時停止
- violations を返却
- AuditLog に記録（将来拡張）

変更なし

---

## 7. 不足情報の補完定義

### 7.1 Relationship 型定義（追加）

Enum:

- LOCATION_STAY
- INTERACTION
- OWNERSHIP

変更なし

---

### 7.2 Graph Persistence（暫定）

JSON形式：

{
    "nodes": [...],
    "edges": [...]
}

変更なし

---

### 7.3 Loop Detection（Phase 3.3では未実装）

理由：

- Phase 4で実装予定
- 現段階では非必須

変更なし

---

## 8. DoD（Definition of Done）

- Entity → Graph 変換が動作
- Stardate順 Timeline 生成
- 整合性チェック統合
- NarrativeUnit 出力成功

追加：

- World Rule による挙動分岐が確認可能

修正理由：
本フェーズの設計変更の中核要素のため

---

## 9. 将来拡張

- Emotional Curve 統合
- AI Narrative 補完
- Graph Query Engine 連携
- World Rule Engine 高度化（スコープ階層・優先順位）

---

## 10. まとめ

旧設計：

- 物語 = ロジック制約

新設計：

- 物語 = ロジック + 世界法則（World Rule）

本仕様により以下が保証される：

- モジュール間インターフェースの完全一致
- Phase 3.1 / 3.2 との整合性維持
- World Rule によるナラティブ相対性の実現
- Story Engine の最小実装可能状態

これにより、NWF は「点（Entity）」から「線（Story）」への変換能力に加え、
「世界ごとに異なる物語生成能力」を獲得する。

---

[EOF]