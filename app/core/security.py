"""Application security utilities."""

from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
ALGORITHM = settings.algorithm
SECRET_KEY = settings.secret_key
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash.

    Args:
        plain_password: Plain text password
        hashed_password: Hashed password

    Returns:
        bool: True if password matches, False otherwise
    """
    return bool(pwd_context.verify(plain_password, hashed_password))  # type: ignore[return-value]


def get_password_hash(password: str) -> str:
    """Hash password.

    Args:
        password: Plain text password

    Returns:
        str: Hashed password
    """
    return str(pwd_context.hash(password))  # type: ignore[return-value]


def create_access_token(
    data: dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """Create JWT access token.

    Args:
        data: Data to encode
        expires_delta: Token expiration time delta

    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(  # type: ignore[assignment]
        to_encode, SECRET_KEY, algorithm=ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str) -> Optional[dict[str, Any]]:
    """Decode JWT token.

    Args:
        token: JWT token

    Returns:
        dict: Decoded token data or None if invalid
    """
    try:
        payload: dict[str, Any] = jwt.decode(  # type: ignore[assignment]
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
        return None
