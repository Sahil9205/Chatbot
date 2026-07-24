"""
Schema representing the output of a reranker.
"""

from pydantic import BaseModel, Field, field_validator


class RerankResult(BaseModel):
    """
    Represents the reranking score for a retrieved chunk.
    """

    chunk_id: str = Field(
        ...,
        description="Unique identifier of the retrieved chunk.",
    )

    score: float = Field(
        ...,
        description="Cross-encoder relevance score.",
    )

    @field_validator("chunk_id")
    @classmethod
    def validate_chunk_id(cls,value: str,) -> str:
        """
        Validate chunk identifier.
        """

        value = value.strip()

        if not value:
            raise ValueError(
                "Chunk ID cannot be empty."
            )

        return value