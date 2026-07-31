"""
Memory Service.

Provides access to conversation memory.
"""

from app.core.logging import get_logger

from .conversation_service import ConversationService
from .schemas.message import Message


logger = get_logger(__name__)


class MemoryService:
    """
    Manages conversation memory.
    """

    def __init__(
        self,
        conversation_service: ConversationService,
    ) -> None:
        """
        Parameters
        ----------
        conversation_service : ConversationService
        """

        self.conversation_service = conversation_service

    ####################################################################
    # Public Methods
    ####################################################################

    def add_message(
        self,
        conversation_id: str,
        message: Message,
    ) -> None:
        """
        Store a message in conversation memory.
        """

        self.conversation_service.add_message(
            conversation_id=conversation_id,
            message=message,
        )

    def get_messages(
        self,
        conversation_id: str,
    ) -> list[Message]:
        """
        Return the complete conversation history.
        """

        conversation = self.conversation_service.get_conversation(
            conversation_id
        )

        return conversation.messages

    def clear_memory(
        self,
        conversation_id: str,
    ) -> None:
        """
        Remove all stored messages.
        """

        self.conversation_service.clear_conversation(
            conversation_id
        )