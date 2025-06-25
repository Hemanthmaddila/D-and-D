# Source Code

This directory contains the core implementation of the Dungeon Master's Oracle RAG system.

## Architecture

The application follows a modular architecture with clear separation of concerns:

### Core Components

- **`rag_engine/`** - Hybrid RAG implementation with intelligent routing
- **`api/`** - FastAPI application with async endpoints
- **`utils/`** - Shared utilities and helper functions

### RAG Engine Architecture

```
User Query
    ↓
Router Chain (Gemini)
    ↓
┌─────────────────┬─────────────────┐
│  Structured     │  Unstructured   │
│  Path           │  Path           │
│                 │                 │
│  Text-to-SQL    │  FAISS Vector   │
│  ↓              │  Search         │
│  BigQuery       │  ↓              │
│  Self-Correct   │  MultiQuery     │
│  Loop           │  Retriever      │
└─────────────────┴─────────────────┘
    ↓
Final Generation Chain (Gemini)
    ↓
Response to User
```

## Key Features

### Intelligent Routing
- **Query Classification**: LLM-powered routing between structured and unstructured data
- **Context-Aware**: Understands D&D-specific terminology and intent
- **Fallback Handling**: Graceful degradation when routing is uncertain

### Structured Data Path (Text-to-SQL)
- **Self-Correcting**: Automatic SQL error detection and retry logic
- **Schema-Aware**: Deep understanding of the monster data schema
- **BigQuery Optimized**: Native integration with Google BigQuery

### Unstructured Data Path (Vector Search)
- **FAISS Integration**: High-performance in-memory vector search
- **MultiQuery Enhancement**: Query expansion for comprehensive retrieval
- **Semantic Chunking**: Preserves document structure and context

### Advanced Prompt Engineering
- **Persona-Based**: DM-specific tone and style
- **Few-Shot Learning**: Examples for consistent output quality
- **Context Injection**: Dynamic prompt construction with retrieved data

## Development

### Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your configuration
```

### Environment Variables
- `PROJECT_ID` - GCP project ID
- `GOOGLE_API_KEY` - Gemini API key
- `DATA_BUCKET` - GCS bucket for data storage
- `DATASET_ID` - BigQuery dataset ID
- `TABLE_ID` - BigQuery table ID

### Testing
```bash
# Run unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Run with coverage
pytest --cov=src tests/
```

### Code Quality
```bash
# Format code
black src/

# Lint code
flake8 src/

# Type checking
mypy src/
```

## API Endpoints

- **POST /query** - Main RAG endpoint with hybrid routing
- **POST /narrate** - Creative storytelling endpoint
- **GET /health** - Health check endpoint

## Performance Considerations

- **Async Operations**: All I/O operations use async/await
- **Connection Pooling**: Efficient database connection management
- **Caching**: Strategic caching of embeddings and query results
- **Resource Management**: Proper cleanup of vector stores and connections 