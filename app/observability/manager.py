"""
Observability Manager.

Acts as the application's single entry point for observability.

All application components should interact with this manager
instead of talking directly to a specific provider.
"""

from __future__ import annotations

from typing import Any

from app.observability.base import BaseObservability


class ObservabilityManager:
    """
    Central observability manager.
    """

    def __init__(
        self,
        provider: BaseObservability,
    ) -> None:
        """
        Initialize the manager.

        Parameters
        ----------
        provider : BaseObservability
            Observability provider implementation.
        """

        self._provider = provider

    def start_trace(
        self,
        name: str,
        **kwargs: Any,
    ) -> Any:
        """
        Start a trace.
        """

        return self._provider.start_trace(
            name=name,
            **kwargs,
        )

    def end_trace(
        self,
        trace: Any,
    ) -> None:
        """
        End a trace.
        """

        self._provider.end_trace(trace)

    def start_span(
        self,
        trace: Any,
        name: str,
        **kwargs: Any,
    ) -> Any:
        """
        Start a span.
        """

        return self._provider.start_span(
            trace=trace,
            name=name,
            **kwargs,
        )

    def end_span(
        self,
        span: Any,
    ) -> None:
        """
        End a span.
        """

        self._provider.end_span(span)

    def log_event(
        self,
        trace: Any,
        name: str,
        data: dict[str, Any] | None = None,
    ) -> None:
        """
        Log an event.
        """

        self._provider.log_event(
            trace=trace,
            name=name,
            data=data,
        )

    def record_error(
        self,
        trace: Any,
        error: Exception,
    ) -> None:
        """
        Record an exception.
        """

        self._provider.record_error(
            trace=trace,
            error=error,
        )