"""
Chat Response Schema.
"""

from pydantic import BaseModel, Field

from app.rag_engine.generation.schemas.citation import Citation


class ChatResponse(BaseModel):
    """
    Outgoing chat response.
    """

    conversation_id: str = Field(
        ...,
        description="Conversation identifier.",
    )

    answer: str = Field(
        ...,
        description="Generated answer.",
    )

    citations: list[Citation] = Field(
        default_factory=list,
        description="Supporting citations.",
    )