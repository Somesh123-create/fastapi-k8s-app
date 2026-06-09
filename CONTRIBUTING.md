# Contributing Guide

Thank you for your interest in contributing to the FastAPI Kubernetes microservice platform! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful, inclusive, and constructive in all interactions.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a feature branch** from `develop`
4. **Set up development environment** using `scripts/setup.sh`

## Development Process

### 1. Make Your Changes

- Write clean, well-documented code
- Follow the [code style guide](docs/FORMAT.md)
- Include docstrings and type hints
- Write tests for new features

### 2. Run Tests and Checks

```bash
# Format code
make format

# Run linting
make lint

# Run all tests
make test

# Check coverage
make test-coverage
```

### 3. Commit Your Changes

```bash
# Use conventional commits
git commit -m "feat: add new feature"
git commit -m "fix: resolve bug"
git commit -m "docs: update documentation"
git commit -m "test: add test cases"
```

#### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Build, CI, dependencies

**Scope:** Component affected (e.g., `user`, `auth`, `database`)

**Subject:** Short description (50 characters max)

**Body:** Detailed explanation (optional)

**Footer:** References to issues, breaking changes (optional)

### 4. Push and Create Pull Request

```bash
git push origin feature/my-feature
```

Then create a Pull Request with:
- Clear title describing the change
- Description of what was changed and why
- Link to related issues
- Screenshots or examples if applicable

## Pull Request Guidelines

### Before Submitting

- [ ] Code follows style guide
- [ ] Tests pass locally
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No merge conflicts
- [ ] Commits are clean and descriptive

### PR Description Template

```markdown
## Description
Brief description of changes

## Related Issues
Fixes #123
Related to #456

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation

## Testing Done
Describe testing approach and results

## Screenshots
Add if relevant

## Checklist
- [ ] Code reviewed
- [ ] Tests pass
- [ ] Documentation updated
```

## Testing Guidelines

### Writing Tests

- Place tests in appropriate `tests/` subdirectory
- Use descriptive test names
- Test both success and failure cases
- Aim for 80%+ code coverage
- See [TEST.md](docs/TEST.md) for detailed strategy

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/unit/test_security.py -v

# Specific test
pytest tests/unit/test_security.py::TestPasswordHashing::test_hash_password -v

# With coverage
pytest tests/ --cov=app --cov-report=html
```

## Code Style

### Python Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use 100 character line length
- Type hints required for functions
- Docstrings for modules, classes, and public methods

### Tools

- **Formatting**: Black (`make black`)
- **Import sorting**: isort (`make isort`)
- **Linting**: Ruff (`make ruff`)
- **Type checking**: MyPy (`make mypy`)

### Example

```python
"""Module docstring."""

from typing import Optional

from fastapi import APIRouter

from app.models import User
from app.services.user import UserService

router = APIRouter()


@router.get("/users/{user_id}")
async def get_user(user_id: str, service: UserService) -> User:
    """Get user by ID.

    Args:
        user_id: The user ID
        service: User service (injected)

    Returns:
        User object

    Raises:
        HTTPException: If user not found
    """
    return await service.get_user(user_id)
```

## Documentation

### Update Documentation For

- New features
- API changes
- Configuration changes
- Breaking changes
- New endpoints

### Documentation Files

- **README.md**: Overview and quick start
- **docs/INSTRUCTIONS.md**: Development setup
- **docs/TEST.md**: Testing strategy
- **docs/FORMAT.md**: Code style
- **docs/CLAUDE.md**: Architecture
- **Docstrings**: In-code documentation

## Release Process

1. Update version in appropriate files
2. Update CHANGELOG.md
3. Create git tag
4. Push tag to trigger release workflow
5. GitHub Actions builds and publishes

## Questions or Issues?

- Check existing [issues](https://github.com/your-org/fastapi-k8s-app/issues)
- Review [documentation](docs/)
- Create new issue with detailed description

## Recognition

Contributors will be recognized in:
- CHANGELOG.md
- GitHub contributors page
- Release notes

## License

By contributing, you agree your code will be licensed under MIT License.

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Python Development Best Practices](https://docs.python-guide.org/)
- [Git Workflow Guide](https://guides.github.com/introduction/flow/)
- [Conventional Commits](https://www.conventionalcommits.org/)
