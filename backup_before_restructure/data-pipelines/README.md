# Data Pipelines

This directory contains Apache Airflow DAGs for automated data ingestion and processing for the Dungeon Master's Oracle knowledge base.

## Architecture

The data pipeline consists of:
- **Web Scraping**: Automated extraction of D&D SRD content from online sources
- **Data Cleaning**: Pandas-based transformation of raw monster data
- **Vector Index Building**: FAISS index creation for semantic search
- **Data Loading**: Upload to GCS and BigQuery for the hybrid RAG system

## Components

### DAGs
- `dnd_data_ingestion.py` - Main DAG orchestrating the entire data pipeline
- `srd_scraping.py` - Specialized DAG for SRD content extraction
- `monster_data_cleaning.py` - Data transformation and validation

### Scripts
- `scrapers/` - Web scraping utilities for different D&D sources
- `cleaners/` - Data cleaning and transformation modules
- `loaders/` - GCS and BigQuery data loading utilities

## Data Sources

### Unstructured Data (SRD)
- **5esrd.com** - Complete SRD content in HTML format
- **D&D Beyond SRD** - Alternative source with structured markup
- **Sections**: Classes, Spells, Magic Items, Rules, Lore

### Structured Data (Monsters)
- **Kaggle Datasets** - Community-curated monster statistics
- **CSV Format** - Standardized columns for easy processing
- **Schema Validation** - Ensures BigQuery compatibility

## Pipeline Schedule

The main ingestion DAG runs:
- **Daily** at 2 AM UTC for incremental updates
- **Manual triggers** for immediate data refresh
- **Dependency handling** ensures proper execution order

## Data Quality

### Validation Steps
- Schema validation for BigQuery tables
- Data type conversion and null handling
- Duplicate detection and removal
- Referential integrity checks

### Error Handling
- Retry logic for transient failures
- Dead letter queues for persistent errors
- Comprehensive logging and monitoring
- Slack/email notifications for failures

## Setup

### Prerequisites
1. **Airflow Installation**: Python 3.11+ with Apache Airflow
2. **GCP Authentication**: Service account with pipeline permissions
3. **Dependencies**: Install required packages from `requirements.txt`

### Configuration
1. **Airflow Variables**: Set GCP project and bucket names
2. **Connections**: Configure GCS and BigQuery connections
3. **Secrets**: Store API keys in Airflow Variables or Secret Manager

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Set up Airflow database
airflow db init

# Create admin user
airflow users create --username admin --firstname Admin --lastname User --role Admin --email admin@example.com

# Start scheduler and webserver
airflow scheduler &
airflow webserver --port 8080
```

## Monitoring

### Metrics
- Pipeline success/failure rates
- Data freshness and volume
- Processing times and resource usage
- Data quality score trends

### Alerting
- Failed task notifications
- Data quality threshold breaches
- Long-running pipeline alerts
- Resource utilization warnings

## Data Lineage

The pipeline maintains full data lineage:
1. **Source** → Raw web content and CSV files
2. **Bronze** → Raw extracted data in GCS
3. **Silver** → Cleaned and validated data
4. **Gold** → Production-ready FAISS index and BigQuery tables 