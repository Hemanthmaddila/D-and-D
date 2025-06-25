#!/usr/bin/env python3
"""
Load sample monster data into BigQuery table
Run this after creating the table to test with real D&D monster data
"""

import os
import json
from google.cloud import bigquery
from sample_data import SAMPLE_MONSTERS, format_for_insert

def load_sample_data():
    """Load sample monster data into the BigQuery table."""
    
    # Get configuration from environment
    project_id = os.getenv("PROJECT_ID", "dandd-oracle")
    dataset_id = os.getenv("DATASET_ID", "dnd_data")
    table_id = os.getenv("TABLE_ID", "monsters")
    
    print(f"Loading data into: {project_id}.{dataset_id}.{table_id}")
    
    # Initialize BigQuery client
    client = bigquery.Client(project=project_id)
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    
    # Check if table exists
    try:
        table = client.get_table(table_ref)
        print(f"✅ Found table {table_ref}")
    except Exception as e:
        print(f"❌ Table not found: {e}")
        print("Run 'python sql_schema/create_table.py' first to create the table")
        return False
    
    # Format sample data for insertion
    formatted_data = format_for_insert()
    print(f"📊 Preparing to insert {len(formatted_data)} monsters")
    
    # Show what we're inserting
    print("\n🐉 Sample monsters to insert:")
    for monster in formatted_data:
        cr = monster.get('challenge_rating', 'Unknown')
        monster_type = monster.get('type', 'Unknown')
        print(f"  - {monster['name']} ({monster_type}, CR {cr})")
    
    # Insert data
    try:
        errors = client.insert_rows_json(table_ref, formatted_data)
        
        if errors:
            print(f"❌ Errors occurred during insertion:")
            for error in errors:
                print(f"  - {error}")
            return False
        else:
            print(f"\n✅ Successfully inserted {len(formatted_data)} monsters!")
            
            # Verify the data was inserted
            query = f"""
            SELECT COUNT(*) as total_monsters,
                   COUNT(DISTINCT type) as unique_types,
                   MIN(challenge_rating) as min_cr,
                   MAX(challenge_rating) as max_cr
            FROM `{table_ref}`
            """
            
            result = client.query(query).result()
            for row in result:
                print(f"📈 Table now contains:")
                print(f"   - Total monsters: {row.total_monsters}")
                print(f"   - Unique types: {row.unique_types}")
                print(f"   - CR range: {row.min_cr} to {row.max_cr}")
            
            return True
            
    except Exception as e:
        print(f"❌ Failed to insert data: {e}")
        return False

def test_queries():
    """Run some test queries to verify the data."""
    
    project_id = os.getenv("PROJECT_ID", "dandd-oracle")
    dataset_id = os.getenv("DATASET_ID", "dnd_data")
    table_id = os.getenv("TABLE_ID", "monsters")
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    
    client = bigquery.Client(project=project_id)
    
    test_queries = [
        {
            "name": "All Dragons",
            "sql": f"SELECT name, challenge_rating, hit_points FROM `{table_ref}` WHERE type = 'Dragon'"
        },
        {
            "name": "High CR Monsters (CR 10+)",
            "sql": f"""
            SELECT name, type, challenge_rating 
            FROM `{table_ref}` 
            WHERE SAFE_CAST(REGEXP_EXTRACT(challenge_rating, r'^(\\d+)') AS INT64) >= 10
            ORDER BY SAFE_CAST(REGEXP_EXTRACT(challenge_rating, r'^(\\d+)') AS INT64) DESC
            """
        },
        {
            "name": "Monsters with Fire Immunity",
            "sql": f"SELECT name, damage_immunities FROM `{table_ref}` WHERE damage_immunities LIKE '%Fire%'"
        }
    ]
    
    print("\n🔍 Running test queries:")
    print("=" * 50)
    
    for query_info in test_queries:
        print(f"\n{query_info['name']}:")
        try:
            results = client.query(query_info['sql']).result()
            for row in results:
                print(f"  - {dict(row)}")
        except Exception as e:
            print(f"  ❌ Error: {e}")

if __name__ == "__main__":
    print("📊 Loading Sample Monster Data")
    print("=" * 50)
    
    success = load_sample_data()
    
    if success:
        print("\n🎉 Sample data loaded successfully!")
        
        # Ask if they want to run test queries
        run_tests = input("\n🔍 Run test queries to verify data? (y/n): ").lower().strip()
        if run_tests == 'y':
            test_queries()
        
        print("\n✅ Your BigQuery table is ready!")
        print("Next steps:")
        print("  1. Open BigQuery Console: https://console.cloud.google.com/bigquery")
        print("  2. Navigate to your project > dnd_data > monsters")
        print("  3. Try running your own queries")
        print("  4. Set up your data pipeline to load more monsters")
        
    else:
        print("\n❌ Failed to load sample data")
        print("Check the errors above and try again") 