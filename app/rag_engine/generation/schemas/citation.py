"""
Schema representing a citation used to support
a generated answer.
"""

from pydantic import BaseModel, Field, field_validator


class Citation(BaseModel):
    """
    Represents a citation attached to an answer.
    """

    document_id: str = Field(
        ...,
        description="Unique document identifier.",
    )

    chunk_id: str = Field(
        ...,
        description="Chunk that supports the answer.",
    )

    page_number: int | None = Field(
        default=None,
        ge=1,
        description="Page number in the source document.",
    )

    score: float = Field(
        ...,
        ge=0.0,
        description="Retrieval or reranking confidence score.",
    )

    @field_validator(
        "document_id",
        "chunk_id",
    )
    @classmethod
    def validate_strings(
        cls,
        value: str,
    ) -> str:
        """
        Validate string fields.
        """

        value = value.strip()

        if not value:
            raise ValueError(
                "Field cannot be empty."
            )

        return value