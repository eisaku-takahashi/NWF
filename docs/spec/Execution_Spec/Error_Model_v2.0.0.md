Source: docs/spec/Execution_Spec/Error_Model_v2.0.0.md
Updated: 2026-03-18T23:45:00+09:00
PIC: Engineer / ChatGPT

# NWF Error Model v2.0.0

---

## 1. 概要

Error Model は NWF におけるエラーの分類および処理方法を定義する。

多層構造データの整合性を維持するため、エラーの体系的管理を行う。

---

## 2. 目的

Error Model の目的は以下である。

- エラー分類の標準化  
- 問題の早期検出  
- Validation System との統合  
- 修正プロセスの明確化  

---

## 3. エラー分類

NWF では以下のエラータイプを定義する。

- structure_error  
- reference_error  
- validation_error  
- narrative_error  

---

## 4. Structure Error

データ構造が仕様に違反している場合に発生する。

例：

- Scene が Thread に属していない  
- Beat が Scene に属していない  
- 階層構造の破綻  

---

## 5. Reference Error

参照先データが存在しない場合に発生する。

例：

- 存在しない character_id  
- 存在しない scene_id  
- 無効な参照  

---

## 6. Validation Error

Validation System によって検出される整合性エラー。

例：

- 未回収の伏線  
- 感情曲線の不整合  
- データ欠損  

---

## 7. Narrative Error

物語構造として問題がある場合に発生する。

例：

- 論理矛盾  
- キャラクター動機の破綻  
- 不自然なプロット  

---

## 8. エラーレベル

各エラーには重要度レベルを設定する。

- critical  
  実行不能レベル  

- warning  
  実行可能だが問題あり  

- info  
  改善推奨  

---

## 9. エラーコード

各エラーには識別用の error_code を付与する。

例：

- structure_error_001  
- reference_error_001  
- validation_error_001  
- narrative_error_001  

error_code は一意である必要がある。

---

## 10. エラー処理

エラーは以下の方法で処理される。

- Engine ログ出力  
- Validation レポート生成  
- AI による修正提案  

critical エラーは Pipeline の停止条件とする。

---

## 11. Validation System連携

Error Model は Validation System と連携する。

- Validation によりエラー検出  
- Error Model により分類  
- Engine および AI により修正  

---

## 12. 実行フロー内の扱い

エラーは Execution Pipeline の各段階で処理される。

- 入力段階：structure_error / reference_error  
- 中間段階：validation_error  
- 出力段階：narrative_error  

---

## 13. まとめ

Error Model は NWF の品質と安定性を支える基盤である。

本モデルにより、エラーの体系的管理と継続的改善が可能となる。

---

[EOF]