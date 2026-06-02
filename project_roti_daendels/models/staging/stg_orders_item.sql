{{ config(materialized='view') }}

WITH source AS (

    SELECT *
    FROM {{ source('stg', 'order_items') }}

),

renamed AS (

    SELECT
        order_item_id AS order_item_id,
        order_id AS order_id,
        product_id AS product_id,
        quantity AS quantity,
        unit_price AS unit_price,
        discount_amount AS discount_amount,
        line_total AS line_total
        
    FROM  source

)

select *
from renamed