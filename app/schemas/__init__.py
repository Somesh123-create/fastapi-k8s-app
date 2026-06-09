"""Pydantic schemas for request/response validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr
    username: str
    full_name: Optional[str] = None
    bio: Optional[str] = None


class UserCreate(UserBase):
    """User creation schema."""

    password: str


class UserUpdate(BaseModel):
    """User update schema."""

    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    bio: Optional[str] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    """User response schema."""

    id: str
    is_active: bool
    is_superuser: bool
    role: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    """Token response schema."""

    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int


class LoginRequest(BaseModel):
    """Login request schema."""

    username: str
    password: str


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    version: str
    environment: str


class MetricsResponse(BaseModel):
    """Metrics response."""

    timestamp: datetime
    uptime_seconds: float
    requests_total: int
    requests_errors: int
    database_connections: int
