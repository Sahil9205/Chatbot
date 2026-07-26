"""
Bootstrap the Retrieval Pipeline.
"""

from app.rag_engine.indexing.bm25.bm25_index import BM25Index
from app.rag_engine.indexing.embeddings.embedding_service import EmbeddingService
from app.rag_engine.indexing.embeddings.hf_embeddings import (
    HuggingFaceEmbeddingModel,
)
from app.rag_engine.indexing.vector_store.qdrant_store import QdrantStore

from app.rag_engine.retrieval.query_understanding import QueryUnderstanding
from app.rag_engine.retrieval.dense_retriever import DenseRetriever
from app.rag_engine.retrieval.sparse_retriever import SparseRetriever
from app.rag_engine.retrieval.hybrid_retriever import HybridRetriever
from app.rag_engine.retrieval.fusion.reciprocal_rank_fusion import (
    ReciprocalRankFusion,
)
from app.rag_engine.retrieval.reranker.huggingface_cross_encoder import (
    HuggingFaceCrossEncoderModel,
)
from app.rag_engine.retrieval.reranker.reranker import (
    RerankerService,
)
from app.rag_engine.retrieval.retrieval_pipeline import (
    RetrievalPipeline,
)


def build_retrieval_pipeline() -> RetrievalPipeline:
    """
    Build the complete retrieval pipeline.
    """

    ###############################################################
    # Embeddings
    ###############################################################

    embedding_model = HuggingFaceEmbeddingModel()

    embedding_service = EmbeddingService(
        embedding_model=embedding_model,
    )

    ###############################################################
    # Vector Store
    ###############################################################

    vector_store = QdrantStore(
        embedding_dimension=embedding_model.embedding_dimension,
    )

    ###############################################################
    # Dense Retriever
    ###############################################################

    dense_retriever = DenseRetriever(
        embedding_service=embedding_service,
        vector_store=vector_store,
    )

    ###############################################################
    # Sparse Retriever
    ###############################################################

    bm25_index = BM25Index()

    sparse_retriever = SparseRetriever(
        keyword_index=bm25_index,
    )

    ###############################################################
    # Fusion
    ###############################################################

    fusion = ReciprocalRankFusion()

    ###############################################################
    # Hybrid Retriever
    ###############################################################

    hybrid_retriever = HybridRetriever(
        dense_retriever=dense_retriever,
        sparse_retriever=sparse_retriever,
        fusion_strategy=fusion,
    )

    ###############################################################
    # Cross Encoder
    ###############################################################

    cross_encoder = HuggingFaceCrossEncoderModel()

    reranker = RerankerService(
        model=cross_encoder,
    )

    ###############################################################
    # Query Understanding
    ###############################################################

    query_pipeline = QueryUnderstanding()

    ###############################################################
    # Retrieval Pipeline
    ###############################################################

    retrieval_pipeline = RetrievalPipeline(
        query_pipeline=query_pipeline,
        retriever=hybrid_retriever,
        reranker=reranker,
    )

    return retrieval_pipeline