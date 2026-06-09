"""FastAPI application factory."""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from app.api.v1 import router as api_router
from app.core.config import settings
from app.core.database import close_db, init_db
from app.core.logging_config import setup_logging
from app.observability import (
    CorrelationIdMiddleware,
    MetricsMiddleware,
    setup_opentelemetry,
)

# Setup logging
setup_logging()
logger = logging.getLogger("app")


def create_app() -> FastAPI:
    """Create and configure FastAPI application.

    Returns:
        FastAPI: Configured application instance
    """
    # Create FastAPI app
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Production-ready FastAPI microservice",
        docs_url=settings.docs_url,
        openapi_url=settings.openapi_url,
        redoc_url=settings.redoc_url,
        debug=settings.debug,
        default_response_class=ORJSONResponse,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_credentials,
        allow_methods=settings.cors_methods,
        allow_headers=settings.cors_headers,
    )

    # Add custom middleware
    app.add_middleware(CorrelationIdMiddleware)
    app.add_middleware(MetricsMiddleware)

    # Setup OpenTelemetry
    setup_opentelemetry(app)

    # Include routers
    app.include_router(api_router)

    # Event handlers
    @app.on_event("startup")
    async def startup_event() -> None:
        """Startup event handler."""
        logger.info(f"Starting {settings.app_name} v{settings.app_version}")
        await init_db()
        logger.info("Database initialized")

    @app.on_event("shutdown")
    async def shutdown_event() -> None:
        """Shutdown event handler."""
        logger.info(f"Shutting down {settings.app_name}")
        await close_db()
        logger.info("Database closed")

    return app


# Create app instance
app = create_app()
