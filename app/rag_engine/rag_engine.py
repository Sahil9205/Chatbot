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

from app.observability.manager import ObservabilityManager


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
        observability: ObservabilityManager,
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

        trace = self.observability.start_trace(
            name="rag_request",
            input={
                "query": query,
            },
        )

        try:

            retrieval_result = self.retrieval_pipeline.retrieve(
                query=query,
                trace=trace,
            )

            generation_request = GenerationRequest(

                query=query,

                retrieved_chunks=retrieval_result.retrieved_chunks,
            )

            response = self.generation_pipeline.generate(
                request=generation_request,
                trace=trace,
            )

            logger.info("RAG Engine completed successfully.")

            self.observability.end_trace(trace)

            return response

        except Exception as exc:

            logger.exception("RAG Engine failed.")

            self.observability.record_error(
                trace,
                exc,
            )

            self.observability.end_trace(trace)

            raise