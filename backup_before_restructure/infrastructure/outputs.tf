# Service Account outputs
output "service_account_email" {
  description = "Email of the service account for the DM Oracle application"
  value       = google_service_account.dm_oracle_sa.email
}

output "service_account_id" {
  description = "ID of the service account"
  value       = google_service_account.dm_oracle_sa.id
}

# Storage outputs
output "data_bucket_name" {
  description = "Name of the GCS bucket for application data"
  value       = google_storage_bucket.data_bucket.name
}

output "data_bucket_url" {
  description = "URL of the GCS bucket for application data"
  value       = google_storage_bucket.data_bucket.url
}

output "tf_state_bucket_name" {
  description = "Name of the GCS bucket for Terraform state"
  value       = google_storage_bucket.tf_state_bucket.name
}

# BigQuery outputs
output "bigquery_dataset_id" {
  description = "BigQuery dataset ID for D&D data"
  value       = google_bigquery_dataset.dnd_dataset.dataset_id
}

output "bigquery_table_id" {
  description = "BigQuery table ID for monster data"
  value       = google_bigquery_table.monsters_table.table_id
}

output "bigquery_table_reference" {
  description = "Full BigQuery table reference"
  value       = "${var.project_id}.${google_bigquery_dataset.dnd_dataset.dataset_id}.${google_bigquery_table.monsters_table.table_id}"
}

# Artifact Registry outputs
output "artifact_registry_repository" {
  description = "Artifact Registry repository for Docker images"
  value       = google_artifact_registry_repository.dm_oracle_repo.name
}

output "docker_repository_url" {
  description = "Docker repository URL for pushing images"
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.dm_oracle_repo.repository_id}"
}

# Cloud Run outputs
output "cloud_run_service_name" {
  description = "Name of the Cloud Run service"
  value       = google_cloud_run_v2_service.dm_oracle_api.name
}

output "cloud_run_service_url" {
  description = "URL of the deployed Cloud Run service"
  value       = google_cloud_run_v2_service.dm_oracle_api.uri
}

output "cloud_run_service_id" {
  description = "ID of the Cloud Run service"
  value       = google_cloud_run_v2_service.dm_oracle_api.id
}

# Secret Manager outputs
output "google_api_key_secret_id" {
  description = "Secret Manager secret ID for Google API key"
  value       = google_secret_manager_secret.google_api_key.secret_id
}

output "openai_api_key_secret_id" {
  description = "Secret Manager secret ID for OpenAI API key"
  value       = google_secret_manager_secret.openai_api_key.secret_id
}

# Project information
output "project_id" {
  description = "The GCP project ID"
  value       = var.project_id
}

output "region" {
  description = "The GCP region"
  value       = var.region
}

# Environment information
output "environment" {
  description = "The deployment environment"
  value       = var.environment
} 