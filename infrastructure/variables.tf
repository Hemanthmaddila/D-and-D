# Core GCP Configuration
variable "project_id" {
  description = "The GCP project ID where resources will be created"
  type        = string
}

variable "region" {
  description = "The GCP region for regional resources"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "The GCP zone for zonal resources"
  type        = string
  default     = "us-central1-a"
}

# Application Configuration
variable "app_name" {
  description = "Name of the application (used for resource naming)"
  type        = string
  default     = "dm-oracle"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}

# Storage Configuration
variable "data_bucket_name" {
  description = "Name for the GCS bucket storing application data (must be globally unique)"
  type        = string
}

variable "tf_state_bucket_name" {
  description = "Name for the GCS bucket storing Terraform state (must be globally unique)"
  type        = string
}

# BigQuery Configuration
variable "bigquery_dataset_id" {
  description = "BigQuery dataset ID for monster data"
  type        = string
  default     = "dnd_data"
}

variable "bigquery_table_id" {
  description = "BigQuery table ID for monster statistics"
  type        = string
  default     = "monsters"
}

variable "bigquery_location" {
  description = "Location for BigQuery dataset"
  type        = string
  default     = "US"
}

# Artifact Registry Configuration
variable "artifact_registry_repository" {
  description = "Name of the Artifact Registry repository for Docker images"
  type        = string
  default     = "dm-oracle-images"
}

# Cloud Run Configuration
variable "cloud_run_service_name" {
  description = "Name of the Cloud Run service"
  type        = string
  default     = "dm-oracle-api"
}

variable "cloud_run_min_instances" {
  description = "Minimum number of Cloud Run instances"
  type        = number
  default     = 0
}

variable "cloud_run_max_instances" {
  description = "Maximum number of Cloud Run instances"
  type        = number
  default     = 10
}

variable "cloud_run_cpu" {
  description = "CPU allocation for Cloud Run instances"
  type        = string
  default     = "1"
}

variable "cloud_run_memory" {
  description = "Memory allocation for Cloud Run instances"
  type        = string
  default     = "2Gi"
}

variable "cloud_run_port" {
  description = "Port that the Cloud Run service listens on"
  type        = number
  default     = 8080
}

# Labels for resource organization
variable "labels" {
  description = "Labels to apply to all resources"
  type        = map(string)
  default = {
    project     = "dm-oracle"
    managed-by  = "terraform"
    component   = "rag-system"
  }
} 