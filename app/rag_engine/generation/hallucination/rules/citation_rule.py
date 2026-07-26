"""
Hallucination Rule:
Fail if there are not enough supporting citations.
"""

from app.core.config import settings

from app.rag_engine.generation.hallucination.base import (
    BaseHallucinationRule,
)

from app.rag_engine.generation.schemas.answer import Answer
from app.rag_engine.generation.schemas.citation import Citation
from app.rag_engine.generation.schemas.hallucination_result import (
    HallucinationResult,
)


class CitationRule(BaseHallucinationRule):
    """
    Ensures the generated answer is supported by enough citations.
    """

    def evaluate(
        self,
        answer: Answer,
        **kwargs,
    ) -> HallucinationResult:
        """
        Evaluate citation coverage.
        """

        citations: list[Citation] = kwargs.get(
            "citations",
            [],
        )

        minimum = settings.MINIMUM_CITATIONS

        if len(citations) < minimum:

            return HallucinationResult(

                passed=False,

                confidence=0.0,

                reason=(
                    f"Only {len(citations)} citation(s) found. "
                    f"Minimum required is {minimum}."
                ),
            )

        return HallucinationResult(

            passed=True,

            confidence=1.0,

            reason="Sufficient supporting citations found.",
        )