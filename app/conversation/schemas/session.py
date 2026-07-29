"""
Session schema.

Represents an active chat session.
"""

from datetime import UTC, datetime
from uuid import uuid4

from pydantic import BaseModel, Field


class Session(BaseModel):
    """
    Chat session.
    """

    session_id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique session identifier.",
    )

    conversation_id: str = Field(
        ...,
        description="Conversation associated with this session.",
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Session creation time.",
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Last activity time.",
    )