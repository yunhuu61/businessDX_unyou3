"""処理2: Excel企業分析

Excelの企業リストをGoogle Gemini APIで分析し、構造化データを生成する。
- input/ 内の .xlsx ファイルを検出し、すべて処理
- input/分類.csv の全列（産業サブグループ/産業グループ/産業）を参照して業種分類
- プロンプトは prompt.txt から毎回読み込む（外出し仕様）
- 出力: full版（概要あり）と DL版（概要なし）の2種類のExcel
- 企業名の秘匿化（生成テキストに具体的企業名を出さない）
- エラー時: 3回リトライ、失敗行は「要確認」シートに記録
"""

import csv
import json
import os
import re
import time
from pathlib import Path

from google import genai
import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm


def load_classification_csv(csv_path: Path) -> str:
    """分類.csv の全列を読み込み、テーブル形式の文字列として返す。

    Returns:
        「産業サブグループ | 産業グループ | 産業」のテーブル文字列
    """
    lines = ["産業サブグループ | 産業グループ | 産業", "--- | --- | ---"]
    with open(csv_path, encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            a = row[0].strip() if len(row) >= 1 else ""
            b = row[1].strip() if len(row) >= 2 else ""
            c = row[2].strip() if len(row) >= 3 else ""
            if b:
                lines.append(f"{a} | {b} | {c}")
    return "\n".join(lines)


def load_prompt_template(prompt_path: Path) -> str:
    """外部プロンプトファイルを読み込む。毎回ファイルから読む（編集即反映）。"""
    with open(prompt_path, encoding="utf-8") as f:
        return f.read()


def extract_yyyymm_from_excel(filename: str) -> str:
    """ファイル名から yyyyMM を抽出。見つからなければファイル名のステムを返す。"""
    match = re.match(r"(\d{6})", filename)
    if match:
        return match.group(1)
    return Path(filename).stem


def build_prompt(prompt_template: str, company_data: dict, classification_table: str) -> str:
    """プロンプトテンプレートに企業データと分類テーブルを埋め込む。"""
    return prompt_template.format(
        company_data=json.dumps(company_data, ensure_ascii=False, indent=2),
        classification_table=classification_table,
    )


def parse_ai_response(response_text: str) -> dict | None:
    """AIのレスポンスからJSONを抽出してパースする。"""
    text = response_text.strip()

    json_match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if json_match:
        text = json_match.group(1).strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        json_match = re.search(r"\{[\s\S]*\}", text)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                return None
    return None


def analyze_company(
    client,
    model_name: str,
    prompt_template: str,
    company_data: dict,
    classification_table: str,
    max_retries: int = 5,
) -> dict | None:
    """1企業をGemini APIで分析する。失敗時は最大max_retries回リトライ。"""
    prompt = build_prompt(prompt_template, company_data, classification_table)

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            result = parse_ai_response(response.text)
            if result:
                return result
            # JSONパース失敗等のリトライ
            if attempt < max_retries - 1:
                time.sleep(2)
        except Exception as e:
            error_msg = str(e)
            if attempt < max_retries - 1:
                if "429" in error_msg:
                    print(f"  [Retry {attempt+1}/{max_retries}] APIレート制限(429)を検知。30秒待機してリトライします...")
                    time.sleep(30)
                else:
                    wait = 2 ** (attempt + 1)
                    print(f"  [Retry {attempt+1}/{max_retries}] エラー: {e} ({wait}秒待機)")
                    time.sleep(wait)
            else:
                raise

    return None


def process_excel(
    excel_path: Path,
    classification_table: str,
    prompt_template: str,
    output_dir: Path,
    client,
    model_name: str,
) -> dict:
    """1つのExcelファイルを処理する。

    Returns:
        処理結果サマリ dict
    """
    yyyymm = extract_yyyymm_from_excel(excel_path.name)

    df = pd.read_excel(excel_path)

    results = []
    errors = []

    for idx, row in tqdm(df.iterrows(), total=len(df), desc=f"  {excel_path.name}", leave=False):
        company_data = {}
        for col in df.columns:
            val = row[col]
            if pd.notna(val):
                company_data[str(col)] = str(val)

        if not company_data:
            continue

        try:
            analysis = analyze_company(
                client, model_name, prompt_template,
                company_data, classification_table,
            )
            if analysis:
                analysis["#"] = idx + 1
                results.append(analysis)
            else:
                errors.append({
                    "#": idx + 1,
                    "理由": "AI分析の結果をパースできませんでした",
                    **company_data,
                })
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg:
                error_reason = "APIレート制限（429）: 短時間のアクセス過多です"
            else:
                error_reason = f"APIエラー（3回リトライ後）: {e}"
            
            errors.append({
                "#": idx + 1,
                "理由": error_reason,
                **company_data,
            })

        # 無料枠(15 RPM)対策: 4秒待機（エラー時はリトライでカバー）
        time.sleep(4)

    output_dir.mkdir(parents=True, exist_ok=True)

    full_columns = ["#", "業種", "ターゲット業種", "取引形態", "キーワード", "キャッチコピー", "概要"]
    dl_columns = ["#", "業種", "ターゲット業種", "取引形態", "キーワード", "キャッチコピー"]

    if results:
        df_results = pd.DataFrame(results)

        for col in full_columns:
            if col not in df_results.columns:
                df_results[col] = ""

        # full版: 概要あり
        full_path = output_dir / f"{yyyymm}_index_full.xlsx"
        df_full = df_results[full_columns]
        with pd.ExcelWriter(full_path, engine="openpyxl") as writer:
            df_full.to_excel(writer, index=False, sheet_name="分析結果")
            if errors:
                df_errors = pd.DataFrame(errors)
                df_errors.to_excel(writer, index=False, sheet_name="要確認")

        # DL版: 概要なし
        dl_path = output_dir / f"{yyyymm}_index_DLver.xlsx"
        df_dl = df_results[dl_columns]
        with pd.ExcelWriter(dl_path, engine="openpyxl") as writer:
            df_dl.to_excel(writer, index=False, sheet_name="分析結果")
            if errors:
                df_errors = pd.DataFrame(errors)
                df_errors.to_excel(writer, index=False, sheet_name="要確認")

        print(f"  出力: {full_path.name}, {dl_path.name}")
    else:
        if errors:
            error_path = output_dir / f"{yyyymm}_errors.xlsx"
            df_errors = pd.DataFrame(errors)
            df_errors.to_excel(error_path, index=False, sheet_name="要確認")
            print(f"  出力（エラーのみ）: {error_path.name}")

    return {
        "file": excel_path.name,
        "total_rows": len(df),
        "analyzed": len(results),
        "errors": len(errors),
    }


def run(input_dir: str = "input", output_dir: str = "output/index") -> dict:
    """Excel企業分析処理のメインエントリポイント。

    Args:
        input_dir: 入力ディレクトリのパス
        output_dir: 出力ディレクトリのパス

    Returns:
        処理結果のサマリ dict
    """
    # .env はスクリプトと同じフォルダ（src/）から読む
    env_path = Path(__file__).parent / ".env"
    load_dotenv(env_path, override=True)

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("[Excel分析] エラー: GOOGLE_API_KEY が設定されていません。.env ファイルを確認してください。")
        return {"processed": 0, "errors": 0}

    model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-2.0-flash")
    client = genai.Client(api_key=api_key)

    input_path = Path(input_dir)
    output_path = Path(output_dir)

    # プロンプトファイル読み込み（src/prompt.txt）
    prompt_path = Path(__file__).parent / "prompt.txt"
    if not prompt_path.exists():
        print(f"[Excel分析] エラー: {prompt_path} が見つかりません。")
        return {"processed": 0, "errors": 0}
    prompt_template = load_prompt_template(prompt_path)
    print(f"[Excel分析] プロンプト読み込み: {prompt_path.name}")

    # 分類CSV読み込み（全列: 産業サブグループ / 産業グループ / 産業）
    classification_csv = input_path / "分類.csv"
    if not classification_csv.exists():
        print(f"[Excel分析] エラー: {classification_csv} が見つかりません。")
        return {"processed": 0, "errors": 0}
    classification_table = load_classification_csv(classification_csv)

    xlsx_files = sorted(input_path.glob("*.xlsx"))
    xlsx_files = [f for f in xlsx_files if not f.name.startswith("~$")]

    if not xlsx_files:
        print("[Excel分析] input/ にExcelファイル(.xlsx)が見つかりません。スキップします。")
        return {"processed": 0, "errors": 0}

    print(f"[Excel分析] {len(xlsx_files)} 件のExcelファイルを処理します。")

    summaries = []
    for xlsx_file in xlsx_files:
        try:
            summary = process_excel(
                xlsx_file, classification_table, prompt_template,
                output_path, client, model_name,
            )
            summaries.append(summary)
            print(f"  OK: {xlsx_file.name} ({summary['analyzed']}/{summary['total_rows']} 件分析, {summary['errors']} 件エラー)")
        except Exception as e:
            print(f"  SKIP: {xlsx_file.name} (エラー: {e})")
            summaries.append({"file": xlsx_file.name, "total_rows": 0, "analyzed": 0, "errors": 1})

    total_analyzed = sum(s["analyzed"] for s in summaries)
    total_errors = sum(s["errors"] for s in summaries)
    print(f"[Excel分析] 完了: {len(summaries)} ファイル処理, 合計 {total_analyzed} 件分析, {total_errors} 件エラー")

    return {"processed": len(summaries), "total_analyzed": total_analyzed, "errors": total_errors}


if __name__ == "__main__":
    run()
