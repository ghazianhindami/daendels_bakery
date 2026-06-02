{{ config(materialized='view') }}
WITH rfm_raw AS (
  SELECT
    *
FROM {{ ref('int_orders__rfm_raw') }}
),

rfm_score as(
    SELECT
        customer_id,
        recency,
        frequency,
        monetary,
        NTILE(5) OVER (ORDER BY recency) AS recency_score,
        NTILE(5) OVER (ORDER BY frequency DESC) AS frequency_score,
        NTILE(5) OVER (ORDER BY monetary DESC) AS monetary_score
    FROM rfm_raw
)

SELECT * FROM rfm_score