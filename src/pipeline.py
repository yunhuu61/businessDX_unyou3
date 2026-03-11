"""Shared pipeline entry point for CLI and Google Colab."""

from __future__ import annotations

from pathlib import Path

from app_config import AppConfig
import excel_analyzer
import pdf_splitter


def validate_config(config: AppConfig) -> None:
    if not config.enabled_steps():
        raise ValueError("At least one step must be enabled.")

    if not config.input_path.exists():
        raise FileNotFoundError(f"Input directory not found: {config.input_path}")

    if config.run_pdf:
        pdf_files = list(config.input_path.glob("*.pdf"))
        if not pdf_files:
            raise FileNotFoundError(f"No PDF files found in input directory: {config.input_path}")

    if config.run_excel:
        xlsx_files = [file for file in config.input_path.glob("*.xlsx") if not file.name.startswith("~$")]
        if not xlsx_files:
            raise FileNotFoundError(f"No Excel files found in input directory: {config.input_path}")
        if not config.gemini_api_key or not config.gemini_api_key.strip():
            raise ValueError("Gemini API key is required when Excel analysis is enabled.")
        if not config.classification_csv_path:
            raise ValueError("classification_csv_path is required when Excel analysis is enabled.")
        classification_path = Path(config.classification_csv_path)
        if not classification_path.exists():
            raise FileNotFoundError(f"Classification CSV not found: {classification_path}")


def run_pipeline(config: AppConfig) -> dict:
    validate_config(config)
    config.output_path.mkdir(parents=True, exist_ok=True)

    results: dict[str, dict] = {}

    if config.run_pdf:
        print("-" * 40)
        print("Step: PDF split")
        print("-" * 40)
        results["pdf"] = pdf_splitter.run(
            input_dir=str(config.input_path),
            output_dir=str(config.pdf_output_path),
        )

    if config.run_excel:
        print("-" * 40)
        print("Step: Excel analysis")
        print("-" * 40)
        results["excel"] = excel_analyzer.run(
            input_dir=str(config.input_path),
            output_dir=str(config.excel_output_path),
            output_yyyymm=config.run_yyyymm,
            classification_csv_path=config.classification_csv_path or "",
            api_key=config.gemini_api_key or "",
            model_name=config.model_name,
            prompt_path=config.prompt_path,
        )

    return results
