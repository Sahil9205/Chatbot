"""
Dense Retriever

Performs semantic retrieval using vector embeddings
and the configured vector store.
"""

from qdrant_client.models import Filter, FieldCondition, MatchValue

from app.core.logging import get_logger

from app.rag_engine.indexing.embeddings.embedding_service import (EmbeddingService,)
from app.rag_engine.indexing.vector_store.base import (BaseVectorStore,)

from .schemas.query import SearchQuery
from .schemas.retrieved_chunk import RetrievedChunk
from .schemas.source import RetrievalSource

from base import BaseRetriever

logger = get_logger(__name__)


class DenseRetriever(BaseRetriever):
    """
    Semantic document retriever.
    """

    def __init__(self,embedding_service: EmbeddingService,vector_store: BaseVectorStore,) -> None:
        """
        Parameters
        ----------
        embedding_service : EmbeddingService

        vector_store : BaseVectorStore
        """

        self.embedding_service = embedding_service

        self.vector_store = vector_store

    def retrieve(self,search_query: SearchQuery,) -> list[RetrievedChunk]:
        """
        Perform semantic retrieval.

        Parameters
        ----------
        search_query : SearchQuery

        Returns
        -------
        list[RetrievedChunk]
        """

        logger.info("Starting dense retrieval.")

        try:

            query_embedding = self.embedding_service.embed_query(
                search_query.rewritten_query
            )

            query_filter = self._build_filter(
                search_query.metadata_filters
            )

            results = self.vector_store.search(

                query_vector=query_embedding,

                top_k=search_query.top_k,

                query_filter=query_filter,
            )

            retrieved_chunks = [

                self._convert_result(result)

                for result in results
            ]

            logger.info(
                "Dense retrieval returned %d chunk(s).",
                len(retrieved_chunks),
            )

            return retrieved_chunks

        except Exception:

            logger.exception("Dense retrieval failed.")

            raise

    ##################################################################
    # Private Methods
    ##################################################################

    def _build_filter(self,metadata_filters: dict[str, object],) -> Filter | None:
        """
        Build a Qdrant metadata filter.
        """

        if not metadata_filters:
            return None

        conditions = []

        for field, value in metadata_filters.items():

            conditions.append(

                FieldCondition(

                    key=f"metadata.{field}",

                    match=MatchValue(value=value),
                )

            )

        return Filter(must=conditions,)

    def _convert_result(self,result,) -> RetrievedChunk:
        """
        Convert a Qdrant result into a RetrievedChunk.
        """

        payload = result.payload

        return RetrievedChunk(

            chunk_id=str(result.id),

            document_id=payload["document_id"],

            text=payload["text"],

            score=result.score,

            source=RetrievalSource.DENSE,

            page_number=payload["metadata"].get(
                "page"
            ),

            metadata=payload["metadata"],
        )