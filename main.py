"""
Main entry point for the Dungeon Master's Oracle
This file serves as the entry point for Cloud Run deployment
"""

import os
import sys

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    # Import and run the FastAPI application
    from api.main import app
    
    if __name__ == "__main__":
        import uvicorn
        port = int(os.environ.get("PORT", 8080))
        print(f"Starting Dungeon Master's Oracle on port {port}")
        uvicorn.run(app, host="0.0.0.0", port=port)
        
except Exception as e:
    print(f"Error starting application: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1) 