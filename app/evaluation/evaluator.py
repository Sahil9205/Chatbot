"""
Evaluation Service.

High-level service responsible for evaluating
RAG responses.
"""

from __future__ import annotations

from app.core.logging import get_logger
from app.evaluation.base import BaseEvaluator
from app.evaluation.schemas import (
    EvaluationRequest,
    EvaluationResult,
)

logger = get_logger(__name__)


class Evaluator:
    """
    High-level evaluation service.
    """

    def __init__(
        self,
        provider: BaseEvaluator,
    ) -> None:
        """
        Parameters
        ----------
        provider : BaseEvaluator
            Concrete evaluation provider.
        """

        self.provider = provider

    def evaluate(
        self,
        request: EvaluationRequest,
    ) -> EvaluationResult:
        """
        Evaluate a generated response.
        """

        logger.info(
            "Starting response evaluation."
        )

        result = self.provider.evaluate(
            request,
        )

        logger.info(
            "Evaluation completed successfully."
        )

        return result