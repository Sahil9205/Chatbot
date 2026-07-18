"""
Recursive Character Chunker

Splits documents into overlapping chunks while preserving
metadata.

This is the default chunking strategy used by the ingestion
pipeline.
"""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import settings
from app.core.logging import get_logger

from .base import BaseChunker
from .chunk_schema import Chunk

logger = get_logger(__name__)


class RecursiveChunker(BaseChunker):
    """
    Production-ready recursive text chunker.
    """

    def __init__(self) -> None:

        self.text_splitter = RecursiveCharacterTextSplitter(

            chunk_size=settings.CHUNK_SIZE,

            chunk_overlap=settings.CHUNK_OVERLAP,

            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ],
        )

    def split( self,documents: list[Document] ) -> list[Chunk]:
        """
        Split documents into chunks.

        Parameters
        ----------
        documents : list[Document]

        Returns
        -------
        list[Chunk]
        """

        logger.info("Chunking %d document(s)...",len(documents) )

        chunks: list[Chunk] = []

        for document in documents:

            split_text = self.text_splitter.split_text( document.page_content)

            document_id = (  document.metadata.get( "content_hash","") )

            for index, text in enumerate(split_text):

                chunk = Chunk(

                    text=text,

                    chunk_index=index,

                    document_id=document_id,

                    page_number=document.metadata.get("page"),

                    metadata=document.metadata.copy(),
                )

                chunks.append(chunk)

        logger.info("Generated %d chunks.", len(chunks) )

        return chunks