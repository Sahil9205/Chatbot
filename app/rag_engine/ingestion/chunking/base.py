"""
Base Chunker Interface

Every chunking strategy must inherit from this class.
"""

from abc import ABC, abstractmethod

from langchain_core.documents import Document


class BaseChunker(ABC):
    """
    Abstract interface for all chunkers.
    """

    @abstractmethod
    def split(
        self,
        documents: list[Document]
    ) -> list[Document]:
        """
        Split documents into chunks.

        Parameters
        ----------
        documents : list[Document]

        Returns
        -------
        list[Document]
        """
        pass