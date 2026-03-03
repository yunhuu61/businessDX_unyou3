from pathlib import Path

log_path = Path("execution_log.txt")
if log_path.exists():
    try:
        # Try reading as UTF-16LE first (PowerShell default for > redirection)
        print(log_path.read_text(encoding="utf-16le", errors="ignore"))
    except Exception:
        # Fallback to UTF-8 or CP932
        try:
            print(log_path.read_text(encoding="utf-8", errors="ignore"))
        except:
             print(log_path.read_text(encoding="cp932", errors="ignore"))
else:
    print("Log file not found.")
