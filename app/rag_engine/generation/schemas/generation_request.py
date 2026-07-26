"""
Schema representing the input to the generation pipeline.
"""

from pydantic import BaseModel, Field, field_validator

from app.rag_engine.retrieval.schemas.retrieved_chunk import RetrievedChunk


class GenerationRequest(BaseModel):
    """
    Input required for answer generation.
    """

    query: str = Field(
        ...,
        description="Original user query.",
    )

    retrieved_chunks: list[RetrievedChunk] = Field(
        default_factory=list,
        description="Retrieved document chunks.",
    )

    system_prompt: str | None = Field(
        default=None,
        description="Optional system prompt override.",
    )

    @field_validator("query")
    @classmethod
    def validate_query(
        cls,
        value: str,
    ) -> str:
        """
        Validate user query.
        """

        value = value.strip()

        if not value:
            raise ValueError(
                "Query cannot be empty."
            )

        return value

    @field_validator("retrieved_chunks")
    @classmethod
    def validate_chunks(
        cls,
        value: list[RetrievedChunk],
    ) -> list[RetrievedChunk]:
        """
        Ensure at least one chunk is available.
        """

        if not value:
            raise ValueError(
                "At least one retrieved chunk is required."
            )

        return value