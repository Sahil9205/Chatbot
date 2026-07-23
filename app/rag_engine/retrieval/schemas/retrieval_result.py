"""
Schema representing the final retrieval result.

This schema is returned by the retrieval pipeline before
the Generation pipeline begins.
"""

from pydantic import BaseModel, Field, field_validator

from .retrieved_chunk import RetrievedChunk


class RetrievalResult(BaseModel):
    """
    Final output of the retrieval pipeline.
    """

    query: str = Field(
        ...,
        description="Original user query.",
    )

    retrieved_chunks: list[RetrievedChunk] = Field(
        default_factory=list,
        description="Retrieved document chunks.",
    )

    retrieval_time: float = Field(
        ...,
        ge=0.0,
        description="Retrieval latency in seconds.",
    )

    total_chunks: int = Field(
        default=0,
        ge=0,
        description="Number of retrieved chunks.",
    )

    @field_validator("query")
    @classmethod
    def validate_query(
        cls,
        value: str,
    ) -> str:
        """
        Validate the user query.
        """

        value = value.strip()

        if not value:
            raise ValueError(
                "Query cannot be empty."
            )

        return value

    @field_validator("total_chunks")
    @classmethod
    def validate_total_chunks(
        cls,
        value: int,
        info,
    ) -> int:
        """
        Ensure total_chunks matches the retrieved chunks.
        """

        chunks = info.data.get("retrieved_chunks", [])

        if value != len(chunks):
            raise ValueError(
                "total_chunks must equal the number of retrieved chunks."
            )

        return value