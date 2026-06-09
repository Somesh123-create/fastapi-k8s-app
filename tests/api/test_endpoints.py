"""API tests for FastAPI endpoints."""

import pytest
from httpx import AsyncClient

from app.main import app


@pytest.fixture
async def client():
    """Create test client."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
class TestHealthEndpoints:
    """Test health check endpoints."""

    async def test_health(self, client: AsyncClient) -> None:
        """Test health endpoint."""
        response = await client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    async def test_readiness(self, client: AsyncClient) -> None:
        """Test readiness endpoint."""
        response = await client.get("/api/v1/ready")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"

    async def test_liveness(self, client: AsyncClient) -> None:
        """Test liveness endpoint."""
        response = await client.get("/api/v1/live")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "alive"


@pytest.mark.asyncio
class TestAuthEndpoints:
    """Test authentication endpoints."""

    async def test_login_invalid_credentials(self, client: AsyncClient) -> None:
        """Test login with invalid credentials."""
        response = await client.post(
            "/api/v1/auth/login",
            json={"username": "nonexistent", "password": "wrong"},
        )
        assert response.status_code == 401


@pytest.mark.asyncio
class TestMetricsEndpoints:
    """Test metrics endpoints."""

    async def test_metrics_summary(self, client: AsyncClient) -> None:
        """Test metrics summary endpoint."""
        response = await client.get("/api/v1/metrics/summary")
        assert response.status_code == 200
        data = response.json()
        assert "timestamp" in data
        assert "uptime_seconds" in data
