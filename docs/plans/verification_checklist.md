# Verification Checklist

## 目的
- Colab 対応実装が要件どおりに動くか確認する
- 実運用前に最低限の確認観点を固定化する

## 事前条件
- Google Colab が利用できる
- Google Drive にアクセスできる
- `分類.csv` が `MyDrive/businessDX/setting/分類.csv` に存在する
- テスト用 Excel と PDF を用意している
- Gemini API キーを用意している

## 確認項目
### 1. セットアップ
- Notebook で依存ライブラリのインストールが完了する
- Google Drive のマウントが成功する
- `src` の import が成功する

### 2. API キー制御
- API キー未入力時に実行が止まる
- 入力した API キーで Gemini 呼び出しが行われる
- `.env` や既存環境変数がなくても動く
- `.env` が存在しても自動採用されない

### 3. 分類 CSV
- `分類.csv` を毎回アップロードしなくても実行できる
- Drive 上の固定パスから読み込める
- Drive 上の `分類.csv` を更新した場合、次回実行に反映される

### 4. 入出力
- アップロードした Excel が分析される
- アップロードした PDF が分割される
- 出力が `MyDrive/businessDX/Output/{yyyyMM}/pdfs` に保存される
- 出力が `MyDrive/businessDX/Output/{yyyyMM}/index` に保存される

### 5. ログとエラー
- 実行サマリが Colab 上に表示される
- Excel 分析エラーが出力ファイルに残る
- 入力不足時に原因が分かるメッセージが表示される

## 現時点の確認結果
- `src/app_config.py`, `src/pipeline.py`, `src/excel_analyzer.py`, `src/main.py` は構文チェック済み
- `src/debug_api.py` は構文チェック済み
- Colab 実行確認は未実施
- Gemini 実 API 呼び出し確認は未実施
- Notebook の事前入力チェックは実装済み
- Excel 出力ファイル名は入力した `yyyymm` を優先する実装に変更済み

## 次のアクション
1. Colab で Notebook を起動する
2. テスト用ファイルで一連の実行を確認する
3. 検証結果をこのファイルへ追記する
