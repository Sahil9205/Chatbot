"""
PDF Document Loader

This module provides a production-ready PDF loader using LangChain.

Responsibilities
----------------
- Load PDF documents
- Return LangChain Document objects
- Log loading events
- Raise application-specific exceptions
"""

from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

from app.core.exceptions import DocumentLoadingError
from app.core.logging import get_logger

from .base import BaseDocumentLoader

logger = get_logger(__name__)


class PDFLoader(BaseDocumentLoader):
    """
    Loader for PDF documents.
    """

    def load(self, file_path: Path) -> list[Document]:
        """
        Load a PDF document.

        Parameters
        ----------
        file_path : Path
            Path to the PDF file.

        Returns
        -------
        list[Document]
            List of LangChain Document objects.

        Raises
        ------
        DocumentLoadingError
            If the PDF cannot be loaded.
        """

        try:
            logger.info("Loading PDF: %s", file_path)

            loader = PyPDFLoader(str(file_path))

            documents = loader.load()

            logger.info(
                "Loaded %d pages from '%s'.",
                len(documents),
                file_path.name,
            )

            return documents

        except Exception as e:
            logger.exception("Failed to load PDF: %s", file_path)

            raise DocumentLoadingError(f"Unable to load PDF '{file_path.name}'." ) from e
        


# if __name__=='__main__':
#     # Example usage
#     pdf_loader = PDFLoader()
#     documents = pdf_loader.load(Path("C:\\Users\\ASUS\\Desktop\\resume project\\Rag_Chatbot\\Resume.pdf"))
#     for doc in documents:
#         print(doc.page_content)git 