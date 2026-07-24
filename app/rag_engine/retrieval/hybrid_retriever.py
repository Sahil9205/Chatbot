"""
Hybrid Retriever

Combines dense and sparse retrieval using a configurable
fusion strategy.
"""

from app.core.logging import get_logger

from .dense_retriever import DenseRetriever
from .fusion.base import BaseFusionStrategy
from .schemas.query import SearchQuery
from .schemas.retrieved_chunk import RetrievedChunk
from .sparse_retriever import SparseRetriever

from .base import BaseRetriever

logger = get_logger(__name__)


class HybridRetriever(BaseRetriever):
    """
    Hybrid document retriever.
    """

    def __init__(
        self,
        dense_retriever: DenseRetriever,
        sparse_retriever: SparseRetriever,
        fusion_strategy: BaseFusionStrategy,
    ) -> None:
        """
        Parameters
        ----------
        dense_retriever : DenseRetriever

        sparse_retriever : SparseRetriever

        fusion_strategy : BaseFusionStrategy
        """

        self.dense_retriever = dense_retriever

        self.sparse_retriever = sparse_retriever

        self.fusion_strategy = fusion_strategy

    ################
    # Public Methods
    ################

    def retrieve(self,search_query: SearchQuery,) -> list[RetrievedChunk]:
        """
        Perform hybrid retrieval.

        Parameters
        ----------
        search_query : SearchQuery

        Returns
        -------
        list[RetrievedChunk]
        """

        logger.info("Starting hybrid retrieval.")

        try:

            dense_results = self.dense_retriever.retrieve(
                search_query
            )

            sparse_results = self.sparse_retriever.retrieve(
                search_query
            )

            fused_results = self.fusion_strategy.fuse(

                dense_results,

                sparse_results,
            )

            logger.info("Hybrid retrieval returned %d chunk(s).",len(fused_results),)

            return fused_results

        except Exception:

            logger.exception("Hybrid retrieval failed.")

            raise