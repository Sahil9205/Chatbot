"""
Hallucination Rule:
Fail if no document chunks were retrieved.
"""

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


class EmptyContextRule(BaseHallucinationRule):
    """
    Ensures that retrieval returned at least one chunk.
    """

    def evaluate(
        self,
        answer: Answer,
        **kwargs,
    ) -> HallucinationResult:
        """
        Evaluate whether retrieval returned any chunks.
        """

        retrieved_chunks: list[RetrievedChunk] = kwargs.get(
            "retrieved_chunks",
            [],
        )

        if not retrieved_chunks:

            return HallucinationResult(

                passed=False,

                confidence=1.0,

                reason="No supporting document chunks were retrieved.",
            )

        return HallucinationResult(

            passed=True,

            confidence=1.0,

            reason="Supporting document chunks found.",
        )