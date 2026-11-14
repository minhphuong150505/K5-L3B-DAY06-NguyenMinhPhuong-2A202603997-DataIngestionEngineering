"""OCR for grouped bar charts whose numbers are drawn as vector outlines (no text layer).

Used for pp. 35–37 of the corpus (e-Conomy SEA charts per country). Strategy:

* Geometry comes from the PDF itself (PyMuPDF `get_drawings`), not from OCR:
  - every number is one small near-black filled path  -> exact position & count;
  - every series is one coloured path (all bars of that colour); legend squares share the
    colour and have the series name to their right    -> series of each bar slot;
  - grey baseline ticks mark the bar slots; slots cluster into one group per year.
* OCR (Tesseract 5 CLI, digit whitelist) reads only the padded crop around each number,
  4 times (2 zooms x psm 7/8). Trailing ',' '.' are dropped (psm 8 artefact). A value is
  accepted if >= 2 reads are non-empty and ALL non-empty reads are identical, or if
  >= 3 of the 4 reads agree;
  otherwise it is reported and left out, never guessed.
* The minus sign is decided by geometry (a thin dash path left of the digits), not by OCR,
  because OCR drops it intermittently and a lost sign silently flips the meaning.

Output per chart: title, unit, rows "year — series: value" and growth "%" per year.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

import pymupdf

TESSERACT = shutil.which("tesseract")
WHITELIST = "0123456789%-,."
GLYPH_MAX_W, GLYPH_MAX_H = 30.0, 9.0
BASELINE_COLOR = (0.86, 0.87, 0.87)
ZOOMS = (8, 12)
PSMS = ("7", "8")
MIN_AGREE = 2                    # non-empty reads required; all must be identical
PAD = 4.0                        # pt of white margin around a number crop
YEAR_RE = re.compile(r"^20\d\d$")
VALUE_RE = re.compile(r"^-?\d{1,4}(,\d+)?%?$")


def _rgb(c) -> tuple[float, float, float]:
    return tuple(round(x, 2) for x in c)


def _dark(c) -> bool:
    return max(c) < 0.25


@dataclass
class Glyph:
    rect: pymupdf.Rect
    negative: bool = False
    text: str = ""
    reads: list[str] = field(default_factory=list)

    @property
    def cx(self) -> float:
        return (self.rect.x0 + self.rect.x1) / 2


@dataclass
class OcrChart:
    page: int
    title: str
    unit: str | None
    rows: list[str]
    issues: list[str]

    def to_text(self) -> str:
        head = self.title + (f" (đơn vị: {self.unit})" if self.unit else "")
        return "\n".join(f"{head} — {r}" for r in self.rows)


def _ocr_crop(page: pymupdf.Page, rect: pymupdf.Rect, zoom: int, psm: str, tmp: Path) -> str:
    """Render only the number glyph (other vector art is hidden by drawing a white page
    first is not possible, so we crop tightly and pad with white instead)."""
    clip = pymupdf.Rect(rect.x0 - 0.6, rect.y0 - 0.6, rect.x1 + 0.6, rect.y1 + 0.6)
    pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), clip=clip, alpha=False)
    pad = int(PAD * zoom)
    canvas = pymupdf.Pixmap(pymupdf.csRGB, pymupdf.IRect(0, 0, pix.width + 2 * pad, pix.height + 2 * pad), False)
    canvas.set_rect(canvas.irect, (255, 255, 255))
    pix.set_origin(pad, pad)
    canvas.copy(pix, pix.irect)
    f = tmp / f"g_{rect.x0:.0f}_{rect.y0:.0f}_{zoom}.png"
    canvas.save(f)
    out = subprocess.run(
        [TESSERACT, str(f), "stdout", "--psm", psm, "-c", f"tessedit_char_whitelist={WHITELIST}"],
        capture_output=True, text=True, check=True).stdout
    return re.sub(r"\s+", "", out)


def _is_dash(r: pymupdf.Rect) -> bool:
    return r.height < 1.5 and r.width > 1.2 and r.width / max(r.height, 0.1) > 2


def _merge_glyphs(rects: list[pymupdf.Rect]) -> list[tuple[pymupdf.Rect, bool]]:
    """Characters of one number may be separate paths: merge those on one line, touching."""
    rects = sorted(rects, key=lambda r: (round(r.y0), r.x0))
    out: list[pymupdf.Rect] = []
    rects = sorted(rects, key=lambda r: r.x0)
    neg: list[bool] = []
    for r in rects:
        # same text line = vertical overlap (a minus sign is thin and sits mid-height)
        j = next((i for i, o in enumerate(out) if r.y0 < o.y1 and r.y1 > o.y0
                  and -0.5 <= r.x0 - o.x1 < 2.0), None)
        if j is None:
            out.append(pymupdf.Rect(r))
            neg.append(_is_dash(r))           # leftmost component is a dash -> negative
        else:
            out[j] = out[j] | r
    return [(r, n) for r, n in zip(out, neg) if not (n and r.width < 3)]   # drop lone dashes


def _regions(page: pymupdf.Page) -> list[tuple[str, float, float]]:
    """Chart regions split at bold numbered headings like '5. Thái Lan'."""
    heads = []
    for b in page.get_text("dict")["blocks"]:
        for ln in b.get("lines", []):
            t = "".join(s["text"] for s in ln["spans"]).strip()
            if re.match(r"^\d+\.\s*\S", t) and any("Bold" in s["font"] for s in ln["spans"]):
                heads.append((ln["bbox"][1], t))
    heads.sort()
    bounds = [(t, y, heads[i + 1][0] if i + 1 < len(heads) else page.rect.y1)
              for i, (y, t) in enumerate(heads)]
    return bounds


def _lines_in(page: pymupdf.Page, y0: float, y1: float) -> list[tuple[pymupdf.Rect, str]]:
    out = []
    for b in page.get_text("dict")["blocks"]:
        for ln in b.get("lines", []):
            r = pymupdf.Rect(ln["bbox"])
            if y0 <= r.y0 < y1:
                out.append((r, "".join(s["text"] for s in ln["spans"]).strip()))
    return out


def extract_page(page: pymupdf.Page, page_no: int) -> list[OcrChart]:
    if not TESSERACT:
        raise RuntimeError("tesseract not found on PATH")
    drawings = page.get_drawings()
    charts = []
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for title, top, bottom in _regions(page):
            inside = [d for d in drawings if d.get("fill") and top < d["rect"].y0 < bottom]
            texts = _lines_in(page, top, bottom)
            issues: list[str] = []

            # legend: coloured squares (w>10, h<7) + text immediately to the right
            legend: dict[tuple, str] = {}
            legend_ids: set[int] = set()
            for d in inside:
                r, col = d["rect"], _rgb(d["fill"])
                if 10 < r.width < 30 and r.height < 7 and not _dark(col):
                    right = [t for tr, t in texts if abs(tr.y0 + tr.height / 2 - (r.y0 + r.height / 2)) < 5
                             and 0 <= tr.x0 - r.x1 < 8]
                    if right:
                        legend[col] = right[0]
                        legend_ids.add(id(d))
            growth_name = next((t for _, t in texts if t.startswith("Tốc độ tăng trưởng")), "Tốc độ tăng trưởng")
            unit = next((t.split(":", 1)[1].strip() for _, t in texts if t.startswith("Đơn vị tính")), None)

            # series order: each series path starts at its slot's x
            first_x: dict[tuple, float] = {}
            for d in inside:
                col = _rgb(d["fill"])
                if col in legend and id(d) not in legend_ids:       # bars (even very short ones)
                    first_x[col] = min(first_x.get(col, 1e9), d["rect"].x0)
            slot_series = [legend[c] for c in sorted(first_x, key=first_x.get)]
            n_series = len(slot_series)

            # slots (grey baseline ticks) grouped by year
            slots = sorted((d["rect"] for d in inside if _rgb(d["fill"]) == BASELINE_COLOR
                            and d["rect"].height < 3 and d["rect"].width < 25), key=lambda r: r.x0)
            if not n_series or len(slots) % n_series:
                issues.append(f"{title}: {len(slots)} slots vs {n_series} series")
                charts.append(OcrChart(page_no, title, unit, [], issues))
                continue
            groups = [slots[i:i + n_series] for i in range(0, len(slots), n_series)]
            baseline_y = slots[0].y0

            # number glyphs
            glyph_rects = _merge_glyphs([d["rect"] for d in inside if _dark(_rgb(d["fill"]))
                                         and d["rect"].width < GLYPH_MAX_W and d["rect"].height < GLYPH_MAX_H])
            glyphs = []
            for r, negative in glyph_rects:
                g = Glyph(r, negative, reads=[_ocr_crop(page, r, z, m, tmp) for z in ZOOMS for m in PSMS])
                cleaned = [t.strip(",.").lstrip("-") for t in g.reads]
                nonempty = [t for t in cleaned if t]
                top_t, top_n = max(((t, nonempty.count(t)) for t in set(nonempty)),
                                   key=lambda x: x[1], default=("", 0))
                if (len(nonempty) >= MIN_AGREE and len(set(nonempty)) == 1) or top_n >= 3:
                    g.text = ("-" if negative else "") + top_t
                else:
                    issues.append(f"{title}: OCR not accepted at ({r.x0:.0f},{r.y0:.0f}): {g.reads}")
                glyphs.append(g)

            years = [g for g in glyphs if g.rect.y0 > baseline_y]
            above = [g for g in glyphs if g.rect.y1 <= baseline_y]

            # year label per group
            group_year: dict[int, str] = {}
            for gi, grp in enumerate(groups):
                gx0, gx1 = grp[0].x0, grp[-1].x1
                ys = [g for g in years if gx0 <= g.cx <= gx1]
                text_years = [t for tr, t in texts if YEAR_RE.match(t) and tr.y0 > baseline_y
                              and gx0 <= (tr.x0 + tr.x1) / 2 <= gx1]   # some year labels are real text
                if len(ys) == 1 and YEAR_RE.match(ys[0].text):
                    group_year[gi] = ys[0].text
                elif not ys and len(text_years) == 1:
                    group_year[gi] = text_years[0]
                else:
                    issues.append(f"{title}: year label for group {gi} not resolved ({[y.text for y in ys]})")

            values: dict[tuple[int, int], str] = {}
            growth: dict[int, str] = {}
            for g in above:
                if not g.text or not VALUE_RE.match(g.text):
                    if g.text:
                        issues.append(f"{title}: unexpected token '{g.text}'")
                    continue
                if g.text.endswith("%"):
                    gi = min(range(len(groups)), key=lambda i: abs((groups[i][0].x0 + groups[i][-1].x1) / 2 - g.cx))
                    if gi in growth:
                        issues.append(f"{title}: two growth values for group {gi}")
                    growth[gi] = g.text
                    continue
                hit = [(gi, si) for gi, grp in enumerate(groups) for si, s in enumerate(grp)
                       if s.x0 - 1 <= g.cx <= s.x1 + 1]
                if len(hit) != 1:
                    issues.append(f"{title}: value '{g.text}' not under exactly one bar")
                    continue
                if hit[0] in values:
                    issues.append(f"{title}: two values for slot {hit[0]}")
                values[hit[0]] = g.text

            rows = []
            for gi in range(len(groups)):
                year = group_year.get(gi, f"nhóm {gi + 1}")
                for si, name in enumerate(slot_series):
                    v = values.get((gi, si))
                    if v is None:
                        issues.append(f"{title}: missing value {year} / {name}")
                    else:
                        rows.append(f"{year} — {name}: {v}")
                if gi in growth:
                    rows.append(f"{year} — {growth_name}: {growth[gi]}")
            charts.append(OcrChart(page_no, title, unit, rows, issues))
    return charts


def extract_document(pdf_path: str, pages: set[int]) -> dict[int, list[OcrChart]]:
    with pymupdf.open(pdf_path) as doc:
        return {p: extract_page(doc[p - 1], p) for p in sorted(pages)}
