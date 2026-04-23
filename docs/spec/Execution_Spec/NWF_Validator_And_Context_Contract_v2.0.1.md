Source: docs/spec/Execution_Spec/NWF_Validator_And_Context_Contract_v2.0.1.md
Updated: 2026-04-19T07:05:00+09:00
PIC: Engineer / ChatGPT

# NWF Validator and Context Interface Contract v2.0.1

---

## 1. 概要

本仕様書は、NWF Phase 3.4「Validator Integration」において必要となる「Validator」と「WorkflowContext」のインターフェース契約（I/F Contract）を定義する。

本契約は以下を保証することを目的とする。

- モジュール間インターフェースの完全一致
- 実装依存（getattr等）の排除
- 型安全性および決定論的動作の担保
- StoryEngine / Validator / IntegrityChecker の責務分離

本仕様は Execution Layer における Single Source of Truth（SSoT）である。

---

## 2. WorkflowContext 定義

### 2.1 概要

WorkflowContext は実行時の全ての動的情報を保持する唯一のコンテナであり、
すべての Engine および Validator はこのオブジェクトを通じてのみ状態にアクセスする。

---

### 2.2 スキーマ定義

- metadata: Dict[str, Any]
  - 由来: metadata_schema.json
  - 必須キー:
    - base_date: str
    - time_unit: str
    - coordinate_system: str

- world_rules: Dict[str, bool]
  - 例:
    - allow_ghost_activity: bool
    - allow_time_reversal: bool
    - allow_multi_location: bool

- transaction: List[TransactionEntry]
  - 状態変更履歴

- current_stardate: float
  - 単位: stardate
  - 精度: 小数点以下6桁
  - 比較時許容誤差: epsilon = 0.000001

---

### 2.3 TransactionEntry 定義

- timestamp: float (stardate)
- target_id: str
- op_type: str
- field: str
- old_val: Any
- new_val: Any

---

### 2.4 Context 所有権

- WorkflowContext は WorkflowEngine により生成される
- StoryEngine は受け取るのみ（生成禁止）
- Validator は読み取り専用

---

### 2.5 アクセス制約

- Manager層への直接アクセスは禁止
- context は immutable として扱う（書き換え禁止）

---

## 3. Validator Interface 定義

### 3.1 メソッドシグネチャ

def validate(self, context: WorkflowContext, target: Any) -> ValidationResult

---

### 3.2 入力対象

target は以下のいずれか

- Entity
- Node（str）
- Edge（Dict）

---

### 3.3 動作要件

- 副作用禁止
- 決定論的
- context依存のみ

---

### 3.4 Strict Return Contract（追加）

すべての Validator は必ず ValidationResult を返すこと。  
bool / dict の返却は禁止。

移行期間中は Adapter による変換を許容する。

---

## 4. ValidationResult 定義

### 4.1 プロパティ

- is_valid: bool
- severity: NWFSeverity
- error_code: str
- message: str
- violated_rules: List[str]

---

### 4.2 JSON変換

to_dict() を必須実装

---

### 4.3 Extended Fields（Implementation Binding）

以下は実装上必須とする：

- transaction_id: str  
  実行コンテキスト識別子

- stardate: float  
  検証実行時刻

- metadata: Dict[str, Any]  
  拡張情報（監査・デバッグ用）

---

### 4.4 Immutability（追加）

ValidationResult は immutable として扱う。  
すべてのフィールドは生成後変更不可とする。

---

## 5. Enum 定義

### 5.1 NWFSeverity

- INFO
- WARNING
- ERROR
- CRITICAL

---

### 5.2 NWFActionType

- STAY
- MOVE
- INTERACT
- BATTLE

---

### 5.3 EngineState

- INIT
- RUNNING
- VALIDATING
- HALTED
- COMPLETED

---

### 5.4 Severity Assignment Rule（追加）

Validator は以下の基準で severity を決定する：

- CRITICAL:
    システム整合性が破壊される場合
    （例：時間逆行、存在矛盾）

- ERROR:
    シナリオ整合性違反

- WARNING:
    許容されるが望ましくない状態

- INFO:
    情報提供

---

## 6. エラーコード体系

### 6.1 World Rule

- ERR_WR_001: GHOST_ACTIVITY_DENIED
- ERR_WR_002: TEMPORAL_INCONSISTENCY
- ERR_WR_003: LOCATION_MISMATCH

---

### 6.2 Temporal

- ERR_TM_001: STARDATE_REVERSAL

---

### 6.3 Logical

- ERR_LM_001: ENTITY_STATE_CONFLICT

---

## 7. StoryEngine 契約

### 7.1 入力

- entities: List[NWFObject]

---

### 7.2 出力

- timeline: List[Dict]

各要素:

- actor: str
- action: NWFActionType
- location: str
- stardate: float

---

### 7.3 Validator 呼び出し

- 各イベント生成後に validate 実行

---

### 7.4 制御フロー

- CRITICAL: 即時停止
- ERROR: 停止（設定依存）
- WARNING: 継続
- INFO: 無視

---

## 8. Validator Integration Adapter

### 8.1 役割

- Validator呼び出し統一
- 例外変換

---

### 8.2 Error Mapper

例外 → ValidationResult

---

### 8.3 Adapter Responsibility（追加）

Adapter は以下を行う：

- Validator結果に対して文脈情報を付与する
    - transaction_id
    - current_stardate

- 旧形式（bool / dict）を ValidationResult に変換する（移行期間のみ）

---

## 9. IntegrityChecker との関係

- Validator: 判定のみ
- IntegrityChecker: 実行制御

---

## 10. 禁止事項

- getattr による暗黙補完
- Any 型の無制限使用
- context外参照

---

## 11. 追加必須仕様

### 11.1 Entity 必須プロパティ

- id: str
- is_alive: bool
- current_location: str

---

### 11.2 ID 体系

- UUID v7 を標準
- テスト用IDは Adapterで変換

---

### 11.3 Stardate 比較

- abs(a - b) < epsilon を同一とみなす

---

## 12. 実装ブロッカー解決

- Context生成責任: WorkflowEngine
- Enum: 本仕様で固定
- ValidationResult: 本仕様準拠

---

## 13. まとめ

本契約により以下が保証される

- インターフェース不一致ゼロ
- 実装迷いゼロ
- Phase 3.4 安全実装

---

## 🔍 不足している具体ポイント（監査追記）

### ① ValidationResult の完全スキーマ不足

既存仕様では以下が未定義：

- transaction_id
- stardate
- metadata

これらは実装上必須であり、4.3 にて補完済み。

---

### ② Adapter責務の未定義

従来仕様では責務が抽象的であったため：

- 文脈付与（transaction_id / stardate）
- 旧I/F吸収

を 8.3 にて明確化。

---

### ③ validate() 戻り値の拘束力不足

旧実装（bool / dict）混在問題を解消するため：

- Strict Return Contract を追加

---

### ④ Immutability の適用範囲不足

- context のみ定義されていたため
- ValidationResult にも適用を拡張

---

### ⑤ Severity 判定基準の欠如

- Validatorごとの判断ブレを防ぐため
- 明確なルールを追加

---

## 最終結論（監査）

- 既存仕様は正しいが拘束力が不足していた
- 本追記により「実装一意性」を確保
- Phase 3.4 における I/F 不一致ゼロを達成可能

---

[EOF]