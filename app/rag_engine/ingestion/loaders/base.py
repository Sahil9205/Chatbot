"""
Base document loader.

Every document loader (PDF, DOCX, TXT, etc.) must inherit from this
interface so that the ingestion pipeline can treat all document types
uniformly.
"""

from abc import ABC, abstractmethod
from pathlib import Path

from langchain_core.documents import Document


class BaseDocumentLoader(ABC):
    """
    Abstract base class for all document loaders.
    """

    @abstractmethod
    def load(self, file_path: Path) -> list[Document]:
        """
        Load a document and return a list of LangChain Documents.

        Parameters
        ----------
        file_path : Path
            Path to the input document.

        Returns
        -------
        list[Document]
            Loaded documents.

        Raises
        ------
        DocumentLoadingError
            If the document cannot be loaded.
        """
        raise NotImplementedError