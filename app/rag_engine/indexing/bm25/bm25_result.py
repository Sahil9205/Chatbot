"""
BM25 Search Result Schema.

Represents a raw result returned by the BM25 index.

This schema belongs to the indexing layer and must not
depend on the retrieval layer.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class BM25Result:
    """
    Raw BM25 search result.
    """

    chunk_id: str

    document_id: str

    chunk_index: int

    text: str

    score: float

    metadata: dict[str, Any] = field(default_factory=dict)