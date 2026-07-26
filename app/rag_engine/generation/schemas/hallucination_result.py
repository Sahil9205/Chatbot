"""
Schema representing the result of hallucination detection.
"""

from pydantic import BaseModel, Field


class HallucinationResult(BaseModel):
    """
    Result returned by the Hallucination Guard.
    """

    passed: bool = Field(
        ...,
        description="Whether the generated answer passed hallucination checks.",
    )

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence in the hallucination assessment.",
    )

    reason: str = Field(
        ...,
        description="Explanation of the hallucination decision.",
    )