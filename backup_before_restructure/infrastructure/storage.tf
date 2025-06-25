# GCS Bucket for application data (SRD text files, FAISS index)
resource "google_storage_bucket" "data_bucket" {
  name     = var.data_bucket_name
  location = var.region
  project  = var.project_id

  # Enable versioning for data protection
  versioning {
    enabled = true
  }

  # Lifecycle management to control costs
  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete"
    }
  }

  # Security configurations
  uniform_bucket_level_access = true
  
  # Labels for organization
  labels = var.labels
}

# GCS Bucket for Terraform state (if not already exists)
resource "google_storage_bucket" "tf_state_bucket" {
  name     = var.tf_state_bucket_name
  location = var.region
  project  = var.project_id

  # Enable versioning for state file safety
  versioning {
    enabled = true
  }

  # Prevent accidental deletion of state files
  lifecycle_rule {
    condition {
      age = 365  # Keep state files for 1 year
    }
    action {
      type = "Delete"
    }
  }

  # Security configurations
  uniform_bucket_level_access = true
  
  # Labels for organization
  labels = merge(var.labels, {
    purpose = "terraform-state"
  })
}

# BigQuery Dataset for D&D structured data
resource "google_bigquery_dataset" "dnd_dataset" {
  dataset_id    = var.bigquery_dataset_id
  friendly_name = "D&D Monster Data"
  description   = "Dataset containing structured D&D monster statistics and information"
  location      = var.bigquery_location
  project       = var.project_id

  # Access control
  access {
    role          = "OWNER"
    user_by_email = google_service_account.dm_oracle_sa.email
  }

  # Labels for organization
  labels = var.labels
}

# BigQuery Table for monster statistics
# Schema matches the specification in Table 2 of the plan
resource "google_bigquery_table" "monsters_table" {
  dataset_id = google_bigquery_dataset.dnd_dataset.dataset_id
  table_id   = var.bigquery_table_id
  project    = var.project_id

  description = "Table containing D&D 5e monster statistics and abilities"

  # Schema definition matching the specification
  schema = jsonencode([
    {
      name = "name"
      type = "STRING"
      mode = "REQUIRED"
      description = "The unique name of the monster"
    },
    {
      name = "size"
      type = "STRING"
      mode = "NULLABLE"
      description = "The size category (Tiny, Small, Medium, Large, Huge, Gargantuan)"
    },
    {
      name = "type"
      type = "STRING"
      mode = "NULLABLE"
      description = "The creature type (Beast, Fiend, Dragon, etc.)"
    },
    {
      name = "alignment"
      type = "STRING"
      mode = "NULLABLE"
      description = "The monster's alignment (Lawful Good, Chaotic Evil, etc.)"
    },
    {
      name = "armor_class"
      type = "INTEGER"
      mode = "NULLABLE"
      description = "The monster's Armor Class (AC)"
    },
    {
      name = "hit_points"
      type = "INTEGER"
      mode = "NULLABLE"
      description = "The monster's hit points"
    },
    {
      name = "challenge_rating"
      type = "FLOAT"
      mode = "NULLABLE"
      description = "The monster's Challenge Rating (CR)"
    },
    {
      name = "strength"
      type = "INTEGER"
      mode = "NULLABLE"
      description = "Strength ability score"
    },
    {
      name = "dexterity"
      type = "INTEGER"
      mode = "NULLABLE"
      description = "Dexterity ability score"
    },
    {
      name = "constitution"
      type = "INTEGER"
      mode = "NULLABLE"
      description = "Constitution ability score"
    },
    {
      name = "intelligence"
      type = "INTEGER"
      mode = "NULLABLE"
      description = "Intelligence ability score"
    },
    {
      name = "wisdom"
      type = "INTEGER"
      mode = "NULLABLE"
      description = "Wisdom ability score"
    },
    {
      name = "charisma"
      type = "INTEGER"
      mode = "NULLABLE"
      description = "Charisma ability score"
    },
    {
      name = "special_abilities"
      type = "STRING"
      mode = "NULLABLE"
      description = "Special traits or abilities"
    },
    {
      name = "actions"
      type = "STRING"
      mode = "NULLABLE"
      description = "Actions the monster can take"
    }
  ])

  # Deletion protection
  deletion_protection = true

  # Labels for organization
  labels = var.labels
} 