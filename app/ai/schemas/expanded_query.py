"""
Schema for expanded user queries.
"""

from pydantic import BaseModel, Field, field_validator


class ExpandedQuery(BaseModel):
    """
    Structured response returned by the query expansion service.
    """

    queries: list[str] = Field(
        ...,
        min_length=1,
        description="Alternative search queries generated from the user's query.",
    )

    reasoning: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Short explanation of the query expansion.",
    )

    @field_validator("queries")
    @classmethod
    def validate_queries(cls, values: list[str]) -> list[str]:
        """
        Validate generated queries.
        """

        cleaned_queries: list[str] = []

        for query in values:
            query = query.strip()

            if not query:
                raise ValueError(
                    "Expanded query cannot be empty."
                )

            cleaned_queries.append(query)

        return cleaned_queries

    @field_validator("reasoning")
    @classmethod
    def validate_reasoning(cls, value: str) -> str:
        """
        Validate reasoning.
        """

        value = value.strip()

        if not value:
            raise ValueError(
                "Reasoning cannot be empty."
            )

        return value