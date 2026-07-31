"""
Application Container.

Creates and owns all application dependencies.
Acts as the Composition Root of the application.
"""

from app.chat.chat_service import ChatService
from app.rag_engine.rag_engine import RAGEngine

from .chat import build_chat_service
from .conversation import ConversationContainer
from .rag import build_rag_engine

from app.conversation.conversation_service import ConversationService
from app.conversation.session_service import SessionService
from app.conversation.memory_service import MemoryService


class ApplicationContainer:
    """
    Dependency Injection Container.

    Responsible for constructing every application
    service exactly once.
    """

    def __init__(self) -> None:

        ###############################################################
        # RAG Engine
        ###############################################################

        self._rag_engine = build_rag_engine()

        ###############################################################
        # Conversation Layer
        ###############################################################

        self._conversation = ConversationContainer()

        ###############################################################
        # Chat Service
        ###############################################################

        self._chat_service = build_chat_service(
            rag_engine=self._rag_engine,
            conversation_container=self._conversation,
        )

    ####################################################################
    # Properties
    ####################################################################

    @property
    def rag_engine(self) -> RAGEngine:
        """
        Return configured RAG Engine.
        """

        return self._rag_engine

    @property
    def conversation(self) -> ConversationContainer:
        """
        Return conversation container.
        """

        return self._conversation

    @property
    def chat_service(self) -> ChatService:
        """
        Return configured ChatService.
        """

        return self._chat_service

    @property
    def conversation_service(self) -> ConversationService:
        """
        Return configured ConversationService.
        """

        return self._conversation.conversation_service


    @property
    def session_service(self) -> SessionService:
        """
        Return configured SessionService.
        """

        return self._conversation.session_service


    @property
    def memory_service(self) -> MemoryService:
        """
        Return configured MemoryService.
        """

        return self._conversation.memory_service