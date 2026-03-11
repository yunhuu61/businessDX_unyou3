# Google Colab 実行マニュアル

## 1. このマニュアルの対象者
- IT に詳しくない人でも、月次の Excel と PDF を使って処理を実行できるようにするための手順書
- チームで共用している Google アカウントを使って実行することを前提とする

## 2. 事前に用意するもの
- チーム共用の Google アカウント
- 月次 Excel ファイル
- 月次 PDF ファイル
- Gemini API キー
- Google Drive 上の `分類.csv`

## 3. 使うリンク
- Google ログイン: [https://accounts.google.com/](https://accounts.google.com/)
- Google Colab: [https://colab.research.google.com/](https://colab.research.google.com/)
- 実行用 Notebook: [https://colab.research.google.com/github/yunhuu61/businessDX_unyou3/blob/main/notebooks/run_businessdx_colab.ipynb](https://colab.research.google.com/github/yunhuu61/businessDX_unyou3/blob/main/notebooks/run_businessdx_colab.ipynb)
- GitHub リポジトリ: [https://github.com/yunhuu61/businessDX_unyou3](https://github.com/yunhuu61/businessDX_unyou3)
- Google AI Studio: [https://aistudio.google.com/](https://aistudio.google.com/)
- Gemini API キー説明ページ: [https://ai.google.dev/gemini-api/docs/api-key](https://ai.google.dev/gemini-api/docs/api-key)

## 4. 最初にやること
### 4.1 Google アカウントにログインする
1. ブラウザで [Google ログイン](https://accounts.google.com/) を開く
2. チーム共用の Google アカウントでログインする
3. ログイン後、そのまま同じブラウザで作業を続ける

### 4.2 `分類.csv` の場所を確認する
- `分類.csv` は Google Drive の次の場所に置く
- `マイドライブ / businessDX / setting / 分類.csv`

Google Drive 上の見え方:
1. [Google Drive](https://drive.google.com/) を開く
2. `マイドライブ` を開く
3. `businessDX` フォルダを開く
4. `setting` フォルダを開く
5. その中に `分類.csv` があることを確認する

## 5. `分類.csv` を変更したい場合
- `分類.csv` を変更したい場合は、Google Drive 上の次の場所にあるファイルを直接編集または差し替える
- `マイドライブ / businessDX / setting / 分類.csv`
- Notebook 実行時は毎回この場所の最新ファイルを読む
- 毎回アップロードし直す必要はない

## 6. Gemini API キーを発行する方法
### 6.1 API キーがすでにある場合
- そのキーを使う
- ただし、漏えいした可能性があるキーは使わない

### 6.2 API キーを新しく発行する場合
1. [Google AI Studio](https://aistudio.google.com/) を開く
2. 同じ Google アカウントでログインする
3. 画面内の `Get API key` または `API Keys` に進む
4. API キー一覧画面で新しいキーを作成する
5. 表示された API キーをコピーする
6. メモ帳など一時的な場所に控える

補足:
- Google 公式の API キー説明: [Using Gemini API keys](https://ai.google.dev/gemini-api/docs/api-key)
- Google 公式の AI Studio: [Google AI Studio](https://aistudio.google.com/)
- Notebook では API キーを毎回その場で入力する
- API キーを GitHub やファイルに保存しない

## 7. Colab で Notebook を開く方法
1. [実行用 Notebook](https://colab.research.google.com/github/yunhuu61/businessDX_unyou3/blob/main/notebooks/run_businessdx_colab.ipynb) を開く
2. 読み取り専用で開いた場合は、画面上部または右上の `ドライブにコピー` または `Copy to Drive` を押す
3. 自分の Drive にコピーされた Notebook を開く
4. 画面右上に `接続` ボタンがあれば押す

## 8. Colab で実行する手順
### 8.1 画面の見方
- 各手順ごとに灰色のコード枠がある
- その左側にある三角の再生ボタンを押すと、その枠だけ実行される
- 上から順に 1 つずつ実行する

### 8.2 実行する順番
1. `1. リポジトリ取得`
2. `2. 依存ライブラリのインストール`
3. `3. Google Drive をマウント`
4. `4. ライブラリ読み込み`
5. `5. 月次ファイルをアップロード`
6. `6. 実行設定を作成`
7. `7. 実行`
8. `8. 出力確認`

## 9. 各セルで何をすればよいか
### 9.1 `1. リポジトリ取得`
やること:
1. 左側の再生ボタンを押す
2. `Cloning repository...` と表示されても、そのまま待つ
3. エラーが出なければ次へ進む

### 9.2 `2. 依存ライブラリのインストール`
やること:
1. 左側の再生ボタンを押す
2. ライブラリのインストールが終わるまで待つ
3. エラーが出なければ次へ進む

### 9.3 `3. Google Drive をマウント`
やること:
1. 左側の再生ボタンを押す
2. Google の認証画面が出たら `このまま続行` または `許可` を押す
3. Colab に認証コード入力欄が出る場合は、表示されたコードを貼り付ける
4. エラーが出なければ次へ進む

### 9.4 `4. ライブラリ読み込み`
やること:
1. 左側の再生ボタンを押す
2. 何もエラーが出なければ次へ進む

### 9.5 `5. 月次ファイルをアップロード`
やること:
1. 左側の再生ボタンを押す
2. ファイル選択画面が開く
3. 当月の Excel ファイルを選ぶ
4. 当月の PDF ファイルを選ぶ
5. `開く` を押す

補足:
- Excel と PDF は一度にまとめて選んでよい
- アップロードが終わったら次へ進む

### 9.6 `6. 実行設定を作成`
このセルでは人が入力する内容がある。

入力内容:
- `Gemini API key:`
  - ここには発行した Gemini API キーを貼り付ける
- `Run yyyymm (example: 202603):`
  - ここには対象年月を 6 桁で入力する
  - 例: 2026年3月分なら `202603`
- `Run PDF split? [y/n]:`
  - PDF 分割をしたい場合は `y`
  - PDF 分割をしない場合は `n`
  - 通常は `y`
- `Run Excel analysis? [y/n]:`
  - Excel 分析をしたい場合は `y`
  - Excel 分析をしない場合は `n`
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

これらが表示されれば次へ進める

### 9.7 `7. 実行`
やること:
1. 左側の再生ボタンを押す
2. 処理が終わるまで待つ
3. `Step: PDF split`
4. `Step: Excel analysis`
5. `OK:` や件数サマリが表示されることを確認する

### 9.8 `8. 出力確認`
やること:
1. 左側の再生ボタンを押す
2. 保存先の一覧が表示されることを確認する

## 10. 出力ファイルの保存先
- 出力は Google Drive の次の場所に保存される
- `マイドライブ / businessDX / Output / {yyyyMM} /`

保存先の例:
- `マイドライブ / businessDX / Output / 202603 / pdfs /`
- `マイドライブ / businessDX / Output / 202603 / index /`

## 11. よくある質問
### 11.1 `Classification CSV not found` と出る
- Google Drive の `マイドライブ / businessDX / setting / 分類.csv` にファイルがない
- その場所に `分類.csv` を置いてから、セル 6 を再実行する

### 11.2 `No Excel files were uploaded` と出る
- セル 5 で Excel がアップロードできていない
- セル 5 をやり直してから、セル 6 を再実行する

### 11.3 `No PDF files were uploaded` と出る
- セル 5 で PDF がアップロードできていない
- セル 5 をやり直してから、セル 6 を再実行する

### 11.4 API キー関連のエラーが出る
- API キーが間違っている
- 失効済みのキーを使っている
- 新しい API キーを発行して、セル 6 を再実行する

## 12. 実行後に確認すること
- Google Drive の出力先にファイルができているか
- PDF 分割結果が `pdfs` にあるか
- Excel 分析結果が `index` にあるか
- エラーがあれば Colab 画面の表示内容を控える

## 13. 困ったときに共有してほしい情報
- どのセルで止まったか
- 画面に出たエラーメッセージ全文
- 入力した `yyyyMM`
- `分類.csv` を置いた場所
- Excel と PDF をアップロードしたかどうか
