# Artifact Registry Repository for Docker images
resource "google_artifact_registry_repository" "dm_oracle_repo" {
  location      = var.region
  repository_id = var.artifact_registry_repository
  description   = "Docker repository for DM Oracle application images"
  format        = "DOCKER"
  project       = var.project_id

  labels = var.labels
}

# Cloud Run Service for the FastAPI application
resource "google_cloud_run_v2_service" "dm_oracle_api" {
  name     = var.cloud_run_service_name
  location = var.region
  project  = var.project_id

  template {
    # Service account configuration
    service_account = google_service_account.dm_oracle_sa.email

    # Scaling configuration
    scaling {
      min_instance_count = var.cloud_run_min_instances
      max_instance_count = var.cloud_run_max_instances
    }

    containers {
      # Initial placeholder image (will be updated by CI/CD)
      image = "gcr.io/cloudrun/hello"

      # Resource allocation
      resources {
        limits = {
          cpu    = var.cloud_run_cpu
          memory = var.cloud_run_memory
        }
        cpu_idle = true
        startup_cpu_boost = true
      }

      # Port configuration
      ports {
        container_port = var.cloud_run_port
      }

      # Environment variables for application configuration
      env {
        name  = "PROJECT_ID"
        value = var.project_id
      }

      env {
        name  = "DATASET_ID"
        value = var.bigquery_dataset_id
      }

      env {
        name  = "TABLE_ID"
        value = var.bigquery_table_id
      }

      env {
        name  = "DATA_BUCKET"
        value = var.data_bucket_name
      }

      env {
        name  = "ENVIRONMENT"
        value = var.environment
      }

      # Secret environment variables (API keys stored in Secret Manager)
      env {
        name = "GOOGLE_API_KEY"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.google_api_key.secret_id
            version = "latest"
          }
        }
      }

      # Startup and liveness probes
      startup_probe {
        http_get {
          path = "/health"
          port = var.cloud_run_port
        }
        initial_delay_seconds = 30
        timeout_seconds = 10
        failure_threshold = 3
        period_seconds = 10
      }

      liveness_probe {
        http_get {
          path = "/health"
          port = var.cloud_run_port
        }
        initial_delay_seconds = 60
        timeout_seconds = 5
        failure_threshold = 3
        period_seconds = 30
      }
    }

    # Container concurrency (requests per instance)
    max_instance_request_concurrency = 100

    # Request timeout
    timeout = "300s"
  }

  # Traffic configuration (100% to latest revision)
  traffic {
    percent = 100
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
  }

  # Labels for organization
  labels = var.labels

  depends_on = [
    google_service_account.dm_oracle_sa,
    google_secret_manager_secret.google_api_key
  ]
}

# IAM policy to allow public access to Cloud Run service
resource "google_cloud_run_service_iam_member" "public_access" {
  location = google_cloud_run_v2_service.dm_oracle_api.location
  project  = google_cloud_run_v2_service.dm_oracle_api.project
  service  = google_cloud_run_v2_service.dm_oracle_api.name
  role     = "roles/run.invoker"
  member   = "allUsers"
} 