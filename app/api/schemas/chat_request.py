"""
Chat Request Schema.
"""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Incoming chat request.
    """

    conversation_id: str | None = Field(
        default=None,
        description="Existing conversation identifier.",
    )

    message: str = Field(
        ...,
        min_length=1,
        description="User message.",
    )