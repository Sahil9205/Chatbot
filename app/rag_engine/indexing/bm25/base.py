"""
Abstract BM25 Interface.
"""

from abc import ABC, abstractmethod

from app.rag_engine.ingestion.chunking.chunk_schema import Chunk
from .bm25_result import BM25Result

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
    def search(self,query: str,top_k: int = 5,) -> list[BM25Result]:
        """
        Perform keyword search.
        """
        pass