"""
Base Evaluation Interface.

Defines the contract for all evaluation providers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.evaluation.schemas import (
    EvaluationRequest,
    EvaluationResult,
)


class BaseEvaluator(ABC):
    """
    Abstract interface for evaluating RAG responses.
    """

    @abstractmethod
    def evaluate(
        self,
        request: EvaluationRequest,
    ) -> EvaluationResult:
        """
        Evaluate a RAG response.
        """
        pass