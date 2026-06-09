"""Application configuration and settings."""

from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables."""

    # Application
    app_name: str = "FastAPI K8s App"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = False

    # API
    api_v1_prefix: str = "/api/v1"
    openapi_url: str = "/openapi.json"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi_db"
    database_pool_size: int = 20
    database_max_overflow: int = 10
    database_pool_pre_ping: bool = True
    database_pool_recycle: int = 3600

    # Redis
    redis_url: str = "redis://localhost:6379/0"
    redis_pool_min_size: int = 5
    redis_pool_max_size: int = 10

    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # Observability
    enable_logging: bool = True
    log_level: str = "INFO"
    enable_tracing: bool = True
    jaeger_enabled: bool = False
    jaeger_host: str = "localhost"
    jaeger_port: int = 6831
    enable_metrics: bool = True
    metrics_port: int = 8001

    # CORS
    cors_origins: list[str] = ["*"]
    cors_credentials: bool = True
    cors_methods: list[str] = ["*"]
    cors_headers: list[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = False

    def get_database_url(self) -> str:
        """Get database URL."""
        return self.database_url

    def get_redis_url(self) -> str:
        """Get Redis URL."""
        return self.redis_url


settings = Settings()
