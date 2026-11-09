# Real-Time Attribution Pipeline & Dashboard

[**View Looker Studio Dashboard Here**](https://datastudio.google.com/reporting/5fc34874-d642-4a99-ae9e-fa49822bb4cb)

## Overview
This project implements an end-to-end data pipeline to ingest data  transform the data and visualize Google Analytics 4 (GA4) e-commerce data. It involves a batch processing dbt architecture for historical data and a Python streaming application for real-time events into BigQuery.

## Architecture
1. we used bigquery-public-data.ga4_obfuscated_sample_ecommerce as source & real-time Python streaming payload.
2. Google BigQuery as a storage option.
3. for the transformation part i have used dbt (Data Build Tool) utilizing `FIRST_VALUE` and `LAST_VALUE` window functions for marketing attribution (30-day lookback).
4. at the final stage i used  Google Looker Studio as visulaization tool.

## 1. Run Instructions
To execute this pipeline in a production environment:

**Streaming Events:**
Run the Python script to stream live events to BigQuery.

```bash
pip install google-cloud-bigquery
python stream_events.py


** dbt Transformations & Testing: **
Execute the staging, intermediate, and mart models, followed by data quality tests.

```bash
dbt run --select stg_ga4_events int_sessions mart_attribution
dbt test
```

## Cost Notes & FinOps.

To respec the GCP Free Trial constraints and optimize BigQuery bytes-billed, this pipeline implements strict cost-control measures:

7-Day Window Optimization: where The assessment requested a 14-day time series, but querying 14 days of the public GA4 dataset exceeded safe sandbox limits. The dbt staging model (stg_ga4_events) uses a strict _TABLE_SUFFIX filter for a 7-day rolling window to minimize bytes scanned.


## Failure Handling

Idempotency: The Python streamer generates a UUID for the insert_id in insert_rows_json. If a network timeout occurs and the payload is retried, BigQuery will automatically deduplicate the rows.

Data Quality Constraints: Unique and not-null tests are defined in schema.yml. If critical fields like user_pseudo_id are missing, the dbt pipeline fails gracefully, preventing bad data from entering the mart layer.

## Monitoring Suggestions

BigQuery Information Schema: Monitor INFORMATION_SCHEMA.PARTITIONS to track storage growth and ensure partition expiration configurations are working.

Streaming Insert Errors: Configure GCP Cloud Monitoring alerts on the metric bigquery.googleapis.com/storage/uploaded_bytes to detect drops in streaming volume, and monitor the streaming buffer for insertion failures.

