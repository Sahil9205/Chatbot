"""
Langfuse Observability Provider.

Concrete implementation of the BaseObservability interface
using Langfuse.
"""

from __future__ import annotations

from typing import Any

from langfuse import Langfuse

from app.core.config import settings
from app.core.logging import get_logger
from app.observability.base import BaseObservability

logger = get_logger(__name__)


class LangfuseProvider(BaseObservability):
    """
    Langfuse implementation of the observability interface.
    """

    def __init__(self) -> None:
        """
        Initialize the Langfuse client.
        """

        self.client = Langfuse(
            public_key=settings.LANGFUSE_PUBLIC_KEY,
            secret_key=settings.LANGFUSE_SECRET_KEY,
            host=settings.LANGFUSE_HOST,
        )

        logger.info("Langfuse initialized.")

    def start_trace(self,name: str,**kwargs: Any,) -> Any:
        """
        Start a new trace.
        """

        return self.client.trace(
            name=name,
            **kwargs,
        )

    def end_trace(self,trace: Any,) -> None:
        """
        End a trace.
        """

        trace.update()

    def start_span(self, trace: Any, name: str, **kwargs: Any,) -> Any:
        """
        Start a span.
        """

        return trace.span(
            name=name,
            **kwargs,
        )

    def end_span(self, span: Any,) -> None:
        """
        End a span.
        """

        span.end()

    def log_event(self, trace: Any, name: str, data: dict[str, Any] | None = None,) -> None:
        """
        Record an event.
        """

        trace.event(
            name=name,
            metadata=data,
        )

    def record_error( self, trace: Any, error: Exception,) -> None:
        """
        Record an exception.
        """

        trace.event(
            name="error",
            metadata={
                "type": type(error).__name__,
                "message": str(error),
            },
        )