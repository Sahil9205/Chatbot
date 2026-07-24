"""
Abstract Retriever Interface.
"""

from abc import ABC, abstractmethod

from .schemas.query import SearchQuery
from .schemas.retrieved_chunk import RetrievedChunk


class BaseRetriever(ABC):
    """
    Base interface for all retrieval strategies.
    """

    @abstractmethod
    def retrieve(
        self,
        search_query: SearchQuery,
    ) -> list[RetrievedChunk]:
        """
        Retrieve relevant document chunks.
        """
        pass