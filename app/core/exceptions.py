"""
Custom Exceptions
=================

This module contains all custom exceptions used throughout the
application.
"""




class ApplicationError(Exception):
    """
    Base exception for the application.

    All custom exceptions should inherit from this class.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        return self.message


class ConfigurationError(ApplicationError):
    """Raised when application configuration is invalid."""


class DatabaseError(ApplicationError):
    """Raised when a database operation fails."""


class LLMError(ApplicationError):
    """Raised when an LLM request fails."""

class IntentClassificationError(ApplicationError):
    """Raised when query intent classification fails."""


########################################################################
# Conversation
########################################################################


class ConversationError(ApplicationError):
    """
    Base conversation exception.
    """


class ConversationNotFoundError(ConversationError):
    """
    Raised when a conversation does not exist.
    """


class SessionNotFoundError(ConversationError):
    """
    Raised when a session cannot be found.
    """


class MemoryError(ApplicationError):
    """
    Raised when memory operations fail.
    """

########################################################################
# Documents
########################################################################

class DocumentLoadingError(ApplicationError):
    """Raised when a document cannot be loaded."""


class RetrievalError(ApplicationError):
    """Raised when document retrieval fails."""


class GuardrailError(ApplicationError):
    """Raised when guardrail validation fails."""


class ValidationError(ApplicationError):
    """Raised when input validation fails."""