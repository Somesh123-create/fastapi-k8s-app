# Development Instructions

## Environment Setup

### Prerequisites

- Python 3.12+
- Docker & Docker Compose
- kubectl (for Kubernetes)
- Helm (for Helm deployments)
- Git

### Local Setup

1. **Clone Repository**
   ```bash
   git clone https://github.com/your-org/fastapi-k8s-app.git
   cd fastapi-k8s-app
   ```

2. **Create Virtual Environment**
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   make install
   make dev-install
   ```

4. **Setup Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize Database**
   ```bash
   docker-compose up postgres redis
   make migrate
   ```

6. **Run Application**
   ```bash
   make run
   # Application available at http://localhost:8000
   ```

## Development Workflow

### Creating a Feature

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make Changes**
   - Write code following project standards
   - Write tests as you go (TDD)
   - Update documentation

3. **Format & Lint**
   ```bash
   make format
   make lint
   ```

4. **Run Tests**
   ```bash
   make test
   ```

5. **Commit & Push**
   ```bash
   git add .
   git commit -m "feat: add my feature"
   git push origin feature/my-feature
   ```

6. **Create Pull Request**
   - Link related issues
   - Describe changes
   - Request reviews

### Adding New Endpoints

1. **Create Request/Response Schemas**
   ```python
   # app/schemas/__init__.py
   class MyRequestSchema(BaseModel):
       field1: str
       field2: int
   ```

2. **Create Service Layer**
   ```python
   # app/services/my_service.py
   class MyService:
       async def process_request(self, data: MyRequestSchema):
           # Business logic here
           pass
   ```

3. **Create API Endpoint**
   ```python
   # app/api/v1/endpoints/my_endpoint.py
   @router.post("/my-endpoint", response_model=ResponseSchema)
   async def my_endpoint(
       data: MyRequestSchema,
       session: AsyncSession = Depends(get_db)
   ):
       service = MyService(session)
       return await service.process_request(data)
   ```

4. **Create Tests**
   ```python
   # tests/api/test_my_endpoint.py
   @pytest.mark.asyncio
   async def test_my_endpoint(client):
       response = await client.post("/api/v1/my-endpoint", json={...})
       assert response.status_code == 200
   ```

### Adding New Database Models

1. **Create Model**
   ```python
   # app/models/my_model.py
   class MyModel(Base, TimeStampMixin):
       __tablename__ = "my_table"
       id = Column(String(36), primary_key=True)
       name = Column(String(255), unique=True)
   ```

2. **Create Repository**
   ```python
   # app/repositories/my_model.py
   class MyRepository(BaseRepository[MyModel]):
       async def get_by_name(self, name: str):
           # Custom query
           pass
   ```

3. **Create Migration**
   ```bash
   make migrate-create
   # Edit migration file
   ```

4. **Run Migration**
   ```bash
   make migrate
   ```

## Debugging

### Print Debugging

```python
import logging
logger = logging.getLogger("app")

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

### Using Debugger

```python
# Add breakpoint
breakpoint()  # Python 3.7+

# Then in terminal
make run
# Application will pause at breakpoint
```

### Viewing Logs

```bash
# Application logs
docker-compose logs -f app

# Database logs
docker-compose logs -f postgres

# Redis logs
docker-compose logs -f redis
```

## Database Management

### Create Migration

```bash
# Auto-generate migration based on model changes
make migrate-create

# Or manually
alembic revision -m "description"
```

### Run Migrations

```bash
# Apply all pending migrations
make migrate

# Or specific version
alembic upgrade abc123
```

### Downgrade Migration

```bash
alembic downgrade -1  # Rollback one migration
```

### View Migration History

```bash
alembic current  # Current version
alembic history  # All versions
```

### Reset Database

```bash
docker-compose down -v
docker-compose up postgres
make migrate
```

## Docker Development

### Build Image

```bash
make docker-build
```

### Run Container

```bash
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://... \
  -e REDIS_URL=redis://... \
  ghcr.io/fastapi-k8s-app:latest
```

### Docker Compose

```bash
# Start all services
docker-compose up

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Reset everything
docker-compose down -v
```

## Kubernetes Development

### Local Kubernetes

```bash
# Start Minikube
minikube start

# Build image in Minikube
eval $(minikube docker-env)
make docker-build

# Deploy
make k8s-deploy-dev
```

### View Deployment

```bash
# List pods
kubectl get pods

# View pod logs
kubectl logs -f pod/fastapi-app-xxx

# Port forward
kubectl port-forward svc/fastapi-app 8000:80

# Access application
curl http://localhost:8000/health
```

### Scale Deployment

```bash
kubectl scale deployment/fastapi-app --replicas=3
```

### Delete Deployment

```bash
make k8s-delete
# or
kubectl delete -f kubernetes/dev/
```

## Performance Testing

### Locust Load Testing

```bash
pip install locust

# Create locustfile.py
cat > locustfile.py << 'EOF'
from locust import HttpUser, task

class WebsiteUser(HttpUser):
    @task
    def health(self):
        self.client.get("/health")
EOF

locust --host=http://localhost:8000
```

### Benchmarking

```bash
# Using Apache Bench
ab -n 1000 -c 10 http://localhost:8000/health

# Using wrk
wrk -t4 -c100 -d30s http://localhost:8000/health
```

## Security Development

### Generate Secret Key

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### JWT Token Testing

```bash
# Create token
python3
>>> from app.core.security import create_access_token
>>> token = create_access_token({"sub": "user123"})
>>> print(token)

# Use in curl
curl -H "Authorization: Bearer $token" http://localhost:8000/api/v1/users
```

## Performance Optimization

### Database Query Analysis

```bash
# Enable SQL query logging
export DEBUG=true
make run
# See all SQL queries in logs

# Use EXPLAIN
psql $DATABASE_URL
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
```

### Memory Profiling

```bash
pip install memory-profiler

# Add decorator
@profile
def my_function():
    pass

python -m memory_profiler app/main.py
```

### CPU Profiling

```bash
pip install py-spy

py-spy record -o profile.svg python -m uvicorn app.main:app
```

## Documentation

### Update Documentation

1. Edit relevant `.md` file
2. Build HTML docs (if applicable)
3. Commit and push
4. Docs auto-deploy to GitHub Pages

### Code Comments

- Document complex algorithms
- Explain business logic
- Link to external references
- Keep comments up-to-date

### Docstrings

```python
def my_function(param1: str, param2: int) -> str:
    """Brief description.

    Longer description explaining what the function does,
    its parameters, and return value.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        str: Description of return value

    Raises:
        ValueError: When something is invalid
    """
```

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   ```bash
   psql $DATABASE_URL
   # If fails, ensure PostgreSQL is running
   docker-compose up postgres
   ```

2. **Redis Connection Failed**
   ```bash
   redis-cli -u $REDIS_URL ping
   # If fails, ensure Redis is running
   docker-compose up redis
   ```

3. **Tests Failing**
   ```bash
   make test-coverage
   # Check which tests failed
   # Review test logs for details
   ```

4. **Docker Build Fails**
   ```bash
   docker build --no-cache -t fastapi-k8s-app:latest .
   # Rebuild without cache
   ```

5. **Module Not Found**
   ```bash
   python -c "import app"
   # Ensure venv is activated
   source venv/bin/activate
   ```

## Getting Help

1. **Check Documentation**
   - Review docs/ folder
   - Read inline code comments
   - Check pytest output

2. **Search Issues**
   - GitHub Issues
   - Stack Overflow
   - Documentation

3. **Ask Questions**
   - Create GitHub Discussion
   - Reach out to team
   - Join Discord/Slack channel

## Tips & Tricks

### Faster Test Execution

```bash
# Run only modified tests
pytest --lf

# Run tests in parallel
pytest -n auto

# Run specific test
pytest tests/unit/test_security.py::TestPasswordHashing::test_hash_password
```

### Database Reset Script

```bash
# Create reset-db.sh
#!/bin/bash
docker-compose down -v
docker-compose up -d postgres redis
sleep 5
make migrate

chmod +x reset-db.sh
./reset-db.sh
```

### Auto-format on Save

Configure your editor to run `black` and `isort` on save.

### Watch Mode

```bash
# Install watchdog
pip install watchdog

# Auto-run tests on changes
ptw tests/
```
