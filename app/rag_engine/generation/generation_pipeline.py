"""
Generation Pipeline.

Coordinates the complete answer generation pipeline.
"""

from time import perf_counter

from typing import Any

from app.core.logging import get_logger

from app.observability.manager import ObservabilityManager

from .answer_generator import AnswerGenerator
from .citation_builder import CitationBuilder
from .hallucination.hallucination_guard import HallucinationGuard
from .response_validator import ResponseValidator
from .schemas.generation_request import GenerationRequest
from .schemas.generation_response import GenerationResponse


logger = get_logger(__name__)


class GenerationPipeline:
    """
    Complete generation pipeline.
    """

    def __init__(
        self,
        answer_generator: AnswerGenerator,
        citation_builder: CitationBuilder,
        hallucination_guard: HallucinationGuard,
        response_validator: ResponseValidator,
        observability: ObservabilityManager,
    ) -> None:
        """
        Parameters
        ----------
        answer_generator : AnswerGenerator
            Generates the final answer.

        citation_builder : CitationBuilder
            Builds citations from retrieved chunks.

        hallucination_guard : HallucinationGuard
            Runs hallucination checks.

        response_validator : ResponseValidator
            Validates the final response.
        """

        self.answer_generator = answer_generator
        self.citation_builder = citation_builder
        self.hallucination_guard = hallucination_guard
        self.response_validator = response_validator
        self.observability = observability

    def generate(
        self,
        request: GenerationRequest,
        trace: Any = None,
    ) -> GenerationResponse:
        """
        Generate the final answer.

        Parameters
        ----------
        request : GenerationRequest

        Returns
        -------
        GenerationResponse
        """

        logger.info("Starting generation pipeline.")

        trace = self.observability.start_trace(
            name="generation_pipeline",
            input={
                "query": request.query,
            },
        )

        start_time = perf_counter()

        span = self.observability.start_span(
            trace,
            "generate_answer",
        )

        try:
            answer = self.answer_generator.generate(request)

            citations = self.citation_builder.build(
                request.retrieved_chunks
            )

            hallucination_result = self.hallucination_guard.evaluate(
                answer=answer,
                retrieved_chunks=request.retrieved_chunks,
                citations=citations,
            )

            generation_time = perf_counter() - start_time

            response = GenerationResponse(
                answer=answer,
                citations=citations,
                has_sufficient_context=hallucination_result.passed,
                generation_time=generation_time,
                prompt_tokens=0,
                completion_tokens=0,
                total_tokens=0,
            )

            validated_response = self.response_validator.validate(response)

            logger.info("Generation pipeline completed successfully.")

            self.observability.end_span(span)

        

            return validated_response

        except Exception as exc:
            logger.exception("Generation pipeline failed.")

            self.observability.record_error(
                trace,
                exc,
            )

            self.observability.end_span(span)

            raise