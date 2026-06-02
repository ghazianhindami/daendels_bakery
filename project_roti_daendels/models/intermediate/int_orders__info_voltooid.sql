{{ config(materialized='view') }}

SELECT
    *
FROM {{ ref('int_orders__info_complete') }} o
WHERE o.order_status = 'Voltooid'
ORDER BY o.order_id DESC