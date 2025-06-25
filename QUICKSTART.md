# 🚀 Quick Start Guide - Dungeon Master's Oracle

This guide will get you up and running with the Dungeon Master's Oracle in just a few steps!

## 📋 Prerequisites

Before you start, make sure you have:

1. **Python 3.11+** installed
2. **Google Cloud SDK** installed and configured
3. **Terraform** installed (for infrastructure)
4. **Docker** installed (optional, for containerized deployment)
5. **A Google Cloud Project** with billing enabled

## 🎯 Option 1: Quick Setup with Make

The fastest way to get started:

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd dm-oracle

# 2. Run the automated setup
make help          # See all available commands
make config        # Create configuration files
make install       # Install dependencies
```

## 🔧 Option 2: Manual Setup

### Step 1: Create Configuration Files

```bash
# Create environment file
cat > .env << 'EOF'
PROJECT_ID=your-gcp-project-id
DATASET_ID=dnd_data
TABLE_ID=monsters
DATA_BUCKET=your-unique-data-bucket-name
GOOGLE_API_KEY=your-gemini-api-key-here
ENVIRONMENT=development
APP_VERSION=1.0.0
DEBUG=true
LOG_LEVEL=INFO
EOF

# Create Terraform variables
cp infrastructure/terraform.tfvars.example infrastructure/terraform.tfvars
```

### Step 2: Update Configuration

Edit the files you just created:

**`.env` file:**
```bash
PROJECT_ID=my-dm-oracle-project          # Your actual GCP project ID
DATA_BUCKET=my-dm-oracle-data-unique     # Globally unique bucket name
GOOGLE_API_KEY=AIza...                   # Your actual Gemini API key
```

**`infrastructure/terraform.tfvars` file:**
```hcl
project_id = "my-dm-oracle-project"
data_bucket_name = "my-dm-oracle-data-unique"
tf_state_bucket_name = "my-dm-oracle-tf-state-unique"
```

### Step 3: Authenticate with Google Cloud

```bash
# Authenticate
gcloud auth application-default login

# Set your project
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable bigquery.googleapis.com
gcloud services enable iam.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable secretmanager.googleapis.com
```

### Step 4: Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r src/requirements.txt
pip install -r tests/requirements.txt
```

## 🏗️ Deploy Infrastructure

### Initialize and Deploy with Terraform

```bash
cd infrastructure

# Initialize Terraform
terraform init

# Review the infrastructure plan
terraform plan

# Deploy infrastructure
terraform apply
```

This creates:
- ✅ GCS buckets for data and Terraform state
- ✅ BigQuery dataset and monster table
- ✅ Artifact Registry for Docker images
- ✅ Cloud Run service
- ✅ IAM service accounts with proper permissions
- ✅ Secret Manager for API keys

### Add Your API Key to Secret Manager

```bash
# Add your Gemini API key to Secret Manager
echo "your-actual-api-key" | gcloud secrets create google-api-key --data-file=-

# Or update existing secret
echo "your-actual-api-key" | gcloud secrets versions add google-api-key --data-file=-
```

## 📊 Run Data Pipelines

### Option A: Local Airflow Development

```bash
cd data-pipelines

# Initialize Airflow database
export AIRFLOW_HOME=$(pwd)
airflow db init

# Create admin user
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com

# Start Airflow (in separate terminals)
airflow scheduler &
airflow webserver --port 8081
```

Access Airflow UI at http://localhost:8081 and trigger the `dnd_data_ingestion` DAG.

### Option B: Quick Data Setup (for testing)

```bash
# Run the data ingestion script directly
cd data-pipelines
python -c "
from dags.dnd_data_ingestion import *
import asyncio

# Run data ingestion tasks
asyncio.run(scrape_srd_task())
asyncio.run(clean_monster_data_task())
asyncio.run(load_bigquery_data())
"
```

## 🚀 Start the Application

### Option A: Local Development

```bash
cd src
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8080
```

### Option B: Docker Compose

```bash
# Make sure .env file is in root directory
docker-compose up --build
```

### Option C: Using Make

```bash
make run          # Local development
make run-docker   # Docker Compose
```

## 🧪 Test the System

### 1. Health Check

```bash
curl http://localhost:8080/health
```

### 2. Test Structured Query (Monster Data)

```bash
curl -X POST "http://localhost:8080/query" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "What is a Beholder'\''s armor class?",
       "session_id": "test_session"
     }'
```

### 3. Test Unstructured Query (Rules/Lore)

```bash
curl -X POST "http://localhost:8080/query" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "How does grappling work in D&D 5e?",
       "session_id": "test_session"
     }'
```

### 4. Test Narrative Generation

```bash
curl -X POST "http://localhost:8080/narrate" \
     -H "Content-Type: application/json" \
     -d '{
       "prompt": "Describe a spooky, abandoned tavern in a haunted forest",
       "style": "mysterious"
     }'
```

### 5. Run Automated Tests

```bash
# Run all tests
make test

# Or manually
pytest tests/ -v --cov=src
```

## ☁️ Deploy to Production

### Deploy with Cloud Build

```bash
# Update cloudbuild.yaml with your bucket name and settings
# Then deploy
make deploy

# Or manually
gcloud builds submit --config cloudbuild.yaml
```

### Access Your Deployed API

After deployment, get your Cloud Run URL:

```bash
gcloud run services describe dm-oracle-api --region=us-central1 --format="value(status.url)"
```

## 📚 Interactive API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc

## 🔧 Common Commands

```bash
# Development workflow
make dev           # Install, lint, test, run

# Infrastructure management
make tf-init       # Initialize Terraform
make tf-plan       # Plan infrastructure changes
make tf-apply      # Apply infrastructure
make tf-destroy    # Destroy infrastructure

# Testing and quality
make test          # Run tests
make lint          # Run linting
make format        # Format code

# Deployment
make build         # Build Docker image
make deploy        # Deploy to Google Cloud

# Cleanup
make clean         # Clean build artifacts
```

## 🆘 Troubleshooting

### Common Issues

1. **"RAG engine not initialized"**
   - Check your `.env` file has correct values
   - Ensure `GOOGLE_API_KEY` is set
   - Verify GCP authentication: `gcloud auth list`

2. **BigQuery permission errors**
   - Run: `terraform apply` to ensure IAM roles are set
   - Check service account has correct permissions

3. **Missing data in responses**
   - Run the data ingestion pipeline first
   - Check BigQuery table has data: `bq query "SELECT COUNT(*) FROM your_project.dnd_data.monsters"`

4. **Docker build fails**
   - Ensure all requirements.txt files exist
   - Check Docker has enough memory allocated

### Get Help

- Check the logs: `docker-compose logs dm-oracle`
- Review API documentation: http://localhost:8080/docs
- Verify infrastructure: `terraform plan`

## 🎉 You're Ready!

Your Dungeon Master's Oracle is now running! The system provides:

- 🧠 **Intelligent Query Routing** between structured and unstructured data
- 🗄️ **Monster Database Queries** with self-correcting SQL
- 📖 **D&D Rules and Lore** from the SRD
- 🎭 **Creative Narrative Generation** for storytelling
- ⚡ **Production-Ready** deployment on Google Cloud

Start asking questions and generating epic D&D content! 🐉⚔️🧙‍♂️ 