{{ config(materialized='view') }}
WITH rfm_scored AS (
  SELECT
    customer_id, recency, frequency, monetary, 'whole_year' AS period,
    CASE
      WHEN recency <= 30 THEN 5 
      WHEN recency <= 90 THEN 4
      WHEN recency <= 180 THEN 3 
      WHEN recency <= 365 THEN 2 
      ELSE 1
    END AS r_score,
    CASE
      WHEN frequency >= 200 THEN 5 
      WHEN frequency >= 100 THEN 4
      WHEN frequency >= 50 THEN 3 
      WHEN frequency >= 20 THEN 2 ELSE 1
    END AS f_score,
    CASE
      WHEN monetary >= 20000 THEN 5 
      WHEN monetary >= 10000 THEN 4
      WHEN monetary >= 5000  THEN 3 
      WHEN monetary >= 2000  THEN 2 
      ELSE 1
    END AS m_score
  FROM {{ ref('fct_rfm_all') }} o
)

SELECT * FROM rfm_scored