"""
Main FastAPI Application for the Dungeon Master's Oracle

This module implements the high-performance, async API server that exposes
the hybrid RAG functionality through RESTful endpoints.
"""

import os
import time
import asyncio
from datetime import datetime
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file - try multiple locations
# First try from project root (when running from src/)
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
if not os.path.exists(env_path):
    # Try from current directory (when running from project root)
    env_path = '.env'

load_dotenv(env_path)

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from .models import (
    QueryRequest, QueryResponse,
    NarrateRequest, NarrateResponse,
    HealthResponse
)

# Import the RAG engine
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from rag_engine import HybridRAGEngine

# Configuration from environment variables
PROJECT_ID = os.getenv("PROJECT_ID", "your-project-id")
DATASET_ID = os.getenv("DATASET_ID", "dnd_data")
TABLE_ID = os.getenv("TABLE_ID", "monsters")
DATA_BUCKET = os.getenv("DATA_BUCKET", "your-data-bucket")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

# Initialize FastAPI app
app = FastAPI(
    title="Dungeon Master's Oracle",
    description="A hybrid RAG system for D&D Dungeon Masters providing intelligent answers about rules, lore, and monster statistics.",
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global RAG engine instance (initialized on startup)
rag_engine: HybridRAGEngine = None


async def get_rag_engine() -> HybridRAGEngine:
    """
    Dependency to get the RAG engine instance.
    Ensures the engine is initialized before handling requests.
    """
    if rag_engine is None:
        raise HTTPException(
            status_code=503,
            detail="RAG engine not initialized. Please check service health."
        )
    return rag_engine


@app.on_event("startup")
async def startup_event():
    """
    Initialize the RAG engine and other startup tasks.
    This runs once when the FastAPI application starts.
    """
    global rag_engine
    
    try:
        print("Initializing Dungeon Master's Oracle...")
        
        # Validate required environment variables
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        # Initialize the hybrid RAG engine
        rag_engine = HybridRAGEngine(
            project_id=PROJECT_ID,
            dataset_id=DATASET_ID,
            table_id=TABLE_ID,
            data_bucket=DATA_BUCKET,
            api_key=GOOGLE_API_KEY
        )
        
        print("✅ RAG engine initialized successfully")
        print(f"🌟 Dungeon Master's Oracle is ready! (Environment: {ENVIRONMENT})")
        
    except Exception as e:
        print(f"❌ Failed to initialize RAG engine: {e}")
        # In production, you might want to exit here
        # For development, we'll continue and handle errors in endpoints


@app.on_event("shutdown")
async def shutdown_event():
    """
    Cleanup tasks when the application shuts down.
    """
    print("🛑 Shutting down Dungeon Master's Oracle...")
    # Add any cleanup logic here (close database connections, etc.)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint for monitoring and load balancer probes.
    
    Returns the overall health status of the service and its components.
    """
    try:
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        # Basic health check
        if rag_engine is None:
            return HealthResponse(
                status="unhealthy",
                timestamp=timestamp,
                version=APP_VERSION
            )
        
        # Detailed health check (optional - can be expensive)
        # Uncomment for production monitoring
        # health_status = await rag_engine.health_check()
        
        return HealthResponse(
            status="healthy",
            timestamp=timestamp,
            version=APP_VERSION,
            components={
                "rag_engine": {"status": "healthy"},
                "environment": ENVIRONMENT
            }
        )
        
    except Exception as e:
        return HealthResponse(
            status="unhealthy",
            timestamp=datetime.utcnow().isoformat() + "Z",
            version=APP_VERSION,
            components={"error": str(e)}
        )


@app.post("/query", response_model=QueryResponse)
async def query_oracle(
    request: QueryRequest,
    engine: HybridRAGEngine = Depends(get_rag_engine)
) -> QueryResponse:
    """
    Main query endpoint for the Dungeon Master's Oracle.
    
    This endpoint uses the hybrid RAG system to intelligently route queries
    to either structured (BigQuery) or unstructured (vector search) data sources
    and provides comprehensive answers about D&D rules, lore, and monster statistics.
    
    **Example structured queries:**
    - "What is a Beholder's armor class?"
    - "List all dragons with CR above 10"
    - "Show me monsters with resistance to fire damage"
    
    **Example unstructured queries:**
    - "How does grappling work in D&D 5e?"
    - "Explain the difference between a spell attack and a weapon attack"
    - "What are the rules for multiclassing?"
    """
    try:
        start_time = time.time()
        
        # Process the query through the hybrid RAG system
        result = await engine.query(
            question=request.query,
            session_id=request.session_id
        )
        
        # Add processing time to metadata
        processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        if result.get("metadata"):
            result["metadata"]["processing_time_ms"] = round(processing_time, 2)
        else:
            result["metadata"] = {"processing_time_ms": round(processing_time, 2)}
        
        return QueryResponse(**result)
        
    except Exception as e:
        print(f"Error in query endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing your query: {str(e)}"
        )


@app.post("/narrate", response_model=NarrateResponse)
async def generate_narrative(
    request: NarrateRequest,
    engine: HybridRAGEngine = Depends(get_rag_engine)
) -> NarrateResponse:
    """
    Creative narrative generation endpoint for D&D storytelling.
    
    This endpoint generates immersive, descriptive content for D&D scenarios
    using advanced prompt engineering and persona-based generation.
    
    **Supported styles:**
    - `descriptive`: Rich, atmospheric descriptions (default)
    - `action`: Fast-paced, dynamic scenes
    - `mysterious`: Eerie, suspenseful content
    - `dramatic`: Epic, emotionally charged moments
    
    **Example prompts:**
    - "Describe a spooky, abandoned tavern in a haunted forest"
    - "Create an epic battle scene between dragons and adventurers"
    - "Describe the throne room of an ancient lich king"
    """
    try:
        # Generate narrative content using the RAG engine
        result = await engine.narrate(
            prompt=request.prompt,
            style=request.style.value
        )
        
        return NarrateResponse(**result)
        
    except Exception as e:
        print(f"Error in narrate endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while generating narrative: {str(e)}"
        )


@app.get("/")
async def root():
    """
    Root endpoint providing basic information about the API.
    """
    return {
        "service": "Dungeon Master's Oracle",
        "version": APP_VERSION,
        "description": "A hybrid RAG system for D&D Dungeon Masters",
        "environment": ENVIRONMENT,
        "endpoints": {
            "query": "/query - Ask questions about D&D rules, lore, and monsters",
            "narrate": "/narrate - Generate creative D&D narrative content", 
            "health": "/health - Service health check",
            "docs": "/docs - Interactive API documentation"
        },
        "status": "operational"
    }


# Custom exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom handler for HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Custom handler for general exceptions."""
    print(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "An unexpected error occurred",
            "status_code": 500,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    )


# For local development
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    ) 