{{ config(materialized='view') }}
WITH rfm AS (
  SELECT
   customer_id,
   ('2023-12-31' - MAX(order_datetime)::date)  AS recency,   -- hari sejak transaksi terakhir
    COUNT(order_id)                           AS frequency,
    SUM(total_amount)                         AS monetary
  FROM {{ ref('fct_orders__total_amount_1m') }} o
  GROUP BY customer_id
)

SELECT * FROM rfm