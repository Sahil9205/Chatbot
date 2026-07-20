"""
Base Hybrid Retrieval Interface.
"""

from abc import ABC, abstractmethod

from app.rag_engine.retrieval.schemas.retrieved_chunk import RetrievedChunk


class BaseHybridIndex(ABC):
    """
    Interface for hybrid retrieval implementations.
    """

    @abstractmethod
    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[RetrievedChunk]:
        """
        Perform hybrid retrieval.
        """
        pass