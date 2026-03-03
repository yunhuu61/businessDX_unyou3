"""処理1: PDF分割

複数ページの企業紹介PDFを1ページずつのPDFに分割する。
- input/ 内のPDFファイルを検出し、すべて処理
- ファイル名の先頭6桁(yyyyMM)を使って出力ファイル名を生成
- output/pdfs/{元のPDF名}/ に yyyyMM_001.pdf 形式で保存
- 破損PDFはスキップして次に進む
"""

import os
import re
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from tqdm import tqdm


def extract_yyyymm(filename: str) -> str:
    """ファイル名の先頭6桁(yyyyMM)を抽出する。"""
    match = re.match(r"(\d{6})", filename)
    if match:
        return match.group(1)
    return "000000"


def split_pdf(pdf_path: Path, output_base_dir: Path) -> int:
    """1つのPDFを1ページずつに分割する。

    Args:
        pdf_path: 入力PDFのパス
        output_base_dir: output/pdfs/ のパス

    Returns:
        分割したページ数
    """
    filename = pdf_path.stem
    yyyymm = extract_yyyymm(pdf_path.name)

    output_dir = output_base_dir / filename
    output_dir.mkdir(parents=True, exist_ok=True)

    reader = PdfReader(str(pdf_path))
    total_pages = len(reader.pages)

    for i, page in enumerate(tqdm(reader.pages, desc=f"  {pdf_path.name}", leave=False)):
        writer = PdfWriter()
        writer.add_page(page)

        page_num = f"{i + 1:03d}"
        output_filename = f"{yyyymm}_{page_num}.pdf"
        output_path = output_dir / output_filename

        with open(output_path, "wb") as f:
            writer.write(f)

    return total_pages


def run(input_dir: str = "input", output_dir: str = "output/pdfs") -> dict:
    """PDF分割処理のメインエントリポイント。

    Args:
        input_dir: 入力ディレクトリのパス
        output_dir: 出力ディレクトリのパス

    Returns:
        処理結果のサマリ dict
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    pdf_files = sorted(input_path.glob("*.pdf"))

    if not pdf_files:
        print("[PDF分割] input/ にPDFファイルが見つかりません。スキップします。")
        return {"processed": 0, "skipped": 0, "total_pages": 0}

    print(f"[PDF分割] {len(pdf_files)} 件のPDFファイルを処理します。")

    processed = 0
    skipped = 0
    total_pages = 0

    for pdf_file in pdf_files:
        try:
            pages = split_pdf(pdf_file, output_path)
            total_pages += pages
            processed += 1
            print(f"  OK: {pdf_file.name} ({pages} ページ)")
        except Exception as e:
            skipped += 1
            print(f"  SKIP: {pdf_file.name} (エラー: {e})")

    print(f"[PDF分割] 完了: {processed} 件処理, {skipped} 件スキップ, 合計 {total_pages} ページ")

    return {"processed": processed, "skipped": skipped, "total_pages": total_pages}


if __name__ == "__main__":
    run()
