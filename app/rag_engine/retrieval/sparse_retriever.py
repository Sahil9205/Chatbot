"""
Sparse Retriever

Performs keyword-based retrieval using the BM25 index.
"""

from app.core.logging import get_logger

from app.rag_engine.indexing.bm25.base import BaseKeywordIndex
from app.rag_engine.indexing.bm25.bm25_result import BM25Result

from .schemas.query import SearchQuery
from .schemas.retrieved_chunk import RetrievedChunk
from .schemas.source import RetrievalSource

from .base import BaseRetriever 

logger = get_logger(__name__)


class SparseRetriever(BaseRetriever):
    """
    Keyword-based document retriever.
    """

    def __init__(self,keyword_index: BaseKeywordIndex,) -> None:
        """
        Parameters
        ----------
        keyword_index : BaseKeywordIndex
            BM25 keyword index implementation.
        """

        self.keyword_index = keyword_index

    ####################################################################
    # Public Methods
    ####################################################################

    def retrieve(self,search_query: SearchQuery,) -> list[RetrievedChunk]:
        """
        Perform sparse retrieval.

        Parameters
        ----------
        search_query : SearchQuery

        Returns
        -------
        list[RetrievedChunk]
        """

        logger.info("Starting sparse retrieval.")

        try:

            results = self.keyword_index.search(

                query=search_query.rewritten_query,

                top_k=search_query.top_k,
            )

            retrieved_chunks = [

                self._convert_result(result)

                for result in results
            ]

            logger.info("Sparse retrieval returned %d chunk(s).",len(retrieved_chunks),)

            return retrieved_chunks

        except Exception:

            logger.exception("Sparse retrieval failed.")

            raise

    ####################################################################
    # Private Methods
    ####################################################################

    def _convert_result(self,result: BM25Result,) -> RetrievedChunk:
        """
        Convert a BM25 result into a RetrievedChunk.
        """

        return RetrievedChunk(

            chunk_id=result.chunk_id,

            document_id=result.document_id,

            chunk_index=result.chunk_index,

            text=result.text,

            metadata=result.metadata,

            score=result.score,

            source=RetrievalSource.SPARSE,
        )