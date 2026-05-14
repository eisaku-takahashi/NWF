Source: docs/spec/Execution_Spec/NWF_Mock_Design_Guideline_v2.0.1.md
Updated: 2026-05-03T10:09:00+09:00
PIC: Engineer / ChatGPT

# NWF Mock Design Guideline v2.0.1

---

## 1. 概要

本ドキュメントは、NWF v2.0.1 におけるテスト用 Mock（モックオブジェクト）の設計規約を定義する。

目的：

- プロダクションコードとのI/F整合性の保証
- テストの信頼性・再現性の確保
- Mockによる実装ブレの排除
- Spec Driven Development における検証精度の向上

---

## 2. 基本原則（Core Principles）

### 2.1 I/F完全準拠（Interface Compliance）

Mockは必ずプロダクションI/Fに完全準拠しなければならない。

禁止事項：

- 内部構造への直接アクセスを前提とする設計
- プロダクションに存在しないメソッドの定義
- プロダクションI/Fを省略した簡易実装

必須条件：

- プロダクションコードが呼び出すメソッドを正確に再現する
- メソッドシグネチャ（引数・戻り値）を一致させる

---

### 2.2 アクセス制御（Encapsulation Enforcement）

Mockは内部データ構造を外部に公開してはならない。

理由：

- I/F経由アクセスを強制するため
- 実装依存のテストを防止するため

禁止事項：

- 辞書やリストへの直接アクセス（例: mock.data["id"]）
- 内部属性の外部公開

---

### 2.3 単一責務（Single Responsibility）

Mockは特定のI/Fの振る舞いを再現することのみに責務を限定する。

例：

- StoryDB Mock → `get(entity_id)` のみ提供
- Logger Mock → `log(level, message)` のみ提供

不要な機能は実装しない。

---

## 3. StoryDB Mock 設計規約

### 3.1 必須I/F

StoryDBのMockは以下のI/Fのみを提供する：

get(entity_id: str) -> Optional[Entity]

仕様：

- entity_id は必ず str として扱う
- 存在しない場合は None を返す
- 内部データ構造は外部から不可視とする

---

### 3.2 標準実装テンプレート

class MockStoryDB:
    def __init__(self, data: dict):
        # 内部データ（外部非公開）
        self._data = data

    def get(self, entity_id: str):
        # ID正規化（Spec準拠）
        return self._data.get(str(entity_id))

---

### 3.3 禁止パターン（アンチパターン）

以下の実装は禁止する：

1. get_previous_state の使用

理由：
- ValidatorはこのI/Fを使用しない
- レイヤー責務違反（Engine層の機能混入）

例（禁止）：

def get_previous_state(self, transaction_id):
    return {...}

---

2. 内部辞書の直接公開

例（禁止）：

self.data = data

理由：
- テストがI/Fではなく実装に依存する

---

3. ID型未正規化

例（禁止）：

return self._data.get(entity_id)

理由：
- UUID / str 混在による取得失敗を引き起こす

---

## 4. Validatorとの契約（Contract）

### 4.1 データ取得責務

- current（現在値）：
  - context.global_vars または target

- previous（過去値）：
  - story_db.get(entity_id)

この責務分離を破ってはならない。

---

### 4.2 レイヤー分離原則

| レイヤー | 責務 |
|----------|------|
| Context | 実行中の一時状態 |
| DB | 永続化された過去状態 |
| Validator | 整合性検証 |

MockはDBレイヤーとして振る舞う必要がある。

---

## 5. テスト安定性要件

Mockは以下を満たす必要がある：

- 完全決定論的であること（同一入力 → 同一出力）
- 副作用が存在しないこと
- 外部状態に依存しないこと

---

## 6. Spec Driven Development との関係

Mock設計は以下に従う：

- Core Spec
- Data Spec
- Execution Spec
- Validator Contract Spec

Specに存在しないI/FはMockにも実装してはならない。

---

## 7. DoD（Definition of Done）

Mock実装が完了したとみなされる条件：

- プロダクションI/Fと100%一致している
- Validatorから正常にデータ取得が可能
- `previous is None` が意図しない形で発生しない
- テストが安定して再現可能
- I/F以外のアクセス手段が存在しない

---

## 8. まとめ

本ガイドラインは以下を保証する：

- Mockとプロダクションの完全整合
- テストの信頼性向上
- I/F断絶の完全排除
- Spec Driven Development の徹底

Mockは「簡易実装」ではなく「I/Fの忠実な再現」である。

---

[EOF]