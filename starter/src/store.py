"""Store and search chunk vectors in PostgreSQL + pgvector."""
from __future__ import annotations

import hashlib
from typing import Any

import numpy as np
import psycopg
from pgvector.psycopg import register_vector
from psycopg.types.json import Jsonb

from .models import Chunk

# Metadata keys that may be used as SQL filters (whitelist; values are parameterised).
FILTER_COLUMNS = {"document_id", "page", "section", "year", "language", "chart_heavy"}


def _text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class PgVectorStore:
    def __init__(self, database_url: str, dimensions: int, model_name: str = "") -> None:
        if not database_url:
            raise ValueError("DATABASE_URL is empty")
        if dimensions <= 0 or dimensions > 2000:
            raise ValueError(f"Unsupported dimensions {dimensions} (HNSW index max is 2000)")
        self.database_url = database_url
        self.dimensions = dimensions
        self.model_name = model_name

    def _connect(self) -> psycopg.Connection:
        conn = psycopg.connect(self.database_url, connect_timeout=5)
        register_vector(conn)
        return conn

    def create_schema(self) -> None:
        dim = int(self.dimensions)
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS chunks (
                    strategy     TEXT        NOT NULL,
                    chunk_id     TEXT        NOT NULL,
                    document_id  TEXT        NOT NULL,
                    source       TEXT        NOT NULL,
                    page         INTEGER     NOT NULL,
                    section      TEXT,
                    year         INTEGER,
                    language     TEXT,
                    chart_heavy  BOOLEAN     NOT NULL DEFAULT FALSE,
                    text         TEXT        NOT NULL,
                    text_hash    TEXT        NOT NULL,
                    metadata     JSONB       NOT NULL DEFAULT '{{}}'::jsonb,
                    model_name   TEXT        NOT NULL,
                    embedding    vector({dim}) NOT NULL,
                    updated_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
                    PRIMARY KEY (strategy, chunk_id)
                )""")
            # Guard against reusing the table with a different model dimension.
            cur.execute("""
                SELECT format_type(a.atttypid, a.atttypmod)
                FROM pg_attribute a
                WHERE a.attrelid = 'chunks'::regclass AND a.attname = 'embedding'""")
            existing = cur.fetchone()[0]
            if existing != f"vector({dim})":
                raise RuntimeError(
                    f"Table chunks has {existing}, model needs vector({dim}). "
                    "Migrate or use a new table instead of mixing dimensions.")
            cur.execute("""
                CREATE INDEX IF NOT EXISTS chunks_embedding_hnsw
                ON chunks USING hnsw (embedding vector_cosine_ops)""")
            cur.execute("CREATE INDEX IF NOT EXISTS chunks_strategy_doc ON chunks (strategy, document_id)")
            cur.execute("CREATE INDEX IF NOT EXISTS chunks_section ON chunks (strategy, section)")

    def existing_hashes(self, strategy: str, document_id: str) -> dict[str, str]:
        """chunk_id -> text_hash for one document, to skip re-embedding unchanged chunks."""
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT chunk_id, text_hash FROM chunks "
                "WHERE strategy = %s AND document_id = %s AND model_name = %s",
                (strategy, document_id, self.model_name))
            return dict(cur.fetchall())

    def prune(self, strategy: str, document_ids: list[str], keep_ids: list[str]) -> int:
        """Delete chunks of these documents that are not in keep_ids (obsolete after re-chunking)."""
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(
                "DELETE FROM chunks WHERE strategy = %s AND document_id = ANY(%s) "
                "AND NOT (chunk_id = ANY(%s))",
                (strategy, list(document_ids), list(keep_ids)))
            return cur.rowcount

    def count(self, strategy: str) -> int:
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute("SELECT count(*) FROM chunks WHERE strategy = %s", (strategy,))
            return cur.fetchone()[0]

    def upsert(self, strategy: str, chunks: list[Chunk], vectors: list[list[float]]) -> None:
        """Insert or update chunks by (strategy, chunk_id). Obsolete rows are removed by prune()."""
        if len(chunks) != len(vectors):
            raise ValueError(f"{len(chunks)} chunks but {len(vectors)} vectors")
        ids = [c.chunk_id for c in chunks]
        if len(set(ids)) != len(ids):
            raise ValueError("Duplicate chunk_id in batch")
        for c, v in zip(chunks, vectors):
            if len(v) != self.dimensions:
                raise ValueError(f"{c.chunk_id}: vector has {len(v)} dims, expected {self.dimensions}")

        rows = []
        for c, v in zip(chunks, vectors):
            md = c.metadata or {}
            rows.append((
                strategy, c.chunk_id, c.document_id, c.source, c.page,
                md.get("section"), md.get("year"), md.get("language"),
                bool(md.get("chart_heavy", False)), c.text, _text_hash(c.text),
                Jsonb(md), self.model_name, np.asarray(v, dtype=np.float32),
            ))

        if not rows:
            return
        with self._connect() as conn, conn.cursor() as cur:
            cur.executemany("""
                INSERT INTO chunks (strategy, chunk_id, document_id, source, page, section, year,
                                    language, chart_heavy, text, text_hash, metadata, model_name, embedding)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (strategy, chunk_id) DO UPDATE SET
                    document_id = EXCLUDED.document_id, source = EXCLUDED.source,
                    page = EXCLUDED.page, section = EXCLUDED.section, year = EXCLUDED.year,
                    language = EXCLUDED.language, chart_heavy = EXCLUDED.chart_heavy,
                    text = EXCLUDED.text, text_hash = EXCLUDED.text_hash,
                    metadata = EXCLUDED.metadata, model_name = EXCLUDED.model_name,
                    embedding = EXCLUDED.embedding, updated_at = now()""", rows)

    def search(self, strategy: str, query_vector: list[float], top_k: int = 3,
               filters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        if len(query_vector) != self.dimensions:
            raise ValueError(f"Query vector has {len(query_vector)} dims, expected {self.dimensions}")
        if top_k <= 0:
            raise ValueError("top_k must be positive")

        where = ["strategy = %s"]
        params: list[Any] = [strategy]
        for key, value in (filters or {}).items():
            if key not in FILTER_COLUMNS:
                raise ValueError(f"Filter '{key}' not allowed; use one of {sorted(FILTER_COLUMNS)}")
            if isinstance(value, (list, tuple, set)):
                where.append(f"{key} = ANY(%s)")
                params.append(list(value))
            else:
                where.append(f"{key} = %s")
                params.append(value)

        qv = np.asarray(query_vector, dtype=np.float32)
        sql = f"""
            SELECT chunk_id, document_id, source, page, section, text, metadata,
                   1 - (embedding <=> %s) AS score
            FROM chunks
            WHERE {' AND '.join(where)}
            ORDER BY embedding <=> %s
            LIMIT %s"""
        with self._connect() as conn, conn.cursor() as cur:
            # Filtered HNSW scans can return < top_k rows; iterative scan fixes that (pgvector >= 0.8).
            cur.execute("SET hnsw.iterative_scan = relaxed_order")
            cur.execute(sql, [qv, *params, qv, top_k])
            cols = [d.name for d in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]
