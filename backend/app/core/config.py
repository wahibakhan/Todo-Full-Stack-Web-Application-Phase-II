"""
Application configuration using Pydantic settings.
All environment variables loaded from .env file.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Required environment variables:
    - BETTER_AUTH_SECRET: Shared secret for JWT (MUST match frontend)
    - DATABASE_URL: Neon PostgreSQL connection string
    """

    # JWT Configuration
    BETTER_AUTH_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24

    # Database Configuration
    DATABASE_URL: str

    # Application Configuration
    ENVIRONMENT: str = "development"
    API_V1_PREFIX: str = "/api"

    # CORS Configuration
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


# Global settings instance
settings = Settings()
