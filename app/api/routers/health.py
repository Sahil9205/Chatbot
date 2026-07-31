"""
Health Router.

Provides application health endpoints.
"""

from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("")
def health() -> dict[str, str]:
    """
    Health check endpoint.
    """

    return {
        "status": "healthy",
    }