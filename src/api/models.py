"""Pydantic Models for API Request/Response Schemas."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class NarrativeStyle(str, Enum):
    """Available narrative styles."""
    DESCRIPTIVE = "descriptive"
    ACTION = "action"
    MYSTERIOUS = "mysterious"
    DRAMATIC = "dramatic"


class QueryRequest(BaseModel):
    """Request model for the main query endpoint."""
    query: str = Field(
        ...,
        description="The D&D-related question to ask the Oracle",
        example="What is a Beholder's armor class?"
    )
    session_id: Optional[str] = Field(
        default=None,
        description="Optional session identifier",
        example="session_123456"
    )


class NarrateRequest(BaseModel):
    """Request model for narrative generation."""
    prompt: str = Field(
        ...,
        description="Creative prompt for narrative generation",
        example="Describe a spooky, abandoned tavern"
    )
    style: NarrativeStyle = Field(
        default=NarrativeStyle.DESCRIPTIVE,
        description="Narrative style"
    )


class QueryResponse(BaseModel):
    """Response model for queries."""
    answer: str = Field(..., description="The Oracle's response")
    route: str = Field(..., description="Routing decision (structured/unstructured)")
    sources: List[str] = Field(..., description="Sources used")
    retrieval_success: bool = Field(..., description="Whether retrieval succeeded")
    session_id: Optional[str] = Field(default=None, description="Session ID")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Query metadata")


class NarrateResponse(BaseModel):
    """Response model for narrative generation."""
    text: str = Field(..., description="Generated narrative content")
    style: str = Field(..., description="Narrative style used")
    success: bool = Field(..., description="Whether generation succeeded")
    error: Optional[str] = Field(default=None, description="Error message if failed")


class HealthResponse(BaseModel):
    """Response model for health checks."""
    status: str = Field(..., description="Overall health status")
    timestamp: str = Field(..., description="Health check timestamp")
    version: Optional[str] = Field(default=None, description="App version")
    components: Optional[Dict[str, Any]] = Field(default=None, description="Component health")