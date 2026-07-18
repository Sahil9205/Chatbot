"""
Embedding Service

Converts Chunk objects into EmbeddedChunk objects.
"""

from app.core.logging import get_logger
from app.rag.ingestion.chunking.chunk_schema import Chunk

from .base import BaseEmbeddingModel
from .embedding_schema import EmbeddedChunk

logger = get_logger(__name__)


class EmbeddingService:
    """
    Generates embeddings for document chunks.
    """

    def __init__(self,embedding_model: BaseEmbeddingModel,) -> None:
        """
        Parameters
        ----------
        embedding_model : BaseEmbeddingModel
            Embedding model implementation.
        """

        self.embedding_model = embedding_model

    def embed_chunks(self,chunks: list[Chunk],) -> list[EmbeddedChunk]:
        """
        Convert Chunk objects into EmbeddedChunk objects.

        Parameters
        ----------
        chunks : list[Chunk]

        Returns
        -------
        list[EmbeddedChunk]
        """

        logger.info("Generating embeddings for %d chunks...",len(chunks),)

        texts = [chunk.text for chunk in chunks]

        vectors = self.embedding_model.embed_documents(texts)

        embedded_chunks: list[EmbeddedChunk] = []

        for chunk, vector in zip(chunks, vectors):

            embedded_chunks.append(

                EmbeddedChunk(

                    chunk_id=chunk.chunk_id,

                    document_id=chunk.document_id,

                    chunk_index=chunk.chunk_index,

                    text=chunk.text,

                    embedding=vector,

                    metadata=chunk.metadata,
                )

            )

        logger.info("Successfully generated %d embeddings.",len(embedded_chunks),)

        return embedded_chunks