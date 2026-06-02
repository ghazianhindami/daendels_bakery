{{ config(materialized='view') }}
WITH orders_clean AS (
  SELECT
    order_id,
    branch_id,
    customer_id,
    order_datetime,
    total_amount
    FROM {{ ref('int_orders__info_voltooid_customer') }} o
)

SELECT * FROM orders_clean