{{ config(materialized='view') }}
WITH rfm_scored AS (
  SELECT
    customer_id, recency, frequency, monetary, '1_month' AS period,
    CASE
      WHEN recency <= 3 THEN 5 
      WHEN recency <= 7 THEN 4
      WHEN recency <= 14 THEN 3 
      WHEN recency <= 21 THEN 2 
      ELSE 1
    END AS r_score,
    CASE
      WHEN frequency >= 12 THEN 5 
      WHEN frequency >= 8 THEN 4
      WHEN frequency >= 5 THEN 3 
      WHEN frequency >= 3 THEN 2 
      ELSE 1
    END AS f_score,
    CASE
      WHEN monetary >= 500 THEN 5 
      WHEN monetary >= 250 THEN 4
      WHEN monetary >= 100  THEN 3 
      WHEN monetary >= 50  THEN 2 
      ELSE 1
    END AS m_score
  FROM {{ ref('fct_rfm_1m') }} o
)

SELECT * FROM rfm_scored