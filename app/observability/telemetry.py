"""OpenTelemetry and Prometheus observability setup."""

import time
from datetime import datetime
from typing import Callable

from opentelemetry import metrics, trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from prometheus_client import Counter, Gauge, Histogram
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.config import settings

# Prometheus metrics
REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total requests",
    ["method", "endpoint", "status"],
)

REQUEST_DURATION = Histogram(
    "app_request_duration_seconds",
    "Request duration",
    ["method", "endpoint"],
)

REQUEST_SIZE = Histogram(
    "app_request_size_bytes",
    "Request size",
    ["method", "endpoint"],
)

RESPONSE_SIZE = Histogram(
    "app_response_size_bytes",
    "Response size",
    ["method", "endpoint"],
)

REQUEST_ERRORS = Counter(
    "app_requests_errors_total",
    "Total request errors",
    ["method", "endpoint", "error_type"],
)

ACTIVE_REQUESTS = Gauge(
    "app_active_requests",
    "Active requests",
)


def setup_opentelemetry() -> None:
    """Setup OpenTelemetry tracing and metrics."""
    if not settings.enable_tracing:
        return

    # Resource attributes
    resource = Resource.create(
        {
            SERVICE_NAME: settings.app_name,
            "environment": settings.environment,
            "version": settings.app_version,
        }
    )

    # Tracing setup
    if settings.jaeger_enabled:
        jaeger_exporter = JaegerExporter(
            agent_host_name=settings.jaeger_host,
            agent_port=settings.jaeger_port,
        )
        trace_provider = TracerProvider(resource=resource)
        trace_provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
    else:
        trace_provider = TracerProvider(resource=resource)

    trace.set_tracer_provider(trace_provider)

    # Metrics setup
    if settings.enable_metrics:
        prometheus_reader = PrometheusMetricReader()
        meter_provider = MeterProvider(
            resource=resource, metric_readers=[prometheus_reader]
        )
        metrics.set_meter_provider(meter_provider)

    # Instrumentations
    FastAPIInstrumentor.instrument_app(app)
    SQLAlchemyInstrumentor().instrument()
    RedisInstrumentor().instrument()
    HTTPXClientInstrumentor().instrument()


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware for collecting metrics."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and collect metrics.

        Args:
            request: Request object
            call_next: Next middleware/route handler

        Returns:
            Response object
        """
        ACTIVE_REQUESTS.inc()
        start_time = time.time()

        try:
            response = await call_next(request)
            request_duration = time.time() - start_time

            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.url.path,
                status=response.status_code,
            ).inc()

            REQUEST_DURATION.labels(
                method=request.method,
                endpoint=request.url.path,
            ).observe(request_duration)

            return response

        except Exception as e:
            REQUEST_ERRORS.labels(
                method=request.method,
                endpoint=request.url.path,
                error_type=type(e).__name__,
            ).inc()
            raise

        finally:
            ACTIVE_REQUESTS.dec()


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """Middleware for adding correlation IDs."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Add correlation ID to request.

        Args:
            request: Request object
            call_next: Next middleware/route handler

        Returns:
            Response object
        """
        correlation_id = request.headers.get("X-Correlation-ID", str(datetime.now().timestamp()))
        request.state.correlation_id = correlation_id

        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id

        return response
