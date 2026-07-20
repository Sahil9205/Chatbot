"""
Hybrid Retrieval Index.

Combines dense retrieval (Qdrant)
and sparse retrieval (BM25)
using Reciprocal Rank Fusion.
"""

from app.rag_engine.indexing.vector_store.base import BaseVectorStore
from app.rag_engine.indexing.bm25.base import BaseKeywordIndex
from app.rag_engine.indexing.hybrid.fusion import ReciprocalRankFusion
from app.rag_engine.retrieval.schemas.retrieved_chunk import RetrievedChunk


class HybridIndex:
    """
    Hybrid Retrieval System.
    """

    def __init__(
        self,
        vector_store: BaseVectorStore,
        keyword_index: BaseKeywordIndex,
        fusion: ReciprocalRankFusion,
    ):

        self.vector_store = vector_store

        self.keyword_index = keyword_index

        self.fusion = fusion

    def search(
        self,
        query: str,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> list[RetrievedChunk]:
        """
        Perform hybrid retrieval.
        """

        ##################################################
        # Dense Search
        ##################################################

        dense_results = self.vector_store.search(

            query_vector=query_embedding,

            top_k=top_k,
        )

        ##################################################
        # Sparse Search
        ##################################################

        sparse_results = self.keyword_index.search(

            query=query,

            top_k=top_k,
        )

        ##################################################
        # Fusion
        ##################################################

        results = self.fusion.fuse(

            dense_results,

            sparse_results,
        )

        ##################################################
        # Top K
        ##################################################

        return results[:top_k]