{{ config(materialized='view') }}
WITH rfm_scored AS (
  SELECT
    customer_id, recency, frequency, monetary, '1_week' AS period,
    CASE
      WHEN recency <= 1 THEN 5 WHEN recency <= 2 THEN 4
      WHEN recency <= 4 THEN 3 WHEN recency <= 6 THEN 2 ELSE 1
    END AS r_score,
    CASE
      WHEN frequency >= 7 THEN 5 WHEN frequency >= 5 THEN 4
      WHEN frequency >= 3 THEN 3 WHEN frequency >= 2 THEN 2 ELSE 1
    END AS f_score,
    CASE
      WHEN monetary >= 100 THEN 5 WHEN monetary >= 75 THEN 4
      WHEN monetary >= 50  THEN 3 WHEN monetary >= 25  THEN 2 ELSE 1
    END AS m_score
  FROM {{ ref('fct_rfm_1w') }} o
)

SELECT * FROM rfm_scored