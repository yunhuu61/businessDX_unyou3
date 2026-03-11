# Local Validation

## 目的
- Colab 実行前に、ローカルで最低限の整合性確認を行う
- 実 API を叩かなくても確認できる範囲を固定する

## 実施内容
1. Python ファイルの構文チェック
2. `.env` / `GOOGLE_API_KEY` 依存が `src` 配下に残っていないことの確認
3. ドキュメントとノートブックの配置確認

## 現在の結果
- `src/app_config.py` 構文チェック: OK
- `src/pipeline.py` 構文チェック: OK
- `src/excel_analyzer.py` 構文チェック: OK
- `src/main.py` 構文チェック: OK
- `src/debug_api.py` 構文チェック: OK
- `src` 配下の `.env` / `GOOGLE_API_KEY` / `getenv` 依存: なし

## 未確認
- Colab 上での実行
- Google Drive への出力
- Gemini API の実呼び出し
