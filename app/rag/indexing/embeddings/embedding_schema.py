"""
Embedding Schema

Represents a chunk after it has been converted into
an embedding vector.

This object is passed to the vector store.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class EmbeddedChunk:
    """
    Represents an embedded chunk ready for indexing.
    """

    chunk_id: str

    document_id: str

    chunk_index: int

    text: str

    embedding: list[float]

    metadata: dict[str, Any] = field(default_factory=dict)