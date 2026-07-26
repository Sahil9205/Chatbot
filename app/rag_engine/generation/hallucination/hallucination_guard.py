"""
Hallucination Guard.

Runs all hallucination detection rules and returns
the first failed result (fail-fast).
"""

from app.core.logging import get_logger

from app.rag_engine.generation.schemas.answer import Answer
from app.rag_engine.generation.schemas.citation import Citation
from app.rag_engine.generation.schemas.hallucination_result import (
    HallucinationResult,
)
from app.rag_engine.retrieval.schemas.retrieved_chunk import (
    RetrievedChunk,
)

from .base import BaseHallucinationRule
from .rules.citation_rule import CitationRule
from .rules.empty_answer_rule import EmptyAnswerRule
from .rules.empty_context_rule import EmptyContextRule
from .rules.retrieval_score_rule import RetrievalScoreRule

logger = get_logger(__name__)


class HallucinationGuard:
    """
    Runs hallucination detection rules.
    """

    def __init__(self) -> None:

        self.rules: list[BaseHallucinationRule] = [

            EmptyAnswerRule(),

            EmptyContextRule(),

            RetrievalScoreRule(),

            CitationRule(),

        ]

    ####################################################################
    # Public Methods
    ####################################################################

    def evaluate(
        self,
        answer: Answer,
        retrieved_chunks: list[RetrievedChunk],
        citations: list[Citation],
    ) -> HallucinationResult:
        """
        Evaluate all hallucination rules.

        Parameters
        ----------
        answer : Answer

        retrieved_chunks : list[RetrievedChunk]

        citations : list[Citation]

        Returns
        -------
        HallucinationResult
        """

        logger.info(
            "Running %d hallucination rule(s).",
            len(self.rules),
        )

        for rule in self.rules:

            result = rule.evaluate(

                answer=answer,

                retrieved_chunks=retrieved_chunks,

                citations=citations,
            )

            if not result.passed:

                logger.warning(
                    "Hallucination check failed: %s",
                    result.reason,
                )

                return result

        logger.info(
            "All hallucination checks passed."
        )

        return HallucinationResult(

            passed=True,

            confidence=1.0,

            reason="All hallucination checks passed.",
        )