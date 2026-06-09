"""Metrics endpoint."""

import time
from datetime import datetime

from fastapi import APIRouter, status
from prometheus_client import generate_latest

from app.schemas import MetricsResponse

router = APIRouter(tags=["metrics"])

# Track application start time
app_start_time = time.time()


@router.get("/metrics", status_code=status.HTTP_200_OK)
async def metrics() -> str:
    """Get Prometheus metrics.

    Returns:
        str: Prometheus metrics in text format
    """
    return generate_latest().decode("utf-8")


@router.get("/metrics/summary", response_model=MetricsResponse, status_code=status.HTTP_200_OK)
async def metrics_summary() -> MetricsResponse:
    """Get metrics summary.

    Returns:
        MetricsResponse: Metrics summary
    """
    uptime = time.time() - app_start_time

    return MetricsResponse(
        timestamp=datetime.utcnow(),
        uptime_seconds=uptime,
        requests_total=0,
        requests_errors=0,
        database_connections=0,
    )
