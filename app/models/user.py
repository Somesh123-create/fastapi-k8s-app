"""Database models."""

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, String, Text, func
from sqlalchemy.orm import declared_attr

from app.core.database import Base


class TimeStampMixin:
    """Mixin that adds timestamp fields to models."""

    @declared_attr
    def created_at(cls) -> DateTime:
        """Created at timestamp."""
        return Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )

    @declared_attr
    def updated_at(cls) -> DateTime:
        """Updated at timestamp."""
        return Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
        )


class User(Base, TimeStampMixin):
    """User model."""

    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, index=True)
    is_superuser = Column(Boolean, default=False)
    role = Column(String(50), default="user", index=True)
    bio = Column(Text, nullable=True)

    def __repr__(self) -> str:
        """String representation."""
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"
