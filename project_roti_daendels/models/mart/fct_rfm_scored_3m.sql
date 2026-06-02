{{ config(materialized='view') }}
WITH rfm_scored AS (
  SELECT
    customer_id, recency, frequency, monetary, '3_months' AS period,
    CASE
      WHEN recency <= 7 THEN 5 
      WHEN recency <= 15 THEN 4
      WHEN recency <= 30 THEN 3 
      WHEN recency <= 60 THEN 2 
      ELSE 1
    END AS r_score,
    CASE
      WHEN frequency >= 20 THEN 5 
      WHEN frequency >= 15 THEN 4
      WHEN frequency >= 10 THEN 3 
      WHEN frequency >= 5 THEN 2 
      ELSE 1
    END AS f_score,
    CASE
      WHEN monetary >= 1000 THEN 5 
      WHEN monetary >= 500 THEN 4
      WHEN monetary >= 250  THEN 3 
      WHEN monetary >= 100  THEN 2 
      ELSE 1
    END AS m_score
  FROM {{ ref('fct_rfm_3m') }} o
)

SELECT * FROM rfm_scored