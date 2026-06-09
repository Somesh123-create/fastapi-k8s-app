"""Unit tests for models."""

import pytest

from app.models import User


class TestUserModel:
    """Test user model."""

    def test_user_creation(self) -> None:
        """Test user model creation."""
        user = User(
            id="user123",
            email="user@example.com",
            username="testuser",
            hashed_password="hashed_password",
            is_active=True,
            role="user",
        )
        assert user.id == "user123"
        assert user.email == "user@example.com"
        assert user.username == "testuser"
        assert user.is_active is True
        assert user.role == "user"

    def test_user_repr(self) -> None:
        """Test user repr."""
        user = User(
            id="user123",
            email="user@example.com",
            username="testuser",
            hashed_password="hashed_password",
        )
        repr_str = repr(user)
        assert "user@example.com" in repr_str
        assert "testuser" in repr_str
