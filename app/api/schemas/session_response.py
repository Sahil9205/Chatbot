"""
Session Response Schema.
"""

from pydantic import BaseModel, Field


class SessionResponse(BaseModel):
    """
    Response returned after creating a session.
    """

    session_id: str = Field(
        ...,
        description="Unique session identifier.",
    )