"""
Abstract Vector Store Interface.
"""

from abc import ABC, abstractmethod

from qdrant_client.models import Filter, ScoredPoint

from app.rag_engine.indexing.embeddings.embedding_schema import EmbeddedChunk


class BaseVectorStore(ABC):
    """
    Abstract interface for every vector database.
    """

    @abstractmethod
    def create_collection(self) -> None:
        """
        Create a collection if it does not exist.
        """
        pass

    @abstractmethod
    def collection_exists(self) -> bool:
        """
        Check whether the collection exists.
        """
        pass

    @abstractmethod
    def add(
        self,
        chunks: list[EmbeddedChunk],
    ) -> None:
        """
        Insert embedded chunks into the vector store.
        """
        pass

    @abstractmethod
    def search(
        self,
        query_vector: list[float],
        top_k: int = 5,
        query_filter: Filter | None = None,) -> list[ScoredPoint]:
        """
        Search for similar vectors.
        """
        pass

    @abstractmethod
    def delete(self,ids: list[str],) -> None:
        """
        Delete vectors by their IDs.
        """
        pass