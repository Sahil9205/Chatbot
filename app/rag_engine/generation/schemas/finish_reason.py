"""
Generation finish reasons.
"""

from enum import Enum


class FinishReason(str, Enum):
    """
    Reason why generation stopped.
    """

    STOP = "stop"

    LENGTH = "length"

    CONTENT_FILTER = "content_filter"

    TOOL_CALL = "tool_call"

    ERROR = "error"