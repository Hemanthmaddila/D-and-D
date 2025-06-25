# Infrastructure

This directory contains Terraform Infrastructure as Code (IaC) for provisioning all GCP resources needed for the Dungeon Master's Oracle.

## Architecture

The infrastructure provisions:
- **GCS Buckets**: Terraform state storage and application data
- **BigQuery**: Dataset and table for monster statistics
- **Artifact Registry**: Docker image repository
- **Cloud Run**: Serverless application hosting
- **IAM**: Service accounts with least-privilege permissions
- **Secret Manager**: Secure API key storage

## Prerequisites

1. **GCP Project**: Create a new GCP project with billing enabled
2. **APIs**: Enable required APIs:
   ```bash
   gcloud services enable run.googleapis.com
   gcloud services enable bigquery.googleapis.com
   gcloud services enable iam.googleapis.com
   gcloud services enable artifactregistry.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable aiplatform.googleapis.com
   gcloud services enable secretmanager.googleapis.com
   ```
3. **Authentication**: Set up Application Default Credentials:
   ```bash
   gcloud auth application-default login
   ```

## Setup

1. **Configure Variables**: Copy and customize the terraform.tfvars file:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your GCP project details
   ```

2. **Initialize Terraform**:
   ```bash
   terraform init
   ```

3. **Plan Deployment**:
   ```bash
   terraform plan
   ```

4. **Apply Infrastructure**:
   ```bash
   terraform apply
   ```

## State Management

The Terraform state is stored remotely in a GCS bucket for:
- **Centralized State**: Accessible by team members and CI/CD
- **Versioning**: State file history for rollback capability
- **Locking**: Prevents concurrent modifications

## Security

- **Least Privilege IAM**: Each service account has minimal required permissions
- **Secret Manager**: API keys and sensitive data stored securely
- **Private Resources**: Internal communication where possible

## Outputs

After successful deployment, Terraform outputs:
- GCS bucket names for data storage
- BigQuery dataset and table references
- Cloud Run service URL
- Service account email for application identity 