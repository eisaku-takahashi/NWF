# NWF Engine Order v1.0

## 1. 概要

Engine OrderはNWFにおける各Engineの実行順序を定義する。

物語構造は階層的に構築されているため、
Engineも同様に階層順で処理される必要がある。

---

## 2. Engine一覧

NWFでは以下のEngineが存在する。

ThreadEngine  
SceneEngine  
BeatEngine  
ForeshadowingEngine  
EmotionalCurveEngine

---

## 3. 実行順序

Engineは以下の順序で実行される。

1 ThreadEngine  
2 SceneEngine  
3 BeatEngine  
4 ForeshadowingEngine  
5 EmotionalCurveEngine

---

## 4. 実行理由

ThreadEngine

物語の大枠となるThread構造を解析する。

SceneEngine

Thread内部のScene構造を解析する。

BeatEngine

Scene内部のイベント構造を解析する。

ForeshadowingEngine

伏線構造を解析する。

EmotionalCurveEngine

物語の感情曲線を解析する。

---

## 5. Engine依存関係

Engineは以下の依存関係を持つ。

SceneEngineはThreadEngineに依存する。

BeatEngineはSceneEngineに依存する。

ForeshadowingEngineはScene情報を参照する。

EmotionalCurveEngineはSceneおよびBeat情報を参照する。

---

## 6. 将来拡張

将来追加可能なEngine例。

CharacterArcEngine  
DialogueEngine  
ThemeAnalysisEngine

---

## 7. Version

v1.0