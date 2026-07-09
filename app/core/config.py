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

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


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

    DEFAULT_LLM_PROVIDER: str = "openai"

    DEFAULT_MODEL: str = "gpt-4.1"

    TEMPERATURE: float = 0.2

    MAX_TOKENS: int = 2048

    # ======================================================
    # Embeddings
    # ======================================================

    EMBEDDING_MODEL: str = "text-embedding-3-large"

    # ======================================================
    # API Keys
    # ======================================================

    OPENAI_API_KEY: str = ""

    GEMINI_API_KEY: str = ""

    ANTHROPIC_API_KEY: str = ""

    # ======================================================
    # Database
    # ======================================================

    DATABASE_URL: str = ""

    REDIS_URL: str = ""

    QDRANT_URL: str = ""

    # ======================================================
    # RAG
    # ======================================================

    CHUNK_SIZE: int = 1000

    CHUNK_OVERLAP: int = 200

    TOP_K: int = 5

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