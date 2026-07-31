"""
FastAPI Dependencies.

Provides application-level dependencies.
"""

from app.conversation.memory_service import MemoryService
from app.conversation.session_service import SessionService

from functools import lru_cache

from app.bootstrap.container import ApplicationContainer
from app.chat.chat_service import ChatService


@lru_cache
def get_container() -> ApplicationContainer:
    """
    Return the singleton application container.
    """

    return ApplicationContainer()


def get_chat_service() -> ChatService:
    """
    Return the configured ChatService.
    """

    return get_container().chat_service


def get_session_service() -> SessionService:
    """
    Return the configured SessionService.
    """

    return get_container().session_service



def get_memory_service() -> MemoryService:
     
    """
    Return configured MemoryService.
    """

    return get_container().memory_service