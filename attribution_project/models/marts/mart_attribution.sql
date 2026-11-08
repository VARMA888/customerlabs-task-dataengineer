{{ config(materialized='table') }}
WITH user_traffic AS (
    SELECT
        user_pseudo_id,
        event_time,
        utm_source,
        utm_medium,
        utm_campaign,
        event_id
    FROM {{ ref('stg_ga4_events') }}
    WHERE utm_source IS NOT NULL
),

purchases AS (
    SELECT
        user_pseudo_id,
        event_time AS purchase_time,
        event_id AS purchase_event_id
    FROM {{ ref('stg_ga4_events') }}
    WHERE event_name = 'purchase'
),

attribution_prep AS (
    SELECT
        p.user_pseudo_id,
        p.purchase_time,
        p.purchase_event_id,
        t.utm_source,
        t.event_time AS touchpoint_time,
        FIRST_VALUE(t.utm_source) OVER (
            PARTITION BY p.user_pseudo_id, p.purchase_event_id 
            ORDER BY t.event_time ASC 
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS first_click_source,
        LAST_VALUE(t.utm_source) OVER (
            PARTITION BY p.user_pseudo_id, p.purchase_event_id 
            ORDER BY t.event_time ASC 
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS last_click_source
    FROM purchases p
    LEFT JOIN user_traffic t 
        ON p.user_pseudo_id = t.user_pseudo_id
        AND t.event_time <= p.purchase_time
        -- Assumption: 30-day lookback window[cite: 1]
        AND TIMESTAMP_DIFF(p.purchase_time, t.event_time, DAY) <= 30
)

-- Deduplicate so we have one row per purchase
SELECT DISTINCT
    user_pseudo_id,
    purchase_time,
    purchase_event_id,
    first_click_source,
    last_click_source
FROM attribution_prep