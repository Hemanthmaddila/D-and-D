# BigQuery Table for D&D Monster Data
# This Terraform resource creates the monsters table with the exact schema specified

resource "google_bigquery_table" "monsters_table_updated" {
  dataset_id = var.bigquery_dataset_id
  table_id   = var.bigquery_table_id
  project    = var.project_id

  description = "D&D 5e Monster statistics and abilities with complete schema"

  # Schema definition matching the user's specification
  schema = jsonencode([
    {
      name = "name"
      type = "STRING"
      mode = "REQUIRED"
      description = "The unique name of the monster"
    },
    {
      name = "type"
      type = "STRING"
      mode = "NULLABLE"
      description = "The creature type (Beast, Fiend, Dragon, etc.)"
    },
    {
      name = "size"
      type = "STRING"
      mode = "NULLABLE"
      description = "The size category (Tiny, Small, Medium, Large, Huge, Gargantuan)"
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
      name = "speed"
      type = "STRING"
      mode = "NULLABLE"
      description = "Movement speeds (walk, fly, swim, etc.)"
    },
    {
      name = "challenge_rating"
      type = "STRING"
      mode = "NULLABLE"
      description = "The monster's Challenge Rating (CR as string)"
    },
    {
      name = "abilities"
      type = "STRING"
      mode = "NULLABLE"
      description = "All ability scores formatted as string (STR, DEX, CON, INT, WIS, CHA)"
    },
    {
      name = "skills"
      type = "STRING"
      mode = "NULLABLE"
      description = "Proficient skills and bonuses"
    },
    {
      name = "damage_resistances"
      type = "STRING"
      mode = "NULLABLE"
      description = "Damage types the monster resists"
    },
    {
      name = "damage_immunities"
      type = "STRING"
      mode = "NULLABLE"
      description = "Damage types the monster is immune to"
    },
    {
      name = "condition_immunities"
      type = "STRING"
      mode = "NULLABLE"
      description = "Conditions the monster is immune to"
    },
    {
      name = "senses"
      type = "STRING"
      mode = "NULLABLE"
      description = "Special senses (darkvision, blindsight, etc.)"
    },
    {
      name = "languages"
      type = "STRING"
      mode = "NULLABLE"
      description = "Languages the monster can speak/understand"
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
    },
    {
      name = "legendary_actions"
      type = "STRING"
      mode = "NULLABLE"
      description = "Legendary actions (if any)"
    },
    {
      name = "source"
      type = "STRING"
      mode = "NULLABLE"
      description = "Source book or material"
    }
  ])

  # Performance optimizations
  time_partitioning {
    type  = "DAY"
    field = null  # Uses _PARTITIONTIME
  }

  clustering = ["challenge_rating", "type", "size"]

  # Deletion protection for production
  deletion_protection = true

  # Labels for organization
  labels = var.labels
}

# Output the table reference for use in other resources
output "monsters_table_full_reference" {
  description = "Full BigQuery table reference for the updated monsters table"
  value       = "${var.project_id}.${var.bigquery_dataset_id}.${google_bigquery_table.monsters_table_updated.table_id}"
} 