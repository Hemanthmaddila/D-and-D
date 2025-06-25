# 🎲 The Dungeon Master's Oracle

> **A production-grade, hybrid RAG system for D&D Dungeon Masters**

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Google Cloud](https://img.shields.io/badge/GoogleCloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white)](https://cloud.google.com/)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white)](https://www.terraform.io/)

**The Dungeon Master's Oracle** is an AI-powered assistant that answers D&D questions with intelligent routing between structured monster data and unstructured rules/lore content.

## ✨ **Features**

- 🧠 **Intelligent Query Routing** - Automatically routes queries to structured (BigQuery) or unstructured (vector search) data
- 🗄️ **Monster Database** - Self-correcting Text-to-SQL queries against D&D monster statistics  
- 📖 **Rules & Lore** - Vector search through D&D SRD content
- 🎭 **Creative Generation** - AI-powered narrative generation for storytelling
- ⚡ **High Performance** - Async FastAPI with auto-scaling deployment
- 🔧 **Production Ready** - Complete infrastructure as code with Terraform

## 🚀 **Quick Start**

### **Try It Live**
Visit the deployed API: [Coming Soon - Deploy Your Own!]

### **Run Locally**

1. **Clone the repository**
   ```bash
   git clone https://github.com/Hemanthmaddila/dungeon-masters-oracle.git
   cd dungeon-masters-oracle
   ```

2. **Set up environment**
   ```bash
   python create_config.py  # Creates .env file
   # Edit .env with your Google Cloud project and Gemini API key
   ```

3. **Install dependencies**
   ```bash
   pip install -r src/requirements.txt
   pip install google-cloud-bigquery python-dotenv
   ```

4. **Set up BigQuery database**
   ```bash
   cd sql_schema
   python setup_bigquery.py  # Creates table and loads sample data
   ```

5. **Start the server**
   ```bash
   python -m uvicorn src.api.main:app --reload --host 127.0.0.1 --port 8080
   ```

6. **Test it out**
   - API Docs: http://localhost:8080/docs
   - Health Check: http://localhost:8080/health

## 📊 **Example Queries**

### **Monster Stats** (Structured Queries)
```bash
curl -X POST "http://localhost:8080/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is a Beholder'\''s armor class?"}'

# Response: "A Beholder has an Armor Class (AC) of 18."
```

### **Rules & Mechanics** (Unstructured Queries)  
```bash
curl -X POST "http://localhost:8080/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "How does grappling work in D&D 5e?"}'

# Response: Detailed explanation of grappling mechanics...
```

### **Creative Narratives**
```bash
curl -X POST "http://localhost:8080/narrate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Describe a spooky haunted tavern", "style": "mysterious"}'

# Response: Rich, atmospheric description for your campaign...
```

## 🏗️ **Architecture**

```
User Query → Router (Gemini) → Structured/Unstructured Path → Response Generator
                ↓                        ↓                           ↓
           Query Classification    BigQuery/Vector Search      Formatted Answer
```

- **Query Router**: Gemini-powered classification of user intent
- **Structured Retriever**: Text-to-SQL generation for monster database queries
- **Unstructured Retriever**: FAISS vector search for D&D rules/lore
- **Response Generator**: Context-aware answer formatting

## 🌍 **Deploy to Production**

### **One-Click Deployment**
```bash
python deploy_to_production.py
```

This will:
- 🏗️ Deploy infrastructure with Terraform
- 🐳 Build and deploy with Google Cloud Run  
- 🔗 Provide public URL for sharing
- 💰 Cost: ~$5-10/month for moderate usage

### **Manual Deployment**
1. Configure Terraform: `cd infrastructure && terraform apply`
2. Build Docker image: `gcloud builds submit --config cloudbuild.yaml`
3. Deploy to Cloud Run: Automatic via Cloud Build

## 📈 **Expand the Database**

The system comes with 5 sample monsters. Add more data:

```bash
# Add 20+ monsters from D&D 5e API
python expand_data.py

# Or build comprehensive database
python data_expansion_guide.py
```

## 🛠️ **Development**

### **Project Structure**
```
dungeon-masters-oracle/
├── src/
│   ├── api/              # FastAPI application
│   ├── rag_engine/       # Core RAG implementation
│   └── requirements.txt  # Python dependencies
├── infrastructure/       # Terraform IaC
├── data-pipelines/      # Airflow data ingestion
├── sql_schema/          # BigQuery schema & scripts
├── tests/               # Test suites
└── docker/              # Docker configuration
```

### **Running Tests**
```bash
python test_rag_connection.py  # Test RAG system
python test_live_api.py        # Test full API
```

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 **Roadmap**

- [ ] Spells database integration
- [ ] Magic items support  
- [ ] Advanced campaign management
- [ ] Character sheet integration
- [ ] Homebrew content support
- [ ] Multi-language support

## 🙏 **Acknowledgments**

- **D&D 5e SRD** - Source of D&D content
- **Google Gemini** - AI/ML capabilities
- **FastAPI** - High-performance web framework
- **LangChain** - RAG implementation framework
- **D&D Community** - Inspiration and feedback

---

**Built with ❤️ for the D&D community**

*Help make D&D better for Dungeon Masters worldwide!* 🧙‍♂️⚔️🐉 
