"""
Schema representing a retrieved document chunk.

This schema is shared across the entire retrieval pipeline.
Every retriever returns RetrievedChunk objects.
"""

from typing import Any

from pydantic import BaseModel, Field, field_validator

from .source import RetrievalSource

class RetrievedChunk(BaseModel):
    """
    Represents a retrieved document chunk.
    """

    chunk_id: str = Field(
        ...,
        description="Unique identifier of the retrieved chunk.",
    )

    document_id: str = Field(
        ...,
        description="Document identifier.",
    )

    text: str = Field(
        ...,
        description="Retrieved chunk text.",
    )

    score: float = Field(
        ...,
        description="Retrieval similarity score.",
    )

    source: RetrievalSource = Field(
        ...,
        description="Retriever that returned this chunk.",
    )

    page_number: int | None = Field(
        default=None,
        description="Page number within the original document.",
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Chunk metadata.",
    )

    @field_validator(
        "chunk_id",
        "document_id",
        "text",
        "source",
    )
    @classmethod
    def validate_string_fields(cls,value: str,) -> str:
        """
        Validate string fields.
        """

        value = value.strip()

        if not value:
            raise ValueError(
                "Field cannot be empty."
            )

        return value

    @field_validator("score")
    @classmethod
    def validate_score(
        cls,
        value: float,) -> float:
        """
        Validate retrieval score.
        """

        if value < 0:
            raise ValueError(
                "Retrieval score cannot be negative."
            )

        return value