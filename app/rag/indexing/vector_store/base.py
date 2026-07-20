"""
Abstract Vector Store Interface.
"""

from abc import ABC, abstractmethod

from app.rag.indexing.embeddings.embedding_schema import EmbeddedChunk


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
    def add(
        self,
        chunks: list[EmbeddedChunk],
    ) -> None:
        """
        Insert embedded chunks.
        """
        pass

    @abstractmethod
    def search(
        self,
        query_vector: list[float],
        top_k: int = 5,
    ) -> list[EmbeddedChunk]:
        """
        Search similar vectors.
        """
        pass

    @abstractmethod
    def delete(
        self,
        ids: list[str],
    ) -> None:
        """
        Delete vectors.
        """
        pass

    @abstractmethod
    def collection_exists(self) -> bool:
        """
        Check collection existence.
        """
        pass