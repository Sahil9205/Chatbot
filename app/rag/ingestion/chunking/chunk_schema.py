"""
Internal Chunk Schema

Represents a single chunk produced by the chunking pipeline.
"""

from dataclasses import dataclass, field
from typing import Any
import uuid


@dataclass
class Chunk:
    """
    Standard representation of a chunk.
    """

    text: str

    metadata: dict[str, Any] = field(default_factory=dict)

    chunk_id: str = field( default_factory=lambda: str(uuid.uuid4()))

    chunk_index: int = 0

    document_id: str = ""

    page_number: int | None = None
    