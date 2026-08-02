"""
Observability bootstrap.

Creates and configures the application's
observability implementation.
"""

from app.observability.langfuse_provider import (
    LangfuseProvider,
)
from app.observability.manager import (
    ObservabilityManager,
)


def build_observability() -> ObservabilityManager:
    """
    Build the application's observability manager.
    """

    provider = LangfuseProvider()

    return ObservabilityManager(provider)