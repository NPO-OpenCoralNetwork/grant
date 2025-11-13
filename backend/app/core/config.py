from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""

    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Grants Search API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Backend API for Japanese Subsidies and Grants Search"

    # CORS Settings
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:8501",  # Streamlit default port
        "http://127.0.0.1:8501",
    ]

    # External API Settings
    JGRANTS_BASE_URL: str = "https://api.jgrants-portal.go.jp/exp/v1/public"

    # Redis Settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_CACHE_TTL: int = 3600  # 1 hour

    # Database Settings
    DATABASE_URL: Optional[str] = None

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
