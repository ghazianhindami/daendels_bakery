{{ config(materialized='table') }}

SELECT
    o.order_id,
    o.branch_id,
    b.branch_name,
    o.customer_id,
    c.full_name AS customer_full_name,
    o.order_datetime,
    o.order_status,
    o.payment_method,
    o.subtotal,
    o.vat_amount,
    o.total_amount,
    o.loyalty_points_earned,
    o.notes
FROM {{ ref('stg_orders') }} o
LEFT JOIN {{ ref('stg_branches') }} b ON o.branch_id = b.branch_id
LEFT JOIN {{ ref('stg_customer') }} c ON o.customer_id = c.customer_id
ORDER BY o.order_id DESC