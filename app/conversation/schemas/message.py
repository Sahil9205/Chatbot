"""
Message schema.

Represents a single message in a conversation.
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class MessageRole(str, Enum):
    """
    Supported chat roles.
    """

    USER = "user"

    ASSISTANT = "assistant"

    SYSTEM = "system"


class Message(BaseModel):
    """
    Represents a single chat message.
    """

    role: MessageRole = Field(
        ...,
        description="Role of the message sender.",
    )

    content: str = Field(
        ...,
        min_length=1,
        description="Message content.",
    )

    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Message creation time.",
    )