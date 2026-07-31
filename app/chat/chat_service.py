"""
Chat Service.

Coordinates chat interactions between the
application layer and the RAG engine.
"""
from app.core.logging import get_logger

from app.conversation.memory_service import MemoryService
from app.conversation.schemas.message import (
    Message,
    MessageRole,
)
from app.conversation.session_service import SessionService

from app.api.schemas.chat_request import ChatRequest
from app.api.schemas.chat_response import ChatResponse

from app.rag_engine.rag_engine import RAGEngine


logger = get_logger(__name__)


class ChatService:
    """
    High-level application service.
    """

    def __init__(
        self,
        rag_engine: RAGEngine,
        session_service: SessionService,
        memory_service: MemoryService,
    ) -> None:

        self.rag_engine = rag_engine

        self.session_service = session_service

        self.memory_service = memory_service

    ####################################################################
    # Public Methods
    ####################################################################

    def chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:
        """
        Process a user chat request.
        """

        logger.info("Processing chat request.")

        conversation_id = (
            self.session_service.get_conversation_id(
                request.session_id
            )
        )

        ###############################################################
        # Store User Message
        ###############################################################

        self.memory_service.add_message(

            conversation_id,

            Message(

                role=MessageRole.USER,

                content=request.query,
            ),
        )

        ###############################################################
        # Run RAG
        ###############################################################

        generation_response = self.rag_engine.answer(
            query=request.message,
        )

        ###############################################################
        # Store Assistant Message
        ###############################################################

        self.memory_service.add_message(

            conversation_id,

            Message(

                role=MessageRole.ASSISTANT,

                content=generation_response.answer.text,
            ),
        )

        logger.info(
            "Chat request completed."
        )

        return ChatResponse(
            
            session_id=request.session_id,
            answer=generation_response.answer.text,
            citations=generation_response.citations,
            generation_time=generation_response.generation_time,
            has_sufficient_context=generation_response.has_sufficient_context,
        )