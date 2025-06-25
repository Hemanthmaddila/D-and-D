#!/usr/bin/env python3
"""
Create BigQuery table using the JSON schema
Run this to actually create the monsters table in your GCP project
"""

import json
import os
from google.cloud import bigquery

def load_schema_from_json(schema_file: str):
    """Load the BigQuery schema from JSON file."""
    with open(schema_file, 'r') as f:
        schema_json = json.load(f)
    
    # Convert JSON to BigQuery SchemaField objects
    schema_fields = []
    for field in schema_json:
        schema_fields.append(
            bigquery.SchemaField(
                name=field["name"],
                field_type=field["type"],
                mode=field["mode"]
            )
        )
    return schema_fields

def create_monsters_table():
    """Create the monsters table using our JSON schema."""
    
    # Get configuration from environment
    project_id = os.getenv("PROJECT_ID", "dandd-oracle")
    dataset_id = os.getenv("DATASET_ID", "dnd_data") 
    table_id = os.getenv("TABLE_ID", "monsters")
    
    print(f"Creating table: {project_id}.{dataset_id}.{table_id}")
    
    # Initialize BigQuery client
    client = bigquery.Client(project=project_id)
    
    # Load schema from our JSON file
    schema = load_schema_from_json("bigquery_schema.json")
    
    # Create dataset if it doesn't exist
    dataset_ref = bigquery.DatasetReference(project_id, dataset_id)
    try:
        client.get_dataset(dataset_ref)
        print(f"✅ Dataset {dataset_id} already exists")
    except Exception:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "US"
        dataset.description = "D&D Monster Data"
        client.create_dataset(dataset)
        print(f"✅ Created dataset {dataset_id}")
    
    # Create table
    table_ref = dataset_ref.table(table_id)
    table = bigquery.Table(table_ref, schema=schema)
    
    # Set table properties
    table.description = "D&D 5e Monster statistics and abilities"
    
    # Add clustering for better performance
    table.clustering_fields = ["challenge_rating", "type", "size"]
    
    try:
        table = client.create_table(table)
        print(f"✅ Created table {project_id}.{dataset_id}.{table_id}")
        print(f"📊 Table has {len(table.schema)} columns")
        
        # Print schema for verification
        print("\n📋 Table Schema:")
        for field in table.schema:
            print(f"  - {field.name}: {field.field_type} ({field.mode})")
            
        return table
        
    except Exception as e:
        if "already exists" in str(e).lower():
            print(f"✅ Table {project_id}.{dataset_id}.{table_id} already exists")
            return client.get_table(table_ref)
        else:
            print(f"❌ Error creating table: {e}")
            raise e

if __name__ == "__main__":
    print("🏗️  Creating BigQuery Monsters Table")
    print("=" * 50)
    
    # Check if schema file exists
    if not os.path.exists("sql_schema/bigquery_schema.json"):
        print("❌ Schema file not found: sql_schema/bigquery_schema.json")
        exit(1)
    
    try:
        table = create_monsters_table()
        print("\n🎉 Success! Your monsters table is ready.")
        print("Next steps:")
        print("  1. Load sample data: python sql_schema/load_sample_data.py")
        print("  2. Test queries in BigQuery console")
        print("  3. Run your data pipeline to populate real data")
        
    except Exception as e:
        print(f"\n❌ Failed to create table: {e}")
        print("Make sure you have:")
        print("  - Set up GCP authentication: gcloud auth application-default login")
        print("  - Set PROJECT_ID environment variable")
        print("  - Enabled BigQuery API in your project") 