# FastAPI Kubernetes Microservice Platform

Production-ready FastAPI microservice platform with complete Docker, Kubernetes, and CI/CD integration.

## Features

✨ **Core Features**
- FastAPI with async support
- PostgreSQL database with SQLAlchemy ORM
- Redis caching
- JWT authentication & RBAC
- Clean Architecture with dependency injection
- Repository pattern for data access

🔍 **Observability**
- OpenTelemetry tracing integration
- Prometheus metrics
- Structured JSON logging
- Correlation IDs for request tracking
- Jaeger support for distributed tracing

🐳 **Container & Orchestration**
- Multi-stage Docker builds
- Non-root user execution
- Kubernetes manifests (Dev, QA, Prod)
- Helm charts with environment-specific values
- Horizontal Pod Autoscaling
- Pod Disruption Budgets
- Network Policies

🔐 **Security**
- JWT token-based authentication
- Password hashing with bcrypt
- Input validation with Pydantic V2
- Security headers
- Network policies
- Non-root containers
- Secret management

🧪 **Testing**
- Unit tests with pytest
- Integration tests with test database
- API endpoint tests
- Coverage reporting (80%+ target)
- Async test support

⚡ **Developer Experience**
- Pre-commit hooks
- Code formatting with Black
- Import sorting with isort
- Linting with Ruff
- Type checking with MyPy
- Makefile for common tasks
- GitHub Codespaces ready

🚀 **CI/CD**
- GitHub Actions workflows
- Automated linting and testing
- Docker image building and pushing
- Multi-environment deployment
- Automated security scanning
- Production approval workflow

## Quick Start

### Local Development

```bash
# Install dependencies
make install
make dev-install

# Run locally
make run

# Run with Docker
make run-docker

# Run tests
make test

# Format and lint code
make lint
make format
```

### Docker

```bash
# Build image
make docker-build

# Run with docker-compose
make docker-run

# Clean up
make docker-clean
```

### Kubernetes

```bash
# Deploy to development
make k8s-deploy-dev

# Deploy to QA
make k8s-deploy-qa

# Deploy to production
make k8s-deploy-prod

# View logs
make k8s-logs
```

### GitHub Codespaces

1. Click "Code" → "Codespaces" → "Create codespace on main"
2. Wait for container to start and dependencies to install
3. Run `make run` to start the application
4. Application available at `http://localhost:8000`

## API Documentation

### Health Endpoints

- `GET /health` - Health check
- `GET /ready` - Readiness probe
- `GET /live` - Liveness probe
- `GET /startup` - Startup probe

### Authentication

- `POST /api/v1/auth/login` - Login with credentials

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "password"}'
```

### Users

- `POST /api/v1/users` - Create user
- `GET /api/v1/users` - List users (requires auth)
- `GET /api/v1/users/{id}` - Get user (requires auth)
- `PUT /api/v1/users/{id}` - Update user (requires auth)
- `DELETE /api/v1/users/{id}` - Delete user (requires auth)

### Metrics

- `GET /api/v1/metrics` - Prometheus metrics
- `GET /api/v1/metrics/summary` - Metrics summary

## Project Structure

```
fastapi-k8s-app/
├── .github/workflows/         # CI/CD workflows
├── .devcontainer/             # GitHub Codespaces config
├── app/
│   ├── api/v1/                # API endpoints
│   ├── core/                  # Configuration & database
│   ├── models/                # SQLAlchemy models
│   ├── repositories/          # Data access layer
│   ├── schemas/               # Pydantic schemas
│   ├── services/              # Business logic
│   ├── middleware/            # Custom middleware
│   ├── observability/         # OpenTelemetry setup
│   ├── migrations/            # Alembic migrations
│   ├── main.py                # Application factory
│   └── __init__.py
├── tests/
│   ├── unit/                  # Unit tests
│   ├── integration/           # Integration tests
│   └── api/                   # API endpoint tests
├── helm/
│   └── fastapi-k8s-app/       # Helm chart
├── kubernetes/
│   ├── dev/                   # Dev environment
│   ├── qa/                    # QA environment
│   └── prod/                  # Production environment
├── docs/                      # Documentation
├── scripts/                   # Utility scripts
├── Dockerfile                 # Multi-stage Dockerfile
├── docker-compose.yml         # Local development stack
├── Makefile                   # Development commands
├── pyproject.toml             # Python project config
├── requirements.txt           # Production dependencies
├── requirements-dev.txt       # Development dependencies
└── README.md                  # This file
```

## Configuration

### Environment Variables

```bash
# Application
APP_NAME=FastAPI K8s App
ENVIRONMENT=development
DEBUG=true

# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi_db

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256

# Logging
LOG_LEVEL=INFO
ENABLE_LOGGING=true

# Observability
ENABLE_TRACING=true
ENABLE_METRICS=true
JAEGER_ENABLED=false
```

Create `.env` file in root directory for local development.

## Database Migrations

```bash
# Run migrations
make migrate

# Create new migration
make migrate-create
```

## Testing

See [TEST.md](docs/TEST.md) for detailed testing strategy and guidelines.

```bash
# Run all tests
make test

# Run specific test suite
make test-unit
make test-integration
make test-api

# Run with coverage
make test-coverage
```

## Security

### Implemented Security Measures

- JWT authentication for API protection
- Password hashing with bcrypt
- CORS middleware configuration
- Security headers
- Input validation with Pydantic
- Network policies in Kubernetes
- Non-root user in containers
- Read-only root filesystem (when possible)
- Resource limits and requests

### Running Security Checks

```bash
# Run Bandit (security linter)
make bandit

# Run safety check (dependency vulnerabilities)
pip install safety && safety check

# Run Trivy (container scanning)
trivy image ghcr.io/fastapi-k8s-app:latest
```

## Code Quality

### Standards

- **Code Format**: Black
- **Import Sorting**: isort
- **Linting**: Ruff
- **Type Checking**: MyPy
- **Pre-commit**: Automated checks before commit

### Running Quality Checks

```bash
# Run all checks
make lint

# Format code
make format

# Individual checks
make black
make isort
make ruff
make mypy
```

## Deployment

### Development Deployment

Automatically deploys on push to `develop` branch.

```bash
make k8s-deploy-dev
```

### QA Deployment

Automatically deploys on push to `release/*` branch.

```bash
make k8s-deploy-qa
```

### Production Deployment

Requires manual approval. Deploys on push to `main` branch after approval.

```bash
make k8s-deploy-prod
```

## Monitoring

### Prometheus Metrics

Metrics available at `GET /api/v1/metrics`

### OpenTelemetry Traces

Configure Jaeger endpoint in environment variables for distributed tracing.

### Logs

Structured JSON logging for easy log aggregation.

## Troubleshooting

### Application won't start

1. Check database connectivity: `psql $DATABASE_URL`
2. Check Redis connectivity: `redis-cli -u $REDIS_URL ping`
3. Check logs: `kubectl logs deployment/fastapi-app`

### Database migrations fail

1. Ensure database is running and accessible
2. Check migration files in `app/migrations/versions/`
3. Manual migration: `alembic upgrade head`

### Tests fail

1. Ensure test database is running
2. Check test environment variables in CI/CD
3. Run tests locally: `make test-coverage`

## Contributing

1. Create feature branch: `git checkout -b feature/new-feature`
2. Make changes and ensure all tests pass
3. Format code: `make format`
4. Commit and push
5. Create Pull Request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
1. Check documentation in `docs/` directory
2. Review existing GitHub issues
3. Create new issue with detailed description

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
