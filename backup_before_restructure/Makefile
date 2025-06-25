# Makefile for Dungeon Master's Oracle
# Provides convenient commands for development, testing, and deployment

.PHONY: help setup install test lint format clean build run deploy

# Default target
help:
	@echo "🧙‍♂️ Dungeon Master's Oracle - Available Commands:"
	@echo "=================================================="
	@echo "📦 Setup & Installation:"
	@echo "  make setup          - Complete project setup"
	@echo "  make install        - Install dependencies"
	@echo "  make config         - Create configuration files"
	@echo ""
	@echo "🚀 Development:"
	@echo "  make run            - Start development server"
	@echo "  make run-docker     - Run with Docker Compose"
	@echo "  make test           - Run tests"
	@echo "  make lint           - Run linting"
	@echo "  make format         - Format code"
	@echo ""
	@echo "🏗️  Infrastructure:"
	@echo "  make tf-init        - Initialize Terraform"
	@echo "  make tf-plan        - Plan infrastructure changes"
	@echo "  make tf-apply       - Apply infrastructure"
	@echo "  make tf-destroy     - Destroy infrastructure"
	@echo ""
	@echo "🐳 Docker & Deployment:"
	@echo "  make build          - Build Docker image"
	@echo "  make deploy         - Deploy to Google Cloud"
	@echo "  make clean          - Clean up build artifacts"

# Setup and Installation
setup:
	@echo "🧙‍♂️ Setting up Dungeon Master's Oracle..."
	chmod +x scripts/setup.sh
	./scripts/setup.sh

install:
	@echo "📦 Installing Python dependencies..."
	python3 -m venv venv
	. venv/bin/activate && pip install --upgrade pip
	. venv/bin/activate && pip install -r src/requirements.txt
	. venv/bin/activate && pip install -r data-pipelines/requirements.txt

config:
	@echo "🔧 Creating configuration files..."
	@if [ ! -f .env ]; then \
		echo "Creating .env file..."; \
		cat > .env << 'EOF'; \
# Environment Configuration for Dungeon Master's Oracle\
PROJECT_ID=your-gcp-project-id\
DATASET_ID=dnd_data\
TABLE_ID=monsters\
DATA_BUCKET=your-unique-data-bucket-name\
GOOGLE_API_KEY=your-gemini-api-key-here\
ENVIRONMENT=development\
APP_VERSION=1.0.0\
DEBUG=true\
LOG_LEVEL=INFO\
EOF\
		echo "✅ Created .env - please update with your values"; \
	else \
		echo "✅ .env already exists"; \
	fi
	@if [ ! -f infrastructure/terraform.tfvars ]; then \
		cp infrastructure/terraform.tfvars.example infrastructure/terraform.tfvars; \
		echo "✅ Created terraform.tfvars - please update with your values"; \
	else \
		echo "✅ terraform.tfvars already exists"; \
	fi

# Development
run:
	@echo "🚀 Starting development server..."
	cd src && python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8080

run-docker:
	@echo "🐳 Running with Docker Compose..."
	docker-compose up --build

test:
	@echo "🧪 Running tests..."
	. venv/bin/activate && python -m pytest tests/ -v --cov=src

lint:
	@echo "🔍 Running linting..."
	. venv/bin/activate && flake8 src/
	. venv/bin/activate && black --check src/

format:
	@echo "✨ Formatting code..."
	. venv/bin/activate && black src/
	. venv/bin/activate && isort src/

# Infrastructure
tf-init:
	@echo "🏗️  Initializing Terraform..."
	cd infrastructure && terraform init

tf-plan:
	@echo "📋 Planning infrastructure changes..."
	cd infrastructure && terraform plan

tf-apply:
	@echo "🚀 Applying infrastructure..."
	cd infrastructure && terraform apply

tf-destroy:
	@echo "💥 Destroying infrastructure..."
	cd infrastructure && terraform destroy

# Docker and Deployment
build:
	@echo "🐳 Building Docker image..."
	docker build -f docker/Dockerfile -t dm-oracle:latest .

deploy:
	@echo "☁️  Deploying to Google Cloud..."
	gcloud builds submit --config cloudbuild.yaml

# Cleanup
clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	docker system prune -f
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage

# Quick start command
start: config install run

# Full deployment workflow
full-deploy: setup tf-init tf-apply deploy

# Development workflow
dev: install lint test run 