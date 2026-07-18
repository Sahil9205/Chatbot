"""
Base Embedding Interface

Defines the contract that every embedding model
must implement.

Examples
--------
- HuggingFace Embeddings
- OpenAI Embeddings
- VoyageAI Embeddings
- Jina Embeddings
"""

from abc import ABC, abstractmethod


class BaseEmbeddingModel(ABC):
    """
    Abstract base class for embedding models.
    """

    @abstractmethod
    def embed_text(self, text: str) -> list[float]:
        """
        Generate an embedding for a single text.

        Parameters
        ----------
        text : str
            Input text.

        Returns
        -------
        list[float]
            Embedding vector.
        """
        pass

    @abstractmethod
    def embed_documents( self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for multiple documents.

        Parameters
        ----------
        texts : list[str]

        Returns
        -------
        list[list[float]]
        """
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        """
        Name of the embedding model.
        """
        pass

    @property
    @abstractmethod
    def embedding_dimension(self) -> int:
        """
        Dimension of the embedding vector.
        """
        pass