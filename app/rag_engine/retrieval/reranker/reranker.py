"""
Reranker Service.

Uses a CrossEncoder model to rerank retrieved chunks.
"""

from app.core.logging import get_logger

from app.rag_engine.retrieval.schemas.retrieved_chunk import RetrievedChunk

from .base import BaseCrossEncoderModel

from app.rag_engine.retrieval.schemas.source import RetrievalSource

logger = get_logger(__name__)


class RerankerService:
    """
    Business logic for reranking retrieved chunks.
    """

    def __init__(self,model: BaseCrossEncoderModel, ) -> None:

        self.model = model

    def rerank(self,query: str,chunks: list[RetrievedChunk],top_k: int,) -> list[RetrievedChunk]:
        """
        Rerank retrieved chunks.
        """

        if not chunks:
            return []

        logger.info("Reranking %d retrieved chunks.",len(chunks),)

        documents = [

            chunk.text

            for chunk in chunks

        ]

        scores = self.model.predict(

            query=query,

            documents=documents,
        )

        ranked = sorted(

            zip(chunks, scores),

            key=lambda item: item[1],

            reverse=True,
        )

        reranked_chunks =list[RetrievedChunk] = []

        for chunk, score in ranked[:top_k]:

             reranked_chunks.append(

        RetrievedChunk(

            chunk_id=chunk.chunk_id,

            document_id=chunk.document_id,

            chunk_index=chunk.chunk_index,

            text=chunk.text,

            metadata=chunk.metadata,

            score=float(score),

            source=RetrievalSource.RERANKED,
        )

    )
        logger.info("Successfully reranked %d chunks.",len(reranked_chunks),)

        return reranked_chunks