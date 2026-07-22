"""
Schema for query intent classification.
"""

from enum import Enum

from pydantic import BaseModel, Field, field_validator


class Intent(str, Enum):
    """
    Supported query intents.
    """

    DOCUMENT_SEARCH = "DOCUMENT_SEARCH"
    GENERAL_QUERY = "GENERAL_QUERY"
    GREETING = "GREETING"
    UNKNOWN = "UNKNOWN"


class IntentClassification(BaseModel):
    """
    Structured response returned by the intent classifier.
    """

    intent: Intent = Field(
        ...,
        description="Predicted user intent.",
    )

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1.",
    )

    reasoning: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Short explanation for the predicted intent.",
    )

    @field_validator("reasoning")
    @classmethod
    def validate_reasoning(cls, value: str) -> str:
        """
        Remove leading and trailing whitespace.
        """

        value = value.strip()

        if not value:
            raise ValueError(
                "Reasoning cannot be empty."
            )

        return value