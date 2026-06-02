{{ config(materialized='view') }}
WITH rfm_raw AS (
  SELECT
    customer_id,
    ('2023-12-31' - MAX(order_datetime)::date)  AS recency,   -- hari sejak transaksi terakhir
    COUNT(order_id)                           AS frequency,
    SUM(total_amount)                         AS monetary
    FROM {{ ref('int_orders__info_voltooid_customer') }} o
  GROUP BY customer_id
)

SELECT * FROM rfm_raw