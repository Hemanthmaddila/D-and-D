# 🐳 Docker Beginner's Guide - Dungeon Master's Oracle

This guide is specifically for beginners who want to understand and run the DM Oracle project using Docker. No prior Docker experience needed!

## 🎯 Why Docker for This Project?

**The Problem Docker Solves:**
- Installing Python, packages, databases locally can be messy
- "It works on my machine" but not on yours
- Complex setup with many moving parts

**The Docker Solution:**
- Everything packaged in "containers" that work anywhere
- One command to start the entire system
- No need to install Python packages manually

## 🧠 Understanding Our Project Through Docker

### What Our System Looks Like

```
┌─────────────────────────────────────────────────────────┐
│                 Your Computer                           │
│  ┌─────────────────────────────────────────────────┐   │
│  │              Docker Container                   │   │
│  │  ┌─────────────────────────────────────────┐   │   │
│  │  │         DM Oracle Application           │   │   │
│  │  │                                         │   │   │
│  │  │  ┌─────────┐  ┌──────────┐  ┌────────┐ │   │   │
│  │  │  │   AI    │  │   API    │  │  Web   │ │   │   │
│  │  │  │ Engine  │  │ Server   │  │ Server │ │   │   │
│  │  │  └─────────┘  └──────────┘  └────────┘ │   │   │
│  │  └─────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
        ↑                                    ↑
   Port 8080                          Your Browser
   (Internal)                      http://localhost:8080
```

### Key Files for Docker

1. **`Dockerfile`** - Recipe to build our application
2. **`docker-compose.yml`** - Instructions to run everything together
3. **`.env`** - Your configuration (API keys, settings)

## 📋 Prerequisites 

### Step 1: Install Docker Desktop

**Windows:**
1. Go to [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2. Download "Docker Desktop for Windows"
3. Run the installer
4. Restart your computer
5. Start Docker Desktop (you'll see a whale icon in your system tray)

**Mac:**
1. Go to [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2. Download "Docker Desktop for Mac"
3. Drag to Applications folder
4. Start Docker Desktop

**Verification:**
Open PowerShell/Terminal and run:
```bash
docker --version
docker-compose --version
```

You should see version numbers, not errors.

### Step 2: Get Your API Keys

You need a **Google Gemini API Key**:

1. Go to [ai.google.dev](https://ai.google.dev)
2. Click "Get API Key"
3. Sign in with Google account
4. Create a new API key
5. Copy the key (starts with "AIza...")

**Keep this safe!** You'll need it in the next step.

## 🔧 Project Setup

### Step 1: Configure Your Environment

Open the `.env` file in any text editor (Notepad, VS Code, etc.) and update:

```bash
# Replace these with your actual values:
PROJECT_ID=my-dm-oracle-project-2024        # Any unique name
DATA_BUCKET=my-dm-oracle-bucket-unique-123  # Must be globally unique
GOOGLE_API_KEY=AIzaSyC...your-actual-key   # From ai.google.dev

# Keep these as they are:
DATASET_ID=dnd_data
TABLE_ID=monsters
ENVIRONMENT=development
APP_VERSION=1.0.0
DEBUG=true
LOG_LEVEL=INFO
```

**Important Notes:**
- `PROJECT_ID`: Can be any name you like (lowercase, hyphens okay)
- `DATA_BUCKET`: Must be globally unique across all of Google Cloud
- `GOOGLE_API_KEY`: Your actual API key from Google AI Studio

### Step 2: Understanding Docker Compose

Our `docker-compose.yml` file does this:

```yaml
version: '3.8'
services:
  dm-oracle:                    # Our application name
    build:
      context: .                # Build from current directory
      dockerfile: docker/Dockerfile  # Using our custom Dockerfile
    ports:
      - "8080:8080"            # Map port 8080 inside container to port 8080 on your computer
    environment:               # Pass our .env variables to the container
      - PROJECT_ID=${PROJECT_ID}
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      # ... more variables
    volumes:
      - ./src:/app/src         # Mount our source code (for live editing)
    command: ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
```

**What this means:**
- **Build**: Create a container with our app
- **Ports**: Make the app accessible at `http://localhost:8080`
- **Environment**: Pass your API keys and settings
- **Volumes**: Let you edit code files and see changes immediately
- **Command**: Start the web server

## 🚀 Running the Project

### Method 1: Docker Compose (Recommended)

**Step 1: Open Terminal/PowerShell**
Navigate to your project folder:
```bash
cd "A:\D and D"
```

**Step 2: Start Everything**
```bash
docker-compose up --build
```

**What happens:**
1. Downloads Python base image (first time only)
2. Installs all Python packages
3. Copies your code into the container
4. Starts the AI system
5. Starts the web server

**You'll see output like:**
```
dm-oracle_1  | Installing dependencies...
dm-oracle_1  | ✅ RAG engine initialized successfully
dm-oracle_1  | 🌟 Dungeon Master's Oracle is ready!
dm-oracle_1  | INFO:     Uvicorn running on http://0.0.0.0:8080
```

**Step 3: Test It**
Open your browser to: http://localhost:8080/health

### Method 2: Background Mode

If you want to run it in the background:
```bash
docker-compose up -d --build
```

To see logs:
```bash
docker-compose logs -f dm-oracle
```

To stop:
```bash
docker-compose down
```

## 🧪 Testing Your Setup

### 1. Health Check
```bash
curl http://localhost:8080/health
```
Or open in browser: http://localhost:8080/health

**Expected result:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0"
}
```

### 2. Interactive Documentation
Open: http://localhost:8080/docs

This shows you all the available endpoints and lets you test them directly!

### 3. Test a Question

**Using the web interface:**
1. Go to http://localhost:8080/docs
2. Click on `POST /query`
3. Click "Try it out"
4. Enter this:
   ```json
   {
     "query": "What is a Beholder's armor class?",
     "session_id": "test"
   }
   ```
5. Click "Execute"

**Using curl (command line):**
```bash
curl -X POST "http://localhost:8080/query" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "What is a Beholder'\''s armor class?",
       "session_id": "test"
     }'
```

## 🔍 Understanding the Code Files

### Core AI Files (`src/rag_engine/`)

**`router.py`** - The AI Decision Maker
```python
# This AI decides: "Is this question about monster stats or game rules?"
async def route_query(self, question: str):
    # Uses Google Gemini to classify the question
    # Returns either "structured" or "unstructured"
```

**`retrievers.py`** - The Data Fetchers
```python
class StructuredRetriever:
    # Handles monster database queries
    # Converts questions to SQL
    # Example: "Beholder's AC" → "SELECT armor_class FROM monsters WHERE name='Beholder'"

class UnstructuredRetriever:
    # Handles rule/lore searches
    # Searches through D&D text documents
    # Example: "How does grappling work?" → searches SRD documents
```

**`hybrid_rag.py`** - The Main Orchestrator
```python
class HybridRAGEngine:
    async def query(self, question):
        # 1. Route the question (database or text?)
        # 2. Get relevant information
        # 3. Generate final answer
        # 4. Return formatted response
```

### API Files (`src/api/`)

**`main.py`** - The Web Server
```python
@app.post("/query")
async def query_oracle(request: QueryRequest):
    # Receives HTTP requests
    # Calls the AI engine
    # Returns JSON responses
```

**`models.py`** - Data Structures
```python
class QueryRequest(BaseModel):
    query: str          # The user's question
    session_id: str     # Optional conversation tracking

class QueryResponse(BaseModel):
    answer: str         # AI's response
    route: str          # "structured" or "unstructured"
    sources: List[str]  # Where info came from
```

## 🐛 Troubleshooting Docker Issues

### Issue: "Docker daemon not running"
**Solution:** Start Docker Desktop application

### Issue: "Port already in use"
**Solution:** 
```bash
docker-compose down  # Stop any running containers
# Or change port in docker-compose.yml
```

### Issue: "Build failed"
**Check:**
1. Your `.env` file exists and has correct values
2. You're in the right directory
3. Docker has enough disk space

**Debug:**
```bash
# See detailed build output
docker-compose up --build --verbose

# Build just the image
docker build -f docker/Dockerfile -t dm-oracle .
```

### Issue: "Permission denied"
**Windows:** Run PowerShell as Administrator
**Mac/Linux:** 
```bash
sudo docker-compose up --build
```

### Issue: Container keeps restarting
**Check logs:**
```bash
docker-compose logs dm-oracle
```

**Common causes:**
- Missing or invalid `GOOGLE_API_KEY`
- Syntax errors in `.env` file
- Network connectivity issues

## 📈 Docker Commands Cheat Sheet

```bash
# Start everything
docker-compose up --build

# Start in background
docker-compose up -d --build

# Stop everything
docker-compose down

# See what's running
docker ps

# View logs
docker-compose logs dm-oracle

# Follow logs in real time
docker-compose logs -f dm-oracle

# Restart just the app
docker-compose restart dm-oracle

# Rebuild and restart
docker-compose up --build --force-recreate

# Remove everything (clean slate)
docker-compose down --volumes --remove-orphans
docker system prune -f
```

## 🎯 Development Workflow with Docker

### Making Code Changes

1. **Edit files in `src/`** - Your changes are immediately reflected
2. **The server auto-reloads** - No need to restart Docker
3. **Test your changes** - Refresh your browser or make new API calls

### Adding New Python Packages

1. **Edit `src/requirements.txt`**
2. **Rebuild the container:**
   ```bash
   docker-compose up --build
   ```

### Debugging

**Access the container shell:**
```bash
docker-compose exec dm-oracle bash
```

**Check environment variables:**
```bash
docker-compose exec dm-oracle env | grep PROJECT_ID
```

## 🎉 You're Ready!

Congratulations! You now understand:

✅ **What Docker is** and why we use it  
✅ **How our AI system works** through containers  
✅ **How to start and stop** the entire system  
✅ **How to test** the API endpoints  
✅ **How to troubleshoot** common issues  
✅ **How to make changes** to the code  

### Next Steps:

1. **Experiment** with different questions
2. **Read the code** in `src/` to understand how it works
3. **Check out** the interactive docs at http://localhost:8080/docs
4. **Try the narrative generation** endpoint for creative content

**Happy D&D adventures!** 🧙‍♂️🐉⚔️ 