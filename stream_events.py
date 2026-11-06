import uuid
from datetime import datetime, timezone
from google.cloud import bigquery

# Update this to your actual GCP Project ID
project_id = "customerlabs-task-8888" 
dataset_id = "analytics_stg"
table_id = f"{project_id}.{dataset_id}.streamed_events"

client = bigquery.Client(project=project_id)

def generate_mock_event():
    return {
        "user_pseudo_id": f"mock_user_{uuid.uuid4().hex[:6]}",
        "event_timestamp": int(datetime.now(timezone.utc).timestamp() * 1000000),
        "event_name": "purchase",
        "utm_source": "google",
        "utm_medium": "cpc",
        "utm_campaign": "spring_sale",
        # Unique ID for idempotency/deduplication
        "insert_id": str(uuid.uuid4()) 
    }

events_to_stream = 10
rows_to_insert = [generate_mock_event() for _ in range(events_to_stream)]

errors = client.insert_rows_json(table_id, rows_to_insert, row_ids=[row["insert_id"] for row in rows_to_insert])

if not errors:
    print(f"Successfully streamed {events_to_stream} events.")
else:
    print(f"Errors: {errors}")