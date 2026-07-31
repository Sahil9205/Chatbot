"""
Application lifespan.

Handles startup and shutdown events.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.ai.llm.llm import initialize_llm
from app.api.dependencies import get_container
from app.core.logging import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(
    app: FastAPI,
):
    """
    Manage application startup and shutdown.
    """

    ###############################################################
    # Startup
    ###############################################################

    logger.info("Starting application.")


    initialize_llm()


    # Initialize application container.
    get_container()

    logger.info("Application started successfully.")

    yield

    ###############################################################
    # Shutdown
    ###############################################################

    logger.info("Shutting down application.")

    # Future:
    # - Close Redis
    # - Flush Langfuse
    # - Close database connections
    # - Shutdown background workers

    logger.info("Application shutdown complete.")