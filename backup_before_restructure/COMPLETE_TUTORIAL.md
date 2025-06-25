# 🧙‍♂️ Complete Beginner's Tutorial - Dungeon Master's Oracle

Welcome! This tutorial will guide you through every aspect of the Dungeon Master's Oracle project, from understanding what each file does to getting everything running perfectly. No prior experience with Docker or cloud platforms required!

## 📚 Table of Contents

1. [What is This Project?](#what-is-this-project)
2. [Understanding the Project Structure](#understanding-the-project-structure)
3. [Docker Basics for Beginners](#docker-basics-for-beginners)
4. [Step-by-Step Setup Guide](#step-by-step-setup-guide)
5. [Testing and Using the System](#testing-and-using-the-system)
6. [Troubleshooting Common Issues](#troubleshooting-common-issues)

---

## 🎯 What is This Project?

The **Dungeon Master's Oracle** is an AI-powered assistant for Dungeons & Dragons game masters. Think of it as having a super-smart D&D expert that can:

- **Answer questions about monster stats**: "What's a Beholder's armor class?"
- **Explain game rules**: "How does grappling work in D&D 5e?"
- **Generate creative stories**: "Describe a spooky haunted tavern"
- **Access both databases and text**: It intelligently knows whether to search a database or text documents

### 🏗️ How It Works (Technical Overview)

```
User asks question → AI Router decides → Either:
                                       ├── Database Query (for monster stats)
                                       └── Text Search (for rules/lore)
                                    ↓
                           AI generates final answer
```

---

## 📁 Understanding the Project Structure

Let's walk through every file and folder so you understand what each piece does:

### 🗂️ **Root Directory Files**

```
dm-oracle/
├── 📄 README.md              # Project overview
├── 📄 QUICKSTART.md          # Quick setup guide  
├── 📄 COMPLETE_TUTORIAL.md   # This file!
├── 📄 .gitignore             # Files Git should ignore
├── 📄 .env                   # Your configuration (API keys, project settings)
├── 📄 config.yaml            # Application settings
├── 📄 docker-compose.yml     # Docker setup for easy local development
├── 📄 Makefile               # Shortcuts for common commands
├── 📄 cloudbuild.yaml        # Google Cloud deployment instructions
└── 📄 create_config.py       # Script to create missing config files
```

**What each file does:**
- **`.env`**: Your secret configuration (like API keys and project ID)
- **`docker-compose.yml`**: Instructions for Docker to run everything locally
- **`Makefile`**: Shortcuts like `make run` instead of typing long commands
- **`config.yaml`**: Application settings (ports, timeouts, etc.)

### 🏗️ **infrastructure/** - Cloud Infrastructure

```
infrastructure/
├── 📄 main.tf               # Main Terraform setup
├── 📄 variables.tf          # Input variables (what you can customize)
├── 📄 iam.tf                # User permissions and security
├── 📄 storage.tf            # Database and file storage
├── 📄 compute.tf            # Server and container setup  
├── 📄 secrets.tf            # Secure storage for API keys
├── 📄 outputs.tf            # Information after deployment
└── 📄 terraform.tfvars      # Your specific settings
```

**What this does:**
- **Terraform** is like a blueprint for cloud resources
- These files tell Google Cloud: "Create a database, storage, and servers for me"
- You run this once to set up your cloud infrastructure

### 📊 **data-pipelines/** - Data Collection

```
data-pipelines/
├── 📄 README.md
├── 📄 requirements.txt      # Python packages needed
└── dags/
    └── 📄 dnd_data_ingestion.py  # Script to collect D&D data
```

**What this does:**
- **Scrapes D&D websites** to get rules and monster data
- **Cleans the data** and stores it in your database
- **Apache Airflow** runs these scripts automatically

### 🧠 **src/** - The Main Application

```
src/
├── 📄 requirements.txt      # Python packages for the app
├── rag_engine/             # The AI "brain"
│   ├── 📄 __init__.py
│   ├── 📄 router.py         # Decides: database vs text search?
│   ├── 📄 retrievers.py     # Gets data from database/text
│   └── 📄 hybrid_rag.py     # Main AI orchestrator
└── api/                    # Web API (how users interact)
    ├── 📄 main.py           # Web server
    └── 📄 models.py         # Data structures
```

**What each AI file does:**
- **`router.py`**: AI that decides "Is this question about monster stats or game rules?"
- **`retrievers.py`**: Gets data from either the database or text documents
- **`hybrid_rag.py`**: The main brain that coordinates everything
- **`api/main.py`**: The web server that receives questions and sends answers

### 🐳 **docker/** - Containerization

```
docker/
├── 📄 Dockerfile          # Instructions to build the app container
└── 📄 .dockerignore       # Files to exclude from container
```

### 🧪 **tests/** - Quality Assurance

```
tests/
├── 📄 __init__.py
├── 📄 test_api.py          # Tests for the web API
└── 📄 requirements.txt     # Testing tools
```

---

## 🐳 Docker Basics for Beginners

### What is Docker?

Think of Docker like a **shipping container** for your software:

- **Traditional way**: Install Python, install packages, hope it works on your computer
- **Docker way**: Everything packaged together in a "container" that works everywhere

### Key Docker Concepts

1. **Image**: A blueprint (like a recipe)
2. **Container**: A running instance of an image (like a cake made from the recipe)
3. **Dockerfile**: Instructions to build an image
4. **docker-compose**: Tool to run multiple containers together

### Our Docker Setup

```yaml
# docker-compose.yml does this:
1. Builds our app from the Dockerfile
2. Sets up environment variables  
3. Exposes port 8080 for web access
4. Mounts your code so you can edit it live
```

### Docker Commands You'll Use

```bash
# See what's running
docker ps

# Build and start everything
docker-compose up --build

# Stop everything
docker-compose down

# See logs
docker-compose logs dm-oracle

# Start in background
docker-compose up -d
```

---

## 🚀 Step-by-Step Setup Guide

### Phase 1: Prerequisites Check

Let's check if you have everything installed:

#### 1. Check Python
```bash
python --version
# Should show Python 3.11 or higher
```

#### 2. Install Docker Desktop
- **Windows/Mac**: Download from [docker.com](https://www.docker.com/products/docker-desktop)
- **Linux**: Follow instructions for your distribution

#### 3. Verify Docker Works
```bash
docker --version
docker-compose --version
```

#### 4. Get a Google Cloud Account
- Go to [cloud.google.com](https://cloud.google.com)
- Create a free account (comes with $300 credit)
- Create a new project

#### 5. Get a Gemini API Key
- Go to [ai.google.dev](https://ai.google.dev)
- Get your free API key for Gemini

### Phase 2: Configuration Setup

#### Step 1: Configure Your Environment
```bash
# 1. Open your .env file in any text editor
# 2. Update these values:

PROJECT_ID=your-actual-gcp-project-id      # From Google Cloud Console
DATA_BUCKET=your-unique-bucket-name        # Must be globally unique
GOOGLE_API_KEY=your-actual-gemini-api-key  # From ai.google.dev
```

**Real example:**
```bash
PROJECT_ID=my-dm-oracle-2024
DATA_BUCKET=my-dm-oracle-data-bucket-unique-123
GOOGLE_API_KEY=AIzaSyC7...your-actual-key-here
```

#### Step 2: Understand What Each Setting Does
```bash
PROJECT_ID          # Your Google Cloud project (like a workspace)
DATASET_ID          # Name of your database (keep as "dnd_data")
TABLE_ID            # Name of monster table (keep as "monsters")  
DATA_BUCKET         # Storage for files (must be globally unique)
GOOGLE_API_KEY      # Your AI API key (from Google AI Studio)
ENVIRONMENT         # development, staging, or production
APP_VERSION         # Version number (keep as "1.0.0")
DEBUG               # Shows extra information (keep as "true")
LOG_LEVEL           # How much logging (keep as "INFO")
```

### Phase 3: Choose Your Running Method

You have 3 options. Pick the one that seems easiest for you:

#### 🎯 **Option A: Docker (Recommended for Beginners)**

**Why Docker?** Everything is packaged together. You don't need to install Python packages or worry about conflicts.

```bash
# 1. Make sure your .env file is configured
# 2. Start everything
docker-compose up --build

# This will:
# - Download Python and all packages
# - Build the application
# - Start the web server
# - Show you logs in real time
```

**What you'll see:**
```
dm-oracle_1  | ✅ RAG engine initialized successfully
dm-oracle_1  | 🌟 Dungeon Master's Oracle is ready! 
dm-oracle_1  | INFO:     Uvicorn running on http://0.0.0.0:8080
```

#### 🎯 **Option B: Local Python (For Developers)**

```bash
# 1. Install Python packages
python -m pip install -r src/requirements.txt

# 2. Start the server
cd src
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8080
```

#### 🎯 **Option C: Using Make Commands (Easiest)**

```bash
# See all available commands
make help

# Install everything and run
make start

# Or step by step:
make install    # Install Python packages
make run        # Start the server
```

### Phase 4: Verify Everything Works

#### 1. Check Health
Open your browser to: http://localhost:8080/health

You should see:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0"
}
```

#### 2. View Interactive Documentation
Go to: http://localhost:8080/docs

This shows you all available endpoints and lets you test them!

---

## 🧪 Testing and Using the System

### Understanding the Two Types of Questions

The Oracle handles two types of questions differently:

#### 🗄️ **Structured Questions** (Database Queries)
These ask for specific facts about monsters:
- "What is a Beholder's armor class?"
- "List all dragons with CR above 10"
- "Show me monsters with fire resistance"

**How it works:**
1. AI recognizes this needs database lookup
2. Generates SQL query to search monster database
3. Returns specific stats and numbers

#### 📖 **Unstructured Questions** (Rule/Lore Searches)
These ask about game mechanics or story elements:
- "How does grappling work in D&D 5e?"
- "What are the rules for spellcasting?"
- "Explain advantage and disadvantage"

**How it works:**
1. AI recognizes this needs text search
2. Searches through D&D rule documents
3. Returns explanations and descriptions

### 🧪 Testing Different Query Types

#### Test 1: Health Check
```bash
curl http://localhost:8080/health
```

#### Test 2: Monster Stats (Structured)
```bash
curl -X POST "http://localhost:8080/query" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "What is a Beholder'\''s armor class?",
       "session_id": "test_session"
     }'
```

**Expected response:**
```json
{
  "answer": "A Beholder has an Armor Class of 18 (Natural Armor)...",
  "route": "structured",
  "sources": ["D&D Monster Database"],
  "retrieval_success": true
}
```

#### Test 3: Game Rules (Unstructured)
```bash
curl -X POST "http://localhost:8080/query" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "How does grappling work in D&D 5e?",
       "session_id": "test_session"
     }'
```

#### Test 4: Creative Story Generation
```bash
curl -X POST "http://localhost:8080/narrate" \
     -H "Content-Type: application/json" \
     -d '{
       "prompt": "Describe a spooky, abandoned tavern in a haunted forest",
       "style": "mysterious"
     }'
```

### 🎮 Using the Web Interface

#### Interactive API Documentation
1. Go to http://localhost:8080/docs
2. Click on any endpoint (like `/query`)
3. Click "Try it out"
4. Enter your question
5. Click "Execute"
6. See the response!

#### Example Questions to Try

**Monster Questions:**
- "What's a dragon's challenge rating?"
- "Show me all undead creatures"
- "Which monster has the highest AC?"

**Rule Questions:**
- "How do spell slots work?"
- "What's the difference between a spell attack and weapon attack?"
- "Explain how initiative works in combat"

**Story Prompts:**
- "Describe a mysterious ancient library"
- "Create a dramatic battle scene"
- "Describe a peaceful elven village"

### 📊 Understanding the Responses

Every response includes:

```json
{
  "answer": "The actual answer to your question",
  "route": "structured or unstructured", 
  "sources": ["Where the info came from"],
  "retrieval_success": true,
  "session_id": "your_session",
  "metadata": {
    "query_type": "structured",
    "processing_time_ms": 1250
  }
}
```

**What each field means:**
- **`answer`**: The AI's response to your question
- **`route`**: Whether it used the database ("structured") or text search ("unstructured")
- **`sources`**: Where the information came from
- **`retrieval_success`**: Whether it found relevant information
- **`metadata`**: Extra info like how long it took

---

## 🆘 Troubleshooting Common Issues

### 🔧 **Issue: "RAG engine not initialized"**

**What this means:** The AI system couldn't start properly.

**Solutions:**
1. **Check your .env file:**
   ```bash
   # Make sure these are set:
   PROJECT_ID=your-actual-project-id
   GOOGLE_API_KEY=your-actual-api-key
   ```

2. **Verify your API key works:**
   - Go to [ai.google.dev](https://ai.google.dev)
   - Test your API key there first

3. **Check authentication:**
   ```bash
   gcloud auth list
   # Should show your Google account
   ```

### 🔧 **Issue: Docker won't start**

**Solutions:**
1. **Make sure Docker Desktop is running**
2. **Check for port conflicts:**
   ```bash
   # Kill anything using port 8080
   docker-compose down
   ```
3. **Rebuild everything:**
   ```bash
   docker-compose down
   docker-compose up --build
   ```

### 🔧 **Issue: "Permission denied" errors**

**On Windows:**
- Run PowerShell as Administrator
- Make sure Docker Desktop has proper permissions

**On Mac/Linux:**
```bash
# Fix file permissions
chmod +x scripts/setup.sh
```

### 🔧 **Issue: Python package installation fails**

**Solution:**
```bash
# Update pip first
python -m pip install --upgrade pip

# Install packages one by one to see which fails
python -m pip install fastapi
python -m pip install langchain
```

### 🔧 **Issue: "No module named..." errors**

**This means Python can't find the packages.**

**Solutions:**
1. **Make sure you're in the right directory:**
   ```bash
   cd src
   python -m uvicorn api.main:app --reload
   ```

2. **Check your virtual environment:**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate it (Windows)
   venv\Scripts\activate
   
   # Activate it (Mac/Linux)  
   source venv/bin/activate
   
   # Install packages
   pip install -r requirements.txt
   ```

### 🔧 **Issue: API returns errors**

**Check the logs:**
```bash
# If using Docker
docker-compose logs dm-oracle

# If running locally, check the terminal where you started the server
```

**Common fixes:**
1. **Restart the server**
2. **Check your .env configuration**
3. **Make sure you have internet connection for AI API calls**

### 🔧 **Issue: Slow responses**

**This is normal for AI systems!** Each question takes time because:
1. AI has to understand your question
2. Search through databases or documents  
3. Generate a thoughtful response

**Typical response times:**
- Simple questions: 2-5 seconds
- Complex questions: 5-15 seconds  
- Story generation: 10-30 seconds

---

## 🎓 Advanced Usage Tips

### 🎯 **Getting Better Responses**

#### For Monster Questions:
- Be specific: "Beholder's AC" vs "What is a Beholder's armor class?"
- Use proper D&D terms: "CR" instead of "difficulty"
- Ask for comparisons: "Which dragon has higher HP, red or blue?"

#### For Rule Questions:  
- Mention the edition: "in D&D 5e"
- Be specific: "grappling rules" vs "how does grappling work step by step?"
- Ask for examples: "explain with an example"

#### For Story Generation:
- Set the mood: "spooky", "epic", "mysterious"
- Include details: "abandoned tavern in a haunted forest"
- Specify the style: Use the style parameter ("mysterious", "action", "dramatic")

### 🔄 **Development Workflow**

If you want to modify the code:

1. **Edit files in `src/`**
2. **If using Docker:** The changes are automatically reflected (volume mounting)
3. **If running locally:** Restart with `--reload` flag for auto-reloading
4. **Test your changes:** Use the `/docs` interface
5. **Run tests:** `make test` or `pytest tests/`

### 📈 **Scaling Up**

When you're ready for production:

1. **Deploy to Google Cloud:**
   ```bash
   # Set up infrastructure
   cd infrastructure
   terraform init
   terraform apply
   
   # Deploy the app
   make deploy
   ```

2. **Monitor performance:**
   - Check Cloud Run logs in Google Cloud Console
   - Monitor API response times
   - Set up alerts for errors

3. **Add more data:**
   - Run the Airflow data pipelines
   - Add custom D&D content
   - Expand the monster database

---

## 🎉 Congratulations!

You now have a fully functional AI-powered D&D assistant! Here's what you've accomplished:

✅ **Built a sophisticated AI system** that can answer both factual and creative questions  
✅ **Learned Docker basics** and can run containerized applications  
✅ **Understood microservices architecture** with separate AI, API, and data components  
✅ **Set up a production-ready system** that can scale to handle many users  
✅ **Created an interactive web API** with automatic documentation  

### 🧙‍♂️ **Your D&D Oracle Can:**
- Answer any question about monster stats instantly
- Explain complex D&D rules clearly  
- Generate immersive story content
- Handle multiple users simultaneously
- Scale automatically based on demand
- Maintain conversation context with session IDs

### 🚀 **Next Steps:**
1. **Experiment** with different types of questions
2. **Share** with your D&D group and get feedback  
3. **Customize** by adding your own homebrew content
4. **Scale up** by deploying to the cloud
5. **Contribute** improvements back to the project

**Happy adventuring, Dungeon Master!** 🐉⚔️✨

---

## 📚 Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com
- **Docker Tutorial**: https://docs.docker.com/get-started/
- **LangChain Docs**: https://python.langchain.com/docs/
- **Google Cloud Platform**: https://cloud.google.com/docs
- **D&D 5e SRD**: https://www.5esrd.com/

---

*Need help? Check the troubleshooting section above or create an issue in the project repository!*