"""Read and normalize source data, keeping page-level traceability and an error log.

Chart pages: pypdf layout mode (horizontal bars) + PyMuPDF word coordinates for vertical
bars (src/chart_pairs.py).

Library: pypdf (text layer). The corpus PDF is born-digital (Adobe InDesign), so no OCR is
used; pages without extractable text are logged instead of silently skipped.

CLI:  python -m src.ingestion            (run from starter/)
Writes results/pages.jsonl, results/ingestion_errors.jsonl, results/ingestion_summary.json
"""
from __future__ import annotations

import hashlib
import json
import logging
import re
import subprocess
import time
import unicodedata
import warnings
from dataclasses import asdict
from pathlib import Path
from typing import Any

from pypdf import PdfReader

from .models import DocumentPage

ROOT = Path(__file__).resolve().parents[2]          # repo root
MANIFEST_PATH = ROOT / "data" / "manifest.json"
BENCHMARK_PATH = ROOT / "benchmark" / "questions.jsonl"
RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"

MIN_PAGE_CHARS = 50          # below this a page is reported as (near-)empty
MIN_CONTENT_PAGES = 30

# Running header/footer printed on every page of the white paper.
_HEADER_PATTERNS = [
    re.compile(r"^SÁCH TRẮNG THƯƠNG MẠI ĐIỆN TỬ VIỆT NAM NĂM 2023$"),
    re.compile(r"^www\.idea\.gov\.vn(\s+\d{1,3})?$", re.IGNORECASE),
    re.compile(r"^\d{1,3}$"),                       # bare printed page number
]
# Zero-width / BOM / soft hyphen: invisible, break exact matching.
_INVISIBLE = dict.fromkeys(map(ord, "​‌‍⁠﻿­"), None)
_SPACE_LIKE = re.compile(r"[  -   　\t\f\v]")


class _ErrorLog:
    """Collects ingestion problems as structured records (never swallows them)."""

    def __init__(self) -> None:
        self.records: list[dict[str, Any]] = []

    def add(self, level: str, code: str, page: int | None, detail: str) -> None:
        self.records.append({"level": level, "code": code, "page": page, "detail": detail})


def normalize_text(text: str) -> str:
    """Unicode NFC + whitespace cleanup, keeping line/paragraph structure.

    - NFC so composed and decomposed Vietnamese diacritics compare equal.
    - Drop invisible characters, map exotic spaces to ' ', CRLF to LF.
    - Collapse runs of spaces inside a line; keep at most one blank line.
    Line breaks are kept because chunking by paragraph/heading (strategy B) needs them.
    """
    text = unicodedata.normalize("NFC", text).translate(_INVISIBLE)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = _SPACE_LIKE.sub(" ", text)
    lines = [re.sub(r" {2,}", " ", line).strip() for line in text.split("\n")]
    out: list[str] = []
    for line in lines:
        if line or (out and out[-1]):
            out.append(line)
    return "\n".join(out).strip()


COL_SEP = " | "
_COL_GAP = re.compile(r" {3,}")


def layout_to_columns(text: str) -> str:
    """Turn pypdf layout-mode output into lines whose visual columns are joined by ' | '.

    Layout mode places a horizontal bar's label and its value on the same line, separated by
    a wide gap; marking that gap keeps the pair readable after whitespace normalization.
    """
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            lines.append(_COL_GAP.sub(COL_SEP, line))
    return "\n".join(lines)


def flatten_for_match(text: str) -> str:
    """Comparison form used for evidence checks: drop column separators, collapse spaces."""
    return re.sub(r"\s+", " ", text.replace(COL_SEP, " ")).strip()


def strip_running_header(text: str, page: int) -> str:
    """Remove the repeated header/footer lines at the top of a page only."""
    lines = [re.sub(r"^\|\s*", "", ln) for ln in text.split("\n")]
    i = 0
    while i < min(len(lines), 4) and any(p.match(lines[i]) for p in _HEADER_PATTERNS):
        if _HEADER_PATTERNS[2].match(lines[i]) and int(lines[i]) != page:
            break                                   # a number that is not the page no. is content
        i += 1
    return "\n".join(lines[i:]).strip()


def _check_quality(text: str, page: int, log: _ErrorLog) -> None:
    if "�" in text:
        log.add("warning", "replacement_char", page, f"{text.count(chr(0xFFFD))} U+FFFD chars")
    pua = sum(1 for c in text if 0xE000 <= ord(c) <= 0xF8FF)
    if pua:
        log.add("warning", "private_use_chars", page, f"{pua} private-use glyphs (font mapping)")
    ctrl = sum(1 for c in text if unicodedata.category(c) == "Cc" and c != "\n")
    if ctrl:
        log.add("warning", "control_chars", page, f"{ctrl} control chars")


def load_pdf(path: Path, document_id: str, source: str,
             log: _ErrorLog | None = None,
             layout_pages: set[int] | None = None) -> list[DocumentPage]:
    """Extract every physical page with its 1-based page number and source.

    Pages in `layout_pages` (chart-heavy) use pypdf layout mode so bar labels stay next to
    their values; other pages use plain mode. Empty/near-empty pages are kept (with
    metadata['empty']=True) and logged, so page numbers never shift. pypdf warnings are
    captured into the error log.
    """
    log = log or _ErrorLog()
    layout_pages = layout_pages or set()
    if not path.exists():
        raise FileNotFoundError(f"Corpus file not found: {path}")

    pypdf_logger = logging.getLogger("pypdf")
    captured: list[str] = []

    class _Capture(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            captured.append(record.getMessage())

    handler = _Capture(level=logging.WARNING)
    pypdf_logger.addHandler(handler)
    prev_propagate, pypdf_logger.propagate = pypdf_logger.propagate, False
    pages: list[DocumentPage] = []
    try:
        reader = PdfReader(str(path))
        for idx, pdf_page in enumerate(reader.pages, start=1):
            captured.clear()
            mode = "layout" if idx in layout_pages else "plain"
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                try:
                    if mode == "layout":
                        raw = layout_to_columns(pdf_page.extract_text(extraction_mode="layout") or "")
                    else:
                        raw = pdf_page.extract_text() or ""
                except Exception as exc:              # noqa: BLE001 - logged, page kept
                    log.add("error", "extract_failed", idx, f"{mode}: {exc!r}")
                    raw = ""
            for msg in captured + [str(x.message) for x in w]:
                code = "missing_fonttools" if "fontTools" in msg else "pypdf_warning"
                detail = msg if code == "pypdf_warning" else msg.split(" in font dictionary")[0]
                log.add("warning", code, idx, detail[:300])

            text = strip_running_header(normalize_text(raw), idx)
            empty = len(text) < MIN_PAGE_CHARS
            if empty:
                log.add("info", "empty_or_near_empty_page", idx, f"{len(text)} chars after cleanup")
            _check_quality(text, idx, log)
            pages.append(DocumentPage(
                document_id=document_id, source=source, page=idx, text=text,
                metadata={"chars": len(text), "raw_chars": len(raw), "empty": empty,
                          "extraction_mode": mode},
            ))
    finally:
        pypdf_logger.removeHandler(handler)
        pypdf_logger.propagate = prev_propagate
    return pages


def _section_for(page: int, sections: list[dict[str, Any]]) -> str | None:
    for s in sections:
        if s["page_start"] <= page <= s["page_end"]:
            return s["section"]
    return None


CHART_BLOCK_HEADER = "[Biểu đồ cột đứng – nhãn và giá trị ghép tự động theo toạ độ]"


def _attach_vertical_charts(pages: list[DocumentPage], pdf_path: Path,
                            chart_pages: set[int], log: _ErrorLog) -> None:
    """Append coordinate-paired vertical bar chart data (PyMuPDF) to chart pages.

    Layout mode already pairs horizontal bars; vertical bars need word coordinates.
    Rows that cannot be paired unambiguously are logged and NOT added to the text.
    """
    from .chart_pairs import extract_document, rotated_texts   # optional dependency: pymupdf

    by_page = {p.page: p for p in pages}
    # pypdf layout mode drops rotated text ("Rotated text discovered"): restore axis titles,
    # which state the denominator of the percentages.
    for page_no, texts in rotated_texts(str(pdf_path), chart_pages).items():
        page = by_page[page_no]
        page.text = f"{page.text}\n\n[Tiêu đề trục dọc] " + "; ".join(texts)
        page.metadata["axis_titles"] = len(texts)
    for page_no, res in extract_document(str(pdf_path), chart_pages).items():
        for u in res.unresolved:
            log.add("warning", "chart_pairing_unresolved", page_no, u)
        page = by_page[page_no]
        page.metadata["chart_pairs"] = res.n_pairs
        if res.rows:
            block = normalize_text(res.to_text())
            page.text = f"{page.text}\n\n{CHART_BLOCK_HEADER}\n{block}"
            page.metadata["chars"] = len(page.text)


OCR_BLOCK_HEADER = "[Số liệu biểu đồ đọc bằng OCR – Tesseract, vị trí và series lấy từ hình vẽ PDF]"


def _attach_ocr_charts(pages: list[DocumentPage], pdf_path: Path,
                       ocr_pages: set[int], log: _ErrorLog) -> None:
    """OCR grouped bar charts whose numbers are vector outlines (src/ocr_charts.py).

    Values that OCR cannot read consistently are logged and left out, never guessed.
    """
    if not ocr_pages:
        return
    from .ocr_charts import TESSERACT, extract_document

    if not TESSERACT:
        log.add("error", "tesseract_missing", None, f"OCR pages {sorted(ocr_pages)} need tesseract")
        return
    version = subprocess.run([TESSERACT, "--version"], capture_output=True, text=True).stdout.split("\n")[0]
    by_page = {p.page: p for p in pages}
    for page_no, charts in extract_document(str(pdf_path), ocr_pages).items():
        page = by_page[page_no]
        rows = [c.to_text() for c in charts if c.rows]
        for c in charts:
            for issue in c.issues:
                log.add("warning", "ocr_value_rejected", page_no, issue)
        page.metadata.update({"ocr": version, "ocr_values": sum(len(c.rows) for c in charts)})
        if rows:
            page.text = f"{page.text}\n\n{OCR_BLOCK_HEADER}\n" + normalize_text("\n".join(rows))
            page.metadata["chars"] = len(page.text)
            page.metadata["empty"] = False


def load_corpus(manifest_path: Path = MANIFEST_PATH) -> tuple[list[DocumentPage], _ErrorLog, dict]:
    """Load the manifest's document, attach section/counted flags, validate page count."""
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    log = _ErrorLog()
    pdf_path = ROOT / manifest["source_path_or_url"]

    digest = hashlib.sha256(pdf_path.read_bytes()).hexdigest()
    expected = manifest.get("version_snapshot", {}).get("sha256")
    if expected and digest != expected:
        log.add("error", "checksum_mismatch", None, f"manifest {expected[:12]}… != file {digest[:12]}…")

    counted = {p["page"] for p in manifest["pages"]}
    chart_heavy = {p["page"] for p in manifest["pages"] if p.get("chart_heavy")}
    pages = load_pdf(pdf_path, manifest["source_id"], manifest["source_path_or_url"], log,
                     layout_pages=chart_heavy)
    ocr_pages = {p["page"] for p in manifest["pages"] if p.get("ocr")}
    _attach_vertical_charts(pages, pdf_path, (chart_heavy & counted) - ocr_pages, log)
    _attach_ocr_charts(pages, pdf_path, ocr_pages, log)
    if len(pages) != manifest["physical_pages"]:
        log.add("error", "page_count_mismatch", None,
                f"manifest {manifest['physical_pages']} != pdf {len(pages)}")
    for p in pages:
        p.metadata.update({
            "section": _section_for(p.page, manifest["sections"]),
            "counted": p.page in counted,
            "chart_heavy": p.page in chart_heavy,
            "year": 2023,                         # edition year printed on the cover
            "language": manifest.get("language", "vi"),
        })
        if p.page in counted and p.metadata["empty"]:
            log.add("error", "counted_page_empty", p.page, "manifest counts a page with no text")

    n_content = sum(1 for p in pages if p.metadata["counted"] and not p.metadata["empty"])
    if n_content < MIN_CONTENT_PAGES:
        log.add("error", "too_few_content_pages", None, f"{n_content} < {MIN_CONTENT_PAGES}")
    return pages, log, manifest


def verify_benchmark(pages: list[DocumentPage], log: _ErrorLog,
                     path: Path = BENCHMARK_PATH) -> tuple[int, int]:
    """Check each evidence_quote exists on a gold page after normalization."""
    if not path.exists():
        log.add("warning", "benchmark_missing", None, str(path))
        return 0, 0
    flat = {p.page: flatten_for_match(p.text) for p in pages}
    ok = total = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        q = json.loads(line)
        total += 1
        quote = flatten_for_match(normalize_text(q["evidence_quote"]))
        gold = q["gold_page"] if isinstance(q["gold_page"], list) else [q["gold_page"]]
        if any(quote in flat.get(g, "") for g in gold):
            ok += 1
        else:
            log.add("error", "evidence_not_found", gold[0], f"{q['id']}: {quote[:80]}")
    return ok, total


def main() -> None:
    t0 = time.perf_counter()
    pages, log, manifest = load_corpus()
    ok, total = verify_benchmark(pages, log)
    elapsed = time.perf_counter() - t0

    RESULTS_DIR.mkdir(exist_ok=True)
    with (RESULTS_DIR / "pages.jsonl").open("w", encoding="utf-8") as f:
        for p in pages:
            f.write(json.dumps(asdict(p), ensure_ascii=False) + "\n")
    with (RESULTS_DIR / "ingestion_errors.jsonl").open("w", encoding="utf-8") as f:
        for r in log.records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    counted = [p for p in pages if p.metadata["counted"]]
    by_code: dict[str, int] = {}
    for r in log.records:
        by_code[r["code"]] = by_code.get(r["code"], 0) + 1
    summary = {
        "source_id": manifest["source_id"],
        "reader": "pypdf " + __import__("pypdf").__version__,
        "ocr": "Tesseract cho tr. có cờ ocr trong manifest (số liệu biểu đồ vẽ bằng vector); các trang khác dùng lớp text",
        "ocr_values": {p.page: p.metadata["ocr_values"] for p in pages if p.metadata.get("ocr_values")},
        "normalization": "Unicode NFC, bỏ ký tự vô hình, gộp khoảng trắng trong dòng, giữ xuống dòng, bỏ header/footer lặp",
        "physical_pages": len(pages),
        "counted_pages": len(counted),
        "counted_chars": sum(p.metadata["chars"] for p in counted),
        "empty_pages": [p.page for p in pages if p.metadata["empty"]],
        "layout_mode_pages": sum(1 for p in pages if p.metadata.get("extraction_mode") == "layout"),
        "vertical_chart_pairs": {p.page: p.metadata["chart_pairs"]
                                 for p in pages if p.metadata.get("chart_pairs")},
        "benchmark_evidence_found": f"{ok}/{total}",
        "issues_by_code": by_code,
        "errors": sum(1 for r in log.records if r["level"] == "error"),
        "elapsed_seconds": round(elapsed, 2),
    }
    (RESULTS_DIR / "ingestion_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if summary["errors"]:
        raise SystemExit(f"Ingestion finished with {summary['errors']} error(s); see results/ingestion_errors.jsonl")


if __name__ == "__main__":
    main()
