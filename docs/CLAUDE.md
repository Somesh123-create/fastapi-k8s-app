# Architecture & Design Documentation

## System Architecture

### Clean Architecture Layers

The application follows Clean Architecture principles with the following layers:

```
┌─────────────────────────────────────────┐
│         API Layer (Endpoints)           │
│  ┌───────────────────────────────────┐  │
│  │  /api/v1/users                    │  │
│  │  /api/v1/auth                     │  │
│  │  /api/v1/health                   │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│        Service Layer (Business Logic)   │
│  ┌───────────────────────────────────┐  │
│  │  UserService                      │  │
│  │  AuthService                      │  │
│  │  NotificationService              │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│       Repository Layer (Data Access)    │
│  ┌───────────────────────────────────┐  │
│  │  UserRepository                   │  │
│  │  BaseRepository                   │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│    Infrastructure Layer (ORM, Cache)    │
│  ┌───────────────────────────────────┐  │
│  │  SQLAlchemy                       │  │
│  │  Redis Client                     │  │
│  │  Database Connections             │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### Design Patterns

#### Repository Pattern

```python
# Database abstraction layer
class UserRepository(BaseRepository[User]):
    async def get_by_email(self, email: str) -> Optional[User]:
        # Encapsulates database query logic
        pass

# Service uses repository
class UserService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)
    
    async def get_user(self, user_id: str) -> Optional[User]:
        return await self.repository.get(user_id)
```

#### Dependency Injection

```python
# Dependencies injected via FastAPI's Depends
@router.get("/users/{id}")
async def get_user(
    user_id: str,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pass
```

#### Service Locator

```python
# Service creation follows factory pattern
async def get_user_service(
    session: AsyncSession = Depends(get_db)
) -> UserService:
    return UserService(session)
```

## Data Flow

### Request Processing

```
1. HTTP Request
   ↓
2. Middleware (Auth, Logging, Metrics)
   ↓
3. Route Handler (Validation with Pydantic)
   ↓
4. Service Layer (Business Logic)
   ↓
5. Repository Layer (Data Access)
   ↓
6. Database/Cache
   ↓
7. Response Serialization (Pydantic)
   ↓
8. HTTP Response
```

### Example: Create User

```python
# 1. Request arrives
POST /api/v1/users
{
    "email": "user@example.com",
    "username": "testuser",
    "password": "password123"
}

# 2. FastAPI validates schema
user_in: UserCreate = UserCreate(...)

# 3. Endpoint calls service
service = UserService(session)
user = await service.create_user(user_in)

# 4. Service validates business rules
# - Check if user exists
# - Hash password
# - Generate user ID

# 5. Service calls repository
user_data = {
    "id": str(uuid.uuid4()),
    "email": user_in.email,
    "hashed_password": hash(user_in.password),
}
user = await self.repository.create(user_data)

# 6. Repository executes SQL
INSERT INTO users (...) VALUES (...)

# 7. Response serialized
UserResponse(
    id=user.id,
    email=user.email,
    ...
)

# 8. HTTP 201 Created with user data
```

## Configuration Management

### Environment-Based Configuration

```python
# settings.py - Single source of truth
class Settings(BaseSettings):
    environment: str  # development, qa, production
    debug: bool
    database_url: str
    redis_url: str
    
    class Config:
        env_file = ".env"

settings = Settings()

# Usage throughout app
@app.on_event("startup")
async def startup():
    logger.info(f"Starting in {settings.environment}")
```

### Environment Variables

```bash
# .env.development
ENVIRONMENT=development
DEBUG=true
DATABASE_URL=postgresql://...
REDIS_URL=redis://...

# .env.production
ENVIRONMENT=production
DEBUG=false
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
```

## Security Architecture

### Authentication Flow

```
1. User Login
   POST /api/v1/auth/login
   {
       "username": "user",
       "password": "password"
   }

2. Verify Credentials
   - Check username exists
   - Verify password hash
   - Check user is active

3. Generate JWT Token
   - User ID in 'sub' claim
   - Expiration timestamp
   - Sign with SECRET_KEY

4. Return Token
   {
       "access_token": "eyJ...",
       "token_type": "bearer",
       "expires_in": 3600
   }

5. Subsequent Requests
   GET /api/v1/users
   Authorization: Bearer eyJ...

6. Verify Token
   - Decode JWT
   - Verify signature
   - Check expiration
   - Load user

7. Process Request
   - Execute with authenticated user context
   - Check permissions/roles
```

### RBAC (Role-Based Access Control)

```python
# Models
class User(Base):
    role: str  # "user", "admin", "moderator"

# Permissions
ROLE_PERMISSIONS = {
    "user": ["read", "update_own"],
    "admin": ["read", "create", "update", "delete"],
    "moderator": ["read", "delete"],
}

# Middleware/Decorator
@require_role("admin")
async def delete_user(user_id: str, current_user: User):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    # Delete user
```

## Observability Architecture

### Logging

```
Request Context
    ├── Correlation ID (X-Correlation-ID)
    ├── User ID
    ├── Request ID
    └── Timestamps

Structured JSON Logs
{
    "timestamp": "2024-01-10T10:00:00Z",
    "level": "INFO",
    "logger": "app.services.user",
    "message": "User created",
    "user_id": "123",
    "email": "user@example.com",
    "correlation_id": "abc-123"
}
```

### Metrics

```
Prometheus Metrics
├── Request count by endpoint
├── Request duration histogram
├── Request errors by type
├── Active connections
├── Database connection pool
└── Cache hit/miss ratio

Exposed at /api/v1/metrics
```

### Tracing

```
OpenTelemetry Traces
├── HTTP requests (auto-instrumented)
├── Database queries (SQL Alchemy)
├── Redis operations
├── External API calls

Sent to Jaeger collector
```

## Deployment Architecture

### Kubernetes Architecture

```
┌─────────────────────────────────────────┐
│         Ingress Controller               │
│  (SSL/TLS, Rate Limiting, Routing)      │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│        Kubernetes Service               │
│  (Load Balancing, Discovery)            │
└──────────────────┬──────────────────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
┌───▼──┐      ┌───▼──┐      ┌───▼──┐
│ Pod 1│      │ Pod 2│      │ Pod 3│
│FastAPI
        │      │FastAPI
        │      │FastAPI
        │
└───────┘      └────┘      └────┘
    │              │              │
    └──────────────┼──────────────┘
                   │
┌──────────────────▼──────────────────────┐
│   Persistent Storage / Databases        │
│   (PostgreSQL, Redis)                   │
└─────────────────────────────────────────┘
```

### High Availability

```
Multi-AZ Deployment
├── Pod Anti-Affinity
│   └── Spread pods across nodes
├── Pod Disruption Budgets
│   └── Maintain min replicas during updates
├── Health Checks
│   ├── Liveness (container alive)
│   ├── Readiness (ready to serve)
│   └── Startup (app initialized)
└── Auto-Scaling
    └── HPA based on CPU/Memory
```

## Performance Optimization

### Caching Strategy

```
Request
    │
    ▼
Cache Layer (Redis)
    │
    ├─ HIT  → Return cached data
    │
    └─ MISS → Query Database
            ├─ Update Cache
            ├─ Return Data
            └─ Set TTL
```

### Database Optimization

```python
# Connection pooling
pool_size: 20        # Min connections
max_overflow: 10     # Additional connections
pool_pre_ping: true  # Check connection health

# Query optimization
- Proper indexes
- N+1 query prevention
- Pagination for large datasets
```

## Scalability

### Horizontal Scaling

```
Load Balancer
    │
    ├─ Instance 1 (Server)
    ├─ Instance 2 (Server)
    ├─ Instance 3 (Server)
    └─ Instance N (Server)

Shared Database (PostgreSQL)
Shared Cache (Redis)
```

### Vertical Scaling

```
Single Instance with:
- More CPU cores
- More memory
- Faster disk I/O
- Better network
```

## Disaster Recovery

### Backup Strategy

```
Daily Database Backups
├── Full backup (daily)
├── Incremental backups (hourly)
└── Stored in S3 / Cloud Storage

Retention: 30 days

Recovery Time Objective (RTO): 1 hour
Recovery Point Objective (RPO): 1 hour
```

### Failover

```
Primary Database
    │
    ├─ Replication
    ▼
Standby Database
    │
    ├─ Automatic failover on failure
    └─ Promote to primary
```

## API Design

### RESTful Principles

```
Resource-Oriented Design
├── POST   /users          → Create
├── GET    /users          → List
├── GET    /users/{id}     → Get
├── PUT    /users/{id}     → Update
└── DELETE /users/{id}     → Delete

Status Codes
├── 2xx Success
├── 3xx Redirect
├── 4xx Client Error
└── 5xx Server Error
```

### Versioning

```
URL Path Versioning
├── /api/v1/users          → Version 1
├── /api/v2/users          → Version 2
└── /api/v3/users          → Version 3

Header Versioning (Alternative)
├── API-Version: 1
├── API-Version: 2
└── API-Version: 3
```

## Testing Architecture

### Test Pyramid

```
        /\
       /  \  E2E Tests (10%)
      /----\
     /      \  Integration Tests (30%)
    /--------\
   /          \ Unit Tests (60%)
  /____________\

Execution Speed: Slow → Fast
Cost: High → Low
```

## References

- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Microservices Architecture](https://microservices.io/)
- [12-Factor App](https://12factor.net/)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
