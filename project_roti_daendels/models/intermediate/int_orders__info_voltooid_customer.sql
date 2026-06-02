{{ config(materialized='view') }}

SELECT
    *
FROM {{ ref('int_orders__info_voltooid') }} o
WHERE o.customer_id IS NOT NULL
ORDER BY o.order_datetime DESC