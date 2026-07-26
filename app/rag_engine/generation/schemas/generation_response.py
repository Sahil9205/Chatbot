"""
Schema representing the final output of the
generation pipeline.
"""

from pydantic import BaseModel, Field, field_validator

from .answer import Answer
from .citation import Citation


class GenerationResponse(BaseModel):
    """
    Final response returned by the generation pipeline.
    """

    answer: Answer = Field(
        ...,
        description="Generated answer.",
    )

    citations: list[Citation] = Field(
        default_factory=list,
        description="Supporting citations.",
    )

    has_sufficient_context: bool = Field(
        default=True,
        description=(
            "Whether the retrieved context is sufficient "
            "to answer the user's question."
        ),
    )

    generation_time: float = Field(
        ...,
        ge=0.0,
        description="Generation latency in seconds.",
    )

    prompt_tokens: int = Field(
        default=0,
        ge=0,
        description="Prompt token count.",
    )

    completion_tokens: int = Field(
        default=0,
        ge=0,
        description="Completion token count.",
    )

    total_tokens: int = Field(
        default=0,
        ge=0,
        description="Total token usage.",
    )

    @field_validator("total_tokens")
    @classmethod
    def validate_total_tokens(
        cls,
        value: int,
        info,
    ) -> int:
        """
        Ensure total_tokens is correct.
        """

        prompt = info.data.get(
            "prompt_tokens",
            0,
        )

        completion = info.data.get(
            "completion_tokens",
            0,
        )

        if value != prompt + completion:
            raise ValueError(
                "total_tokens must equal prompt_tokens + completion_tokens."
            )

        return value