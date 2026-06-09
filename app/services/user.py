"""User service layer."""

import uuid
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.models import User
from app.repositories.user import UserRepository
from app.schemas import UserCreate, UserUpdate


class UserService:
    """User service with business logic."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize user service.

        Args:
            session: AsyncSession instance
        """
        self.repository = UserRepository(session)

    async def create_user(self, user_in: UserCreate) -> User:
        """Create new user.

        Args:
            user_in: User creation data

        Returns:
            Created user

        Raises:
            ValueError: If user already exists
        """
        # Check if user already exists
        existing_user = await self.repository.get_by_email(user_in.email)
        if existing_user:
            raise ValueError(f"User with email {user_in.email} already exists")

        existing_user = await self.repository.get_by_username(user_in.username)
        if existing_user:
            raise ValueError(f"User with username {user_in.username} already exists")

        # Create user
        user_data = user_in.model_dump(exclude={"password"})
        user_data["id"] = str(uuid.uuid4())
        user_data["hashed_password"] = get_password_hash(user_in.password)

        return await self.repository.create(user_data)

    async def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID.

        Args:
            user_id: User ID

        Returns:
            User or None
        """
        return await self.repository.get(user_id)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email.

        Args:
            email: User email

        Returns:
            User or None
        """
        return await self.repository.get_by_email(email)

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username.

        Args:
            username: User username

        Returns:
            User or None
        """
        return await self.repository.get_by_username(username)

    async def get_all_users(
        self, skip: int = 0, limit: int = 100
    ) -> list[User]:
        """Get all users.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of users
        """
        result = await self.repository.get_all(skip=skip, limit=limit)
        return list(result)

    async def update_user(self, user_id: str, user_in: UserUpdate) -> Optional[User]:
        """Update user.

        Args:
            user_id: User ID
            user_in: Update data

        Returns:
            Updated user or None
        """
        user_data = user_in.model_dump(exclude_unset=True, exclude={"password"})

        if user_in.password:
            user_data["hashed_password"] = get_password_hash(user_in.password)

        return await self.repository.update(user_id, user_data)

    async def delete_user(self, user_id: str) -> bool:
        """Delete user.

        Args:
            user_id: User ID

        Returns:
            True if deleted, False otherwise
        """
        return await self.repository.delete(user_id)

    async def authenticate_user(
        self, username: str, password: str
    ) -> Optional[User]:
        """Authenticate user.

        Args:
            username: User username
            password: User password

        Returns:
            User if authenticated, None otherwise
        """
        user = await self.repository.get_by_username(username)
        if not user:
            return None

        if not verify_password(password, str(user.hashed_password)):
            return None

        if not user.is_active:
            return None

        return user
