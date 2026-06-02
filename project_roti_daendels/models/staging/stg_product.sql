{{ config(materialized='view') }}

WITH source AS (

    SELECT *
    FROM {{ source('stg', 'products') }}

),

renamed AS (

    SELECT
        product_id AS product_id,
        product_name AS product_name,
        category_id AS category_id,
        unit_price AS unit_price,
        weight_kg AS weight_kg,
        shelf_life_days AS shelf_life_days,
        is_year_round AS is_year_round,
        allergens AS allergens,
        cost_price AS cost_price,
        currency AS currency,
        is_active AS is_active
    FROM source

)
SELECT *
FROM renamed