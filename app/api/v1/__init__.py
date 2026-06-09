"""API v1 endpoints module."""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, health, metrics, users

# Create main router
router = APIRouter(prefix="/api/v1")

# Include sub-routers
router.include_router(health.router)
router.include_router(auth.router)
router.include_router(users.router)
router.include_router(metrics.router)

__all__ = ["router"]
