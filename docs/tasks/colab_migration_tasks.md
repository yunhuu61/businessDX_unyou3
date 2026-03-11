# Colab Migration Tasks

## 運用ルール
- `Status` は `todo`, `doing`, `done`, `blocked` を使う
- 着手順は上から優先する
- 実装中に増えた作業もこのファイルへ追記する

## タスク一覧
| ID | Status | Task | Output |
|---|---|---|---|
| T001 | done | 開発ドキュメントの格納先を `docs` 配下に整理する | `docs/README.md` |
| T002 | done | Colab 対応要件を Markdown に整理する | `docs/requirements/colab_requirements.md` |
| T003 | done | 方針・判断を残す決定ログを用意する | `docs/plans/decision_log.md` |
| T004 | done | 現行コードの構成を整理し、Colab 化に必要な改修点を設計へ落とす | `docs/plans/colab_implementation_design.md` |
| T005 | done | API キーの取得方法を `.env` 依存から実行時引数へ変更する設計を決める | `docs/plans/colab_implementation_design.md` |
| T006 | done | `分類.csv` の固定参照パス方式をコードへ反映する設計を決める | `docs/plans/colab_implementation_design.md` |
| T007 | done | Google Drive 入出力の扱いを決め、出力フォルダ規約を確定する | `docs/plans/colab_implementation_design.md` |
| T008 | done | Colab 用の実行入口ノートブック構成を決める | `docs/plans/colab_implementation_design.md` |
| T009 | done | Python 側の設定オブジェクトまたは設定関数を追加する | `src/app_config.py`, `src/pipeline.py` |
| T010 | done | Excel 分析処理を実行時 API キー前提へ改修する | `src/excel_analyzer.py` |
| T011 | done | PDF 分割処理を Colab/Drive 前提の入出力で扱えるようにする | `src/pipeline.py` |
| T012 | done | Colab ノートブックを追加する | `notebooks/run_businessdx_colab.ipynb` |
| T013 | done | 利用手順ドキュメントを追加する | `docs/plans/colab_usage.md` |
| T014 | doing | 動作確認手順を整理し、受け入れ条件に沿って検証する | `docs/plans/verification_checklist.md` |
| T015 | done | Colab Notebook の入力チェックと実行導線を補強する | `notebooks/run_businessdx_colab.ipynb` |

## 直近の実施順
1. T009 Python 側の設定オブジェクトまたは設定関数を追加する
2. T010 Excel 分析処理を実行時 API キー前提へ改修する
3. T011 PDF 分割処理を Colab/Drive 前提の入出力で扱えるようにする
4. T012 Colab ノートブックを追加する
5. T013 利用手順ドキュメントを追加する
6. T014 受け入れ条件に沿って検証する

## メモ
- 要件の確定内容が変わったら、先に `docs/requirements/` と `docs/plans/decision_log.md` を更新する
- 実装順は依存関係を優先し、UI 的な入口より先に Python 側の設定注入を整理する
