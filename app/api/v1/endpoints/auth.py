"""Authentication endpoints."""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import create_access_token
from app.schemas import LoginRequest, TokenResponse
from app.services.user import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(
    credentials: LoginRequest, session: AsyncSession = Depends(get_db)
) -> TokenResponse:
    """Login endpoint.

    Args:
        credentials: Login credentials
        session: Database session (injected)

    Returns:
        TokenResponse: Access token and metadata

    Raises:
        HTTPException: If credentials are invalid
    """
    service = UserService(session)
    user = await service.authenticate_user(credentials.username, credentials.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    access_token_expires = timedelta(hours=1)
    access_token = create_access_token(data={"sub": user.id}, expires_delta=access_token_expires)

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=int(access_token_expires.total_seconds()),
    )
