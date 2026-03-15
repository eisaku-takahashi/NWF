# NWF Story JSON Structure v1.0

## 1. 概要

Storyは物語全体を表す最上位データである。

Storyは以下の情報を保持する。

- 作品メタデータ
- Thread一覧
- Character一覧
- World設定
- Foreshadowing一覧
- EmotionalCurve

---

## 2. Story基本構造

Storyは以下の要素で構成される。

id  
title  
author  
genre  
summary

---

## 3. Thread参照

Storyは複数のThreadを持つ。

Threadは物語のプロットラインを表す。

例

- 主人公の成長
- ミステリーの謎
- 恋愛関係

---

## 4. Character参照

StoryはCharacter一覧を持つ。

Characterは物語に登場する人物を定義する。

---

## 5. World参照

Worldは世界設定を表す。

例

- 歴史
- 科学技術
- 社会制度
- 魔法体系

---

## 6. Foreshadowing参照

Storyは伏線を管理する。

伏線は以下を記録する。

- 設置
- 回収
- 関連Scene

---

## 7. EmotionalCurve

物語全体の感情曲線を定義する。

---

## 8. Version

v1.0