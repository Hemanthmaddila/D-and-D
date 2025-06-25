# Terraform backend configuration for remote state management
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }

  backend "gcs" {
    bucket = "dm-oracle-tf-state-bucket"  # Replace with your globally unique bucket name
    prefix = "terraform/state"
  }
}

# Google Cloud Provider configuration
provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

# Data source for current project
data "google_project" "current" {}

# Data source for current client configuration
data "google_client_config" "default" {} 