Source: docs/spec/Core_Spec/NWF_World_Rule_Execution_v2.0.1.md
Updated: 2026-04-16T10:40:00+09:00
PIC: Engineer / ChatGPT

# NWF World Rule Execution v2.0.1

---

## 1. 概要

本仕様書は、NWF World Rule Model v2.0.1 を実行時に適用するための「World Rule Execution Protocol」を定義する。

従来の NWF v2.0.0 においては、World Rule は静的設定として扱われていたが、
v2.0.1 以降では Story Engine / ConsistencyValidator により動的に評価される
「世界制約エンジン」として機能する。

---

## 2. 修正背景（重要）

### 修正前（問題点）

- 因果律がハードコードされていた
- 「死亡キャラは行動禁止」などが固定ルールとして実装されていた
- 作品ごとの世界設定差異を吸収できなかった

例：

死亡状態（is_alive = False）なら行動禁止  
→ ERR_CAUSAL として一律エラー

---

### 修正後（本仕様の目的）

- 因果律を固定ルールから分離
- World Rule による動的制御へ移行
- 物語世界ごとに行動可能性を変更可能にする

---

### 設計原則（確定）

Principle: Narrative Relativity

「因果律は絶対ではない。世界設定によって相対化される」

---

## 3. World Rule Model との関係

本仕様は以下の既存仕様を拡張・実行レイヤーとして補完する：

- NWF_World_Rule_Model_v2.0.1.md（静的 + 動的制約定義）

---

### 修正前（Model側の限界）

World Rule Model は以下の問題を持っていた：

1. 実行時評価ロジックが未定義
2. ConsistencyValidator との接続が不明確
3. Event / Story Engine との統合が未定義
4. 実際の「行動可否判定プロトコル」が存在しない

---

### 修正後（Execution の役割）

本仕様は以下を提供する：

- 実行時ルール解釈
- 優先順位解決
- 判定ロジック定義
- ConsistencyValidator / Story Engine 連携

---

## 4. World Rule Execution フロー

### 4.1 実行パイプライン

1. Fetching  
   WorkflowContext.metadata から world_rules を取得

2. Merge  
   デフォルトルール + コンテキストルールを統合

3. Matching  
   Entity の状態・行動とルールを照合

4. Evaluation  
   条件に一致するか判定

5. Verdict  
   許可 / 拒否 を決定

6. Logging  
   違反時 AuditLog に記録

---

## 5. World Rule 取得仕様

### 修正前

context._metadata に直接依存（非公開属性）

---

### 修正後

context.metadata を使用（公開インターフェース準拠）

例：

world_rules = context.metadata.get("world_rules", {})

---

## 6. World Rule パラメータ定義（標準セット）

以下は最小実装における標準フラグである。

allow_resurrection: 死亡状態からの復帰許可  
allow_ghost_activity: 死亡状態での行動許可  
allow_time_reversal: 時間逆行許可  
physics_override: 物理法則の上書き  

---

### JSON例

{
  "world_rules": {
    "allow_resurrection": true,
    "allow_ghost_activity": true,
    "allow_time_reversal": false
  }
}

---

## 7. 判定ロジック仕様

### 修正前（削除対象：参考として保持）

if current_obj.is_alive is False:
    # 即違反
    raise ERR_CAUSAL

---

### 修正後（正式仕様）

if current_obj.is_alive is False:
    if not world_rules.get("allow_ghost_activity", False):
        違反とする

---

### なぜこの変更が必要か

- ファンタジー：幽霊活動を許可する
- SF：蘇生技術を許可する
- 時間SF：未来からの干渉を許可する

---

## 8. エラーコード仕様変更

### 修正前

ERR_CAUSAL_004  
固定的因果律違反

---

### 修正後

ERR_WORLD_RULE_001  
World Rule 違反

ERR_WORLD_RULE_002  
行動制約違反（例：幽霊活動禁止）

---

## 9. 優先順位・オーバーライド仕様

World Rule は階層構造を持つ：

global < regional < character < scene

優先順位：

scene > character > regional > global

---

### 修正追加（Execution側）

- override_allowed を評価対象に追加
- 実行時に優先順位を解決する

---

## 10. ConsistencyValidator 連携仕様

### 修正前

- 固定ルールによる検証
- is_alive による直接判定

---

### 修正後

- world_rules を読み込む
- 判定を動的化
- エラー種別を変更

---

## 11. Story Engine 連携仕様

Story Engine は以下を行う：

- グラフ生成時に World Rule を参照
- エッジ生成の可否を判定
- Timeline生成時のイベント合法性を確認

---

## 12. 変更影響範囲

### 影響あり

- ConsistencyValidator
- Story Engine（Phase 3.3）
- Event Engine（将来）
- Conflict Engine（将来）

---

### 影響なし

- Data Model
- Entity Schema

---

## 13. まとめ

本仕様により、NWF は以下へ進化する：

修正前：
固定された因果律によるストーリー制御

修正後：
World Rule による動的・相対的ストーリー制御

---

本仕様は NWF における「物語の憲法」であり、
すべてのエンジンは本仕様に従う必要がある。

---

[EOF]