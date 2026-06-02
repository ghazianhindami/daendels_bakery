{{ config(materialized='view') }}
WITH orders_clean AS (
  SELECT
   *
  FROM {{ ref('fct_orders__total_amount') }} o
  WHERE order_datetime >= (DATE '2023-12-31' - INTERVAL '1 month')
)

SELECT * FROM orders_clean
ORDER BY order_datetime DESC