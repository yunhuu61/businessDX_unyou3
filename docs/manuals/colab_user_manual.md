# Google Colab 実行マニュアル

## 1. このマニュアルの対象者
- IT に詳しくない人でも、月次の Excel と PDF を使って処理を実行できるようにするための手順書
- チームで共用している Google アカウントを使って実行することを前提とする

## 2. この処理で何をするのか
- 月次で受け取った PDF を 1ページずつ分割して保存する
- 月次で受け取った Excel を Gemini で分析し、業種分類などの結果を Excel にまとめる
- 入力として使う主なファイルは次の3つ
- PDF ファイル
- Excel ファイル
- `分類.csv`
- 出力される主なファイルは次の2種類
- PDF 分割結果
- Excel 分析結果

## 3. Google Colab とは何か
- Google Colab は、Google が提供しているブラウザ上で Python を動かせるツール
- パソコンに Python をインストールしなくても、ブラウザから処理を実行できる
- 今回はこのツールを使い、共用 Google アカウントで同じ手順の処理を誰でも実行できるようにしている
- 出力先は Google Drive なので、結果をそのまま共有しやすい

## 4. 事前に用意するもの
- チーム共用の Google アカウント
- 月次 Excel ファイル
- 月次 PDF ファイル
- Gemini API キー
- Google Drive 上の `分類.csv`

## 5. 使うリンク
- Google ログイン: [https://accounts.google.com/](https://accounts.google.com/)
- Google Colab: [https://colab.research.google.com/](https://colab.research.google.com/)
- 実行用 Notebook: [https://colab.research.google.com/github/yunhuu61/businessDX_unyou3/blob/main/notebooks/run_businessdx_colab.ipynb](https://colab.research.google.com/github/yunhuu61/businessDX_unyou3/blob/main/notebooks/run_businessdx_colab.ipynb)
- GitHub リポジトリ: [https://github.com/yunhuu61/businessDX_unyou3](https://github.com/yunhuu61/businessDX_unyou3)
- Google Drive: [https://drive.google.com/](https://drive.google.com/)
- Google AI Studio: [https://aistudio.google.com/](https://aistudio.google.com/)
- Gemini API キー説明ページ: [https://ai.google.dev/gemini-api/docs/api-key](https://ai.google.dev/gemini-api/docs/api-key)

## 6. 最初にやること
### 6.1 Google アカウントにログインする
1. ブラウザで [Google ログイン](https://accounts.google.com/) を開く
2. チーム共用の Google アカウントでログインする
3. ログイン後、そのまま同じブラウザで作業を続ける

### 6.2 `分類.csv` の場所を確認する
- `分類.csv` は Google Drive の次の場所に置く
- `マイドライブ / businessDX / setting / 分類.csv`

Google Drive 上の見え方:
1. [Google Drive](https://drive.google.com/) を開く
2. `マイドライブ` を開く
3. `businessDX` フォルダを開く
4. `setting` フォルダを開く
5. その中に `分類.csv` があることを確認する

## 7. `分類.csv` を変更したい場合
- `分類.csv` を変更したい場合は、Google Drive 上の次の場所にあるファイルを直接編集または差し替える
- `マイドライブ / businessDX / setting / 分類.csv`
- Notebook 実行時は毎回この場所の最新ファイルを読む
- 毎回アップロードし直す必要はない

## 8. Gemini API キーを発行する方法
### 8.1 API キーがすでにある場合
- そのキーを使う
- ただし、漏えいした可能性があるキーは使わない

### 8.2 API キーを新しく発行する場合
1. [Google AI Studio](https://aistudio.google.com/) を開く
2. 同じ Google アカウントでログインする
3. 画面内の `Get API key` または `API Keys` に進む
4. API キー一覧画面で新しいキーを作成する
5. 表示された API キーをコピーする
6. 一時的にメモしておく

補足:
- 公式説明: [Using Gemini API keys](https://ai.google.dev/gemini-api/docs/api-key)
- Notebook では API キーを毎回その場で入力する
- API キーを GitHub やファイルに保存しない

## 9. Colab で Notebook を開く方法
1. [実行用 Notebook](https://colab.research.google.com/github/yunhuu61/businessDX_unyou3/blob/main/notebooks/run_businessdx_colab.ipynb) を開く
2. 読み取り専用で開いた場合は、画面上部または右上の `ドライブにコピー` または `Copy to Drive` を押す
3. Drive にコピーされた Notebook を開く
4. 画面右上に `接続` ボタンがあれば押す

## 10. Colab で実行する手順
### 10.1 画面の見方
- 各手順ごとに灰色のコード枠がある
- その左側にある三角の再生ボタンを押すと、その枠だけ実行される
- 上から順に1つずつ実行する

### 10.2 実行する順番
1. `1. リポジトリ取得`
2. `2. 依存ライブラリのインストール`
3. `3. Google Drive をマウント`
4. `4. ライブラリ読み込み`
5. `5. 月次ファイルをアップロード`
6. `6. 実行設定を作成`
7. `7. 実行`
8. `8. 出力確認`

## 11. 各セルで何をすればよいか
### 11.1 `1. リポジトリ取得`
1. 左側の再生ボタンを押す
2. `Cloning repository...` と表示されても、そのまま待つ
3. エラーが出なければ次へ進む

### 11.2 `2. 依存ライブラリのインストール`
1. 左側の再生ボタンを押す
2. インストールが終わるまで待つ
3. エラーが出なければ次へ進む

### 11.3 `3. Google Drive をマウント`
1. 左側の再生ボタンを押す
2. Google の認証画面が出たら `このまま続行` または `許可` を押す
3. 認証コード入力欄が出る場合は、表示されたコードを貼り付ける
4. エラーが出なければ次へ進む

### 11.4 `4. ライブラリ読み込み`
1. 左側の再生ボタンを押す
2. エラーが出なければ次へ進む

### 11.5 `5. 月次ファイルをアップロード`
1. 左側の再生ボタンを押す
2. ファイル選択画面が開く
3. 当月の Excel ファイルを選ぶ
4. 当月の PDF ファイルを選ぶ
5. `開く` を押す

補足:
- Excel と PDF は一度にまとめて選んでよい

### 11.6 `6. 実行設定を作成`
このセルでは人が入力する内容がある。

入力内容:
- `Gemini API key:`
  - 発行した Gemini API キーを貼り付ける
- `Run yyyymm (example: 202603):`
  - 対象年月を6桁で入力する
  - 例: 2026年3月分なら `202603`
- `Run PDF split? [y/n]:`
  - PDF 分割をしたい場合は `y`
  - 通常は `y`
- `Run Excel analysis? [y/n]:`
  - Excel 分析をしたい場合は `y`
  - 通常は `y`

通常の回答例:
- `Gemini API key:` → 取得した API キーを貼り付ける
- `Run yyyymm:` → `202603`
- `Run PDF split? [y/n]:` → `y`
- `Run Excel analysis? [y/n]:` → `y`

画面に表示される内容:
- `Excel files: [...]`
- `PDF files: [...]`
- `Output dir: ...`
- `Classification CSV: ...`
- `Enabled steps: [...]`
- 出力される Excel の名前
- `{yyyymm}_index_DLver.xlsx`
- `{yyyymm}_index_full.xlsx`

### 11.7 `7. 実行`
1. 左側の再生ボタンを押す
2. 処理が終わるまで待つ
3. `Step: PDF split`
4. `Step: Excel analysis`
5. `OK:` や件数サマリが表示されることを確認する

### 11.8 `8. 出力確認`
1. 左側の再生ボタンを押す
2. 保存先の一覧が表示されることを確認する

## 12. 出力ファイルの保存先
- 出力は Google Drive の次の場所に保存される
- `マイドライブ / businessDX / Output / {yyyyMM} /`

保存先の例:
- `マイドライブ / businessDX / Output / 202603 / pdfs /`
- `マイドライブ / businessDX / Output / 202603 / index /`

## 13. よくある質問
### 13.1 `Classification CSV not found` と出る
- Google Drive の `マイドライブ / businessDX / setting / 分類.csv` にファイルがない
- その場所に `分類.csv` を置いてから、セル 6 を再実行する

### 13.2 `No Excel files were uploaded` と出る
- セル 5 で Excel がアップロードできていない
- セル 5 をやり直してから、セル 6 を再実行する

### 13.3 `No PDF files were uploaded` と出る
- セル 5 で PDF がアップロードできていない
- セル 5 をやり直してから、セル 6 を再実行する

### 13.4 API キー関連のエラーが出る
- API キーが間違っている
- 失効済みのキーを使っている
- 新しい API キーを発行して、セル 6 を再実行する

## 14. 実行後に確認すること
- Google Drive の出力先にファイルができているか
- PDF 分割結果が `pdfs` にあるか
- Excel 分析結果が `index` にあるか
- エラーがあれば Colab 画面の表示内容を控える

## 15. 困ったときに共有してほしい情報
- どのセルで止まったか
- 画面に出たエラーメッセージ全文
- 入力した `yyyyMM`
- `分類.csv` を置いた場所
- Excel と PDF をアップロードしたかどうか
