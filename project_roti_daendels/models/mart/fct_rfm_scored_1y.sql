{{ config(materialized='view') }}
WITH rfm_scored AS (
  SELECT
    customer_id, recency, frequency, monetary, '1_year' AS period,
    CASE
      WHEN recency <= 30 THEN 5 
      WHEN recency <= 60 THEN 4
      WHEN recency <= 120 THEN 3 
      WHEN recency <= 180 THEN 2 
      ELSE 1
    END AS r_score,
    CASE
      WHEN frequency >= 50 THEN 5 
      WHEN frequency >= 30 THEN 4
      WHEN frequency >= 15 THEN 3 
      WHEN frequency >= 8 THEN 2 ELSE 1
    END AS f_score,
    CASE
      WHEN monetary >= 5000 THEN 5 
      WHEN monetary >= 2500 THEN 4
      WHEN monetary >= 1000  THEN 3 
      WHEN monetary >= 500  THEN 2 
      ELSE 1
    END AS m_score
  FROM {{ ref('fct_rfm_1y') }} o
)

SELECT * FROM rfm_scored