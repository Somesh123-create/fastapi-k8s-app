"""User repository."""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """User repository with custom queries."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize user repository.

        Args:
            session: AsyncSession instance
        """
        super().__init__(session, User)

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email.

        Args:
            email: User email

        Returns:
            User or None
        """
        statement = select(User).where(User.email == email)
        result = await self.session.execute(statement)
        return result.scalars().first()

    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username.

        Args:
            username: User username

        Returns:
            User or None
        """
        statement = select(User).where(User.username == username)
        result = await self.session.execute(statement)
        return result.scalars().first()

    async def get_active_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Get active users.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of active users
        """
        statement = select(User).where(User.is_active.is_(True)).offset(skip).limit(limit)
        result = await self.session.execute(statement)
        return list(result.scalars().all())
