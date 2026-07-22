"""
Schema for rewritten user queries.
"""

from pydantic import BaseModel, Field, field_validator


class RewrittenQuery(BaseModel):
    """
    Structured response returned by the query rewriter.
    """

    query: str = Field(
        ...,
        min_length=1,
        description="Optimized query for document retrieval.",
    )

    reasoning: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Short explanation of the rewrite.",
    )

    @field_validator("query", "reasoning")
    @classmethod
    def strip_whitespace(cls, value: str) -> str:
        """
        Remove leading and trailing whitespace.
        """

        value = value.strip()

        if not value:
            raise ValueError(
                "Field cannot be empty."
            )

        return value