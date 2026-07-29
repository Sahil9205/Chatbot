"""
Chat Response Schema.

Represents the response returned to the client.
"""

from pydantic import BaseModel, Field

from app.rag_engine.generation.schemas.citation import Citation


class ChatResponse(BaseModel):
    """
    Chat response returned by the application.
    """

    session_id: str = Field(
        ...,
        description="Session identifier.",
    )

    answer: str = Field(
        ...,
        description="Assistant response.",
    )

    citations: list[Citation] = Field(
        default_factory=list,
        description="Supporting citations.",
    )

    generation_time: float = Field(
        ...,
        ge=0.0,
        description="Generation latency in seconds.",
    )

    has_sufficient_context: bool = Field(
        ...,
        description=(
            "Whether sufficient context was available "
            "to answer the query."
        ),
    )