"""
Evaluation Schemas.

Shared data models for RAG evaluation.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class EvaluationRequest(BaseModel):
    """
    Input required to evaluate a RAG response.
    """

    query: str = Field(
        description="Original user query.",
    )

    answer: str = Field(
        description="Generated answer.",
    )

    contexts: list[str] = Field(
        default_factory=list,
        description="Retrieved context documents.",
    )

    ground_truth: str | None = Field(
        default=None,
        description="Reference answer, if available.",
    )


class MetricResult(BaseModel):
    """
    Result for a single evaluation metric.
    """

    name: str

    score: float

    reason: str | None = None


class EvaluationResult(BaseModel):
    """
    Complete evaluation result.
    """

    metrics: list[MetricResult]

    overall_score: float

    passed: bool