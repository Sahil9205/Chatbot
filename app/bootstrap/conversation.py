"""
Bootstrap Conversation Services.
"""

from app.conversation.conversation_service import (
    ConversationService,
)
from app.conversation.memory_service import (
    MemoryService,
)
from app.conversation.session_service import (
    SessionService,
)


class ConversationContainer:
    """
    Builds all conversation-related services.
    """

    def __init__(self) -> None:

        ###############################################################
        # Conversation Service
        ###############################################################

        self.conversation_service = (
            ConversationService()
        )

        ###############################################################
        # Memory Service
        ###############################################################

        self.memory_service = (
            MemoryService(
                conversation_service=self.conversation_service,
            )
        )

        ###############################################################
        # Session Service
        ###############################################################

        self.session_service = (
            SessionService(
                conversation_service=self.conversation_service,
            )
        )