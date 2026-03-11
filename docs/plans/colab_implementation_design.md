# Colab Implementation Design

## 1. 目的
- 既存のローカル実行プログラムを Google Colab 上で誰でも実行できる構成に変更する。
- 既存の業務ロジックは極力維持し、設定・入出力・実行入口のみを再設計する。

## 2. 設計方針
- コア処理と実行環境依存処理を分離する。
- API キーは必ず実行時入力値を使い、`.env` や既存環境変数には依存しない。
- `分類.csv` は Google Drive 上の固定パスから毎回読み込む。
- 出力は Google Drive 配下へ保存する。
- Google Colab は正式な実行入口とし、利用者は Notebook 上の手順だけで実行できるようにする。

## 3. 現行コードの整理
### 3.1 現行の責務
- `src/main.py`
  - CLI 引数を受けて PDF 分割と Excel 分析を呼び出す
- `src/pdf_splitter.py`
  - `input` 配下の PDF を分割し `output/pdfs` に保存する
- `src/excel_analyzer.py`
  - `input` 配下の Excel と `分類.csv` を読み込み、Gemini で分析して `output/index` に保存する

### 3.2 現行の問題点
- `src/excel_analyzer.py` が `.env` と `GOOGLE_API_KEY` に依存している
- `分類.csv` を `input` に都度置く前提になっている
- Colab 実行時に必要な Google Drive マウント、ファイル投入、保存先制御の入口がない
- 設定値がファイルパス文字列として散在しており、差し替えに弱い

## 4. 目標構成
### 4.1 役割分割
- Python コア処理
  - 分析・分割そのものを担当する
- 実行設定
  - API キー、入力先、出力先、`分類.csv` 参照先、実行モードをまとめる
- Colab Notebook
  - Drive マウント、入力受け付け、実行、結果表示を担当する

### 4.2 想定ファイル
- `src/app_config.py`
  - 実行設定を定義する
- `src/pipeline.py`
  - PDF 分割、Excel 分析をまとめて呼び出す共通入口
- `notebooks/run_businessdx_colab.ipynb`
  - Colab 用ノートブック
- `docs/plans/colab_implementation_design.md`
  - 本設計書

## 5. 改修設計
### 5.1 設定の集約
- 新規に設定オブジェクトを追加する
- ここで以下を一元管理する
  - `input_dir`
  - `output_dir`
  - `classification_csv_path`
  - `gemini_api_key`
  - `run_pdf`
  - `run_excel`
  - `model_name`

### 5.2 API キー制御
- `excel_analyzer.run()` は `api_key` を必須引数で受け取る
- `.env` の読込処理は削除する
- `os.getenv("GOOGLE_API_KEY")` は使わない
- `genai.Client(api_key=api_key)` は実行時に受け取った値だけで初期化する
- API キー未指定時は即時エラーにする

### 5.3 `分類.csv` 参照方式
- `excel_analyzer.run()` は `classification_csv_path` を必須引数で受け取る
- `input/分類.csv` 固定参照をやめる
- Colab 実行時は Google Drive 上の固定パスを渡す
- 毎回そのパスの最新ファイルを読み込む

### 5.4 入力ファイルの扱い
- Excel と PDF は Colab 上で利用者がアップロードする
- アップロード後、Colab セッションの一時ディレクトリへ配置する
- Python コア処理は一時ディレクトリを `input_dir` として扱う

### 5.5 出力ファイルの扱い
- 出力先は Google Drive 配下の固定ベースフォルダとする
- サブフォルダは `yyyyMM` 単位で作成する
- 例
  - `MyDrive/businessDX/output/202603/pdfs/`
  - `MyDrive/businessDX/output/202603/index/`

### 5.6 実行入口
- `main.py` の CLI は残してもよいが、Colab では使わない前提にする
- Colab からは共通入口関数を直接呼ぶ
- 入口関数は以下を担当する
  - 設定の検証
  - PDF 分割の実行
  - Excel 分析の実行
  - サマリの返却

## 6. Colab Notebook 設計
### 6.1 セル構成
1. ライブラリインストール
2. Google Drive マウント
3. リポジトリ取得またはファイル配置
4. API キー入力
5. Excel/PDF アップロード
6. 実行設定の定義
7. 実行
8. 出力確認

### 6.2 Notebook で行う処理
- Drive をマウントする
- `分類.csv` 固定パスの存在確認を行う
- Excel と PDF のアップロードを受け付ける
- API キーをユーザー入力で受け取る
- 実行対象年月を決定する
- `pipeline` を呼び出して結果を表示する

## 7. エラー処理設計
- API キー未入力
  - 実行前に停止する
- `分類.csv` が存在しない
  - Drive パスを表示して停止する
- Excel 未投入
  - Excel 分析をスキップまたは停止する
- PDF 未投入
  - PDF 分割をスキップまたは停止する
- Gemini API エラー
  - 現行のリトライ方針を踏襲する
- 出力先作成エラー
  - Drive パスと例外内容を表示して停止する

## 8. 実装順
1. 設定オブジェクトを追加する
2. `excel_analyzer.py` の API キー依存を除去する
3. `分類.csv` 参照先を引数化する
4. 共通実行入口を追加する
5. Colab Notebook を追加する
6. 利用手順を追加する
7. 受け入れ条件に沿って確認する

## 9. 影響範囲
### 9.1 直接修正
- `src/excel_analyzer.py`
- `src/main.py`
- 新規追加する設定・入口モジュール
- Colab Notebook

### 9.2 影響は小さい
- `src/pdf_splitter.py`
  - 主に呼び出し元から渡すパスが変わるだけ

## 10. レビューしてほしい点
- `app_config.py` と `pipeline.py` の分割でよいか
- 出力フォルダを `yyyyMM` 固定で運用してよいか
- Colab では CLI を正式導線から外してよいか
- Excel/PDF 未投入時の挙動を「停止」か「片系スキップ」かどちらに寄せるか
