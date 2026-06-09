# Testing Strategy

## Overview

This document outlines the comprehensive testing strategy for the FastAPI Kubernetes microservice platform.

## Testing Pyramid

```
        /\
       /  \      E2E & Integration Tests (10%)
      /----\
     /      \    API Tests (30%)
    /--------\
   /          \  Unit Tests (60%)
  /____________\
```

## Test Categories

### Unit Tests (60%)

**Location**: `tests/unit/`

**Purpose**: Test individual functions and classes in isolation

**Coverage**: Core business logic, utilities, and security functions

**Examples**:
- Password hashing and verification
- Token creation and validation
- Data model creation and representation
- Service methods in isolation

**Running Tests**:
```bash
make test-unit
pytest tests/unit -v
```

**Characteristics**:
- Fast execution (< 1 second total)
- No external dependencies
- Use mocking for external calls
- High code coverage (>90%)

### Integration Tests (30%)

**Location**: `tests/integration/`

**Purpose**: Test components working together with real database

**Coverage**: Service layer with real data access

**Examples**:
- User service CRUD operations
- Authentication workflows
- Data validation and constraints

**Running Tests**:
```bash
make test-integration
pytest tests/integration -v
```

**Requirements**:
- Test database (SQLite in-memory or PostgreSQL)
- Test fixtures for data setup
- Teardown to clean test data

**Characteristics**:
- Moderate execution time (2-5 seconds)
- Real database interactions
- Transaction rollback after each test
- Test data fixtures

### API Tests (10%)

**Location**: `tests/api/`

**Purpose**: Test HTTP endpoints end-to-end

**Coverage**: Request/response validation, status codes, error handling

**Examples**:
- Health endpoints
- Authentication endpoints
- CRUD endpoint workflows
- Error responses

**Running Tests**:
```bash
make test-api
pytest tests/api -v
```

**Characteristics**:
- Test complete HTTP flow
- Validate request/response schemas
- Test error conditions
- Use async test client

## Testing Best Practices

### 1. Test Naming

```python
# Good
def test_create_user_with_valid_email():
    ...

def test_create_user_with_duplicate_email_fails():
    ...

def test_health_endpoint_returns_200():
    ...

# Bad
def test_user():
    ...

def test_endpoint():
    ...
```

### 2. Test Organization

```python
# Organize related tests in classes
class TestUserAuthentication:
    """Test user authentication."""
    
    def test_login_with_valid_credentials(self):
        ...
    
    def test_login_with_invalid_password(self):
        ...
    
    def test_login_with_inactive_user(self):
        ...
```

### 3. Fixtures

```python
# Use fixtures for setup/teardown
@pytest.fixture
def test_user(test_db):
    """Create test user."""
    user = UserService(test_db).create_user(UserCreate(...))
    yield user
    # Cleanup happens automatically

@pytest.fixture
async def authenticated_client(client):
    """Create authenticated test client."""
    token = create_access_token({"sub": "user123"})
    client.headers = {"Authorization": f"Bearer {token}"}
    return client
```

### 4. Mocking

```python
# Mock external dependencies
from unittest.mock import patch, AsyncMock

@patch('app.services.user.redis_client')
async def test_get_user_from_cache(mock_redis):
    """Test user retrieval from cache."""
    mock_redis.get.return_value = user_data
    result = await service.get_user_cached(user_id)
    assert result == expected_user
    mock_redis.get.assert_called_once_with(f"user:{user_id}")
```

### 5. Async Testing

```python
# Use pytest-asyncio for async tests
@pytest.mark.asyncio
async def test_create_user_async():
    """Test async user creation."""
    service = UserService(test_db)
    user = await service.create_user(user_in)
    assert user.id is not None

# Or configure asyncio_mode = "auto" in pyproject.toml
```

### 6. Parametrized Tests

```python
# Test multiple cases
@pytest.mark.parametrize("email,valid", [
    ("user@example.com", True),
    ("invalid-email", False),
    ("user@", False),
    ("@example.com", False),
])
def test_email_validation(email, valid):
    """Test email validation."""
    result = is_valid_email(email)
    assert result == valid
```

### 7. Error Testing

```python
# Test error conditions
def test_create_user_with_duplicate_email_raises_error():
    """Test user creation with duplicate email."""
    service = UserService(test_db)
    service.create_user(UserCreate(...))
    
    with pytest.raises(ValueError, match="already exists"):
        service.create_user(UserCreate(email="same@example.com", ...))
```

## Test Data

### Fixtures

Use fixtures for consistent test data:

```python
@pytest.fixture
def valid_user_data():
    """Valid user creation data."""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123",
        "full_name": "Test User",
    }

@pytest.fixture
def invalid_user_data():
    """Invalid user creation data."""
    return {
        "email": "invalid-email",
        "username": "",
        "password": "short",
    }
```

### Factory Pattern

```python
class UserFactory:
    """Factory for creating test users."""
    
    @staticmethod
    def create(session, **kwargs):
        """Create test user with optional overrides."""
        data = {
            "id": str(uuid.uuid4()),
            "email": "test@example.com",
            "username": "testuser",
            ...
        }
        data.update(kwargs)
        return UserRepository(session).create(data)
```

## Coverage Requirements

### Minimum Coverage

- Overall: 80%
- Core modules: 85%+
- Controllers: 90%+
- Utilities: 85%+
- Exclude: migrations, CLI utilities

### Running Coverage

```bash
# Generate coverage report
make test-coverage

# View HTML report
open htmlcov/index.html
```

### Coverage Configuration

In `pyproject.toml`:
```toml
[tool.coverage.run]
branch = true
source = ["app"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
]
min_percentage = 80
```

## Continuous Integration

### Pre-commit Hooks

Run tests before commit:
```bash
pre-commit install
```

### GitHub Actions

Automated testing on:
- Pull requests to main/develop
- Push to main/develop
- Manual trigger

### Test Reports

- Coverage reports uploaded to Codecov
- Test results in GitHub Actions UI
- Failure notifications

## Performance Testing

### Load Testing

```bash
# Using locust
pip install locust

# Create locustfile.py
locust -f locustfile.py --host=http://localhost:8000
```

### Benchmark Testing

```python
@pytest.mark.benchmark
def test_user_creation_performance(benchmark):
    """Test user creation performance."""
    result = benchmark(create_user, user_data)
    assert result is not None
```

## Debugging Tests

### Verbose Output

```bash
pytest tests/ -vv -s
```

### Drop into Debugger

```python
def test_something():
    breakpoint()  # Python 3.7+
    # or
    import pdb; pdb.set_trace()
```

### Print Logging

```bash
pytest tests/ --log-cli-level=DEBUG
```

## Test Maintenance

### Regular Reviews

- Monthly: Review test effectiveness
- Quarterly: Refactor test code
- Annually: Update test strategy

### Removing Obsolete Tests

- Remove tests for deprecated features
- Merge redundant tests
- Consolidate similar test cases

### Documentation

- Document complex test scenarios
- Explain non-obvious assertions
- Link to related issues/PRs

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/advanced/testing/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/20/faq/testing.html)
- [Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)
