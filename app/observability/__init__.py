"""Observability module initialization."""

from app.observability.telemetry import (
    CorrelationIdMiddleware,
    MetricsMiddleware,
    setup_opentelemetry,
)

__all__ = [
    "setup_opentelemetry",
    "MetricsMiddleware",
    "CorrelationIdMiddleware",
]
