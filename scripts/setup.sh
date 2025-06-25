#!/bin/bash
# Setup script for Dungeon Master's Oracle
# This script helps initialize the development environment

set -e

echo "🧙‍♂️ Setting up Dungeon Master's Oracle Development Environment"
echo "============================================================"

# Check prerequisites
check_prerequisites() {
    echo "📋 Checking prerequisites..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 is required but not installed"
        exit 1
    fi
    
    # Check gcloud
    if ! command -v gcloud &> /dev/null; then
        echo "❌ Google Cloud SDK is required but not installed"
        echo "   Install from: https://cloud.google.com/sdk/docs/install"
        exit 1
    fi
    
    # Check terraform
    if ! command -v terraform &> /dev/null; then
        echo "❌ Terraform is required but not installed"
        echo "   Install from: https://developer.hashicorp.com/terraform/downloads"
        exit 1
    fi
    
    # Check docker
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker is required but not installed"
        echo "   Install from: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    echo "✅ All prerequisites are installed"
}

# Setup Python environment
setup_python_env() {
    echo "🐍 Setting up Python environment..."
    
    # Create virtual environment
    python3 -m venv venv
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install dependencies
    pip install -r src/requirements.txt
    
    echo "✅ Python environment ready"
}

# Setup GCP authentication
setup_gcp_auth() {
    echo "☁️  Setting up GCP authentication..."
    
    echo "Please run the following command to authenticate:"
    echo "gcloud auth application-default login"
    echo ""
    echo "Then set your project:"
    echo "gcloud config set project YOUR_PROJECT_ID"
    echo ""
    read -p "Press Enter after completing GCP authentication..."
}

# Setup environment variables
setup_env_vars() {
    echo "🔧 Setting up environment variables..."
    
    if [ ! -f .env ]; then
        cat > .env << 'EOF'
# Environment Configuration for Dungeon Master's Oracle
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
        echo "✅ Created .env file - please update with your values"
        echo "📝 Edit .env with your actual GCP project ID and API keys"
    else
        echo "✅ .env file already exists"
    fi
}

# Initialize Terraform
setup_terraform() {
    echo "🏗️  Setting up Terraform..."
    
    cd infrastructure
    
    if [ ! -f terraform.tfvars ]; then
        cp terraform.tfvars.example terraform.tfvars
        echo "✅ Created terraform.tfvars - please update with your values"
    else
        echo "✅ terraform.tfvars already exists"
    fi
    
    echo "To initialize Terraform, run:"
    echo "cd infrastructure && terraform init"
    
    cd ..
}

# Main setup
main() {
    check_prerequisites
    setup_python_env
    setup_gcp_auth
    setup_env_vars
    setup_terraform
    
    echo ""
    echo "🎉 Setup complete! Next steps:"
    echo "1. Update .env with your GCP project details and API keys"
    echo "2. Update infrastructure/terraform.tfvars with your configuration"
    echo "3. Deploy infrastructure: cd infrastructure && terraform apply"
    echo "4. Run data pipelines to populate the knowledge base"
    echo "5. Start the development server: cd src && python -m uvicorn api.main:app --reload"
    echo ""
    echo "For detailed instructions, see README.md"
}

main "$@" 