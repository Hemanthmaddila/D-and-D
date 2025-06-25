"""
BigQuery schema definition for D&D Monsters table
Provides programmatic access to create and manage the monsters table
"""

from google.cloud import bigquery
from typing import List, Dict, Any
import os

# Schema definition
MONSTERS_SCHEMA = [
    bigquery.SchemaField("name", "STRING", mode="REQUIRED", description="The unique name of the monster"),
    bigquery.SchemaField("type", "STRING", mode="NULLABLE", description="The creature type (Beast, Fiend, Dragon, etc.)"),
    bigquery.SchemaField("size", "STRING", mode="NULLABLE", description="The size category (Tiny, Small, Medium, Large, Huge, Gargantuan)"),
    bigquery.SchemaField("armor_class", "INTEGER", mode="NULLABLE", description="The monster's Armor Class (AC)"),
    bigquery.SchemaField("hit_points", "INTEGER", mode="NULLABLE", description="The monster's hit points"),
    bigquery.SchemaField("speed", "STRING", mode="NULLABLE", description="Movement speeds (walk, fly, swim, etc.)"),
    bigquery.SchemaField("challenge_rating", "STRING", mode="NULLABLE", description="The monster's Challenge Rating (CR)"),
    bigquery.SchemaField("abilities", "STRING", mode="NULLABLE", description="All ability scores (STR, DEX, CON, INT, WIS, CHA)"),
    bigquery.SchemaField("skills", "STRING", mode="NULLABLE", description="Proficient skills and bonuses"),
    bigquery.SchemaField("damage_resistances", "STRING", mode="NULLABLE", description="Damage types the monster resists"),
    bigquery.SchemaField("damage_immunities", "STRING", mode="NULLABLE", description="Damage types the monster is immune to"),
    bigquery.SchemaField("condition_immunities", "STRING", mode="NULLABLE", description="Conditions the monster is immune to"),
    bigquery.SchemaField("senses", "STRING", mode="NULLABLE", description="Special senses (darkvision, blindsight, etc.)"),
    bigquery.SchemaField("languages", "STRING", mode="NULLABLE", description="Languages the monster can speak/understand"),
    bigquery.SchemaField("special_abilities", "STRING", mode="NULLABLE", description="Special traits or abilities"),
    bigquery.SchemaField("actions", "STRING", mode="NULLABLE", description="Actions the monster can take"),
    bigquery.SchemaField("legendary_actions", "STRING", mode="NULLABLE", description="Legendary actions (if any)"),
    bigquery.SchemaField("source", "STRING", mode="NULLABLE", description="Source book or material")
]

def create_monsters_table(
    project_id: str,
    dataset_id: str = "dnd_data",
    table_id: str = "monsters",
    location: str = "US"
) -> bigquery.Table:
    """
    Create the monsters table in BigQuery with the specified schema.
    
    Args:
        project_id: Google Cloud project ID
        dataset_id: BigQuery dataset ID
        table_id: BigQuery table ID
        location: BigQuery location
    
    Returns:
        Created BigQuery table object
    """
    client = bigquery.Client(project=project_id)
    
    # Ensure dataset exists
    dataset_ref = bigquery.DatasetReference(project_id, dataset_id)
    try:
        client.get_dataset(dataset_ref)
    except Exception:
        # Create dataset if it doesn't exist
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = location
        dataset.description = "D&D Monster Data"
        client.create_dataset(dataset)
        print(f"Created dataset {dataset_id}")
    
    # Create table reference
    table_ref = dataset_ref.table(table_id)
    table = bigquery.Table(table_ref, schema=MONSTERS_SCHEMA)
    
    # Set table properties
    table.description = "D&D 5e Monster statistics and abilities"
    
    # Partitioning and clustering for performance
    table.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field=None  # _PARTITIONTIME
    )
    table.clustering_fields = ["challenge_rating", "type", "size"]
    
    # Create the table
    try:
        table = client.create_table(table)
        print(f"Created table {project_id}.{dataset_id}.{table_id}")
        return table
    except Exception as e:
        if "already exists" in str(e).lower():
            print(f"Table {project_id}.{dataset_id}.{table_id} already exists")
            return client.get_table(table_ref)
        else:
            raise e

def get_table_schema_dict() -> List[Dict[str, Any]]:
    """
    Get the schema as a list of dictionaries for JSON serialization.
    Useful for Terraform or other IaC tools.
    """
    return [
        {
            "name": field.name,
            "type": field.field_type,
            "mode": field.mode,
            "description": field.description
        }
        for field in MONSTERS_SCHEMA
    ]

def validate_monster_data(monster_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and clean monster data before inserting into BigQuery.
    
    Args:
        monster_data: Dictionary containing monster information
    
    Returns:
        Cleaned and validated monster data
    """
    # Required field validation
    if not monster_data.get("name"):
        raise ValueError("Monster name is required")
    
    # Clean and convert data types
    cleaned_data = {}
    
    for field in MONSTERS_SCHEMA:
        field_name = field.name
        value = monster_data.get(field_name)
        
        if value is None and field.mode == "REQUIRED":
            raise ValueError(f"Required field {field_name} is missing")
        
        if value is not None:
            # Type conversion based on BigQuery schema
            if field.field_type == "INTEGER":
                try:
                    cleaned_data[field_name] = int(value) if value != "" else None
                except (ValueError, TypeError):
                    cleaned_data[field_name] = None
            elif field.field_type == "STRING":
                cleaned_data[field_name] = str(value) if value != "" else None
            else:
                cleaned_data[field_name] = value
        else:
            cleaned_data[field_name] = None
    
    return cleaned_data

def insert_monster_data(
    project_id: str,
    monsters: List[Dict[str, Any]],
    dataset_id: str = "dnd_data",
    table_id: str = "monsters"
) -> None:
    """
    Insert monster data into the BigQuery table.
    
    Args:
        project_id: Google Cloud project ID
        monsters: List of monster dictionaries
        dataset_id: BigQuery dataset ID
        table_id: BigQuery table ID
    """
    client = bigquery.Client(project=project_id)
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    
    # Validate and clean all monster data
    cleaned_monsters = [validate_monster_data(monster) for monster in monsters]
    
    # Insert data
    errors = client.insert_rows_json(table_ref, cleaned_monsters)
    
    if errors:
        raise Exception(f"Failed to insert data: {errors}")
    else:
        print(f"Successfully inserted {len(cleaned_monsters)} monsters")

# Example usage
if __name__ == "__main__":
    # Get configuration from environment variables
    project_id = os.getenv("PROJECT_ID", "your-project-id")
    dataset_id = os.getenv("DATASET_ID", "dnd_data")
    table_id = os.getenv("TABLE_ID", "monsters")
    
    # Create the table
    table = create_monsters_table(project_id, dataset_id, table_id)
    
    # Print schema for verification
    print("\nTable Schema:")
    for field in MONSTERS_SCHEMA:
        print(f"  {field.name}: {field.field_type} ({field.mode})") 