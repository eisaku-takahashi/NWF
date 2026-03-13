# NWF File System v1.0.1

## 概要

本ドキュメントは NWF におけるファイルシステム構造を定義する。

NWFは物語データを構造化されたディレクトリとして管理する。

## NWF Project Root

すべてのNWFプロジェクトは NWF Project Root を基準として構成される。

Specでは以下の表記を使用する。

NWF Project Root

または

<project_root>/

すべてのディレクトリおよびファイルパスはこのルートからの相対パスとして定義される。

## 基本ディレクトリ構造

<project_root>/

docs/
spec/

stories/

nwf/

examples/

tests/

## Story Database

物語データは stories ディレクトリ内に保存される。

stories/

各ストーリーは独立したディレクトリとして管理される。

stories/<story_id>/

story.json  
threads/  
scenes/  
beats/  
characters/  
world/  
foreshadowing/  
emotional_curve/

## Path Convention

すべての Spec 内のパスは以下のルールに従う。

- ルートは NWF Project Root
- 相対パスで記述
- OS依存の絶対パスは使用しない

## Version

Version: v1.0.1