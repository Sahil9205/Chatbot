"""
Conversation Service.

Responsible for creating, retrieving, updating,
and deleting chat conversations.
"""

from datetime import UTC, datetime

from app.core.exceptions import ConversationNotFoundError
from app.core.logging import get_logger

from .schemas.conversation import Conversation
from .schemas.message import Message


logger = get_logger(__name__)


class ConversationService:
    """
    Manages conversations for the application.

    Notes
    -----
    Currently conversations are stored in memory.

    In production this implementation can be replaced
    with Redis or a database without changing the
    public interface.
    """

    def __init__(self) -> None:
        """
        Initialize the conversation store.
        """

        self._conversations: dict[str, Conversation] = {}

    ####################################################################
    # Public Methods
    ####################################################################

    def create_conversation(self) -> Conversation:
        """
        Create a new conversation.

        Returns
        -------
        Conversation
        """

        conversation = Conversation()

        self._conversations[
            conversation.conversation_id
        ] = conversation

        logger.info(
            "Created conversation '%s'.",
            conversation.conversation_id,
        )

        return conversation

    def get_conversation(
        self,
        conversation_id: str,
    ) -> Conversation:
        """
        Retrieve a conversation.

        Parameters
        ----------
        conversation_id : str

        Returns
        -------
        Conversation

        Raises
        ------
        ConversationNotFoundError
        """

        conversation = self._conversations.get(
            conversation_id
        )

        if conversation is None:

            logger.warning(
                "Conversation '%s' not found.",
                conversation_id,
            )

            raise ConversationNotFoundError(
                f"Conversation '{conversation_id}' does not exist."
            )

        return conversation

    def add_message(
        self,
        conversation_id: str,
        message: Message,
    ) -> None:
        """
        Add a message to a conversation.

        Parameters
        ----------
        conversation_id : str

        message : Message
        """

        conversation = self.get_conversation(
            conversation_id
        )

        conversation.messages.append(
            message
        )

        conversation.updated_at = datetime.now(
            UTC
        )

        logger.info(
            "Added message to conversation '%s'.",
            conversation_id,
        )

    def clear_conversation(
        self,
        conversation_id: str,
    ) -> None:
        """
        Remove all messages from a conversation.

        Parameters
        ----------
        conversation_id : str
        """

        conversation = self.get_conversation(
            conversation_id
        )

        conversation.messages.clear()

        conversation.updated_at = datetime.now(
            UTC
        )

        logger.info(
            "Cleared conversation '%s'.",
            conversation_id,
        )

    def delete_conversation(
        self,
        conversation_id: str,
    ) -> None:
        """
        Delete a conversation.

        Parameters
        ----------
        conversation_id : str

        Raises
        ------
        ConversationNotFoundError
        """

        self.get_conversation(
            conversation_id
        )

        del self._conversations[
            conversation_id
        ]

        logger.info(
            "Deleted conversation '%s'.",
            conversation_id,
        )