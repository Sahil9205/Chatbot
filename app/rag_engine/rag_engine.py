"""
RAG Engine.

Coordinates the complete Retrieval-Augmented Generation pipeline.
"""

from app.core.logging import get_logger

from app.rag_engine.generation.generation_pipeline import GenerationPipeline
from app.rag_engine.generation.schemas.generation_request import (
    GenerationRequest,
)
from app.rag_engine.generation.schemas.generation_response import (
    GenerationResponse,
)
from app.rag_engine.retrieval.retrieval_pipeline import RetrievalPipeline


logger = get_logger(__name__)


class RAGEngine:
    """
    High-level interface for the complete RAG workflow.

    This class orchestrates:

        User Query
            ↓
        Retrieval Pipeline
            ↓
        Generation Pipeline
            ↓
        Final Answer
    """

    def __init__(
        self,
        retrieval_pipeline: RetrievalPipeline,
        generation_pipeline: GenerationPipeline,
    ) -> None:
        """
        Parameters
        ----------
        retrieval_pipeline : RetrievalPipeline

        generation_pipeline : GenerationPipeline
        """

        self.retrieval_pipeline = retrieval_pipeline

        self.generation_pipeline = generation_pipeline

    ####################################################################
    # Public Methods
    ####################################################################

    def answer(
        self,
        query: str,
    ) -> GenerationResponse:
        """
        Answer a user query.

        Parameters
        ----------
        query : str

        Returns
        -------
        GenerationResponse
        """

        logger.info("Starting RAG Engine.")

        try:

            retrieval_result = self.retrieval_pipeline.retrieve(
                query
            )

            generation_request = GenerationRequest(

                query=query,

                retrieved_chunks=retrieval_result.retrieved_chunks,
            )

            response = self.generation_pipeline.generate(
                generation_request
            )

            logger.info("RAG Engine completed successfully.")

            return response

        except Exception:

            logger.exception("RAG Engine failed.")

            raise