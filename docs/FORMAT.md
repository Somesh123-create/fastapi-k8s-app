# Code Formatting & Style Guide

## Python Style

This project follows **PEP 8** with the following enhancements:

### Line Length

- **Maximum**: 100 characters
- **Black formatter**: Enforces this automatically

### Imports

- **Organized by**: Standard library → Third-party → Local imports
- **Tool**: isort with Black profile
- **Format**:
  ```python
  # Standard library
  import sys
  from datetime import datetime
  from typing import Optional

  # Third-party
  from fastapi import FastAPI
  from sqlalchemy import Column, String

  # Local
  from app.core.config import settings
  from app.models import User
  ```

### Naming Conventions

```python
# Constants: UPPER_CASE
MAX_CONNECTIONS = 100
DEFAULT_TIMEOUT = 30

# Classes: PascalCase
class UserService:
    pass

# Functions and methods: snake_case
async def get_user_by_id(user_id: str) -> Optional[User]:
    pass

# Private functions: _snake_case
async def _validate_email(email: str) -> bool:
    pass

# Protected attributes: _snake_case
class User:
    _internal_id: str
```

### Type Hints

Always include type hints:

```python
# Good
def create_user(email: str, name: str) -> User:
    pass

async def get_users(skip: int = 0, limit: int = 100) -> list[User]:
    pass

# Bad
def create_user(email, name):
    pass

def get_users(skip=0, limit=100):
    pass
```

### Docstrings

Use Google-style docstrings:

```python
def my_function(param1: str, param2: int) -> str:
    """Brief one-line description.

    Longer description can span multiple lines and explain
    what the function does in more detail.

    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2

    Returns:
        str: Description of return value

    Raises:
        ValueError: When input is invalid
        ConnectionError: When database unavailable

    Example:
        >>> result = my_function("test", 42)
        >>> print(result)
        'test-42'
    """
    pass
```

### Comments

```python
# Good - explains why, not what
# Load user from cache to avoid database query
user = await cache.get(user_id)

# Bad - explains what the code does
# Get user from cache
user = await cache.get(user_id)

# Exception: Complex algorithms
# Implements merge sort with O(n log n) complexity
def sort_algorithm(items: list[int]) -> list[int]:
    pass
```

## Code Organization

### File Structure

```python
# 1. Docstring
"""Module description."""

# 2. Imports (organized)
import sys
from typing import Optional

from fastapi import FastAPI
from sqlalchemy import Column, String

from app.core.config import settings

# 3. Constants
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# 4. Classes
class MyClass:
    """Class description."""
    pass

# 5. Functions
def my_function() -> None:
    """Function description."""
    pass

# 6. Main block
if __name__ == "__main__":
    pass
```

### Class Organization

```python
class MyClass:
    """Class description."""

    # 1. Class variables
    class_var: str = "value"

    # 2. __init__
    def __init__(self, param: str) -> None:
        """Initialize instance."""
        self._param = param

    # 3. Magic methods
    def __str__(self) -> str:
        """String representation."""
        return f"MyClass({self._param})"

    def __repr__(self) -> str:
        """Developer representation."""
        return f"MyClass(param='{self._param}')"

    # 4. Properties
    @property
    def param(self) -> str:
        """Get param."""
        return self._param

    # 5. Public methods
    def public_method(self) -> None:
        """Public method description."""
        pass

    # 6. Protected methods
    def _protected_method(self) -> None:
        """Protected method description."""
        pass

    # 7. Private methods
    def __private_method(self) -> None:
        """Private method description."""
        pass
```

## Async/Await

Always use async/await for I/O operations:

```python
# Good
async def get_user(user_id: str) -> User:
    """Get user by ID."""
    user = await db.query(User).filter(User.id == user_id).first()
    return user

# Bad
def get_user(user_id: str) -> User:
    """Get user by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    return user
```

## Error Handling

```python
# Good - specific exceptions
async def get_user(user_id: str) -> User:
    """Get user by ID."""
    try:
        user = await db.get(User, user_id)
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        raise
    except ValueError as e:
        logger.warning(f"Invalid input: {e}")
        raise

# Bad - generic exceptions
async def get_user(user_id: str) -> User:
    """Get user by ID."""
    try:
        user = await db.get(User, user_id)
    except Exception:
        pass
    return user
```

## Validation

Use Pydantic for request validation:

```python
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    """User creation schema."""

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = Field(None, max_length=100)

    class Config:
        """Pydantic config."""
        example = {
            "email": "user@example.com",
            "username": "testuser",
            "password": "securepass123",
            "full_name": "Test User",
        }
```

## Logging

Use structured logging:

```python
import logging

logger = logging.getLogger("app")

# Good - structured logging
logger.info("User created", extra={
    "user_id": user.id,
    "email": user.email,
    "environment": "production",
})

# Bad - string formatting
logger.info(f"User {user.id} created with email {user.email}")
```

## Testing

### Test File Organization

```python
"""Test module docstring."""

import pytest

class TestMyClass:
    """Test MyClass."""

    def setup_method(self) -> None:
        """Setup before each test."""
        self.instance = MyClass()

    def teardown_method(self) -> None:
        """Cleanup after each test."""
        pass

    def test_something(self) -> None:
        """Test something."""
        result = self.instance.something()
        assert result is True

    @pytest.mark.parametrize("input,expected", [
        ("a", 1),
        ("b", 2),
    ])
    def test_multiple_cases(self, input, expected) -> None:
        """Test multiple input cases."""
        result = self.instance.process(input)
        assert result == expected
```

### Test Naming

```python
# Pattern: test_[function]_[scenario]_[expected_result]

# Good
def test_create_user_with_valid_email():
    pass

def test_create_user_with_duplicate_email_raises_error():
    pass

def test_health_endpoint_returns_200():
    pass

# Bad
def test_user():
    pass

def test_email():
    pass

def test_endpoint():
    pass
```

## FastAPI Endpoints

```python
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create user",
    description="Create a new user account",
)
async def create_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_db),
) -> UserResponse:
    """Create a new user.

    Args:
        user_in: User creation data
        session: Database session (injected)

    Returns:
        UserResponse: Created user

    Raises:
        HTTPException: If user already exists
    """
    # Implementation
    pass
```

## Database Models

```python
from sqlalchemy import Column, DateTime, String, Boolean
from sqlalchemy.orm import declared_attr

from app.core.database import Base

class TimeStampMixin:
    """Mixin for timestamp fields."""

    @declared_attr
    def created_at(cls) -> DateTime:
        """Created at timestamp."""
        return Column(DateTime(timezone=True), server_default=func.now())

class User(Base, TimeStampMixin):
    """User model."""

    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(255), unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True, index=True)

    def __repr__(self) -> str:
        """String representation."""
        return f"<User(id={self.id}, email={self.email})>"
```

## Environment Variables

```python
# Properly typed with defaults
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings from environment variables."""

    # Required
    app_name: str

    # With defaults
    debug: bool = False
    log_level: str = "INFO"

    # Optional
    optional_setting: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = False
```

## Auto-formatting

### Run Formatters

```bash
# Format all code
make format

# Individual tools
make black
make isort
make ruff
```

### Pre-commit Hooks

```bash
# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### Editor Integration

#### VS Code (`settings.json`)

```json
{
  "[python]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "ms-python.python",
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  },
  "python.formatting.provider": "black",
  "python.linting.enabled": true
}
```

#### PyCharm

- Settings → Python Integrated Tools → Python Integrated Tools
- Set default test runner to pytest
- Enable code inspections

## Standards Reference

- [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- [PEP 257](https://www.python.org/dev/peps/pep-0257/) - Docstrings
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Black Code Style](https://black.readthedocs.io/)
- [FastAPI Best Practices](https://fastapi.tiangolo.com/best-practices/)
