#!/usr/bin/env python3
"""
Quick test to verify environment variables are loading correctly
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("🔍 Environment Variable Check")
print("=" * 40)

# Check all our required variables
env_vars = {
    "PROJECT_ID": os.getenv("PROJECT_ID"),
    "DATASET_ID": os.getenv("DATASET_ID"), 
    "TABLE_ID": os.getenv("TABLE_ID"),
    "DATA_BUCKET": os.getenv("DATA_BUCKET"),
    "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY"),
    "ENVIRONMENT": os.getenv("ENVIRONMENT")
}

for key, value in env_vars.items():
    if value:
        # Hide API key for security
        display_value = value[:10] + "..." if key == "GOOGLE_API_KEY" and len(value) > 10 else value
        print(f"✅ {key}: {display_value}")
    else:
        print(f"❌ {key}: NOT SET")

print("\n🎯 Ready to start server!") 