"""Automatic retrieval metrics (Hit@1, Evidence Hit@3) with full per-query traces.

A retrieved chunk is a hit when it belongs to the gold source, its page is one of the gold
pages, and it contains the WHOLE evidence quote (compared after NFC + whitespace/column
flattening, the same normalisation used to verify the benchmark). Coherence and grounding are
manual labels and are NOT inferred here.
"""
from __future__ import annotations

from typing import Any

from .ingestion import flatten_for_match, normalize_text


def _norm(text: str) -> str:
    return flatten_for_match(normalize_text(text))


def evaluate_query(question: dict[str, Any], hits: list[dict[str, Any]]) -> dict[str, Any]:
    gold_pages = question["gold_page"]
    gold_pages = gold_pages if isinstance(gold_pages, list) else [gold_pages]
    quote = _norm(question["evidence_quote"])
    flt = question.get("filter") or {}

    labelled = []
    for rank, h in enumerate(hits, start=1):
        on_gold_page = (h["document_id"] == question["gold_source_id"]
                        and h["page"] in gold_pages)
        has_evidence = quote in _norm(h["text"])
        follows_filter = all(h.get(k) == v for k, v in flt.items()) if flt else None
        labelled.append({
            "rank": rank, "chunk_id": h["chunk_id"], "score": round(float(h["score"]), 4),
            "document_id": h["document_id"], "source": h["source"], "page": h["page"],
            "section": h.get("section"), "metadata": h.get("metadata", {}),
            "on_gold_page": on_gold_page, "contains_evidence": has_evidence,
            "hit": on_gold_page and has_evidence, "follows_filter": follows_filter,
            "text": h["text"],
        })
    # Gold page reached but the quote is not whole in any chunk -> evidence split / partial.
    page_only = any(x["on_gold_page"] and not x["contains_evidence"] for x in labelled)
    return {
        "id": question["id"], "split": question["split"], "type": question.get("type"),
        "question": question["question"], "expected_answer": question["expected_answer"],
        "gold_page": gold_pages, "evidence_quote": question["evidence_quote"],
        "filter": flt or None,
        "hit@1": bool(labelled and labelled[0]["hit"]),
        "hit@3": any(x["hit"] for x in labelled[:3]),
        "gold_page@3": any(x["on_gold_page"] for x in labelled[:3]),
        "gold_page_without_full_evidence": page_only and not any(x["hit"] for x in labelled),
        "filter_compliant@3": (all(x["follows_filter"] for x in labelled) if flt else None),
        "top_k": labelled,
    }


def summarize(traces: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate per split as numerator/denominator (not only %)."""
    out: dict[str, Any] = {}
    for split in ("dev", "test", "all"):
        rows = [t for t in traces if split == "all" or t["split"] == split]
        n = len(rows)
        filt = [t for t in rows if t["filter"]]

        def frac(k: int, d: int) -> dict[str, Any]:
            return {"num": k, "den": d, "rate": round(k / d, 3) if d else None}

        out[split] = {
            "hit@1": frac(sum(t["hit@1"] for t in rows), n),
            "hit@3": frac(sum(t["hit@3"] for t in rows), n),
            "gold_page@3": frac(sum(t["gold_page@3"] for t in rows), n),
            "filter_compliant@3": (frac(sum(bool(t["filter_compliant@3"]) for t in filt), len(filt))
                                   if filt else "N/A"),
            "misses": [t["id"] for t in rows if not t["hit@3"]],
        }
    return out
