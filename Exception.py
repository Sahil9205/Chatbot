"""
Custom Exceptions
=================

This module contains all custom exceptions used throughout the
application.

Why Custom Exceptions?
----------------------
Instead of raising generic exceptions, custom exceptions make the
code more readable, easier to debug, and simpler to handle.

Example
-------
try:
    ...
except Exception as e:
    raise RetrievalError("Failed to retrieve documents.") from e
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


class RetrievalError(ApplicationError):
    """Raised when document retrieval fails."""


class GuardrailError(ApplicationError):
    """Raised when guardrail validation fails."""


class ValidationError(ApplicationError):
    """Raised when input validation fails."""