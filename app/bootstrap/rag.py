"""
Bootstrap the complete RAG Engine.
"""

from app.rag_engine.rag_engine import RAGEngine

from .generation import build_generation_pipeline
from .retrieval import build_retrieval_pipeline


def build_rag_engine() -> RAGEngine:
    """
    Build the complete RAG Engine.
    """

    retrieval_pipeline = build_retrieval_pipeline()

    generation_pipeline = build_generation_pipeline()

    return RAGEngine(
        retrieval_pipeline=retrieval_pipeline,
        generation_pipeline=generation_pipeline,
    )