"""
Abstract Fusion Strategy Interface.
"""

from abc import ABC, abstractmethod

from app.rag_engine.retrieval.schemas.retrieved_chunk import RetrievedChunk


class BaseFusionStrategy(ABC):
    """
    Base interface for retrieval fusion algorithms.
    """

    @abstractmethod
    def fuse(
        self,
        *ranked_lists: list[RetrievedChunk],
    ) -> list[RetrievedChunk]:
        """
        Fuse multiple ranked retrieval lists into a
        single ranked list.

        Parameters
        ----------
        ranked_lists : list[RetrievedChunk]

        Returns
        -------
        list[RetrievedChunk]
        """
        pass