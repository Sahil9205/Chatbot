"""
Base Parser Interface

Every parser must inherit from this class.

Responsibilities
----------------
- Accept loaded documents.
- Convert them into a standardized internal representation.
"""

from abc import ABC, abstractmethod

from langchain_core.documents import Document


class BaseParser(ABC):
    """
    Abstract base class for all document parsers.
    """

    @abstractmethod
    def parse(self, documents: list[Document]) -> list[Document]:
        """
        Parse loaded documents.

        Parameters
        ----------
        documents : list[Document]
            Documents returned by a loader.

        Returns
        -------
        list[Document]
            Parsed documents.
        """
        pass