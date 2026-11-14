"""Pair category labels with values in *vertical* bar charts using word coordinates.

Horizontal bar charts are already readable through pypdf layout mode (label | value on one
line). Vertical/grouped bar charts put each value above its bar, far from the category label
under the x-axis, so text order alone cannot pair them. Here we use PyMuPDF word boxes:

1. Values  = tokens like "51%" or "3,2 %" (number + optional split "%").
2. Labels  = remaining words of body size (<= MAX_LABEL_HEIGHT), grouped into blocks
             (same line with a small gap, or the next line overlapping in x).
3. An *axis row* is >= MIN_ROW_LABELS label blocks sharing the same top y.
4. Each value is assigned to the nearest axis row *below* it (within MAX_VALUE_RISE pt)
   and to the label block in that row with the nearest x-centre, if close enough.

Output is conservative: a chart is emitted only if every label in its row got 1–N values
and no value was left unassigned; otherwise it is reported as unresolved for the error log.
This is a heuristic — results must be checked by hand on a sample (see results/).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

import pymupdf

VALUE_RE = re.compile(r"^\d{1,3}(?:,\d+)?%$")
NUM_RE = re.compile(r"^\d{1,3}(?:,\d+)?$")
LETTER_RE = re.compile(r"[^\W\d_]")
MAX_LABEL_SIZE = 10.4       # chart text is ArialMT 9–10pt; headings are MyriadPro-Bold >= 10.8pt
SAME_LINE_TOL = 2.0
WORD_GAP = 4.5              # space inside one label (~2.3pt) vs gap between labels (>10pt)
LINE_GAP = 5.0
ROW_TOL = 3.0
MIN_ROW_LABELS = 3
MAX_VALUE_RISE = 260.0      # how far above the axis a bar value may sit


@dataclass
class Box:
    x0: float
    y0: float
    x1: float
    y1: float
    text: str

    @property
    def cx(self) -> float:
        return (self.x0 + self.x1) / 2


@dataclass
class LabelBlock:
    words: list[Box]
    values: list[Box] = field(default_factory=list)

    @property
    def x0(self) -> float: return min(w.x0 for w in self.words)
    @property
    def x1(self) -> float: return max(w.x1 for w in self.words)
    @property
    def y0(self) -> float: return min(w.y0 for w in self.words)
    @property
    def y1(self) -> float: return max(w.y1 for w in self.words)
    @property
    def cx(self) -> float: return (self.x0 + self.x1) / 2

    @property
    def text(self) -> str:
        lines: list[list[Box]] = []
        for w in sorted(self.words, key=lambda b: (round(b.y0), b.x0)):
            if lines and abs(lines[-1][0].y0 - w.y0) < SAME_LINE_TOL:
                lines[-1].append(w)
            else:
                lines.append([w])
        return " ".join(" ".join(x.text for x in sorted(l, key=lambda b: b.x0)) for l in lines)


@dataclass
class ChartRow:
    title: str | None
    series: list[str] | None          # legend names, left-to-right bar order
    labels: list[LabelBlock]


@dataclass
class ChartResult:
    page: int
    rows: list[ChartRow]
    unresolved: list[str]

    @property
    def n_pairs(self) -> int:
        return sum(len(b.values) for r in self.rows for b in r.labels)

    def to_text(self) -> str:
        out = []
        for row in self.rows:
            prefix = f"{row.title} — " if row.title else ""
            for b in row.labels:
                vals = [v.text for v in sorted(b.values, key=lambda v: v.x0)]
                if row.series and len(row.series) == len(vals):
                    body = "; ".join(f"{s}: {v}" for s, v in zip(row.series, vals))
                else:
                    body = " / ".join(vals)
                out.append(f"{prefix}{b.text}: {body}")
        return "\n".join(out)


def _excluded_rects(page: pymupdf.Page) -> tuple[list[pymupdf.Rect], list[Box]]:
    """Text that cannot be a chart label/value: headings (bold or > MAX_LABEL_SIZE) and
    non-horizontal lines such as vertical axis titles. Also returns heading boxes."""
    rects, headings = [], []
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            if abs(line["dir"][1]) > 0.5:
                rects.append(pymupdf.Rect(line["bbox"]))
                continue
            for s in line["spans"]:
                if "Bold" in s["font"] or s["size"] > MAX_LABEL_SIZE:
                    rects.append(pymupdf.Rect(s["bbox"]))
                    if s["text"].strip():
                        x0, y0, x1, y1 = s["bbox"]
                        headings.append(Box(x0, y0, x1, y1, s["text"].strip()))
    return rects, headings


def _words(page: pymupdf.Page) -> tuple[list[Box], list[Box]]:
    excluded, _ = _excluded_rects(page)
    raw = [Box(w[0], w[1], w[2], w[3], w[4]) for w in page.get_text("words")
           if not any(r.contains(pymupdf.Point((w[0] + w[2]) / 2, (w[1] + w[3]) / 2)) for r in excluded)]
    raw.sort(key=lambda b: (round(b.y0), b.x0))
    values, labels, used = [], [], set()
    for i, w in enumerate(raw):
        if i in used:
            continue
        if VALUE_RE.match(w.text):
            values.append(w)
            continue
        if NUM_RE.match(w.text):                      # "3,2" followed by a separate "%"
            merged = False
            for j in range(i + 1, min(i + 4, len(raw))):
                n = raw[j]
                if n.text == "%" and abs(n.y0 - w.y0) < SAME_LINE_TOL and 0 <= n.x0 - w.x1 < 4:
                    values.append(Box(w.x0, w.y0, n.x1, n.y1, f"{w.text}%"))
                    used.add(j)
                    merged = True
                    break
            if merged:
                continue                              # otherwise a bare number: part of a label
        labels.append(w)              # includes digits/dashes inside labels ("Từ 3 - 5 tiếng");
    return values, labels             # blocks without any letter are dropped in _blocks


def _blocks(labels: list[Box]) -> list[LabelBlock]:
    blocks: list[LabelBlock] = []
    for w in sorted(labels, key=lambda b: (round(b.y0), b.x0)):
        target = None
        for b in blocks:
            last_y0 = max(x.y0 for x in b.words)
            last_line = [x for x in b.words if abs(x.y0 - last_y0) < SAME_LINE_TOL]
            same_line = any(abs(x.y0 - w.y0) < SAME_LINE_TOL and 0 <= w.x0 - x.x1 < WORD_GAP
                            for x in last_line)
            # word boxes of consecutive lines overlap by ~1.5pt, hence the small negative bound
            lx0, lx1 = min(x.x0 for x in last_line), max(x.x1 for x in last_line)
            next_line = (SAME_LINE_TOL < w.y0 - last_y0 < LINE_GAP + 12
                         and w.x0 < lx1 + 2 and w.x1 > lx0 - 2)
            if same_line or next_line:
                target = b
                break
        if target:
            target.words.append(w)
        else:
            blocks.append(LabelBlock([w]))
    return [b for b in blocks if any(LETTER_RE.search(w.text) for w in b.words)]


def _axis_rows(blocks: list[LabelBlock]) -> list[list[LabelBlock]]:
    rows: list[list[LabelBlock]] = []
    for b in sorted(blocks, key=lambda b: b.y0):
        if rows and abs(rows[-1][0].y0 - b.y0) < ROW_TOL:
            rows[-1].append(b)
        else:
            rows.append([b])
    return [sorted(r, key=lambda b: b.x0) for r in rows if len(r) >= MIN_ROW_LABELS]


YEAR_RE = re.compile(r"^20\d\d$")


def extract_vertical_charts(page: pymupdf.Page, page_no: int) -> ChartResult:
    values, labels = _words(page)
    _, headings = _excluded_rects(page)
    years = [w for w in labels if YEAR_RE.match(w.text)]
    labels = [w for w in labels if not YEAR_RE.match(w.text)]   # legend entries are not categories
    rows = _axis_rows(_blocks(labels))
    unresolved: list[str] = []
    good_rows: list[list[LabelBlock]] = []
    row_tops = sorted(r[0].y0 for r in rows)

    assigned_any: set[int] = set()
    for row in rows:
        top = row[0].y0
        above = [t for t in row_tops if t < top]
        ceiling = max(above) if above else top - MAX_VALUE_RISE
        cands = [(i, v) for i, v in enumerate(values)
                 if ceiling < v.y1 <= top + 1 and top - v.y1 < MAX_VALUE_RISE and i not in assigned_any]
        if not cands:
            continue
        centres = [b.cx for b in row]
        spacing = min((b - a for a, b in zip(centres, centres[1:])), default=60.0)
        span_x0, span_x1 = row[0].x0 - spacing / 2, row[-1].x1 + spacing / 2
        taken = []
        for i, v in cands:
            if not (span_x0 <= v.cx <= span_x1):
                continue                                  # value belongs to another chart
            best = min(row, key=lambda b: abs(b.cx - v.cx))
            if abs(best.cx - v.cx) <= 0.6 * spacing:
                taken.append((i, best, v))
        if not taken:
            continue
        for b in row:
            b.values = [v for _, bb, v in taken if bb is b]
        counts = {len(b.values) for b in row}
        label_desc = ", ".join(b.text for b in row)[:120]
        if 0 in counts or len(counts) != 1:
            unresolved.append(f"row y={top:.0f} [{label_desc}] values/label={[len(b.values) for b in row]}")
            continue
        assigned_any.update(i for i, _, _ in taken)
        chart_top = min(v.y0 for _, _, v in taken)
        above_h = [h for h in headings if h.y1 <= chart_top + 1 and h.y0 > ceiling - 40]
        title = None
        if above_h:                                   # join wrapped multi-line headings
            parts = [max(above_h, key=lambda h: h.y0)]
            while True:
                prev = [h for h in headings if 5 < parts[0].y0 - h.y0 < 18]
                if not prev:
                    break
                parts.insert(0, max(prev, key=lambda h: h.y0))
            title = re.sub(r"\s+", " ", " ".join(p.text for p in parts)).strip()
        legend = sorted((y for y in years if chart_top - 20 <= y.y0 <= top),
                        key=lambda y: (round(y.y0), y.x0))
        n = counts.pop()
        series = [y.text for y in legend] if len(legend) == n and n > 1 else None
        if n > 1 and series is None:
            unresolved.append(f"row y={top:.0f} [{label_desc}] {n} series but legend not found")
        good_rows.append(ChartRow(title, series, row))
    return ChartResult(page_no, good_rows, unresolved)


def extract_document(pdf_path: str, pages: set[int]) -> dict[int, ChartResult]:
    out = {}
    with pymupdf.open(pdf_path) as doc:
        for p in sorted(pages):
            out[p] = extract_vertical_charts(doc[p - 1], p)
    return out


def rotated_texts(pdf_path: str, pages: set[int]) -> dict[int, list[str]]:
    """Non-horizontal text lines per page (vertical axis titles such as
    '(Tỷ lệ người dùng Internet)'), which pypdf layout mode drops."""
    out: dict[int, list[str]] = {}
    with pymupdf.open(pdf_path) as doc:
        for p in sorted(pages):
            texts = []
            for block in doc[p - 1].get_text("dict")["blocks"]:
                for line in block.get("lines", []):
                    if abs(line["dir"][1]) > 0.5:
                        t = re.sub(r"\s+", " ", "".join(s["text"] for s in line["spans"])).strip()
                        if t and t not in texts:
                            texts.append(t)
            if texts:
                out[p] = texts
    return out
