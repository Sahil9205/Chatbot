"""
Schema for metadata filters extracted from a user query.
"""

from typing import Any

from pydantic import BaseModel, Field, field_validator


class MetadataFilter(BaseModel):
    """
    Represents a single metadata filter.
    """

    field: str = Field(
        ...,
        min_length=1,
        description="Metadata field name.",
    )

    operator: str = Field(
        ...,
        description="Comparison operator.",
    )

    value: Any = Field(
        ...,
        description="Value used for filtering.",
    )

    @field_validator("field", "operator")
    @classmethod
    def validate_string_fields(cls, value: str) -> str:
        """
        Remove leading and trailing whitespace.
        """

        value = value.strip()

        if not value:
            raise ValueError(
                "Field cannot be empty."
            )

        return value


class MetadataExtraction(BaseModel):
    """
    Structured response returned by the metadata extractor.
    """

    filters: list[MetadataFilter] = Field(
        default_factory=list,
        description="Metadata filters extracted from the user query.",
    )

    reasoning: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Short explanation of the extracted metadata.",
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