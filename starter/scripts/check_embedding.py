"""Smoke test: load SEA-LION-E5 embedder, write to pgvector, search, then clean up.

Run from starter/:  python -m scripts.check_embedding
Uses a throwaway strategy name so real data is never touched.
"""
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env")

from src.embeddings import SeaLionEmbedder  # noqa: E402
from src.models import Chunk  # noqa: E402
from src.store import PgVectorStore  # noqa: E402

STRATEGY = "__smoke_test__"

t0 = time.time()
emb = SeaLionEmbedder()
print(f"Model: {emb.model_name} | dims={emb.dimensions} | max_seq_length={emb.max_seq_length} "
      f"| load {time.time() - t0:.1f}s")

docs = [
    "Doanh thu thương mại điện tử B2C của Việt Nam năm 2023 đạt khoảng 20,5 tỷ USD.",
    "Thanh toán không dùng tiền mặt ngày càng phổ biến trong mua sắm trực tuyến.",
    "Hà Nội là thủ đô của Việt Nam, có lịch sử hơn một nghìn năm.",
]
chunks = [Chunk(f"smoke-{i}", "smoke-doc", "smoke", i + 1, t,
                {"section": "test", "year": 2023, "language": "vi"}) for i, t in enumerate(docs)]

t0 = time.time()
vectors = emb.embed_documents(docs)
print(f"Embedded {len(vectors)} docs in {time.time() - t0:.1f}s")

store = PgVectorStore(os.environ["DATABASE_URL"], emb.dimensions, emb.model_name)
store.create_schema()
store.upsert(STRATEGY, chunks, vectors)
store.upsert(STRATEGY, chunks, vectors)  # idempotent: must not duplicate

try:
    q = "Quy mô doanh thu TMĐT bán lẻ năm 2023 là bao nhiêu?"
    hits = store.search(STRATEGY, emb.embed_query(q), top_k=3, filters={"year": 2023})
    print(f"Query: {q}")
    for h in hits:
        print(f"  {h['score']:.4f}  p{h['page']}  {h['text'][:70]}")
    assert len(hits) == 3, f"expected 3 rows, got {len(hits)} (duplicates or missing)"
    assert hits[0]["chunk_id"] == "smoke-0", "top-1 should be the revenue sentence"
finally:
    import psycopg
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        conn.execute("DELETE FROM chunks WHERE strategy = %s", (STRATEGY,))
print("Embedding + pgvector OK")
