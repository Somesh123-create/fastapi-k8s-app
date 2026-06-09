"""Unit tests for authentication."""

import pytest

from app.core.security import (
    create_access_token,
    decode_token,
    get_password_hash,
    verify_password,
)


class TestPasswordHashing:
    """Test password hashing functions."""

    def test_hash_password(self) -> None:
        """Test password hashing."""
        password = "test_password_123"
        hashed = get_password_hash(password)
        assert hashed != password
        assert verify_password(password, hashed)

    def test_verify_wrong_password(self) -> None:
        """Test password verification with wrong password."""
        password = "test_password_123"
        hashed = get_password_hash(password)
        assert not verify_password("wrong_password", hashed)


class TestTokenHandling:
    """Test JWT token handling."""

    def test_create_access_token(self) -> None:
        """Test creating access token."""
        data = {"sub": "user123"}
        token = create_access_token(data)
        assert token is not None
        assert isinstance(token, str)

    def test_decode_valid_token(self) -> None:
        """Test decoding valid token."""
        user_id = "user123"
        data = {"sub": user_id}
        token = create_access_token(data)
        decoded = decode_token(token)
        assert decoded is not None
        assert decoded.get("sub") == user_id

    def test_decode_invalid_token(self) -> None:
        """Test decoding invalid token."""
        token = "invalid_token_123"
        decoded = decode_token(token)
        assert decoded is None
