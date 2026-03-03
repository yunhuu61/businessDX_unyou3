import pandas as pd
from pathlib import Path
import sys

# Find the error file
output_dir = Path("output/index")
error_files = list(output_dir.glob("*_errors.xlsx"))

if not error_files:
    print("No error files found.")
    sys.exit(0)

# Sort by modification time to get the latest
latest_error_file = sorted(error_files, key=lambda f: f.stat().st_mtime, reverse=True)[0]
print(f"Reading error file: {latest_error_file.name}")

try:
    df = pd.read_excel(latest_error_file, sheet_name="要確認")
    with open("error_summary.txt", "w", encoding="utf-8") as f:
        if "理由" in df.columns:
            f.write("--- Error Reasons ---\n")
            f.write(df["理由"].value_counts().to_string())
            f.write("\n\n--- Detailed Reasons (First 5) ---\n")
            for reason in df["理由"].head(5):
                f.write(f"- {reason}\n")
        else:
            f.write("Column '理由' not found.")
except Exception as e:
    with open("error_summary.txt", "w", encoding="utf-8") as f:
        f.write(f"Failed to read Excel file: {e}")
