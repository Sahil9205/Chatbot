"""
Chat Request Schema.

Represents an incoming chat request from a client.
"""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Chat request payload.
    """

    session_id: str = Field(
        ...,
        description="Session identifier.",
    )

    query: str = Field(
        ...,
        min_length=1,
        description="User query.",
    )