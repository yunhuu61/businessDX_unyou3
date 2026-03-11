# businessDX_unyou3-online

Google Colab 上で月次 Excel と PDF を処理するためのリポジトリ。

## ドキュメント
- 要件: `docs/requirements/colab_requirements.md`
- 実装設計: `docs/plans/colab_implementation_design.md`
- 利用手順: `docs/plans/colab_usage.md`
- タスク管理: `docs/tasks/colab_migration_tasks.md`

## 実行入口
- Colab: `notebooks/run_businessdx_colab.ipynb`
- CLI: `src/main.py`

## 備考
- Gemini API キーは必ず実行時に渡す
- `分類.csv` は Google Drive 上の固定パスを参照する前提
