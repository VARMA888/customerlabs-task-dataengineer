# Real-time Attribution Pipeline

## Overview
This project implements end-to-end data pipeline to ingest data transform the data and visualize Google Analytics 4 (GA4) e-commerce data. It involves a batch processing dbt architecture for historical data and python script streaming application for real-time events into BigQuery.

## Architecture
1. we used bigquery-public-data.ga4_obfuscated_sample_ecommerce as source & real-time Python streaming payload.
2. Google BigQuery as a storage option.
3. for the trformatio part i have used dbt (Data Build Tool) utilizing `FIRST_VALUE` and `LAST_VALUE` window functions for marketing attribution (30-day lookback).
4. in the final  Google Looker Studio as visulaization tool.

## Production Run Instructions
To execute this pipeline in a production environment:
1. Streaming Events : Run the Python script to stream live events to BigQuery.


   ```bash
   pip install google-cloud-bigquery
   python stream_events.py

## Looker Studio Dashboard 

View Dashboard Here ->(https://datastudio.google.com/reporting/5fc34874-d642-4a99-ae9e-fa49822bb4cb)