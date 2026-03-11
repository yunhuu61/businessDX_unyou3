"""Excel analysis pipeline backed by the Gemini API."""

from __future__ import annotations

import csv
import json
import re
import time
from pathlib import Path

import pandas as pd
from google import genai
from tqdm import tqdm


DEFAULT_MODEL_NAME = "gemini-2.0-flash"
FULL_OUTPUT_COLUMNS = [
    "#",
    "業種",
    "ターゲット業種",
    "分類理由",
    "キーワード",
    "キャッチコピー",
    "URL",
]
DL_OUTPUT_COLUMNS = [
    "#",
    "業種",
    "ターゲット業種",
    "分類理由",
    "キーワード",
    "キャッチコピー",
]


def load_classification_csv(csv_path: Path) -> str:
    """Load the classification CSV and convert it into a markdown table."""
    lines = ["産業サブグループ | 産業グループ | 産業", "--- | --- | ---"]
    with csv_path.open(encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            sub_group = row[0].strip() if len(row) >= 1 else ""
            group = row[1].strip() if len(row) >= 2 else ""
            industry = row[2].strip() if len(row) >= 3 else ""
            if group:
                lines.append(f"{sub_group} | {group} | {industry}")
    return "\n".join(lines)


def load_prompt_template(prompt_path: Path) -> str:
    with prompt_path.open(encoding="utf-8") as file:
        return file.read()


def extract_yyyymm_from_filename(filename: str) -> str:
    match = re.match(r"(\d{6})", filename)
    if match:
        return match.group(1)
    return Path(filename).stem


def build_prompt(prompt_template: str, company_data: dict, classification_table: str) -> str:
    return prompt_template.format(
        company_data=json.dumps(company_data, ensure_ascii=False, indent=2),
        classification_table=classification_table,
    )


def parse_ai_response(response_text: str) -> dict | None:
    text = response_text.strip()

    fenced_match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if fenced_match:
        text = fenced_match.group(1).strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        inline_match = re.search(r"\{[\s\S]*\}", text)
        if not inline_match:
            return None
        try:
            return json.loads(inline_match.group())
        except json.JSONDecodeError:
            return None


def analyze_company(
    client: genai.Client,
    model_name: str,
    prompt_template: str,
    company_data: dict,
    classification_table: str,
    max_retries: int = 5,
) -> dict | None:
    prompt = build_prompt(prompt_template, company_data, classification_table)

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            parsed = parse_ai_response(response.text)
            if parsed:
                return parsed
            if attempt < max_retries - 1:
                time.sleep(2)
        except Exception as exc:  # pragma: no cover - network/API dependent
            message = str(exc)
            if attempt >= max_retries - 1:
                raise
            if "429" in message:
                print(
                    f"  [Retry {attempt + 1}/{max_retries}] "
                    "Gemini rate limit detected. Waiting 30 seconds before retry..."
                )
                time.sleep(30)
            else:
                wait_seconds = 2 ** (attempt + 1)
                print(
                    f"  [Retry {attempt + 1}/{max_retries}] "
                    f"Gemini API error: {exc} ({wait_seconds}s)"
                )
                time.sleep(wait_seconds)

    return None


def build_company_data(row: pd.Series, columns: list[str]) -> dict:
    company_data: dict[str, str] = {}
    for column in columns:
        value = row[column]
        if pd.notna(value):
            company_data[str(column)] = str(value)
    return company_data


def build_error_record(row_number: int, reason: str, company_data: dict) -> dict:
    return {
        "#": row_number,
        "エラー内容": reason,
        **company_data,
    }


def ensure_columns(dataframe: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for column in columns:
        if column not in dataframe.columns:
            dataframe[column] = ""
    return dataframe


def save_excel_outputs(
    output_dir: Path,
    yyyymm: str,
    results: list[dict],
    errors: list[dict],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    if results:
        results_df = pd.DataFrame(results)
        results_df = ensure_columns(results_df, FULL_OUTPUT_COLUMNS)

        full_path = output_dir / f"{yyyymm}_index_full.xlsx"
        with pd.ExcelWriter(full_path, engine="openpyxl") as writer:
            results_df[FULL_OUTPUT_COLUMNS].to_excel(writer, index=False, sheet_name="分析結果")
            if errors:
                pd.DataFrame(errors).to_excel(writer, index=False, sheet_name="エラー一覧")

        dl_path = output_dir / f"{yyyymm}_index_DLver.xlsx"
        with pd.ExcelWriter(dl_path, engine="openpyxl") as writer:
            results_df[DL_OUTPUT_COLUMNS].to_excel(writer, index=False, sheet_name="分析結果")
            if errors:
                pd.DataFrame(errors).to_excel(writer, index=False, sheet_name="エラー一覧")

        print(f"  Saved: {full_path.name}, {dl_path.name}")
        return

    if errors:
        error_path = output_dir / f"{yyyymm}_errors.xlsx"
        pd.DataFrame(errors).to_excel(error_path, index=False, sheet_name="エラー一覧")
        print(f"  Saved: {error_path.name}")


def process_excel(
    excel_path: Path,
    output_yyyymm: str | None,
    classification_table: str,
    prompt_template: str,
    output_dir: Path,
    client: genai.Client,
    model_name: str,
) -> dict:
    yyyymm = output_yyyymm or extract_yyyymm_from_filename(excel_path.name)
    dataframe = pd.read_excel(excel_path)

    results: list[dict] = []
    errors: list[dict] = []

    for index, row in tqdm(
        dataframe.iterrows(),
        total=len(dataframe),
        desc=f"  {excel_path.name}",
        leave=False,
    ):
        company_data = build_company_data(row, list(dataframe.columns))
        if not company_data:
            continue

        row_number = index + 1
        try:
            analysis = analyze_company(
                client=client,
                model_name=model_name,
                prompt_template=prompt_template,
                company_data=company_data,
                classification_table=classification_table,
            )
            if analysis:
                analysis["#"] = row_number
                results.append(analysis)
            else:
                errors.append(
                    build_error_record(
                        row_number=row_number,
                        reason="AI response could not be parsed as JSON.",
                        company_data=company_data,
                    )
                )
        except Exception as exc:  # pragma: no cover - network/API dependent
            message = str(exc)
            if "429" in message:
                reason = "Gemini rate limit exceeded (429)."
            else:
                reason = f"Gemini API error after retries: {exc}"
            errors.append(build_error_record(row_number=row_number, reason=reason, company_data=company_data))

        # Current workflow assumes a low request rate to stay within quota.
        time.sleep(4)

    save_excel_outputs(output_dir=output_dir, yyyymm=yyyymm, results=results, errors=errors)

    return {
        "file": excel_path.name,
        "total_rows": len(dataframe),
        "analyzed": len(results),
        "errors": len(errors),
    }


def run(
    input_dir: str,
    output_dir: str,
    output_yyyymm: str | None,
    classification_csv_path: str,
    api_key: str,
    model_name: str = DEFAULT_MODEL_NAME,
    prompt_path: str | None = None,
) -> dict:
    """Run Excel analysis for all xlsx files in the input directory."""
    if not api_key or not api_key.strip():
        raise ValueError("Gemini API key is required.")

    input_path = Path(input_dir)
    output_path = Path(output_dir)
    classification_csv = Path(classification_csv_path)
    resolved_prompt_path = Path(prompt_path) if prompt_path else Path(__file__).parent / "prompt.txt"

    if not resolved_prompt_path.exists():
        raise FileNotFoundError(f"Prompt template not found: {resolved_prompt_path}")
    if not classification_csv.exists():
        raise FileNotFoundError(f"Classification CSV not found: {classification_csv}")

    xlsx_files = sorted(file for file in input_path.glob("*.xlsx") if not file.name.startswith("~$"))
    if not xlsx_files:
        print("[Excel analysis] No .xlsx files found. Skipping.")
        return {"processed": 0, "total_analyzed": 0, "errors": 0}

    prompt_template = load_prompt_template(resolved_prompt_path)
    classification_table = load_classification_csv(classification_csv)
    client = genai.Client(api_key=api_key.strip())

    print(f"[Excel analysis] Prompt template: {resolved_prompt_path.name}")
    print(f"[Excel analysis] Classification CSV: {classification_csv}")
    print(f"[Excel analysis] {len(xlsx_files)} Excel file(s) found.")

    summaries: list[dict] = []
    for xlsx_file in xlsx_files:
        try:
            summary = process_excel(
                excel_path=xlsx_file,
                output_yyyymm=output_yyyymm,
                classification_table=classification_table,
                prompt_template=prompt_template,
                output_dir=output_path,
                client=client,
                model_name=model_name,
            )
            summaries.append(summary)
            print(
                "  OK: "
                f"{xlsx_file.name} ({summary['analyzed']}/{summary['total_rows']} analyzed, "
                f"{summary['errors']} errors)"
            )
        except Exception as exc:
            print(f"  SKIP: {xlsx_file.name} (error: {exc})")
            summaries.append({"file": xlsx_file.name, "total_rows": 0, "analyzed": 0, "errors": 1})

    total_analyzed = sum(item["analyzed"] for item in summaries)
    total_errors = sum(item["errors"] for item in summaries)
    print(
        f"[Excel analysis] Completed {len(summaries)} file(s). "
        f"Analyzed: {total_analyzed}, Errors: {total_errors}"
    )
    return {"processed": len(summaries), "total_analyzed": total_analyzed, "errors": total_errors}


if __name__ == "__main__":
    raise SystemExit("Run this module via pipeline.py or main.py.")
