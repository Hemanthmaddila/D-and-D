#!/usr/bin/env python3
"""
Deploy Dungeon Master's Oracle to Google Cloud Production
Complete deployment automation script
"""

import os
import subprocess
import sys
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_command(command, description, check=True):
    """Run a shell command with proper error handling."""
    print(f"\n🔄 {description}")
    print(f"Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(f"✅ Output: {result.stdout.strip()}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        if check:
            sys.exit(1)
        return e

def check_prerequisites():
    """Check if all required tools are installed."""
    print("🔍 Checking Prerequisites...")
    
    tools = {
        "gcloud": "gcloud --version",
        "terraform": "terraform --version",
        "docker": "docker --version"
    }
    
    for tool, command in tools.items():
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            print(f"✅ {tool}: Found")
        except subprocess.CalledProcessError:
            print(f"❌ {tool}: Not found or not working")
            print(f"Please install {tool} and try again")
            return False
    
    return True

def setup_gcp_authentication():
    """Ensure GCP authentication is set up."""
    print("\n🔐 Setting up GCP Authentication...")
    
    # Check if already authenticated
    result = run_command("gcloud auth list", "Checking current authentication", check=False)
    
    if "No credentialed accounts" in result.stdout or result.returncode != 0:
        print("🔑 Need to authenticate with GCP...")
        run_command("gcloud auth login", "Authenticating with GCP")
        run_command("gcloud auth application-default login", "Setting up application default credentials")
    else:
        print("✅ Already authenticated with GCP")
    
    # Set project
    project_id = os.getenv("PROJECT_ID", "dandd-oracle")
    run_command(f"gcloud config set project {project_id}", f"Setting project to {project_id}")

def enable_required_apis():
    """Enable all required GCP APIs."""
    print("\n🔧 Enabling Required GCP APIs...")
    
    apis = [
        "run.googleapis.com",
        "bigquery.googleapis.com", 
        "iam.googleapis.com",
        "artifactregistry.googleapis.com",
        "cloudbuild.googleapis.com",
        "aiplatform.googleapis.com",
        "secretmanager.googleapis.com"
    ]
    
    for api in apis:
        run_command(f"gcloud services enable {api}", f"Enabling {api}")

def deploy_infrastructure():
    """Deploy infrastructure using Terraform."""
    print("\n🏗️  Deploying Infrastructure with Terraform...")
    
    os.chdir("infrastructure")
    
    # Initialize Terraform
    run_command("terraform init", "Initializing Terraform")
    
    # Plan deployment
    run_command("terraform plan", "Planning infrastructure deployment")
    
    # Ask for confirmation
    response = input("\n❓ Do you want to apply the infrastructure changes? (y/N): ")
    if response.lower() != 'y':
        print("❌ Deployment cancelled by user")
        return False
    
    # Apply infrastructure
    run_command("terraform apply -auto-approve", "Applying infrastructure changes")
    
    # Get outputs
    run_command("terraform output", "Getting infrastructure outputs")
    
    os.chdir("..")
    return True

def build_and_deploy_app():
    """Build and deploy the FastAPI application."""
    print("\n🐳 Building and Deploying Application...")
    
    # Build and submit to Cloud Build
    run_command(
        "gcloud builds submit --config cloudbuild.yaml .",
        "Building and deploying application with Cloud Build"
    )

def verify_deployment():
    """Verify the deployment is working."""
    print("\n✅ Verifying Deployment...")
    
    # Get the service URL
    result = run_command(
        "gcloud run services describe dm-oracle-api --region=us-central1 --format='value(status.url)'",
        "Getting service URL",
        check=False
    )
    
    if result.returncode == 0 and result.stdout.strip():
        service_url = result.stdout.strip()
        print(f"🌐 Service URL: {service_url}")
        
        # Test health endpoint
        import requests
        try:
            response = requests.get(f"{service_url}/health", timeout=30)
            if response.status_code == 200:
                print("🎉 Health check passed! Your Oracle is live!")
                print(f"📖 API Documentation: {service_url}/docs")
                return service_url
            else:
                print(f"⚠️  Health check failed: {response.status_code}")
        except Exception as e:
            print(f"⚠️  Could not reach service: {e}")
    
    return None

def main():
    """Main deployment function."""
    print("🎲 Deploying Dungeon Master's Oracle to Production")
    print("=" * 60)
    
    # Check prerequisites
    if not check_prerequisites():
        return False
    
    # Setup authentication
    setup_gcp_authentication()
    
    # Enable APIs
    enable_required_apis()
    
    # Deploy infrastructure
    if not deploy_infrastructure():
        return False
    
    # Build and deploy app
    build_and_deploy_app()
    
    # Verify deployment
    service_url = verify_deployment()
    
    if service_url:
        print("\n🎉 DEPLOYMENT SUCCESSFUL!")
        print("=" * 60)
        print(f"🌐 Your Dungeon Master's Oracle is live at:")
        print(f"   {service_url}")
        print(f"📖 API Documentation:")
        print(f"   {service_url}/docs")
        print(f"🧪 Test Query:")
        print(f"   curl -X POST '{service_url}/query' \\")
        print(f"        -H 'Content-Type: application/json' \\")
        print(f"        -d '{{\"query\": \"What is a Beholder's armor class?\"}}'")
        print("\n🎯 Next Steps:")
        print("   1. Share the URL with D&D players!")
        print("   2. Add more monster data (see data expansion guide)")
        print("   3. Monitor usage in Google Cloud Console")
        
        return True
    else:
        print("\n❌ Deployment verification failed")
        print("Check the logs in Google Cloud Console")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 