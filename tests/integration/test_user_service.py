"""Integration tests for user service."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.models import User
from app.schemas import UserCreate
from app.services.user import UserService

# Test database setup
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
async def test_db():
    """Create test database."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with AsyncSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.mark.asyncio
class TestUserService:
    """Test user service."""

    async def test_create_user(self, test_db: AsyncSession) -> None:
        """Test creating user."""
        service = UserService(test_db)
        user_in = UserCreate(
            email="test@example.com",
            username="testuser",
            password="password123",
        )
        user = await service.create_user(user_in)
        assert user.email == "test@example.com"
        assert user.username == "testuser"

    async def test_get_user(self, test_db: AsyncSession) -> None:
        """Test getting user."""
        service = UserService(test_db)
        user_in = UserCreate(
            email="test@example.com",
            username="testuser",
            password="password123",
        )
        created_user = await service.create_user(user_in)
        retrieved_user = await service.get_user(created_user.id)
        assert retrieved_user.email == "test@example.com"

    async def test_authenticate_user(self, test_db: AsyncSession) -> None:
        """Test user authentication."""
        service = UserService(test_db)
        user_in = UserCreate(
            email="test@example.com",
            username="testuser",
            password="password123",
        )
        await service.create_user(user_in)
        user = await service.authenticate_user("testuser", "password123")
        assert user is not None
        assert user.username == "testuser"

    async def test_authenticate_user_wrong_password(self, test_db: AsyncSession) -> None:
        """Test user authentication with wrong password."""
        service = UserService(test_db)
        user_in = UserCreate(
            email="test@example.com",
            username="testuser",
            password="password123",
        )
        await service.create_user(user_in)
        user = await service.authenticate_user("testuser", "wrong_password")
        assert user is None
