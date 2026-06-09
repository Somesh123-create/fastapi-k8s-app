"""User endpoints."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.middleware.security import verify_token
from app.models import User
from app.schemas import UserCreate, UserResponse, UserUpdate
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_db),
) -> UserResponse:
    """Create new user.

    Args:
        user_in: User creation data
        session: Database session (injected)

    Returns:
        UserResponse: Created user

    Raises:
        HTTPException: If user already exists
    """
    service = UserService(session)
    try:
        user = await service.create_user(user_in)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
)
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: AsyncSession = Depends(get_db),
    _: str = Depends(verify_token),
) -> list[User]:  # type: ignore[return]
    """List all users.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records
        session: Database session (injected)
        _: Verified token (injected)

    Returns:
        List of users
    """
    service = UserService(session)
    return await service.get_all_users(skip=skip, limit=limit)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user(
    user_id: str,
    session: AsyncSession = Depends(get_db),
    _: str = Depends(verify_token),
) -> UserResponse:
    """Get user by ID.

    Args:
        user_id: User ID
        session: Database session (injected)
        _: Verified token (injected)

    Returns:
        UserResponse: User data

    Raises:
        HTTPException: If user not found
    """
    service = UserService(session)
    user = await service.get_user(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def update_user(
    user_id: str,
    user_in: UserUpdate,
    session: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(verify_token),
) -> UserResponse:
    """Update user.

    Args:
        user_id: User ID
        user_in: Update data
        session: Database session (injected)
        current_user_id: Current user ID (injected)

    Returns:
        UserResponse: Updated user

    Raises:
        HTTPException: If user not found or unauthorized
    """
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update other users",
        )

    service = UserService(session)
    user = await service.update_user(user_id, user_in)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: str,
    session: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(verify_token),
) -> None:
    """Delete user.

    Args:
        user_id: User ID
        session: Database session (injected)
        current_user_id: Current user ID (injected)

    Raises:
        HTTPException: If user not found or unauthorized
    """
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete other users",
        )

    service = UserService(session)
    deleted = await service.delete_user(user_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
