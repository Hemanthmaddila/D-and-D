# 🎯 Project Restructuring Plan

## Current Issues
- Too many files at root level (13+ documentation and config files)
- Test files scattered between root and tests/ directory
- Multiple requirements.txt files in different locations
- Documentation files not organized
- Configuration files scattered

## Proposed Structure

```
dungeon-masters-oracle/
├── README.md                    # Main project overview
├── LICENSE                      # Project license
├── .gitignore                  # Git ignore rules
├── .env.example                # Environment template
├── requirements.txt            # Main dependencies
├── Makefile                    # Build and deployment commands
├── docker-compose.yml          # Local development setup
│
├── docs/                       # 📚 All Documentation
│   ├── README.md              # Documentation index
│   ├── quickstart.md          # Quick start guide
│   ├── deployment.md          # Deployment instructions
│   ├── tutorial.md            # Complete tutorial
│   ├── docker-guide.md        # Docker beginner guide
│   └── api/                   # API documentation
│       └── README.md
│
├── config/                     # ⚙️ Configuration
│   ├── config.yaml            # Application config
│   ├── cloudbuild.yaml        # Cloud Build config
│   └── environments/          # Environment-specific configs
│       ├── dev.yaml
│       ├── staging.yaml
│       └── prod.yaml
│
├── src/                        # 💻 Source Code
│   ├── __init__.py
│   ├── requirements.txt       # Core app dependencies
│   ├── api/                   # FastAPI application
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── routes/
│   ├── rag_engine/            # RAG implementation
│   │   ├── __init__.py
│   │   ├── hybrid_rag.py
│   │   ├── retrievers.py
│   │   └── router.py
│   └── core/                  # Shared utilities
│       ├── __init__.py
│       ├── config.py
│       └── utils.py
│
├── database/                   # 🗄️ Database & Schema
│   ├── README.md
│   ├── schema/
│   │   ├── create_monsters_table.sql
│   │   ├── bigquery_schema.json
│   │   └── terraform_schema.tf
│   ├── migrations/            # Database migrations
│   ├── seeds/                 # Sample data
│   │   ├── sample_data.py
│   │   └── monsters_schema.py
│   └── scripts/               # Database scripts
│       ├── setup_bigquery.py
│       ├── create_table.py
│       └── load_sample_data.py
│
├── infrastructure/             # 🏗️ Infrastructure as Code
│   ├── README.md
│   ├── terraform/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── compute.tf
│   │   ├── storage.tf
│   │   ├── iam.tf
│   │   ├── secrets.tf
│   │   ├── terraform.tfvars.example
│   │   └── environments/
│   │       ├── dev/
│   │       ├── staging/
│   │       └── prod/
│   └── docker/
│       ├── Dockerfile
│       ├── docker-compose.dev.yml
│       └── docker-compose.prod.yml
│
├── data-pipelines/             # 📊 Data Processing
│   ├── README.md
│   ├── requirements.txt
│   ├── airflow/
│   │   └── dags/
│   │       └── dnd_data_ingestion.py
│   └── scripts/
│       ├── expand_data.py
│       └── data_expansion_guide.py
│
├── tests/                      # 🧪 All Tests
│   ├── __init__.py
│   ├── requirements.txt       # Test-specific dependencies
│   ├── conftest.py           # Pytest configuration
│   ├── unit/                 # Unit tests
│   │   ├── test_api.py
│   │   └── test_rag_engine.py
│   ├── integration/          # Integration tests
│   │   ├── test_live_api.py
│   │   └── test_rag_connection.py
│   └── e2e/                  # End-to-end tests
│       └── test_full_system.py
│
├── scripts/                    # 🔧 Utility Scripts
│   ├── setup.sh              # Project setup
│   ├── create_config.py       # Config generation
│   ├── deploy_to_production.py
│   └── test_env.py
│
└── tools/                      # 🛠️ Development Tools
    ├── linting/
    ├── formatting/
    └── pre-commit/
```

## Benefits of This Structure

1. **Clean Root**: Only essential files at root level
2. **Logical Grouping**: Related files grouped together
3. **Clear Separation**: Code, docs, config, infrastructure separate
4. **Scalable**: Easy to find and add new components
5. **Professional**: Follows industry standards
6. **Maintainable**: Clear ownership and responsibility

## Migration Steps

1. Create new directory structure
2. Move files to appropriate locations
3. Update import paths in code
4. Update documentation references
5. Update build scripts and CI/CD
6. Test everything works
7. Clean up old structure

## File Movement Mapping

### Documentation → docs/
- `QUICKSTART.md` → `docs/quickstart.md`
- `DEPLOYMENT_README.md` → `docs/deployment.md`
- `COMPLETE_TUTORIAL.md` → `docs/tutorial.md`
- `DOCKER_BEGINNER_GUIDE.md` → `docs/docker-guide.md`

### Configuration → config/
- `config.yaml` → `config/config.yaml`
- `cloudbuild.yaml` → `config/cloudbuild.yaml`

### Database → database/
- `sql_schema/` → `database/`

### Tests → tests/ (organized)
- Root test files → `tests/integration/`
- Existing `tests/` → `tests/unit/`

### Scripts → scripts/ (consolidated)
- Utility scripts remain in scripts/
- Database scripts → `database/scripts/`

### Infrastructure → infrastructure/ (organized)
- `infrastructure/` → `infrastructure/terraform/`
- `docker/` → `infrastructure/docker/` 