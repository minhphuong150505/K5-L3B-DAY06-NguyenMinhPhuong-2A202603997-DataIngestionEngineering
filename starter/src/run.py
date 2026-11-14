"""Day 06 pipeline: chunk -> embed -> pgvector -> top-3 retrieval -> metrics + traces.

Run from starter/:   python -m src.run
Input : results/pages.jsonl (output of `python -m src.ingestion`), ../benchmark/questions.jsonl
Output: results/chunks_*.jsonl, results/traces_*.jsonl, results/metrics.json,
        results/run_report.md, results/manual_*.md (sheets for manual labels)

Configurations (same corpus, model, store, cosine metric, questions):
  A  fixed 500 chars / overlap 50          no filter
  B  paragraph/heading, max 1000 chars     no filter
  C  same chunks + index as B              SQL filter on `section` only for questions that
                                           carry a filter (pre-supplied user input); others
                                           run unfiltered, identical to B.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import statistics as st
import time
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from .chunking import chunk_pages_a, chunk_pages_b, split_blocks
from .embeddings import SeaLionEmbedder
from .evaluation import evaluate_query, summarize
from .ingestion import flatten_for_match
from .models import Chunk, DocumentPage
from .store import PgVectorStore

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
PAGES_PATH = RESULTS / "pages.jsonl"
QUESTIONS_PATH = ROOT.parent / "benchmark" / "questions.jsonl"
MIN_CONTENT_PAGES = 30
TOP_K = 3

CONFIGS: dict[str, dict[str, Any]] = {
    "A": {"index": "A", "chunker": "fixed_size(size=500, overlap=50)", "use_filter": False},
    "B": {"index": "B", "chunker": "by_paragraph(max_size=1000, min_size=200)", "use_filter": False},
    "C": {"index": "B", "chunker": "same as B (shares index B)", "use_filter": True},
}


def _jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, default=str) + "\n")


def load_pages() -> list[DocumentPage]:
    if not PAGES_PATH.exists():
        raise SystemExit(f"{PAGES_PATH} missing: run `python -m src.ingestion` first.")
    pages = [DocumentPage(**r) for r in _jsonl(PAGES_PATH)]
    counted = [p for p in pages if p.metadata.get("counted")]
    if len(counted) < MIN_CONTENT_PAGES:
        raise SystemExit(f"Only {len(counted)} content pages (< {MIN_CONTENT_PAGES})")
    return counted


def load_questions(pages: list[DocumentPage]) -> list[dict]:
    qs = _jsonl(QUESTIONS_PATH)
    ids = [q["id"] for q in qs]
    assert len(ids) == len(set(ids)), "duplicate question id"
    assert {q["split"] for q in qs} <= {"dev", "test"}, "split must be dev/test"
    filtered = [q for q in qs if q.get("filter")]
    if len(filtered) < 3 or not any(q["split"] == "test" for q in filtered):
        raise SystemExit("Benchmark needs >=3 filter questions incl. >=1 test question")
    known = {k: {p.metadata.get(k) for p in pages} for k in ("section", "year", "language")}
    for q in filtered:
        for k, v in q["filter"].items():
            if v not in known.get(k, set()):
                raise SystemExit(f"{q['id']}: filter {k}={v!r} does not exist in corpus metadata")
    return qs


def index_strategy(store: PgVectorStore, embedder: SeaLionEmbedder, strategy: str,
                   chunks: list[Chunk]) -> dict[str, Any]:
    """Embed only new/changed chunks (by text hash), upsert, prune obsolete rows."""
    t0 = time.perf_counter()
    doc_ids = sorted({c.document_id for c in chunks})
    existing: dict[str, str] = {}
    for d in doc_ids:
        existing |= store.existing_hashes(strategy, d)
    todo = [c for c in chunks
            if existing.get(c.chunk_id) != hashlib.sha256(c.text.encode()).hexdigest()]
    t_embed = time.perf_counter()
    vectors = embedder.embed_documents([c.text for c in todo])
    embed_s = time.perf_counter() - t_embed
    store.upsert(strategy, todo, vectors)
    pruned = store.prune(strategy, doc_ids, [c.chunk_id for c in chunks])
    rows = store.count(strategy)
    if rows != len(chunks):
        raise RuntimeError(f"{strategy}: {rows} rows in DB but {len(chunks)} chunks")
    return {"chunks": len(chunks), "embedded": len(todo), "reused": len(chunks) - len(todo),
            "pruned": pruned, "rows_in_db": rows, "embed_seconds": round(embed_s, 2),
            "total_seconds": round(time.perf_counter() - t0, 2)}


def chunk_stats(chunks: list[Chunk], embedder: SeaLionEmbedder) -> dict[str, Any]:
    chars = [len(c.text) for c in chunks]
    toks = [embedder.count_tokens(c.text) for c in chunks]
    q = st.quantiles(chars, n=10)
    return {"n": len(chunks), "chars_total": sum(chars), "chars_min": min(chars),
            "chars_p10": round(q[0]), "chars_median": round(st.median(chars)),
            "chars_p90": round(q[-1]), "chars_max": max(chars),
            "tokens_total": sum(toks), "tokens_median": round(st.median(toks)),
            "tokens_max": max(toks),
            "over_max_seq_len": sum(t > embedder.max_seq_length - 2 for t in toks),
            "pages_covered": len({c.page for c in chunks})}


# ---------------------------------------------------------------- manual sheets
def coherence_positions(pages: list[DocumentPage], n: int = 10) -> list[dict]:
    """Fixed BEFORE looking at scores: first n content pages (sorted by page id); position =
    first non-heading paragraph >= 80 chars on that page (anchor = its first 60 chars)."""
    out = []
    for p in sorted(pages, key=lambda x: x.page):
        for text, is_heading in split_blocks(p.text):
            if not is_heading and len(text) >= 80:
                out.append({"page": p.page, "anchor": flatten_for_match(text)[:60]})
                break
        if len(out) == n:
            break
    return out


def chunk_for_anchor(chunks: list[Chunk], page: int, anchor: str) -> Chunk | None:
    probe = anchor[:30]
    for c in chunks:
        if c.page == page and probe in flatten_for_match(c.text):
            return c
    return None


def write_manual_sheets(pages, chunks_by_index, traces_by_cfg) -> None:
    pos = coherence_positions(pages)
    lines = ["# Chunk coherence — mẫu chấm thủ công", "",
             "Vị trí chọn trước khi xem điểm: 10 trang nội dung đầu (sắp theo page), đoạn không phải "
             "heading đầu tiên ≥ 80 ký tự. Thang: 0 = cắt giữa ý/thiếu chủ thể; 1 = hiểu một phần; "
             "2 = tự hiểu, giữ trọn ý. C dùng chung chunk với B nên chỉ chấm A và B.", ""]
    for i, p in enumerate(pos, 1):
        lines += [f"## {i}. Trang {p['page']} — anchor: “{p['anchor']}…”", ""]
        for idx in ("A", "B"):
            c = chunk_for_anchor(chunks_by_index[idx], p["page"], p["anchor"])
            body = c.text if c else "(không tìm thấy chunk chứa anchor)"
            cid = c.chunk_id if c else "-"
            lines += [f"**{idx}** `{cid}` ({len(body)} ký tự) — Điểm: __ /2 — Lý do: ____", "",
                      "```text", body, "```", ""]
    (RESULTS / "manual_coherence.md").write_text("\n".join(lines), encoding="utf-8")

    lines = ["# Grounding + metadata — 5 câu test × top-3 (chấm thủ công)", "",
             "Grounding: 0 = không có bằng chứng; 1 = có nhưng thiếu điều kiện/ngữ cảnh; "
             "2 = đủ để trả lời và truy nguồn. Metadata: kiểm tra `source`, `page`, `section` "
             "so với PDF; cột *auto* chỉ là kiểm tra sơ bộ, không thay nhãn thủ công.", ""]
    for cfg, traces in traces_by_cfg.items():
        lines += [f"## Cấu hình {cfg}", ""]
        for t in traces:
            if t["split"] != "test":
                continue
            lines += [f"### {t['id']} — {t['question']}",
                      f"- Đáp án kỳ vọng: {t['expected_answer']}",
                      f"- Gold page: {t['gold_page']} | filter: {t['filter']} | "
                      f"auto Hit@1={t['hit@1']} Hit@3={t['hit@3']}",
                      "- **Grounding: __ /2 — Lý do: ____**", ""]
            for h in t["top_k"]:
                lines += [f"{h['rank']}. `{h['chunk_id']}` score={h['score']} | source=`{h['source']}` "
                          f"page={h['page']} section=`{h['section']}` | auto: gold_page={h['on_gold_page']} "
                          f"evidence={h['contains_evidence']} filter_ok={h['follows_filter']} | "
                          "Metadata đúng/đủ: __", "", "```text", h["text"], "```", ""]
    (RESULTS / "manual_grounding_metadata.md").write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------- report
def _fmt(m: dict | str) -> str:
    return m if isinstance(m, str) else f"{m['num']}/{m['den']}"


def write_report(meta, stats, ingest, ingest_again, metrics, traces_by_cfg) -> None:
    L = ["# Kết quả chạy A/B/C", "", f"- Thời điểm: {meta['run_at']}",
         f"- Model: `{meta['model']}` ({meta['dimensions']} chiều, max {meta['max_seq_length']} token, "
         f"query prompt `Retrieval`, document không prompt, vector chuẩn hoá L2), chạy local "
         f"{meta['device']} — chi phí 0", f"- Store: PostgreSQL {meta['postgres']} + pgvector "
         f"{meta['pgvector']}, bảng `chunks`, HNSW cosine (approximate, iterative scan khi lọc)",
         f"- Corpus: {meta['pages']} trang nội dung từ `results/pages.jsonl` (sha256 {meta['pages_sha256'][:12]}…)",
         f"- Câu hỏi: {meta['questions']} ({meta['dev']} dev / {meta['test']} test), top-{TOP_K}", "",
         "## Chunk và tài nguyên", "",
         "| Index | Chunker | Số chunk | Ký tự min/median/p90/max | Token median/max | >512 token | Embed (s) | Nạp lại: embed/giữ/xoá |",
         "|---|---|---|---|---|---|---|---|"]
    for idx in ("A", "B"):
        s, a, b = stats[idx], ingest[idx], ingest_again[idx]
        L.append(f"| {idx} | {CONFIGS[idx]['chunker']} | {s['n']} | {s['chars_min']}/{s['chars_median']}/"
                 f"{s['chars_p90']}/{s['chars_max']} | {s['tokens_median']}/{s['tokens_max']} | "
                 f"{s['over_max_seq_len']} | {a['embed_seconds']} | {b['embedded']}/{b['reused']}/{b['pruned']} |")
    L += ["", "C dùng lại index B (không tốn thêm embedding/lưu trữ); chỉ khác ở mệnh đề `WHERE section = …`.", "",
          "## Retrieval accuracy", "",
          "| Cấu hình | Split | Hit@1 | Evidence Hit@3 | Gold page@3 | Filter tuân thủ@3 | Câu trượt @3 |",
          "|---|---|---|---|---|---|---|"]
    for cfg, m in metrics.items():
        for split in ("dev", "test", "all"):
            x = m[split]
            L.append(f"| {cfg} | {split} | {_fmt(x['hit@1'])} | {_fmt(x['hit@3'])} | {_fmt(x['gold_page@3'])} | "
                     f"{_fmt(x['filter_compliant@3'])} | {', '.join(x['misses']) or '—'} |")
    L += ["", "## Từng câu (rank của chunk hit đầu tiên, `-` = không hit trong top-3)", "",
          "| Câu | Split | Loại | Filter | A | B | C |", "|---|---|---|---|---|---|---|"]
    ids = [t["id"] for t in traces_by_cfg["A"]]
    for i, qid in enumerate(ids):
        t0 = traces_by_cfg["A"][i]
        cells = []
        for cfg in ("A", "B", "C"):
            t = traces_by_cfg[cfg][i]
            r = next((h["rank"] for h in t["top_k"] if h["hit"]), None)
            pages = ",".join(str(h["page"]) for h in t["top_k"])
            cells.append(f"{r or '-'} (tr. {pages})")
        flt = ", ".join(f"{k}={v}" for k, v in (t0["filter"] or {}).items()) or ""
        L.append(f"| {qid} | {t0['split']} | {t0['type']} | {flt} | " + " | ".join(cells) + " |")
    L += ["", "Hit = chunk thuộc trang gold **và** chứa trọn `evidence_quote` (sau NFC + gộp khoảng trắng). "
          "Coherence, grounding và metadata cần chấm tay trong `manual_coherence.md` và "
          "`manual_grounding_metadata.md`."]
    (RESULTS / "run_report.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def main() -> None:
    load_dotenv(ROOT / ".env")
    t_start = time.perf_counter()
    pages = load_pages()
    questions = load_questions(pages)

    chunks_by_index = {"A": chunk_pages_a(pages, 500, 50), "B": chunk_pages_b(pages, 1000, 200)}
    for idx, chunks in chunks_by_index.items():
        _write_jsonl(RESULTS / f"chunks_{idx}.jsonl", [asdict(c) for c in chunks])

    embedder = SeaLionEmbedder()
    store = PgVectorStore(os.environ["DATABASE_URL"], embedder.dimensions, embedder.model_name)
    store.create_schema()

    stats = {i: chunk_stats(c, embedder) for i, c in chunks_by_index.items()}
    ingest = {i: index_strategy(store, embedder, i, c) for i, c in chunks_by_index.items()}
    # Re-ingest the same version: must embed nothing and keep row counts (no duplicates).
    ingest_again = {i: index_strategy(store, embedder, i, c) for i, c in chunks_by_index.items()}
    for i, r in ingest_again.items():
        print(f"[reingest {i}] embedded={r['embedded']} rows={r['rows_in_db']} (chunks={r['chunks']})")

    t_q = time.perf_counter()
    qvecs = {q["id"]: embedder.embed_query(q["question"]) for q in questions}
    traces_by_cfg: dict[str, list[dict]] = {}
    for cfg, spec in CONFIGS.items():
        traces = []
        for q in questions:
            flt = q.get("filter") if spec["use_filter"] else None
            hits = store.search(spec["index"], qvecs[q["id"]], top_k=TOP_K, filters=flt)
            tr = evaluate_query(q, hits)
            tr |= {"config": cfg, "index": spec["index"], "applied_filter": flt}
            traces.append(tr)
        traces_by_cfg[cfg] = traces
        _write_jsonl(RESULTS / f"traces_{cfg}.jsonl", traces)
    query_s = time.perf_counter() - t_q

    metrics = {cfg: summarize(tr) for cfg, tr in traces_by_cfg.items()}

    import pgvector
    import psycopg
    import sentence_transformers
    import torch
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        pg_ver, vec_ver = conn.execute(
            "SELECT current_setting('server_version'), extversion FROM pg_extension "
            "WHERE extname='vector'").fetchone()
    meta = {
        "run_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "model": embedder.model_name, "dimensions": embedder.dimensions,
        "max_seq_length": embedder.max_seq_length, "device": str(embedder._model.device),
        "postgres": pg_ver, "pgvector": vec_ver,
        "versions": {"python": platform.python_version(), "torch": torch.__version__,
                     "sentence_transformers": sentence_transformers.__version__,
                     "psycopg": psycopg.__version__, "pgvector_py": pgvector.__version__
                     if hasattr(pgvector, "__version__") else "0.4.x"},
        "pages": len(pages),
        "pages_sha256": hashlib.sha256(PAGES_PATH.read_bytes()).hexdigest(),
        "questions": len(questions), "dev": sum(q["split"] == "dev" for q in questions),
        "test": sum(q["split"] == "test" for q in questions), "cost_usd": 0,
        "query_seconds_all_configs": round(query_s, 2),
        "total_seconds": round(time.perf_counter() - t_start, 2),
    }
    result = {"meta": meta, "configs": CONFIGS, "chunk_stats": stats, "ingest": ingest,
              "reingest_same_version": ingest_again, "metrics": metrics}
    (RESULTS / "metrics.json").write_text(json.dumps(result, ensure_ascii=False, indent=2),
                                          encoding="utf-8")
    write_report(meta, stats, ingest, ingest_again, metrics, traces_by_cfg)
    write_manual_sheets(pages, chunks_by_index, traces_by_cfg)

    for cfg, m in metrics.items():
        print(f"{cfg}: " + " | ".join(
            f"{s}: Hit@1 {_fmt(m[s]['hit@1'])}, Hit@3 {_fmt(m[s]['hit@3'])}, filter {_fmt(m[s]['filter_compliant@3'])}"
            for s in ("dev", "test")))
    print(f"Done in {meta['total_seconds']}s -> results/run_report.md")


if __name__ == "__main__":
    main()
