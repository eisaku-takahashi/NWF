# NWF Thread JSON Structure v1.0

## 1. 概要

Threadは物語のプロットラインを表すデータである。

Threadは複数のSceneで構成される。

---

## 2. Threadの役割

Threadは以下を表現する。

- 物語のテーマ
- キャラクターの成長
- 謎の解決
- 事件の進行

---

## 3. Thread基本情報

Threadは以下の属性を持つ。

id  
title  
description  
theme

---

## 4. Scene構造

Threadは複数のSceneを持つ。

Sceneは物語の具体的な出来事を表す。

---

## 5. Threadタイプ

Threadは以下のタイプを持つことができる。

MainThread  
SubThread  
CharacterThread  
MysteryThread

---

## 6. Thread関係

Thread同士は以下の関係を持つ。

dependency  
parallel  
conflict

---

## 7. Version

v1.0