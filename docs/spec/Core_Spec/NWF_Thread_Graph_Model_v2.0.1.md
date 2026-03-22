Source: docs/spec/Core_Spec/NWF_Thread_Graph_Model_v2.0.1.md
Updated: 2026-03-22T15:04:00+09:00
PIC: Engineer / ChatGPT

# NWF Thread Graph Model v2.0.1

---

## Validation Result

### 1. Terminology Issues
Thread / Scene / Event / Timeline / Graph / Node / Edge の用語を Glossary v2.0.1 に統一した。
「ドラマライン」などの説明用語は定義語として使用しない。

### 2. ID / Reference Issues
Entity ID System v2.0.1 に従い以下の Prefix を使用する。
thread_id
event_id
scene_id
link_id
timeline_id

### 3. Data Structure Issues
Thread Graph は Graph-Document Hybrid 構造として保存される。
nodes と edges を分離した JSON Graph Schema を採用する。

### 4. Graph Structure Issues
Thread を Node、Thread 間関係を Edge として定義。
Edge には dependency / parallel / trigger / merge を定義可能。

### 5. Dependency Issues
Thread の依存関係を Pre-requisite Thread として定義し、
依存 Thread が resolved 状態になるまで進行不可とする。

### 6. Missing Fields / Concepts
以下の概念を追加した。
nodes
edges
edge_type
branch_condition
trigger_event_id
dependency_type
graph_id

### 7. Required Changes for v2.0.1
Thread Graph を単なる関係図から Graph Database モデルへ拡張。
Edge に条件・イベント・依存情報を保持可能に変更。

### 8. Updated Model Proposal (v2.0.1)
Thread Graph は物語の因果構造を表す Graph Database 構造とする。
Story Structure = Thread Graph
Time Structure = Scene Timeline

### 9. Updated Graph Schema Example (JSON)
下記参照。

### 10. Core Architecture Consistency
World Rule
State
Event
Conflict
Thread Graph
Timeline
Story Engine
の Core Architecture と整合。

### 11. Narrative Logic Mapping
Story = Thread Graph + Scene Timeline
を Graph + Timeline の二層構造として定義。

### 12. Graph Database Integration
Thread Graph は Graph Database として保存可能。
Node = Thread
Edge = Thread Relationship

### 13. Summary
Thread Graph Model は
物語の因果構造を表す Graph Database Model である。

---

## 1. 概要

Thread Graph Model は
Thread 間の関係構造を Graph として管理するモデルである。

Thread Graph は物語の因果構造を表す。

Story Structure = Thread Graph
Time Structure = Scene Timeline

---

## 2. Thread Graph の基本概念

Thread Graph は Graph 構造で表現される。

Graph は以下の要素で構成される。

Node
Thread を表す。

Edge
Thread 間の関係を表す。

---

## 3. Thread Node 定義

Thread Node は以下の情報を持つ。

thread_id
title
thread_type
related_character_ids
start_scene_id
end_scene_id
current_state_id
timeline_id

---

## 4. Thread Edge 定義

Thread Edge は Thread 間の関係を表す。

Edge は以下の属性を持つ。

link_id
source_thread_id
target_thread_id
edge_type
branch_condition
trigger_event_id
dependency_type

---

## 5. Edge Type

Thread 関係タイプは以下とする。

dependency
ある Thread が別 Thread に依存する

parallel
Thread が並行進行する

trigger
ある Thread が別 Thread を開始させる

merge
Thread が別 Thread に統合される

branch
Thread が分岐する

---

## 6. Dependency Management

dependency Edge の場合、
source_thread が resolved になるまで
target_thread は active にならない。

これにより物語の論理整合性を保つ。

---

## 7. Thread Graph JSON Schema

例

{
  "thread_graph": {
    "graph_id": "graph_story_main",
    "nodes": [
      {
        "thread_id": "thread_main_001",
        "title": "Main Plot",
        "thread_type": "main_plot",
        "timeline_id": "timeline_main"
      },
      {
        "thread_id": "thread_sub_001",
        "title": "Sub Plot",
        "thread_type": "sub_plot",
        "timeline_id": "timeline_main"
      }
    ],
    "edges": [
      {
        "link_id": "link_001",
        "source_thread_id": "thread_sub_001",
        "target_thread_id": "thread_main_001",
        "edge_type": "merge",
        "branch_condition": null,
        "trigger_event_id": null,
        "dependency_type": null
      }
    ]
  }
}

---

## 8. Thread Graph と Scene Timeline

NWF では物語は次の二層構造になる。

Story Structure = Thread Graph
Time Structure = Scene Timeline

Thread Graph は因果構造
Scene Timeline は時間構造
を表す。

---

## 9. NWF Engine との関係

Thread Graph は以下の Engine によって使用される。

Thread Engine
Story Engine
State Transition Engine
Timeline Engine

Thread Graph は物語構造の基盤データとして使用される。

---

## 10. NWF Core Architecture における位置

NWF Core Architecture は次の構造を持つ。

World Rule Layer
State System Layer
Event / Conflict Layer
Thread Graph Layer
Scene Timeline Layer
Story Engine Layer

Thread Graph は物語構造層に位置する。

---

## 11. まとめ

Thread Graph Model v2.0.1 は
Thread 間の関係を Graph Database として管理するモデルである。

Node = Thread
Edge = Thread Relationship

Thread Graph は物語の因果構造を表し、
Scene Timeline は物語の時間構造を表す。

Story = Thread Graph + Scene Timeline

この構造により
複雑な物語構造
分岐物語
並行物語
伏線構造
因果構造
を体系的に管理できる。

---

[EOF]