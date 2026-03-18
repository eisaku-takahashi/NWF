Source: docs/spec/Execution_Spec/Engine_Order_v2.0.0.md
Updated: 2026-03-18T22:00:00+09:00
PIC: Engineer / ChatGPT

# NWF Engine Order v2.0.0

---

## 1. 概要

Engine Order は NWF における各 Engine の実行順序を定義する。

物語構造は階層的に構築されているため、Engine も同様に階層構造および依存関係に基づいて実行される必要がある。

本仕様は Execution Pipeline と整合する形で Engine の実行順序を標準化する。

---

## 2. Engine一覧

NWF では以下の Engine が存在する。

- ThreadEngine  
- SceneEngine  
- BeatEngine  
- ForeshadowingEngine  
- EmotionalCurveEngine  

---

## 3. 実行順序

Engine は以下の順序で実行される。

1. ThreadEngine  
2. SceneEngine  
3. BeatEngine  
4. ForeshadowingEngine  
5. EmotionalCurveEngine  

この順序はデータ依存関係に基づく必須実行順序である。

---

## 4. 各Engineの役割

- ThreadEngine  
  物語全体の構造単位である Thread を解析し、上位構造を確定する。

- SceneEngine  
  Thread 内の Scene 構造を解析し、シーン単位の構造を定義する。

- BeatEngine  
  Scene 内のイベント単位（Beat）を解析し、詳細な進行構造を定義する。

- ForeshadowingEngine  
  伏線の配置・回収・整合性を解析する。

- EmotionalCurveEngine  
  Scene および Beat を基に物語全体の感情曲線を解析する。

---

## 5. Engine依存関係

各 Engine の依存関係は以下の通りである。

- SceneEngine は ThreadEngine に依存する  
- BeatEngine は SceneEngine に依存する  
- ForeshadowingEngine は SceneEngine および BeatEngine に依存する  
- EmotionalCurveEngine は SceneEngine および BeatEngine に依存する  

依存関係を満たさない状態での実行は禁止される。

---

## 6. 実行ルール

Engine 実行は以下のルールに従う。

- 上位構造から下位構造へ順次処理する  
- 必要な入力データが揃っていない場合は実行不可  
- 各 Engine は独立したモジュールとして動作する  
- 再実行時は依存関係に基づき再計算を行う  

---

## 7. 将来拡張

将来追加可能な Engine 例。

- character_arc_engine  
- dialogue_engine  
- theme_analysis_engine  

新規 Engine は既存の依存関係モデルに適合する必要がある。

---

## 8. まとめ

Engine Order は NWF の処理順序の中核であり、Execution Pipeline の正確な動作を保証する。

階層構造と依存関係に基づく実行により、整合性のある物語解析が実現される。

---

[EOF]