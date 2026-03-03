"""businessDX_unyou リニューアル - 統合エントリポイント

処理1（PDF分割）と処理2（Excel企業分析）を順番に実行する。

使い方:
    python main.py          # 両方実行
    python main.py --pdf    # PDF分割のみ
    python main.py --excel  # Excel分析のみ
"""

import argparse
import sys
import time
from pathlib import Path

import pdf_splitter
import excel_analyzer


def main():
    parser = argparse.ArgumentParser(description="企業紹介PDF処理ツール")
    parser.add_argument("--pdf", action="store_true", help="PDF分割のみ実行")
    parser.add_argument("--excel", action="store_true", help="Excel分析のみ実行")
    parser.add_argument("--input", default="input", help="入力ディレクトリ（デフォルト: input）")
    parser.add_argument("--output", default="output", help="出力ベースディレクトリ（デフォルト: output）")
    args = parser.parse_args()

    run_pdf = not args.excel or args.pdf
    run_excel = not args.pdf or args.excel

    if args.pdf and args.excel:
        run_pdf = True
        run_excel = True

    input_dir = args.input
    output_base = args.output

    print("=" * 60)
    print("企業紹介PDF処理ツール")
    print("=" * 60)

    start_time = time.time()

    if run_pdf:
        print()
        print("-" * 40)
        print("処理1: PDF分割")
        print("-" * 40)
        pdf_result = pdf_splitter.run(
            input_dir=input_dir,
            output_dir=str(Path(output_base) / "pdfs"),
        )

    if run_excel:
        print()
        print("-" * 40)
        print("処理2: Excel企業分析")
        print("-" * 40)
        excel_result = excel_analyzer.run(
            input_dir=input_dir,
            output_dir=str(Path(output_base) / "index"),
        )

    elapsed = time.time() - start_time

    print()
    print("=" * 60)
    print(f"全処理完了（{elapsed:.1f} 秒）")
    print("=" * 60)


if __name__ == "__main__":
    main()
