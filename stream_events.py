# This script simulates a live data stream by generating mock GA4 purchase payloads 
# and appending them to BigQuery. It serves as the real-time ingestion point for our 
# architecture, allowing us to test how downstream dbt models handle fresh incoming data.

import uuid
from datetime import datetime, timezone
from google.cloud import bigquery

project_id = "customerlabs-task-8888" 
dataset_id = "analytics_stg"
table_id = f"{project_id}.{dataset_id}.streamed_events"

client = bigquery.Client(project=project_id)


# 1. Define schema
schema = [
    bigquery.SchemaField("user_pseudo_id", "STRING"),
    bigquery.SchemaField("event_timestamp", "INTEGER"),
    bigquery.SchemaField("event_name", "STRING"),
    bigquery.SchemaField("utm_source", "STRING"),
    bigquery.SchemaField("utm_medium", "STRING"),
    bigquery.SchemaField("utm_campaign", "STRING"),
    bigquery.SchemaField("insert_id", "STRING"),
]

# 2. Generate values as JSON/Dictionaries
events_to_stream = 10
rows_to_insert = []
for _ in range(events_to_stream):
    rows_to_insert.append({
        "user_pseudo_id": f"mock_user_{uuid.uuid4().hex[:6]}",
        "event_timestamp": int(datetime.now(timezone.utc).timestamp() * 1000000),
        "event_name": "purchase",
        "utm_source": "google",
        "utm_medium": "cpc",
        "utm_campaign": "spring_sale",
        "insert_id": str(uuid.uuid4())
    })

# 3. Use a Load Job 
job_config = bigquery.LoadJobConfig(
    schema=schema,
    write_disposition="WRITE_APPEND" 
)

print("Loading data to BigQuery...")
job = client.load_table_from_json(rows_to_insert, table_id, job_config=job_config)
job.result()  # Waits for the job to complete

print(f"Successfully loaded {events_to_stream} events to {table_id}.")