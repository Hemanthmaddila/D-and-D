"""
Basic API tests for the Dungeon Master's Oracle
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from api.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def mock_rag_engine():
    """Mock RAG engine for testing."""
    mock_engine = Mock()
    mock_engine.query.return_value = {
        "answer": "A Beholder has an Armor Class of 18 (Natural Armor).",
        "route": "structured",
        "sources": ["D&D Monster Database"],
        "retrieval_success": True,
        "session_id": "test_session",
        "metadata": {"query_type": "structured"}
    }
    mock_engine.narrate.return_value = {
        "text": "The old tavern stood silent in the moonlight...",
        "style": "mysterious",
        "success": True
    }
    return mock_engine


def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert "timestamp" in data
    assert "version" in data


def test_root_endpoint(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["service"] == "Dungeon Master's Oracle"
    assert "endpoints" in data
    assert data["status"] == "operational"


@patch('api.main.rag_engine')
def test_query_endpoint_structured(mock_engine_global, client, mock_rag_engine):
    """Test the query endpoint with a structured query."""
    mock_engine_global.__bool__ = Mock(return_value=True)
    
    with patch('api.main.get_rag_engine', return_value=mock_rag_engine):
        response = client.post(
            "/query",
            json={
                "query": "What is a Beholder's armor class?",
                "session_id": "test_session"
            }
        )
    
    assert response.status_code == 200
    
    data = response.json()
    assert "answer" in data
    assert "route" in data
    assert "sources" in data
    assert data["retrieval_success"] is True


@patch('api.main.rag_engine')
def test_query_endpoint_unstructured(mock_engine_global, client, mock_rag_engine):
    """Test the query endpoint with an unstructured query."""
    mock_engine_global.__bool__ = Mock(return_value=True)
    
    # Update mock for unstructured response
    mock_rag_engine.query.return_value = {
        "answer": "Grappling is a special melee attack...",
        "route": "unstructured",
        "sources": ["D&D SRD"],
        "retrieval_success": True,
        "session_id": "test_session",
        "metadata": {"query_type": "unstructured"}
    }
    
    with patch('api.main.get_rag_engine', return_value=mock_rag_engine):
        response = client.post(
            "/query",
            json={
                "query": "How does grappling work in D&D?",
                "session_id": "test_session"
            }
        )
    
    assert response.status_code == 200
    
    data = response.json()
    assert data["route"] == "unstructured"
    assert "D&D SRD" in data["sources"]


@patch('api.main.rag_engine')
def test_narrate_endpoint(mock_engine_global, client, mock_rag_engine):
    """Test the narrative generation endpoint."""
    mock_engine_global.__bool__ = Mock(return_value=True)
    
    with patch('api.main.get_rag_engine', return_value=mock_rag_engine):
        response = client.post(
            "/narrate",
            json={
                "prompt": "Describe a spooky tavern",
                "style": "mysterious"
            }
        )
    
    assert response.status_code == 200
    
    data = response.json()
    assert "text" in data
    assert data["style"] == "mysterious"
    assert data["success"] is True


def test_query_endpoint_validation_error(client):
    """Test query endpoint with invalid input."""
    response = client.post(
        "/query",
        json={
            "invalid_field": "test"
        }
    )
    
    assert response.status_code == 422  # Validation error


def test_query_endpoint_without_rag_engine(client):
    """Test query endpoint when RAG engine is not initialized."""
    with patch('api.main.rag_engine', None):
        response = client.post(
            "/query",
            json={
                "query": "What is a Beholder's armor class?"
            }
        )
    
    assert response.status_code == 503  # Service unavailable


@pytest.mark.parametrize("style", ["descriptive", "action", "mysterious", "dramatic"])
def test_narrate_styles(client, style, mock_rag_engine):
    """Test different narrative styles."""
    mock_rag_engine.narrate.return_value = {
        "text": f"Generated text in {style} style...",
        "style": style,
        "success": True
    }
    
    with patch('api.main.rag_engine', mock_rag_engine), \
         patch('api.main.get_rag_engine', return_value=mock_rag_engine):
        response = client.post(
            "/narrate",
            json={
                "prompt": "Test prompt",
                "style": style
            }
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["style"] == style 