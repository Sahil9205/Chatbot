"""
Abstract BM25 Interface.
"""

from abc import ABC, abstractmethod

from app.rag_engine.ingestion.chunking.chunk_schema import Chunk
from app.rag_engine.retrieval.schemas.retrieved_chunk import RetrievedChunk


class BaseKeywordIndex(ABC):
    """
    Base interface for keyword search engines.
    """

    @abstractmethod
    def build(self,chunks: list[Chunk],) -> None:
        """
        Build keyword index.
        """
        pass

    @abstractmethod
    def search(self,query: str,top_k: int = 5,) -> list[RetrievedChunk]:
        """
        Perform keyword search.
        """
        pass