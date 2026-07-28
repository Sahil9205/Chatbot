"""
Conversation schema.

Represents a conversation between a user
and the AI assistant.
"""

from datetime import UTC, datetime
from uuid import uuid4

from pydantic import BaseModel, Field

from .message import Message


class Conversation(BaseModel):
    """
    Represents a conversation.
    """

    conversation_id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique conversation identifier.",
    )

    messages: list[Message] = Field(
        default_factory=list,
        description="Conversation messages.",
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Conversation creation time.",
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Last modification time.",
    )

    metadata: dict[str, str] = Field(
        default_factory=dict,
        description="Conversation metadata.",
    )