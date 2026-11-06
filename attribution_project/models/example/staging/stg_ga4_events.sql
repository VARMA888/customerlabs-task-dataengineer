WITH raw_events AS (
    SELECT * FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
    -- Limiting to one week to save BigQuery processing bytes during testing
    WHERE _TABLE_SUFFIX BETWEEN '20210101' AND '20210107'
)

SELECT
    user_pseudo_id,
    TIMESTAMP_MICROS(event_timestamp) AS event_time,
    event_name,
    traffic_source.source AS utm_source,
    traffic_source.medium AS utm_medium,
    traffic_source.name AS utm_campaign,
    -- Generating a unique event ID for deduplication 
    FARM_FINGERPRINT(CONCAT(user_pseudo_id, CAST(event_timestamp AS STRING), event_name)) AS event_id
FROM
    raw_events
WHERE
    event_name IN ('page_view', 'session_start', 'purchase')