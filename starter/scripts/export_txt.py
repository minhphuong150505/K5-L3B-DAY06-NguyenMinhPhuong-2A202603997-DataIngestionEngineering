"""Export the processed corpus (results/pages.jsonl) to plain text.

Run from starter/:  python scripts/export_txt.py
Writes results/processed_text.txt: every PDF page in order, with a header line per page
(page number, section, extraction mode, counted or excluded). Text is exactly what
src.ingestion produced (NFC, header/footer removed, chart pairs / OCR appended).
"""
import json
from pathlib import Path

RESULTS = Path(__file__).resolve().parents[1] / "results"
src = RESULTS / "pages.jsonl"
out = RESULTS / "processed_text.txt"

pages = [json.loads(l) for l in src.read_text(encoding="utf-8").splitlines() if l.strip()]
counted = sum(p["metadata"].get("counted", False) for p in pages)

lines = [
    f"# Corpus đã xử lý: {pages[0]['document_id']} ({pages[0]['source']})",
    f"# {len(pages)} trang PDF, {counted} trang được tính là nội dung.",
    "# Nguồn: results/pages.jsonl (src.ingestion: pypdf + NFC + bỏ header/footer + ghép biểu đồ/OCR)",
    "",
]
for p in pages:
    md = p["metadata"]
    status = "TÍNH" if md.get("counted") else "LOẠI"
    extra = [f"section={md.get('section') or '-'}", f"mode={md.get('extraction_mode', '-')}",
             f"{md.get('chars', len(p['text']))} ký tự", status]
    if md.get("ocr"):
        extra.append(f"OCR {md['ocr']}")
    lines.append("=" * 80)
    lines.append(f"TRANG {p['page']} | " + " | ".join(extra))
    lines.append("=" * 80)
    lines.append(p["text"] if p["text"] else "(trang trống)")
    lines.append("")

out.write_text("\n".join(lines), encoding="utf-8")
print(f"Wrote {out} ({len(pages)} pages, {out.stat().st_size // 1024} KB)")
