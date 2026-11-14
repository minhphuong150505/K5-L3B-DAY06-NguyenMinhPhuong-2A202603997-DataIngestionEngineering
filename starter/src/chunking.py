"""Chunking strategies.

A  fixed_size   : character windows (size/overlap) per page, end snapped back to whitespace so
                  words are not cut. Ignores structure on purpose (baseline).
B  by_paragraph : rebuilds paragraphs from pypdf lines (headings, sentence ends, blank lines),
                  packs whole paragraphs up to max_size, starts a new chunk at each heading and
                  prefixes the nearest heading as context when a chunk starts mid-section.

Chunks never cross pages, so every chunk keeps an exact `page` for traceability.
"""
from __future__ import annotations

import re

from .models import Chunk, DocumentPage

# "I. ", "1. ", "1.2. ", "a) ", "PHỤ LỤC", "CHƯƠNG" ...
_HEADING = re.compile(r"^(?:[IVXLC]+\.|\d{1,2}(?:\.\d{1,2})*\.|[a-zđ]\)|PHỤ LỤC\b|CHƯƠNG\b)\s*\S")
_NOISE = re.compile(r"^[•;·\-–\s]*$")            # bullet glyph rows left over from the PDF
_SENT_END = re.compile(r"[.!?:;…]\)?$")
_STARTS_NEW = re.compile(r"^[\"“(\[A-ZÀ-ỸĐ0-9]")
_SENT_SPLIT = re.compile(r"(?<=[.!?;])\s+(?=[\"“(A-ZÀ-ỸĐ0-9])")
MAX_HEADING_CHARS = 160


def _base_metadata(page: DocumentPage) -> dict:
    keep = ("section", "year", "language", "chart_heavy", "extraction_mode")
    return {k: page.metadata.get(k) for k in keep if k in page.metadata}


def _make(page: DocumentPage, strategy: str, idx: int, text: str, **extra) -> Chunk:
    md = _base_metadata(page) | {"chunk_index": idx, "chars": len(text)} | extra
    return Chunk(
        chunk_id=f"{page.document_id}:p{page.page:03d}:{strategy}{idx:02d}",
        document_id=page.document_id, source=page.source, page=page.page,
        text=text, metadata=md)


# --------------------------------------------------------------------------- A
def fixed_size(page: DocumentPage, size: int = 500, overlap: int = 50,
               snap: int = 40) -> list[Chunk]:
    if not 0 <= overlap < size:
        raise ValueError("need 0 <= overlap < size")
    text = page.text.strip()
    chunks: list[Chunk] = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        if end < len(text):                      # snap back to a space/newline if close by
            cut = max(text.rfind(" ", end - snap, end), text.rfind("\n", end - snap, end))
            if cut > start:
                end = cut
        piece = text[start:end].strip()
        if piece:
            chunks.append(_make(page, "A", len(chunks), piece, start_char=start, end_char=end))
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)
        # do not start the overlap in the middle of a word
        if start > 0 and not text[start - 1].isspace():
            nxt = text.find(" ", start, end)
            if nxt != -1:
                start = nxt + 1
    return chunks


# --------------------------------------------------------------------------- B
def split_blocks(text: str) -> list[tuple[str, bool]]:
    """Return [(block_text, is_heading)] rebuilt from visual lines."""
    blocks: list[tuple[str, bool]] = []
    cur: list[str] = []

    def close() -> None:
        if cur:
            blocks.append(("\n".join(cur), False))
            cur.clear()

    for raw in text.split("\n"):
        line = raw.strip()
        if not line:
            close()
            continue
        if _NOISE.match(line):
            continue
        # chart label–value rows ("6.2. <chart> — Khác: 14%") start like headings but are data
        if _HEADING.match(line) and len(line) <= MAX_HEADING_CHARS and " — " not in line:
            close()
            blocks.append((line, True))
            continue
        if cur and _SENT_END.search(cur[-1]) and _STARTS_NEW.match(line):
            close()
        cur.append(line)
    close()
    return blocks


def _split_long(block: str, max_size: int) -> list[str]:
    """Split an oversized paragraph at sentence ends, then at whitespace as a last resort."""
    parts, buf = [], ""
    for sent in _SENT_SPLIT.split(block):
        while len(sent) > max_size:              # single huge "sentence" (tables, lists)
            cut = sent.rfind("\n", 0, max_size)
            if cut < max_size // 2:
                cut = sent.rfind(" ", 0, max_size)
            if cut <= 0:
                cut = max_size
            if buf:
                parts.append(buf)
                buf = ""
            parts.append(sent[:cut].strip())
            sent = sent[cut:].strip()
        if buf and len(buf) + 1 + len(sent) > max_size:
            parts.append(buf)
            buf = sent
        else:
            buf = f"{buf} {sent}".strip() if buf else sent
    if buf:
        parts.append(buf)
    return [p for p in parts if p]


def by_paragraph(page: DocumentPage, max_size: int = 1000, min_size: int = 200,
                 context_heading: str | None = None) -> tuple[list[Chunk], str | None]:
    """Chunk one page by structure. Returns (chunks, last_heading) so the caller can carry
    the heading of a section that continues on the next page."""
    units: list[tuple[str, bool]] = []
    for block, is_heading in split_blocks(page.text):
        if is_heading or len(block) <= max_size:
            units.append((block, is_heading))
        else:
            units.extend((p, False) for p in _split_long(block, max_size))

    chunks: list[Chunk] = []
    body: list[str] = []
    heading = context_heading          # nearest heading seen so far
    chunk_heading: str | None = None   # heading prefixed to the chunk being built
    starts_with_heading = False

    def flush() -> None:
        nonlocal body, chunk_heading, starts_with_heading
        if not body:
            return
        if starts_with_heading or not chunk_heading:
            text, prefixed = "\n".join(body), False
        else:
            text, prefixed = f"{chunk_heading}\n" + "\n".join(body), True
        chunks.append(_make(page, "B", len(chunks), text,
                            heading=chunk_heading, heading_prefixed=prefixed))
        body = []
        starts_with_heading = False

    for text, is_heading in units:
        size = sum(len(b) + 1 for b in body)
        if is_heading:
            # A heading opens a new chunk, unless the current chunk is still tiny
            # (then heading + short intro stay together instead of a fragment).
            if body and size >= min_size:
                flush()
            if not body:
                starts_with_heading = True
                chunk_heading = text
            heading = text
            body.append(text)
            continue
        # A short paragraph that would overflow is kept with its neighbour (tolerance =
        # min_size) instead of becoming a context-less fragment, e.g. a trailing condition.
        fits_with_tolerance = len(text) < min_size and size + len(text) <= max_size + min_size
        if body and size + len(text) > max_size and not fits_with_tolerance:
            flush()
        if not body:
            chunk_heading = heading
        body.append(text)
    flush()
    return chunks, heading


def chunk_pages_b(pages: list[DocumentPage], max_size: int = 1000,
                  min_size: int = 200) -> list[Chunk]:
    """Apply by_paragraph over pages in order, carrying the last heading across pages."""
    out: list[Chunk] = []
    carry: dict[str, str | None] = {}
    for page in sorted(pages, key=lambda p: (p.document_id, p.page)):
        chunks, carry[page.document_id] = by_paragraph(
            page, max_size, min_size, carry.get(page.document_id))
        out.extend(chunks)
    return out


def chunk_pages_a(pages: list[DocumentPage], size: int = 500, overlap: int = 50) -> list[Chunk]:
    out: list[Chunk] = []
    for page in sorted(pages, key=lambda p: (p.document_id, p.page)):
        out.extend(fixed_size(page, size, overlap))
    return out
