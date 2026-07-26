"""
Hallucination Rule:
Fail if retrieval confidence is too low.
"""

from app.core.config import settings

from app.rag_engine.generation.hallucination.base import (
    BaseHallucinationRule,
)

from app.rag_engine.generation.schemas.answer import Answer
from app.rag_engine.generation.schemas.hallucination_result import (
    HallucinationResult,
)

from app.rag_engine.retrieval.schemas.retrieved_chunk import (
    RetrievedChunk,
)


class RetrievalScoreRule(BaseHallucinationRule):
    """
    Ensures retrieval confidence is above the configured threshold.
    """

    def evaluate(
        self,
        answer: Answer,
        **kwargs,
    ) -> HallucinationResult:
        """
        Evaluate retrieval confidence.
        """

        retrieved_chunks: list[RetrievedChunk] = kwargs.get(
            "retrieved_chunks",
            [],
        )

        if not retrieved_chunks:

            return HallucinationResult(

                passed=False,

                confidence=1.0,

                reason="No retrieved chunks available.",
            )

        top_score = max(

            chunk.score

            for chunk in retrieved_chunks

        )

        threshold = settings.RETRIEVAL_SCORE_THRESHOLD

        if top_score < threshold:

            return HallucinationResult(

                passed=False,

                confidence=top_score,

                reason=(
                    f"Top retrieval score "
                    f"({top_score:.3f}) is below "
                    f"the configured threshold "
                    f"({threshold:.3f})."
                ),
            )

        return HallucinationResult(

            passed=True,

            confidence=top_score,

            reason="Retrieval confidence is acceptable.",
        )