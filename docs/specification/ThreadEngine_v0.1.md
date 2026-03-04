# NWF ThreadEngine 仕様書 v0.1

---

## 1. 目的

ThreadEngine は、物語内に存在する **スレッド（伏線・テーマ・未解決の問い）** を管理し、物語構造の整合性を検証するための仕組みである。

### 主な目的

- 未回収スレッドの検出
- 物語完成度の定量化
- 構造的一貫性の検証
- CI環境への統合を可能にする検証基盤の提供

---

## 2. ディレクトリ構造

projects/<project_name>/
  ThreadEngine/
    threads_master.json

各プロジェクトは ThreadEngine ディレクトリを持ち、そこにスレッド定義ファイルを配置する。

---

## 3. threads_master.json 仕様

### 3.1 ルート構造

{
  "project": "string",
  "version": "string",
  "threads": []
}

### 必須フィールド

- **project**（string）
- **version**（string）
- **threads**（list）

---

## 4. thread オブジェクト仕様

{
  "id": "string",
  "title": "string",
  "description": "string",
  "type": "string",
  "status": "string"
}

### 必須フィールド

- **id**（string）
- **status**（string）

※ title / description / type は将来的に必須化する可能性がある。

---

## 5. 許可されるステータス値（enum）

- open
- resolved
- partially_resolved
- abandoned
- thematic

---

## 6. ステータスの意味定義

### open
未解決。未回収扱い。strictモードでは ERROR。

### partially_resolved
部分解決。未回収扱い。strictモードでは ERROR。

### resolved
完全解決。未回収扱いしない。strictモードでは OK。

### thematic
哲学的・意図的継続。未回収扱いしない。strictモードでは OK。

### abandoned
意図的放棄。未回収扱い。strictモードでは ERROR。

---

## 7. 未回収率の定義

未回収とみなすステータス：

- open
- partially_resolved
- abandoned

### 計算式

unresolved_count / total_threads

### 出力例

Unresolved: 2 / 5 (40%)

---

## 8. validate コマンドの挙動

### 通常モード

- JSON構造エラー → ERROR
- 未回収スレッドあり → WARNING
- 全て resolved または thematic → OK

### strict モード

コマンド：

nwf validate --strict

挙動：

- 未回収スレッドが1つでもあれば → ERROR
- abandoned が存在すれば → ERROR
- EmotionalCurve が未定義または空 → ERROR

---

## 9. 設計思想

ThreadEngine は創作の自由を制限するためのものではない。

構造を可視化し、物語の完成度を定量化するための補助エンジンである。

thematic ステータスを許可することで、文学的な余韻や哲学的未解決を排除しない設計とする。

ThreadEngine は文学と工学を橋渡しする試みである。