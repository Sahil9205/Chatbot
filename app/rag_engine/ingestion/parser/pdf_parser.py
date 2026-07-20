"""
PDF Parser

Converts raw LangChain Documents into a normalized format.

Responsibilities
----------------
- Normalize whitespace
- Preserve metadata
- Prepare documents for cleaning
"""

import re

from langchain_core.documents import Document

from app.core.logging import get_logger

from .base import BaseParser

logger = get_logger(__name__)


class PDFParser(BaseParser):
    """
    Parser for PDF documents.
    """

    def parse(self, documents: list[Document]) -> list[Document]:
        """
        Parse PDF documents.

        Parameters
        ----------
        documents : list[Document]

        Returns
        -------
        list[Document]
        """

        logger.info("Parsing %d document(s)...", len(documents))

        parsed_documents: list[Document] = []

        for document in documents:

            text = document.page_content

            # Normalize whitespace
            text = re.sub(r"\s+", " ", text).strip()

            parsed_documents.append(
                Document(
                    page_content=text,
                    metadata=document.metadata.copy(),
                )
            )

        logger.info("Parsing completed.")

        return parsed_documents