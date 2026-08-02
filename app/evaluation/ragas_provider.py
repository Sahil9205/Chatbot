"""
RAGAS Evaluation Provider.

Concrete implementation of the BaseEvaluator interface
using RAGAS.
"""

from __future__ import annotations

from statistics import mean

from ragas import evaluate
from ragas.dataset_schema import EvaluationDataset
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)

from app.core.logging import get_logger
from app.evaluation.base import BaseEvaluator
from app.evaluation.schemas import (
    EvaluationRequest,
    EvaluationResult,
    MetricResult,
)

logger = get_logger(__name__)


class RagasProvider(BaseEvaluator):
    """
    Evaluate RAG responses using RAGAS.
    """

    def evaluate(
        self,
        request: EvaluationRequest,
    ) -> EvaluationResult:
        """
        Evaluate a generated response.
        """

        logger.info("Starting RAGAS evaluation.")

        dataset = EvaluationDataset.from_list(
            [
                {
                    "user_input": request.query,
                    "response": request.answer,
                    "retrieved_contexts": request.contexts,
                    "reference": request.ground_truth or "",
                }
            ]
        )

        result = evaluate(
            dataset=dataset,
            metrics=[
                faithfulness,
                answer_relevancy,
                context_precision,
                context_recall,
            ],
        )

        result_dict = result.to_pandas().iloc[0].to_dict()

        metrics: list[MetricResult] = []

        for metric_name in (
            "faithfulness",
            "answer_relevancy",
            "context_precision",
            "context_recall",
        ):
            score = float(result_dict.get(metric_name, 0.0))

            metrics.append(
                MetricResult(
                    name=metric_name,
                    score=score,
                )
            )

        overall_score = mean(
            metric.score for metric in metrics
        )

        logger.info(
            "RAGAS evaluation completed. Overall score: %.3f",
            overall_score,
        )

        return EvaluationResult(
            metrics=metrics,
            overall_score=overall_score,
            passed=overall_score >= 0.75,
        )