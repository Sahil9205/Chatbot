"""
Base Observability Interface.

Defines the contract for all observability providers.

Every observability backend (Langfuse, OpenTelemetry, etc.)
must implement this interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseObservability(ABC):
    """
    Abstract base class for observability providers.
    """

    @abstractmethod
    def start_trace(self,
        name: str,
        **kwargs: Any,) -> Any:
        """
        Start a new trace.

        Parameters
        ----------
        name : str
            Name of the trace.

        Returns
        -------
        Any
            Provider-specific trace object.
        """
        pass

    @abstractmethod
    def end_trace(self,
        trace: Any,) -> None:
        """
        Finish a trace.
        """
        pass

    @abstractmethod
    def start_span(self,
        trace: Any,
        name: str,
        **kwargs: Any,) -> Any:
        """
        Start a child span.
        """
        pass

    @abstractmethod
    def end_span(self,
        span: Any,) -> None:
        """
        Finish a span.
        """
        pass

    @abstractmethod
    def log_event(self,
        trace: Any,
        name: str,
        data: dict[str, Any] | None = None,) -> None:
        """
        Record an event.
        """
        pass

    @abstractmethod
    def record_error(self,
        trace: Any,
        error: Exception,) -> None:
        """
        Record an exception.
        """
        pass