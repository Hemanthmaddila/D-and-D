"""
DM Oracle Data Ingestion DAG

This DAG orchestrates the complete data pipeline for the Dungeon Master's Oracle:
1. Scrapes D&D SRD content from online sources
2. Cleans and validates monster data from CSV sources
3. Uploads raw text files to GCS
4. Loads cleaned data into BigQuery
5. Builds and persists FAISS vector index
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.models import Variable

# DAG Configuration
default_args = {
    'owner': 'dm-oracle-team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
}

# Airflow Variables
PROJECT_ID = Variable.get("GCP_PROJECT_ID", default_var="your-project-id")
DATA_BUCKET = Variable.get("DATA_BUCKET", default_var="your-data-bucket")
DATASET_ID = Variable.get("BIGQUERY_DATASET_ID", default_var="dnd_data")
TABLE_ID = Variable.get("BIGQUERY_TABLE_ID", default_var="monsters")

# Create DAG instance
dag = DAG(
    'dnd_data_ingestion',
    default_args=default_args,
    description='Complete data pipeline for DM Oracle knowledge base',
    schedule_interval='0 2 * * *',  # Daily at 2 AM UTC
    max_active_runs=1,
    tags=['dnd', 'rag', 'data-ingestion'],
    catchup=False,
)

def scrape_srd_task(**context):
    """Task to scrape D&D SRD content from online sources."""
    import os
    import requests
    from bs4 import BeautifulSoup
    
    output_dir = "/tmp/srd_content"
    os.makedirs(output_dir, exist_ok=True)
    
    # Example SRD scraping (simplified)
    sources = [
        {"url": "https://www.5esrd.com/spells/", "filename": "spells.txt"},
        {"url": "https://www.5esrd.com/classes/", "filename": "classes.txt"},
        {"url": "https://www.5esrd.com/magic-items/", "filename": "magic_items.txt"},
    ]
    
    scraped_files = []
    for source in sources:
        try:
            response = requests.get(source["url"], timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            content = soup.get_text()
            
            file_path = os.path.join(output_dir, source["filename"])
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            scraped_files.append(file_path)
            print(f"Scraped {source['url']} -> {file_path}")
            
        except Exception as e:
            print(f"Error scraping {source['url']}: {e}")
    
    context['task_instance'].xcom_push(key='scraped_files', value=scraped_files)
    return scraped_files

def clean_monster_data_task(**context):
    """Task to clean and validate monster data."""
    import pandas as pd
    import numpy as np
    
    # Example monster data cleaning
    output_file = "/tmp/cleaned_monsters.csv"
    
    # Create sample data (in real implementation, load from Kaggle CSV)
    sample_data = {
        'name': ['Goblin', 'Orc', 'Dragon'],
        'size': ['Small', 'Medium', 'Large'],
        'type': ['Humanoid', 'Humanoid', 'Dragon'],
        'alignment': ['Neutral Evil', 'Chaotic Evil', 'Chaotic Evil'],
        'armor_class': [15, 13, 18],
        'hit_points': [7, 15, 200],
        'challenge_rating': [0.25, 0.5, 10.0],
        'strength': [8, 16, 23],
        'dexterity': [14, 12, 10],
        'constitution': [10, 16, 21],
        'intelligence': [10, 7, 14],
        'wisdom': [8, 11, 13],
        'charisma': [8, 10, 17],
        'special_abilities': ['Nimble Escape', 'Aggressive', 'Legendary Actions'],
        'actions': ['Scimitar attack', 'Greataxe attack', 'Breath Weapon']
    }
    
    df = pd.DataFrame(sample_data)
    
    # Data cleaning operations
    df['alignment'] = df['alignment'].fillna('Unaligned')
    df['armor_class'] = pd.to_numeric(df['armor_class'], errors='coerce').fillna(10)
    df['hit_points'] = pd.to_numeric(df['hit_points'], errors='coerce').fillna(1)
    df['challenge_rating'] = pd.to_numeric(df['challenge_rating'], errors='coerce').fillna(0)
    
    # Save cleaned data
    df.to_csv(output_file, index=False)
    
    context['task_instance'].xcom_push(key='cleaned_monster_file', value=output_file)
    return output_file

def load_bigquery_data(**context):
    """Task to load cleaned monster data into BigQuery."""
    import pandas as pd
    from google.cloud import bigquery
    
    # Get cleaned data file
    cleaned_file = context['task_instance'].xcom_pull(
        key='cleaned_monster_file', 
        task_ids='clean_monster_data'
    )
    
    # Read cleaned data
    df = pd.read_csv(cleaned_file)
    
    # Load to BigQuery
    client = bigquery.Client(project=PROJECT_ID)
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
    )
    
    with open(cleaned_file, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_id, job_config=job_config)
    
    job.result()  # Wait for the job to complete
    
    print(f"Successfully loaded {len(df)} monster records to BigQuery")
    return len(df)

# Define tasks
scrape_srd = PythonOperator(
    task_id='scrape_srd',
    python_callable=scrape_srd_task,
    dag=dag,
)

clean_monster_data = PythonOperator(
    task_id='clean_monster_data',
    python_callable=clean_monster_data_task,
    dag=dag,
)

upload_srd_files = LocalFilesystemToGCSOperator(
    task_id='upload_srd_files',
    src='/tmp/srd_content/',
    dst='srd_content/',
    bucket=DATA_BUCKET,
    dag=dag,
)

load_monster_data = PythonOperator(
    task_id='load_monster_data',
    python_callable=load_bigquery_data,
    dag=dag,
)

# Define task dependencies
scrape_srd >> upload_srd_files
clean_monster_data >> load_monster_data 