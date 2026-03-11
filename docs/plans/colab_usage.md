# Colab Usage

## 前提
- Google Colab を使えること
- Google Drive へアクセスできること
- `分類.csv` が `MyDrive/businessDX_unyou/setting/分類.csv` に配置されていること
- 月次 Excel と PDF を手元に持っていること
- Gemini API キーを持っていること

## 実行手順
1. リポジトリを Colab から使える場所に配置する
2. `notebooks/run_businessdx_colab.ipynb` を開く
3. 必要なら Notebook 冒頭のリポジトリ取得セルで配置先をそろえる
4. 依存ライブラリをインストールする
5. Google Drive をマウントする
6. 月次 Excel と PDF をアップロードする
7. 実行時の Gemini API キーを入力する
8. 実行対象の `yyyyMM` を入力する
9. 実行対象を `PDF split` / `Excel analysis` から選ぶ
10. パイプラインを実行する
11. 結果を Google Drive の `MyDrive/businessDX/output/{yyyyMM}` で確認する

## 補足
- API キーは Notebook や `.env` には保存しない
- `分類.csv` は毎回アップロードしない
- 出力は `pdfs/` と `index/` に分かれて保存される
- Notebook は入力不足のとき実行前に停止する
