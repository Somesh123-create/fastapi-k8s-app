"""Health check endpoints."""

from datetime import datetime, timedelta

from fastapi import APIRouter, status

from app.core.config import settings
from app.schemas import HealthResponse

router = APIRouter(tags=["health"])

# Track application start time
app_start_time = datetime.utcnow()


@router.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def health() -> HealthResponse:
    """Health check endpoint.

    Returns:
        HealthResponse: Health status
    """
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        environment=settings.environment,
    )


@router.get("/ready", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def readiness() -> HealthResponse:
    """Readiness probe endpoint.

    Returns:
        HealthResponse: Readiness status
    """
    return HealthResponse(
        status="ready",
        version=settings.app_version,
        environment=settings.environment,
    )


@router.get("/live", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def liveness() -> HealthResponse:
    """Liveness probe endpoint.

    Returns:
        HealthResponse: Liveness status
    """
    return HealthResponse(
        status="alive",
        version=settings.app_version,
        environment=settings.environment,
    )


@router.get("/startup", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def startup() -> HealthResponse:
    """Startup probe endpoint.

    Returns:
        HealthResponse: Startup status
    """
    uptime = datetime.utcnow() - app_start_time
    if uptime < timedelta(seconds=5):
        return HealthResponse(
            status="starting",
            version=settings.app_version,
            environment=settings.environment,
        )

    return HealthResponse(
        status="started",
        version=settings.app_version,
        environment=settings.environment,
    )
