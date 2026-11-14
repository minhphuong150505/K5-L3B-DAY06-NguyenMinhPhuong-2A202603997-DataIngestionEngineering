"""Compare OCR output of pp. 35-37 (src/ocr_charts.py) with the hand-transcribed gold.

Run from starter/:  .venv/bin/python scripts/check_ocr.py
Counts: correct / wrong (accepted but different from gold) / rejected (left out + logged).
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.ocr_charts import extract_document  # noqa: E402

gold = json.loads((ROOT / "results" / "ocr_gold_p35_37.json").read_text(encoding="utf-8"))
series = gold["series"]
pages = {c["page"] for c in gold["charts"].values()}
got: dict[tuple[str, str, str], str] = {}
issues = []
for _, charts in extract_document(str(ROOT.parent / "data" / "BCTMDT2023-file-31-1-pdf.pdf"), pages).items():
    for c in charts:
        issues += c.issues
        for row in c.rows:
            year, rest = row.split(" — ", 1)
            name, value = rest.rsplit(": ", 1)
            got[(c.title, year, name)] = value

correct = wrong = rejected = 0
lines = []
for title, chart in gold["charts"].items():
    for year in ("2022", "2023", "2025"):
        for name, expected in zip(series, chart[year]):
            v = got.get((title, year, name))
            if v is None:
                rejected += 1
                lines.append(f"REJECTED  {title} {year} {name}: gold {expected}")
            elif v == expected:
                correct += 1
            else:
                wrong += 1
                lines.append(f"WRONG     {title} {year} {name}: ocr {v} != gold {expected}")
total = correct + wrong + rejected
print("\n".join(lines))
print(f"\nTotal {total}: correct {correct}, wrong {wrong}, rejected {rejected}")
print(f"Precision of accepted values: {correct}/{correct + wrong}")
print("Logged issues:", *issues, sep="\n  ")
