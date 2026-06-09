# Project Structure

Complete file listing for the FastAPI Kubernetes microservice platform:

## Root Files

```
fastapi-k8s-app/
├── Dockerfile                 # Multi-stage production-grade Dockerfile
├── docker-compose.yml         # Local development environment
├── Makefile                   # Development commands and tasks
├── pyproject.toml             # Python project configuration
├── requirements.txt           # Production dependencies
├── requirements-dev.txt       # Development dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
├── .pre-commit-config.yaml   # Pre-commit hooks configuration
├── README.md                 # Project overview and quick start
├── CHANGELOG.md              # Version history
├── CONTRIBUTING.md           # Contribution guidelines
└── LICENSE                   # MIT License
```

## GitHub Configuration

```
.github/
└── workflows/
    ├── ci.yml               # Continuous Integration pipeline
    └── cd.yml               # Continuous Deployment pipeline
```

## Development Container

```
.devcontainer/
├── devcontainer.json        # GitHub Codespaces configuration
└── post-create.sh          # Post-creation setup script
```

## Application Code

```
app/
├── __init__.py             # Package initialization
├── __main__.py             # Entry point
├── main.py                 # FastAPI application factory

├── core/                   # Configuration and core setup
│   ├── __init__.py
│   ├── config.py          # Settings management
│   ├── database.py        # Database setup and session
│   ├── security.py        # JWT and password utilities
│   └── logging_config.py  # Logging configuration

├── api/
│   ├── __init__.py
│   └── v1/
│       ├── __init__.py
│       └── endpoints/
│           ├── __init__.py
│           ├── health.py      # Health check endpoints
│           ├── auth.py        # Authentication endpoints
│           ├── users.py       # User CRUD endpoints
│           └── metrics.py     # Metrics endpoints

├── models/                 # SQLAlchemy database models
│   ├── __init__.py
│   └── user.py            # User model

├── schemas/               # Pydantic validation schemas
│   └── __init__.py        # Request/response schemas

├── repositories/          # Data access layer
│   ├── __init__.py
│   ├── base.py           # Base repository with CRUD
│   └── user.py           # User-specific repository

├── services/             # Business logic layer
│   ├── __init__.py
│   └── user.py           # User service

├── middleware/           # Custom middleware
│   ├── __init__.py
│   └── security.py       # Token verification middleware

├── observability/        # Monitoring and tracing
│   ├── __init__.py
│   └── telemetry.py      # OpenTelemetry setup

├── utils/                # Utility functions
│   ├── __init__.py
│   └── dependencies.py   # Dependency injection

└── migrations/           # Database migrations
    ├── __init__.py
    ├── env.py           # Alembic environment
    ├── alembic.ini      # Alembic configuration
    ├── script.py.mako   # Alembic template
    └── versions/        # Migration files
        ├── __init__.py
        └── 001_initial_user_table.py
```

## Tests

```
tests/
├── __init__.py

├── unit/                # Unit tests
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_security.py
│   ├── test_models.py
│   └── test_*.py

├── integration/         # Integration tests
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_user_service.py
│   └── test_*.py

└── api/                 # API endpoint tests
    ├── __init__.py
    ├── conftest.py
    ├── test_endpoints.py
    └── test_*.py
```

## Kubernetes

```
kubernetes/

├── dev/                 # Development environment
│   ├── deployment.yaml  # Deployment + ConfigMap + Secret + Service
│   └── ingress.yaml     # Ingress configuration

├── qa/                  # QA environment
│   ├── deployment.yaml
│   └── ingress.yaml

└── prod/               # Production environment
    ├── deployment.yaml
    └── ingress.yaml
```

## Helm Chart

```
helm/
└── fastapi-k8s-app/
    ├── Chart.yaml              # Helm chart metadata
    ├── values.yaml             # Default values
    ├── values-dev.yaml         # Development overrides
    ├── values-qa.yaml          # QA overrides
    ├── values-prod.yaml        # Production overrides
    └── templates/
        ├── _helpers.tpl        # Template helpers
        ├── configmap.yaml      # ConfigMap template
        ├── secret.yaml         # Secret template
        ├── deployment.yaml     # Deployment template
        ├── service.yaml        # Service template
        ├── ingress.yaml        # Ingress template
        ├── hpa.yaml           # HorizontalPodAutoscaler template
        ├── pdb.yaml           # PodDisruptionBudget template
        └── serviceaccount.yaml # ServiceAccount template
```

## Scripts

```
scripts/
├── setup.sh              # Local environment setup
├── setup-minikube.sh     # Minikube setup script
├── deploy-dev.sh         # Deploy to dev environment
├── deploy-prod.sh        # Deploy to production environment
├── build-docker.sh       # Build Docker image
└── create-migration.sh   # Create database migration
```

## Documentation

```
docs/
├── README.md             # This file
├── TEST.md              # Testing strategy and guidelines
├── INSTRUCTIONS.md      # Development setup and workflow
├── FORMAT.md            # Code style guide
└── CLAUDE.md            # Architecture documentation
```

## Key Statistics

- **Total Files**: 100+
- **Python Files**: 40+
- **Configuration Files**: 15+
- **Documentation Files**: 10
- **Test Files**: 8+
- **Kubernetes Manifests**: 6
- **Helm Templates**: 9
- **GitHub Actions Workflows**: 2
- **Docker Images**: 1 (multi-stage)

## File Sizes (Approximate)

- Application Code: ~800 KB
- Tests: ~150 KB
- Configuration: ~100 KB
- Documentation: ~300 KB
- Kubernetes/Helm: ~200 KB
- Scripts: ~50 KB

## Technology Stack Summary

### Backend
- **Framework**: FastAPI 0.109.0
- **ORM**: SQLAlchemy 2.0.23
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Auth**: JWT with python-jose
- **Validation**: Pydantic V2

### Testing
- **Framework**: pytest 7.4.3
- **Async**: pytest-asyncio 0.21.1
- **Coverage**: pytest-cov 4.1.0

### Code Quality
- **Formatting**: Black 23.12.1
- **Imports**: isort 5.13.2
- **Linting**: Ruff 0.1.11
- **Type Checking**: MyPy 1.7.1
- **Security**: Bandit 1.7.5

### Observability
- **Tracing**: OpenTelemetry 1.21.0
- **Metrics**: Prometheus client 0.19.0
- **Logging**: python-json-logger 2.0.7

### Infrastructure
- **Container**: Docker 24.0
- **Orchestration**: Kubernetes 1.28
- **Package Manager**: Helm 3
- **CI/CD**: GitHub Actions

## Environment Support

✅ **Supported Environments**
- Local Development (Docker Compose)
- GitHub Codespaces
- Kubernetes (Minikube, EKS, GKE, AKS)
- Dev/QA/Production (Multi-environment)

## Quick Navigation

- **Getting Started**: [README.md](../README.md)
- **Development Setup**: [docs/INSTRUCTIONS.md](../docs/INSTRUCTIONS.md)
- **Code Style**: [docs/FORMAT.md](../docs/FORMAT.md)
- **Testing Guide**: [docs/TEST.md](../docs/TEST.md)
- **Architecture**: [docs/CLAUDE.md](../docs/CLAUDE.md)
- **Contributing**: [CONTRIBUTING.md](../CONTRIBUTING.md)
