"""
Hallucination Rule:
Fail if the generated answer is empty.
"""

from app.rag_engine.generation.hallucination.base import (
    BaseHallucinationRule,
)

from app.rag_engine.generation.schemas.answer import Answer
from app.rag_engine.generation.schemas.hallucination_result import (
    HallucinationResult,
)


class EmptyAnswerRule(BaseHallucinationRule):
    """
    Ensures the language model returned a non-empty answer.
    """

    def evaluate(
        self,
        answer: Answer,
        **kwargs,
    ) -> HallucinationResult:
        """
        Evaluate whether the answer is empty.
        """

        if not answer.text.strip():

            return HallucinationResult(

                passed=False,

                confidence=1.0,

                reason="Generated answer is empty.",
            )

        return HallucinationResult(

            passed=True,

            confidence=1.0,

            reason="Answer is not empty.",
        )