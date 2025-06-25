# Service Account for the DM Oracle application
# This service account represents the application's identity within GCP
resource "google_service_account" "dm_oracle_sa" {
  account_id   = "${var.app_name}-service-account"
  display_name = "DM Oracle Service Account"
  description  = "Service account for the Dungeon Master's Oracle RAG application"
  project      = var.project_id
}

# IAM Role Bindings - Following Principle of Least Privilege
# Each role is carefully chosen to provide only the minimum permissions required

# Storage Object Admin - Allows read/write access to GCS buckets
# Needed for: Airflow pipeline to upload SRD text files and FAISS index
resource "google_project_iam_member" "storage_object_admin" {
  project = var.project_id
  role    = "roles/storage.objectAdmin"
  member  = "serviceAccount:${google_service_account.dm_oracle_sa.email}"
}

# BigQuery Data Editor - Allows reading and writing data in BigQuery tables
# Needed for: Airflow pipeline to load monster data, RAG agent to query data
resource "google_project_iam_member" "bigquery_data_editor" {
  project = var.project_id
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${google_service_account.dm_oracle_sa.email}"
}

# BigQuery Job User - Allows running BigQuery jobs (queries, data loading)
# Needed for: Text-to-SQL queries and data ingestion processes
resource "google_project_iam_member" "bigquery_job_user" {
  project = var.project_id
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${google_service_account.dm_oracle_sa.email}"
}

# Cloud Run Invoker - Allows public access to the Cloud Run service
# Needed for: HTTP requests to reach the FastAPI application
resource "google_project_iam_member" "run_invoker" {
  project = var.project_id
  role    = "roles/run.invoker"
  member  = "serviceAccount:${google_service_account.dm_oracle_sa.email}"
}

# Artifact Registry Writer - Allows pushing Docker images
# Needed for: Cloud Build pipeline to store built images
resource "google_project_iam_member" "artifact_registry_writer" {
  project = var.project_id
  role    = "roles/artifactregistry.writer"
  member  = "serviceAccount:${google_service_account.dm_oracle_sa.email}"
}

# AI Platform User - Allows access to Vertex AI services
# Needed for: Generating embeddings and LLM API calls
resource "google_project_iam_member" "aiplatform_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.dm_oracle_sa.email}"
}

# Secret Manager Secret Accessor - Allows reading secrets
# Needed for: Accessing API keys and other sensitive configuration at runtime
resource "google_project_iam_member" "secret_manager_accessor" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.dm_oracle_sa.email}"
}

# Create a service account key for local development (optional)
# Note: In production, use Workload Identity instead of service account keys
resource "google_service_account_key" "dm_oracle_sa_key" {
  service_account_id = google_service_account.dm_oracle_sa.name
  public_key_type    = "TYPE_X509_PEM_FILE"
}

# Output the service account email for use in other configurations
output "service_account_email" {
  description = "Email of the service account for the DM Oracle application"
  value       = google_service_account.dm_oracle_sa.email
} 