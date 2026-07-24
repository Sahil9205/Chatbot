"""
Retrieval source enumeration.
"""

from enum import Enum


class RetrievalSource(str, Enum):
    """
    Source of a retrieved document chunk.
    """

    DENSE = "dense"

    SPARSE = "sparse"

    HYBRID = "hybrid"

    RERANKED = "reranked"