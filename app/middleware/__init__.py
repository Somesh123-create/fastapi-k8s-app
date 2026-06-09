"""Middleware module initialization."""

from app.middleware.security import verify_token

__all__ = ["verify_token"]
