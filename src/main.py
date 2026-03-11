"""CLI entry point for the businessDX pipeline."""

from __future__ import annotations

import argparse
import time

from app_config import AppConfig
from pipeline import run_pipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the PDF split and Excel analysis pipeline.")
    parser.add_argument("--pdf", action="store_true", help="Run only PDF splitting.")
    parser.add_argument("--excel", action="store_true", help="Run only Excel analysis.")
    parser.add_argument("--input", default="input", help="Input directory path.")
    parser.add_argument("--output", default="output", help="Output base directory path.")
    parser.add_argument("--classification-csv", required=False, help="Path to classification CSV.")
    parser.add_argument("--api-key", required=False, help="Gemini API key.")
    parser.add_argument("--run-yyyymm", required=False, help="Run month in yyyymm format.")
    parser.add_argument("--model-name", default="gemini-2.0-flash", help="Gemini model name.")
    parser.add_argument("--prompt-path", required=False, help="Path to prompt template.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_pdf = not args.excel or args.pdf
    run_excel = not args.pdf or args.excel
    if args.pdf and args.excel:
        run_pdf = True
        run_excel = True

    config = AppConfig(
        input_dir=args.input,
        output_dir=args.output,
        run_yyyymm=args.run_yyyymm,
        classification_csv_path=args.classification_csv,
        gemini_api_key=args.api_key,
        model_name=args.model_name,
        prompt_path=args.prompt_path,
        run_pdf=run_pdf,
        run_excel=run_excel,
    )

    print("=" * 60)
    print("businessDX pipeline")
    print("=" * 60)
    start = time.time()
    run_pipeline(config)
    elapsed = time.time() - start
    print("=" * 60)
    print(f"Completed in {elapsed:.1f}s")
    print("=" * 60)


if __name__ == "__main__":
    main()
