"""
Observability package.

Provides a provider-agnostic interface for
application tracing and monitoring.
"""

from .manager import ObservabilityManager

__all__ = [
    "ObservabilityManager",
]