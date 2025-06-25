#!/usr/bin/env python3
"""
Complete BigQuery setup for D&D Monsters
Runs table creation and sample data loading in one go
"""

import os
import sys

def main():
    print("🎲 D&D Monsters BigQuery Setup")
    print("=" * 50)
    
    # Check environment
    project_id = os.getenv("PROJECT_ID", "dandd-oracle")
    print(f"📍 Using project: {project_id}")
    
    if project_id == "dandd-oracle":
        print("✅ Using your configured project ID")
    else:
        print("⚠️  Make sure PROJECT_ID is set in your .env file")
    
    print("\n🏗️  Step 1: Creating BigQuery table...")
    
    try:
        # Import and run table creation
        from create_table import create_monsters_table
        table = create_monsters_table()
        print("✅ Table creation completed!")
        
    except Exception as e:
        print(f"❌ Failed to create table: {e}")
        print("\nTroubleshooting:")
        print("  1. Run: gcloud auth application-default login")
        print("  2. Check your .env file has PROJECT_ID set")
        print("  3. Make sure BigQuery API is enabled")
        return False
    
    print("\n📊 Step 2: Loading sample data...")
    
    try:
        # Import and run data loading
        from load_sample_data import load_sample_data
        success = load_sample_data()
        
        if success:
            print("✅ Sample data loaded!")
        else:
            print("⚠️  Sample data loading had issues (check above)")
            
    except Exception as e:
        print(f"❌ Failed to load sample data: {e}")
        return False
    
    print("\n🎉 BigQuery setup complete!")
    print("=" * 50)
    print("Your D&D monsters table is ready!")
    print(f"\n🌐 View in BigQuery Console:")
    print(f"https://console.cloud.google.com/bigquery?project={project_id}")
    print(f"\n📋 Table location:")
    print(f"{project_id}.dnd_data.monsters")
    
    print("\n🔍 Quick test query:")
    print("SELECT name, type, challenge_rating FROM `{}.dnd_data.monsters`".format(project_id))
    
    print("\n✨ Next steps:")
    print("  1. Try the test query in BigQuery Console")
    print("  2. Run your data pipeline to load more monsters")
    print("  3. Test your RAG system queries")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 