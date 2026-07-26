"""
Application Container.

Provides a single place where all application
dependencies are created and managed.
"""

from app.rag_engine.rag_engine import RAGEngine

from .rag import build_rag_engine


class ApplicationContainer:
    """
    Dependency Injection Container.

    Responsible for constructing all application
    services exactly once.
    """

    def __init__(self) -> None:
        """
        Initialize the application container.
        """

        self._rag_engine = build_rag_engine()

    ####################################################################
    # Properties
    ####################################################################

    @property
    def rag_engine(self) -> RAGEngine:
        """
        Return the configured RAG Engine.
        """

        return self._rag_engine