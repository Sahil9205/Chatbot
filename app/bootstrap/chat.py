"""
Bootstrap Chat Service.
"""

from app.chat.chat_service import ChatService
from app.rag_engine.rag_engine import RAGEngine

from .conversation import ConversationContainer


def build_chat_service(
    rag_engine: RAGEngine,
    conversation_container: ConversationContainer,
) -> ChatService:
    """
    Build the ChatService.
    """

    return ChatService(

        rag_engine=rag_engine,

        session_service=(
            conversation_container.session_service
        ),

        memory_service=(
            conversation_container.memory_service
        ),
    )