Source: docs/spec/Core_Spec/NWF_Beat_Model_v2.0.0.md
Updated: 2026-03-17T07:45:00+09:00
PIC: Engineer / ChatGPT

# NWF Beat Model v2.0.0

---

## 1. 概要

Beat Model は NWF における
Scene 内部の最小ドラマ単位を定義するモデルである。

Beat はキャラクターの行動、感情変化、情報提示など
物語の小さな変化を表す。

複数の Beat が連続することで
一つの Scene が構成される。

Beat Model は Scene Model を補完し
物語の細かなドラマ構造を記述するために使用される。

---

## 2. Beat の基本概念

Beat は物語の「変化の単位」である。

Scene が出来事の単位であるのに対して
Beat は Scene 内部で発生する小さな変化を表す。

例

新しい情報が提示される  
キャラクターの感情が変化する  
行動が開始される  
対立が発生する  
決断が行われる  

これらの変化が連続することで
Scene のドラマ構造が形成される。

---

## 3. Beat と Scene の関係

Beat は Scene の内部構造を構成する。

構造

scene  
  beat_1  
  beat_2  
  beat_3  
  beat_4  

複数の Beat が順序を持って並ぶことで
Scene が形成される。

---

## 4. Beat 属性

Beat は以下の属性を持つ。

beat_id

Beat を識別する一意ID

related_scene_id

関連 Scene ID

related_thread_id

関連 Thread ID

related_character_ids

関係する Character ID のリスト

beat_order

Scene 内での順序

beat_type

Beat の種類

description

Beat の説明

emotional_delta

感情変化量

result_state

Beat 結果の状態

---

## 5. Beat 種別

Beat は役割によって分類される。

information

新しい情報が提示される

emotional

キャラクターの感情が変化する

action

キャラクターが行動する

conflict

対立が発生する

decision

キャラクターが決断する

revelation

重要な事実が明らかになる

---

## 6. Beat JSON Example

{
  "beat": {
    "beat_id": "beat_001",
    "related_scene_id": "scene_001",
    "related_thread_id": "thread_main",
    "related_character_ids": [
      "char_001"
    ],
    "beat_order": 1,
    "beat_type": "information",
    "description": "主人公が新しい手がかりを発見する",
    "emotional_delta": 0.2,
    "result_state": "investigation_started"
  }
}

---

## 7. Beat と Character

Beat はキャラクターの行動や感情変化を通じて発生する。

character  
↓  
action / emotion  
↓  
beat  

この関係により
Beat はキャラクターの内面変化を表現する。

---

## 8. Beat と物語テンポ

Beat の配置は物語のテンポを形成する。

短い Beat が連続する場合

物語のテンポは速くなる。

長い説明的 Beat が続く場合

物語のテンポは遅くなる。

Beat の配置を調整することで
Scene のリズムを制御できる。

---

## 9. 関連 Spec

NWF_Scene_Model

NWF_Character_Model

NWF_Event_Model

NWF_Thread_Graph_Model

NWF_Entity_ID_System

---

## 10. まとめ

Beat Model は Scene 内部の
最小ドラマ構造を定義する。

Beat の連続によって
Scene のドラマ構造とテンポが形成される。

本モデルは
NWF Scene Model を補完し
物語構造の詳細分析と生成を支援する。

---

[EOF]