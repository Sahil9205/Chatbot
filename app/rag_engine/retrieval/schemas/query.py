"""
Schema representing a processed search query.

This schema is shared across the entire retrieval pipeline.
It contains the output of the query understanding stage and
is passed to every retriever.
"""

from typing import Any

from pydantic import BaseModel, Field, field_validator


class SearchQuery(BaseModel):
    """
    Processed query used by the retrieval engine.
    """

    original_query: str = Field(
        ...,
        description="Original user query.",
    )

    rewritten_query: str = Field(
        ...,
        description="Query rewritten for improved retrieval.",
    )

    expanded_queries: list[str] = Field(
        default_factory=list,
        description="Alternative semantic search queries.",
    )

    metadata_filters: dict[str, Any] = Field(
        default_factory=dict,
        description="Metadata filters extracted from the query.",
    )

    top_k: int = Field(
        default=10,
        ge=1,
        description="Maximum number of documents to retrieve.",
    )

    @field_validator(
        "original_query",
        "rewritten_query",
    )
    @classmethod
    def validate_queries(
        cls,
        value: str,
    ) -> str:
        """
        Validate query fields.
        """

        value = value.strip()

        if not value:
            raise ValueError(
                "Query cannot be empty."
            )

        return value

    @field_validator("expanded_queries")
    @classmethod
    def validate_expanded_queries(
        cls,
        values: list[str],
    ) -> list[str]:
        """
        Remove empty expanded queries.
        """

        cleaned_queries: list[str] = []

        for query in values:

            query = query.strip()

            if query:
                cleaned_queries.append(query)

        return cleaned_queries