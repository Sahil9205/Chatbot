"""
Application Entry Point.
"""

from fastapi import FastAPI

from app.api.lifespan import lifespan

from app.api.routers.chat import router as chat_router
from app.api.routers.health import router as health_router
from app.api.routers.session import router as session_router


app = FastAPI(
    title="Production RAG Chatbot",
    description="Enterprise Retrieval-Augmented Generation API",
    version="1.0.0",
    lifespan=lifespan,
)


###############################################################
# API Routers
###############################################################

app.include_router(
    health_router,
    prefix="/api/v1",
)

app.include_router(
    session_router,
    prefix="/api/v1",
)

app.include_router(
    chat_router,
    prefix="/api/v1",
)