"""
Retrieval Pipeline.

Coordinates the complete retrieval workflow from
user query to reranked document chunks.
"""

from time import perf_counter

from app.core.logging import get_logger

from app.rag_engine.retrieval.query_understanding import (
    QueryUnderstanding,
)
from app.rag_engine.retrieval.hybrid_retriever import HybridRetriever
from app.rag_engine.retrieval.reranker.reranker import (
    RerankerService,
)

from app.rag_engine.retrieval.schemas.retrieval_result import (
    RetrievalResult,
)


logger = get_logger(__name__)


class RetrievalPipeline:
    """
    End-to-end retrieval pipeline.
    """

    def __init__(
        self,
        query_pipeline: QueryUnderstanding,
        retriever: HybridRetriever,
        reranker: RerankerService,
    ) -> None:
        """
        Parameters
        ----------
        query_pipeline : QueryUnderstanding

        retriever : BaseRetriever

        reranker : BaseReranker
        """

        self.query_pipeline = query_pipeline
        self.retriever = retriever
        self.reranker = reranker

    ####################################################################
    # Public API
    ####################################################################

    def retrieve(
        self,
        query: str,
    ) -> RetrievalResult:
        """
        Execute the retrieval pipeline.
        """

        logger.info(
            "Starting retrieval pipeline."
        )

        start_time = perf_counter()

        ###############################################################
        # Query Understanding
        ###############################################################

        search_query = self.query_pipeline.process(
            query=query,
        )

        ###############################################################
        # Hybrid Retrieval
        ###############################################################

        retrieved_chunks = self.retriever.retrieve(
            search_query,
        )

        ###############################################################
        # CrossEncoder Reranking
        ###############################################################

        reranked_chunks = self.reranker.rerank(

            query=search_query.rewritten_query,

            chunks=retrieved_chunks,

            top_k=search_query.top_k,
        )

        ###############################################################
        # Statistics
        ###############################################################

        retrieval_time = perf_counter() - start_time

        logger.info(

            "Retrieval completed in %.3f seconds.",

            retrieval_time,
        )

        ###############################################################
        # Final Result
        ###############################################################

        return RetrievalResult(

            query=query,

            retrieved_chunks=reranked_chunks,

            retrieval_time=retrieval_time,

            total_chunks=len(reranked_chunks),
        )