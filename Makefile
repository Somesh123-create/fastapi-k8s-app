.PHONY: help install run dev test lint format mypy black isort ruff docker-build docker-run docker-clean k8s-deploy-dev k8s-deploy-qa k8s-deploy-prod k8s-logs k8s-shell clean

# Variables
PYTHON := python3
PIP := pip3
DOCKER_REGISTRY := ghcr.io
IMAGE_NAME := fastapi-k8s-app
IMAGE_TAG := latest
APP_NAME := FastAPI K8s App

help:
	@echo "$(APP_NAME) - Development Commands"
	@echo "=================================="
	@echo ""
	@echo "Setup:"
	@echo "  make install          - Install dependencies"
	@echo "  make dev-install      - Install dev dependencies"
	@echo ""
	@echo "Running:"
	@echo "  make run              - Run application locally"
	@echo "  make run-docker       - Run with docker-compose"
	@echo ""
	@echo "Testing:"
	@echo "  make test             - Run all tests"
	@echo "  make test-unit        - Run unit tests"
	@echo "  make test-integration - Run integration tests"
	@echo "  make test-api         - Run API tests"
	@echo "  make test-coverage    - Run tests with coverage"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint             - Run all linters"
	@echo "  make format           - Format code"
	@echo "  make black            - Format with black"
	@echo "  make isort            - Sort imports"
	@echo "  make ruff             - Run ruff linter"
	@echo "  make mypy             - Type checking"
	@echo "  make bandit           - Security checks"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build     - Build Docker image"
	@echo "  make docker-run       - Run with docker-compose"
	@echo "  make docker-clean     - Clean docker resources"
	@echo ""
	@echo "Kubernetes:"
	@echo "  make k8s-deploy-dev   - Deploy to dev"
	@echo "  make k8s-deploy-qa    - Deploy to qa"
	@echo "  make k8s-deploy-prod  - Deploy to prod"
	@echo "  make k8s-delete       - Delete deployment"
	@echo "  make k8s-logs         - Show pod logs"
	@echo ""
	@echo "Database:"
	@echo "  make migrate          - Run migrations"
	@echo "  make migrate-create   - Create new migration"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean            - Clean temporary files"
	@echo "  make help             - Show this help message"

install:
	$(PIP) install -r requirements.txt
	@echo "✅ Dependencies installed"

dev-install:
	$(PIP) install -r requirements-dev.txt
	pre-commit install
	@echo "✅ Development dependencies installed"

run:
	$(PYTHON) -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

run-docker:
	docker-compose up

test:
	pytest tests/ -v --cov=app --cov-report=html

test-unit:
	pytest tests/unit -v --tb=short

test-integration:
	pytest tests/integration -v --tb=short

test-api:
	pytest tests/api -v --tb=short

test-coverage:
	pytest tests/ --cov=app --cov-report=html --cov-report=term-missing

lint: black isort ruff mypy bandit
	@echo "✅ All linting checks passed"

format: black isort
	@echo "✅ Code formatted"

black:
	black app tests

isort:
	isort app tests

ruff:
	ruff check app tests

mypy:
	mypy app

bandit:
	bandit -r app -ll

docker-build:
	docker build -t $(DOCKER_REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG) .
	@echo "✅ Docker image built: $(DOCKER_REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG)"

docker-run: docker-build
	docker-compose up

docker-clean:
	docker-compose down -v
	docker rmi $(DOCKER_REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG)
	@echo "✅ Docker resources cleaned"

k8s-deploy-dev:
	kubectl apply -f kubernetes/dev/
	@echo "✅ Deployed to dev"

k8s-deploy-qa:
	kubectl apply -f kubernetes/qa/
	@echo "✅ Deployed to qa"

k8s-deploy-prod:
	kubectl apply -f kubernetes/prod/
	@echo "✅ Deployed to prod"

k8s-delete:
	kubectl delete -f kubernetes/dev/
	@echo "✅ Deployment deleted"

k8s-logs:
	kubectl logs -f deployment/fastapi-app

migrate:
	alembic upgrade head

migrate-create:
	@read -p "Enter migration name: " name; \
	alembic revision --autogenerate -m "$$name"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf htmlcov
	rm -rf .coverage
	@echo "✅ Temporary files cleaned"
