"""
Application Configuration

This module centralizes all application settings.

Instead of calling os.getenv() throughout the project,
every component imports the Settings object from here.

Benefits
--------
• Single source of truth
• Type safety
• Easy validation
• Environment-specific configuration
• Better maintainability
"""

from functools import lru_cache
import os

from dotenv import load_dotenv

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()  # Load environment variables from .env file


class Settings(BaseSettings):
    """
    Global application settings.

    Values are automatically loaded from the .env file.
    """

    # ======================================================
    # Application
    # ======================================================

    APP_NAME: str = "Enterprise RAG Chatbot"

    APP_VERSION: str = "1.0.0"

    ENVIRONMENT: str = Field(default="development")

    DEBUG: bool = False

    # ======================================================
    # API
    # ======================================================

    HOST: str = "0.0.0.0"

    PORT: int = 8000

    API_V1_PREFIX: str = "/api/v1"

    # ======================================================
    # LLM
    # ======================================================

    DEFAULT_LLM_PROVIDER: str = "huggingface"

    LLM_MODEL_NAME: str = "mistralai/Mistral-7B-Instruct-v0.3"

    TEMPERATURE: float = 0.2

    MAX_NEW_TOKENS: int = 2048

    # ======================================================
    # Embeddings
    # ======================================================

    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"

    # ======================================================
    # Reranker
    # ======================================================

    RERANKER_MODEL_NAME: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"

    # ======================================================
    # API Keys
    # ======================================================

    OPENAI_API_KEY: str = ""

    GEMINI_API_KEY: str = ""

    ANTHROPIC_API_KEY: str = ""

    HUGGINGFACE_API_KEY: str = os.getenv("HUGGINGFACE_API_KEY")

    # ======================================================
    # Database
    # ======================================================

    DATABASE_URL: str = ""

    REDIS_URL: str = ""

    # ======================================================
    # Qdrant
    # ======================================================

    QDRANT_URL: str = load_dotenv("QDRANT_URL")
    QDRANT_API_KEY: str = load_dotenv("QDRANT_API_KEY") 
    QDRANT_COLLECTION_NAME: str = load_dotenv("QDRANT_COLLECTION_NAME")
    QDRANT_DISTANCE_METRIC: str = "cosine"

    # ======================================================
    # RAG
    # ======================================================sw

    CHUNK_SIZE: int = 1000

    CHUNK_OVERLAP: int = 200

    TOP_K: int = 5

    RRF_K: int = 60

    DENSE_TOP_K: int = 20

    SPARSE_TOP_K: int = 20

    FINAL_TOP_K: int = 10

    # ======================================================
    # generation
    # ======================================================

    RETRIEVAL_SCORE_THRESHOLD: float = 0.70

    MINIMUM_CITATIONS: int = 1
    

    # ======================================================
    # Logging
    # ======================================================

    LOG_LEVEL: str = "INFO"

    # ======================================================
    # Security
    # ======================================================

    SECRET_KEY: str = ""

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Tell Pydantic where to load settings from
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached Settings instance.

    lru_cache ensures the configuration
    is loaded only once during the application's lifetime.
    """
    return Settings()


settings = get_settings()