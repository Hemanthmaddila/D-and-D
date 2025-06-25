# BigQuery Schema for D&D Monsters

This directory contains everything needed to set up your BigQuery table with the D&D monsters schema.

## Files Overview

- **`bigquery_schema.json`** - Clean JSON schema definition (ready for GCP)
- **`create_table.py`** - Script to create the BigQuery table
- **`load_sample_data.py`** - Script to load test data
- **`setup_bigquery.py`** - Combined setup (creates table + loads data)
- **`sample_data.py`** - Sample monster data for testing
- **Other files** - Alternative formats (SQL, Terraform, Python classes)

## Quick Start

### Option 1: All-in-One Setup ⚡
```bash
cd sql_schema
python setup_bigquery.py
```

### Option 2: Step-by-Step 🔧
```bash
cd sql_schema

# Create the table
python create_table.py

# Load sample data
python load_sample_data.py
```

## Schema Fields

Your BigQuery table will have these fields:

| Field Name | Type | Mode | Description |
|------------|------|------|-------------|
| `name` | STRING | REQUIRED | Monster name |
| `type` | STRING | NULLABLE | Creature type (Dragon, Beast, etc.) |
| `size` | STRING | NULLABLE | Size category (Small, Large, etc.) |
| `armor_class` | INTEGER | NULLABLE | Armor Class (AC) |
| `hit_points` | INTEGER | NULLABLE | Hit points |
| `speed` | STRING | NULLABLE | Movement speeds |
| `challenge_rating` | STRING | NULLABLE | Challenge Rating (CR) |
| `abilities` | STRING | NULLABLE | All ability scores |
| `skills` | STRING | NULLABLE | Proficient skills |
| `damage_resistances` | STRING | NULLABLE | Damage resistances |
| `damage_immunities` | STRING | NULLABLE | Damage immunities |
| `condition_immunities` | STRING | NULLABLE | Condition immunities |
| `senses` | STRING | NULLABLE | Special senses |
| `languages` | STRING | NULLABLE | Known languages |
| `special_abilities` | STRING | NULLABLE | Special traits |
| `actions` | STRING | NULLABLE | Available actions |
| `legendary_actions` | STRING | NULLABLE | Legendary actions |
| `source` | STRING | NULLABLE | Source book |

## Sample Data

The setup includes 5 sample monsters:
- **Adult Red Dragon** (CR 17)
- **Beholder** (CR 13) 
- **Lich** (CR 21)
- **Owlbear** (CR 3)
- **Goblin** (CR 1/4)

## After Setup

Once your table is created, you can:

1. **View in BigQuery Console:**
   ```
   https://console.cloud.google.com/bigquery?project=YOUR_PROJECT_ID
   ```

2. **Test with sample queries:**
   ```sql
   -- All dragons
   SELECT name, challenge_rating FROM `your-project.dnd_data.monsters` 
   WHERE type = 'Dragon'
   
   -- High CR monsters
   SELECT name, type, challenge_rating FROM `your-project.dnd_data.monsters`
   WHERE SAFE_CAST(REGEXP_EXTRACT(challenge_rating, r'^(\d+)') AS INT64) >= 10
   ```

3. **Load more data** using your existing data pipeline

## Troubleshooting

**Authentication Error:**
```bash
gcloud auth application-default login
```

**Project Not Found:**
- Check your `.env` file has `PROJECT_ID=your-actual-project-id`
- Verify the project exists: `gcloud projects list`

**BigQuery API Not Enabled:**
```bash
gcloud services enable bigquery.googleapis.com --project=YOUR_PROJECT_ID
```

**Import Errors:**
- Make sure you're in the `sql_schema` directory when running scripts
- Install required packages: `pip install google-cloud-bigquery`

## Next Steps

After your BigQuery table is ready:
1. ✅ Test queries in BigQuery Console
2. ✅ Run your data pipeline to load more monsters  
3. ✅ Update your RAG system to use the new schema
4. ✅ Test end-to-end functionality 