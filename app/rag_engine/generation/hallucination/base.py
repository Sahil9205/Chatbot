"""
Abstract hallucination rule.
"""

from abc import ABC, abstractmethod

from app.rag_engine.generation.schemas.answer import Answer
from app.rag_engine.generation.schemas.hallucination_result import (
    HallucinationResult,
)


class BaseHallucinationRule(ABC):
    """
    Base class for hallucination detection rules.
    """

    @abstractmethod
    def evaluate(
        self,
        answer: Answer,
        **kwargs,
    ) -> HallucinationResult:
        """
        Evaluate one hallucination rule.
        """
        pass