#!/usr/bin/env python3
"""
Configuration file generator for Dungeon Master's Oracle
Run this script to create the necessary .env and terraform.tfvars files
"""

import os
import shutil

def create_env_file():
    """Create .env file with default configuration."""
    env_content = """# Environment Configuration for Dungeon Master's Oracle
# Update these values with your actual configuration

PROJECT_ID=your-gcp-project-id
DATASET_ID=dnd_data
TABLE_ID=monsters
DATA_BUCKET=your-unique-data-bucket-name
GOOGLE_API_KEY=your-gemini-api-key-here
ENVIRONMENT=development
APP_VERSION=1.0.0
DEBUG=true
LOG_LEVEL=INFO

# Optional: For local development with service account key
# GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account-key.json
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Created .env file")
        print("📝 Please edit .env with your actual GCP project details and API keys")
    else:
        print("✅ .env file already exists")

def create_terraform_vars():
    """Create terraform.tfvars from example if it doesn't exist."""
    example_path = "infrastructure/terraform.tfvars.example"
    target_path = "infrastructure/terraform.tfvars"
    
    if os.path.exists(example_path) and not os.path.exists(target_path):
        shutil.copy(example_path, target_path)
        print("✅ Created infrastructure/terraform.tfvars")
        print("📝 Please edit terraform.tfvars with your actual configuration")
    elif os.path.exists(target_path):
        print("✅ terraform.tfvars already exists")
    else:
        print("⚠️  terraform.tfvars.example not found")

def main():
    print("🧙‍♂️ Creating configuration files for Dungeon Master's Oracle...")
    print("=" * 60)
    
    create_env_file()
    create_terraform_vars()
    
    print("\n🎉 Configuration files created!")
    print("\n📋 Next steps:")
    print("1. Edit .env with your GCP project ID and API keys")
    print("2. Edit infrastructure/terraform.tfvars with your configuration")
    print("3. Run: python -m pip install -r src/requirements.txt")
    print("4. Run: cd infrastructure && terraform init && terraform apply")
    print("5. Run: cd src && python -m uvicorn api.main:app --reload")
    print("\nFor detailed instructions, see QUICKSTART.md")

if __name__ == "__main__":
    main() 