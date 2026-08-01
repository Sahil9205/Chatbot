"""
Trace Context.

Stores the active trace and span for the current request.
"""

from __future__ import annotations

from typing import Any


class TraceContext:
    """
    Stores the current trace and span.
    """

    _trace: Any | None = None
    _span: Any | None = None

    @classmethod
    def set_trace(
        cls,
        trace: Any,
    ) -> None:
        cls._trace = trace

    @classmethod
    def get_trace(cls) -> Any | None:
        return cls._trace

    @classmethod
    def clear_trace(cls) -> None:
        cls._trace = None

    @classmethod
    def set_span(
        cls,
        span: Any,
    ) -> None:
        cls._span = span

    @classmethod
    def get_span(cls) -> Any | None:
        return cls._span

    @classmethod
    def clear_span(cls) -> None:
        cls._span = None

    @classmethod
    def clear(cls) -> None:
        cls._trace = None
        cls._span = None