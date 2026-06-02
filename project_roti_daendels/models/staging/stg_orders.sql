{{ config(materialized='view') }}

WITH source AS (

    SELECT *
    FROM {{ source('stg', 'orders') }}

),

renamed AS (

    SELECT
        order_id AS order_id,
        branch_id AS branch_id,
        customer_id AS customer_id,
        order_datetime AS order_datetime,
        order_status AS order_status,
        payment_method AS payment_method,
        subtotal AS subtotal,
        vat_amount AS vat_amount,
        total_amount AS total_amount,
        loyalty_points_earned AS loyalty_points_earned,
        notes AS notes

    FROM source

)

SELECT *
FROM renamed