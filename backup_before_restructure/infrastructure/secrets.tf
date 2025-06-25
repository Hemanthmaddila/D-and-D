# Secret Manager Secret for Google API Key (Gemini/Vertex AI)
resource "google_secret_manager_secret" "google_api_key" {
  secret_id = "google-api-key"
  project   = var.project_id

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }

  labels = var.labels
}

# Secret for OpenAI API key (if using OpenAI as fallback)
resource "google_secret_manager_secret" "openai_api_key" {
  secret_id = "openai-api-key"
  project   = var.project_id

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }

  labels = var.labels
}