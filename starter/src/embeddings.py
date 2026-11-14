"""Local embedding adapter for aisingapore/SEA-LION-E5-Embedding-600M.

Model facts (from the model card / sentence-transformers config):
- XLM-RoBERTa encoder fine-tuned from intfloat/multilingual-e5-large, supports Vietnamese.
- Mean pooling, 1024 dimensions, max 512 tokens (longer input is truncated).
- Queries use the model's "Retrieval" instruct prompt; documents use no prompt.
- Vectors are L2-normalised so cosine distance in pgvector is well defined.
"""
from __future__ import annotations

import os
from typing import Protocol

DEFAULT_MODEL = "aisingapore/SEA-LION-E5-Embedding-600M"
QUERY_PROMPT_NAME = "Retrieval"


class Embedder(Protocol):
    model_name: str
    dimensions: int

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Return one vector per input text, in the same order."""
        ...

    def embed_query(self, question: str) -> list[float]:
        """Return a query vector compatible with the stored document vectors."""
        ...


class SeaLionEmbedder:
    """Runs the model locally with sentence-transformers (CPU or CUDA if available)."""

    def __init__(self, model_name: str | None = None, device: str | None = None,
                 batch_size: int = 8) -> None:
        from sentence_transformers import SentenceTransformer

        self.model_name = model_name or os.getenv("EMBEDDING_MODEL") or DEFAULT_MODEL
        self.batch_size = batch_size
        token = os.getenv("HUGGINGFACEHUB_API_TOKEN") or os.getenv("HF_TOKEN") or None
        self._model = SentenceTransformer(self.model_name, device=device, token=token)
        self.max_seq_length = self._model.max_seq_length
        get_dim = getattr(self._model, "get_embedding_dimension", None) \
            or self._model.get_sentence_embedding_dimension
        dims = get_dim()
        if not dims:
            raise RuntimeError(f"Cannot determine embedding dimension for {self.model_name}")
        self.dimensions = int(dims)
        if QUERY_PROMPT_NAME not in self._model.prompts:
            raise RuntimeError(f"Model {self.model_name} has no '{QUERY_PROMPT_NAME}' prompt")

    def count_tokens(self, text: str) -> int:
        """Token count (without special tokens) to check chunks fit in max_seq_length."""
        return len(self._model.tokenizer(text, add_special_tokens=False)["input_ids"])

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        vectors = self._model.encode(
            texts,
            batch_size=self.batch_size,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=len(texts) > self.batch_size,
        )
        return vectors.tolist()

    def embed_query(self, question: str) -> list[float]:
        vector = self._model.encode(
            [question],
            prompt_name=QUERY_PROMPT_NAME,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )[0]
        return vector.tolist()


# Backwards-compatible name used by the starter skeleton.
MyEmbedder = SeaLionEmbedder
