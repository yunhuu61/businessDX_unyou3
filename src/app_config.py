"""Configuration object for running the businessDX pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class AppConfig:
    input_dir: str
    output_dir: str
    run_yyyymm: str | None = None
    classification_csv_path: str | None = None
    gemini_api_key: str | None = None
    model_name: str = "gemini-2.0-flash"
    prompt_path: str | None = None
    run_pdf: bool = True
    run_excel: bool = True

    @property
    def input_path(self) -> Path:
        return Path(self.input_dir)

    @property
    def output_path(self) -> Path:
        return Path(self.output_dir)

    @property
    def pdf_output_path(self) -> Path:
        return self.output_path / "pdfs"

    @property
    def excel_output_path(self) -> Path:
        return self.output_path / "index"

    def enabled_steps(self) -> list[str]:
        steps: list[str] = []
        if self.run_pdf:
            steps.append("pdf")
        if self.run_excel:
            steps.append("excel")
        return steps
