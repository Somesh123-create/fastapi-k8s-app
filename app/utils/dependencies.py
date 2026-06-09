"""Dependency injection for FastAPI."""

from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import decode_token
from app.models import User
from app.repositories.user import UserRepository
from app.services.user import UserService


async def get_user_service(session: AsyncSession = Depends(get_db)) -> UserService:
    """Get user service.

    Args:
        session: Database session (injected)

    Returns:
        UserService instance
    """
    if session is None:
        async for session in get_db():
            pass
    return UserService(session)


async def get_current_user(token: str, session: AsyncSession) -> User:
    """Get current user from token.

    Args:
        token: JWT token
        session: Database session (injected)

    Returns:
        Current user

    Raises:
        ValueError: If token is invalid or user not found
    """
    payload = decode_token(token)
    if not payload:
        raise ValueError("Invalid token")

    user_id = payload.get("sub")
    if not user_id:
        raise ValueError("Invalid token")

    repository = UserRepository(session)
    user = await repository.get(user_id)
    if not user:
        raise ValueError("User not found")

    return user
